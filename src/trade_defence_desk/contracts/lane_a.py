"""
Lane A contracts: the act cut into sections, one reading of it, and the checks on it.

Made by lane A. ActSection is used by lane C for highlighting. ActExtraction and
FieldCheck are used by lane B (ledger) and lane C (case page).
Columns follow docs/05_DATA_SCHEMA.md. Additions say so in a comment.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Literal

from pydantic import Field, model_validator

from trade_defence_desk.contracts.lane_b import CountryCode, RateCategory, _Contract

# ------------------------------------------------------------------ sections

# Added: "citation" and "final". The schema lists title, recital, article, annex.
# Citations ("Having regard to ...") and the closing lines are neither, and a quote
# can still point at them.
SectionKind = Literal["title", "citation", "recital", "article", "annex", "final"]

# One id per paragraph, stable across runs:
# tit, cit_2, rct_12, art_1.2, anx_1.3, fin_1
SECTION_ID = r"^(tit|(cit|rct|fin)_\d+|(art|anx)_\d+\.\d+)$"


class ActSection(_Contract):
    """
    One paragraph of an act. Table `act_section`. A quote always points at one.
    """

    celex: str = Field(examples=["32026R2393"])
    section_id: str = Field(pattern=SECTION_ID, examples=["art_1.2"])
    kind: SectionKind
    order: int = Field(ge=0)  # reading order inside the act
    text: str = Field(min_length=1)  # exactly as written, spaces cleaned only

    @model_validator(mode="after")
    def _id_matches_kind(self) -> ActSection:
        prefix = {
            "title": "tit",
            "citation": "cit",
            "recital": "rct",
            "article": "art",
            "annex": "anx",
            "final": "fin",
        }[self.kind]
        if not self.section_id.startswith(prefix):
            raise ValueError(f"a {self.kind} section id starts with '{prefix}'")
        return self


# ------------------------------------------------------------------ extraction


class Quoted(_Contract):
    """
    One extracted value and the words in the act it comes from.
    """

    value: str
    quote: str = Field(min_length=1)  # word for word from the act
    section_id: str = Field(pattern=SECTION_ID)


class DutyRow(_Contract):
    """
    One row of the operative duty table, one TARIC additional code.
    """

    # None only for a country-wide rate with no code, as in 2026/2311.
    taric_additional_code: str | None = Field(default=None, examples=["88CB"])
    category: RateCategory
    rate_pct: Decimal | None = Field(default=None, ge=0, le=100)
    rate_text: str  # as written, "39,8"
    names: list[str] = []  # a grouped cell gives two
    section_id: str = Field(pattern=SECTION_ID)
    # Rule 5: a rate that is not a simple percentage is shown, not applied.
    formula_text: str | None = None
    needs_review: bool = False

    @model_validator(mode="after")
    def _no_percentage_goes_to_a_person(self) -> DutyRow:
        if self.rate_pct is None and not self.needs_review:
            raise ValueError("a row without rate_pct must have needs_review = True")
        return self


class ActConditions(_Contract):
    """
    The fine print of one act, each answer with its quote. Table `act_conditions`.
    """

    invoice_declaration_required: bool | None = None
    invoice_declaration: Quoted | None = None
    provisional_collection: Quoted | None = None  # what happens to the secured amounts
    retroactive_collection: Quoted | None = None
    new_exporter_clause: Quoted | None = None
    registration_celex: Quoted | None = None


System = Literal["parser", "llm", "combined"]


class ActExtraction(_Contract):
    """
    One reading of one act by one system. Table `extraction`, the facts in `payload`.
    """

    extraction_id: str
    celex: str
    system: System
    provider: str | None = None  # None for the parser
    model: str | None = None
    prompt_version: str | None = None
    tokens_in: int | None = Field(default=None, ge=0)
    tokens_out: int | None = Field(default=None, ge=0)
    cost_eur: Decimal | None = Field(default=None, ge=0)
    latency_ms: int | None = Field(default=None, ge=0)

    # the payload
    stage: Quoted | None = None
    origins: list[Quoted] = []
    origin_countries: list[CountryCode] = []  # Added: the codes, for lane B's Measure
    product_text: Quoted | None = None
    cn_codes: list[Quoted] = []
    applies_from_rule: Quoted | None = None  # the rule only, Python does the date
    previous_act: Quoted | None = None  # the older act this one follows or changes
    duty_rows: list[DutyRow] = []
    conditions: ActConditions | None = None

    @model_validator(mode="after")
    def _model_reading_says_which_model(self) -> ActExtraction:
        if self.system != "parser" and (self.provider is None or self.model is None):
            raise ValueError("a model reading needs provider and model")
        return self

    @model_validator(mode="after")
    def _one_row_per_code(self) -> ActExtraction:
        # Parser only. A model's odd answer is kept and flagged by the verifier, not refused.
        if self.system != "parser":
            return self
        codes = [r.taric_additional_code for r in self.duty_rows if r.taric_additional_code]
        if len(codes) != len(set(codes)):
            raise ValueError("a TARIC additional code appears in two duty rows")
        return self


# ------------------------------------------------------------------ checks

FieldStatus = Literal["checked_by_program", "quote_found", "not_verified", "failed"]


class FieldCheck(_Contract):
    """
    The verifier's verdict on one field. Table `field_check`.
    """

    extraction_id: str
    field_path: str = Field(examples=["duty_rows[0].rate_pct"])
    status: FieldStatus
    quote: str | None = Field(default=None, min_length=1)
    section_id: str | None = Field(default=None, pattern=SECTION_ID)
    detail: str = ""  # why, in a short sentence

    @model_validator(mode="after")
    def _quote_found_has_a_place(self) -> FieldCheck:
        if self.status == "quote_found" and (self.quote is None or self.section_id is None):
            raise ValueError("'quote_found' needs the quote and its section_id")
        return self
