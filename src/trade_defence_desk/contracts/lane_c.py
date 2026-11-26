"""
Lane C contracts: Bergmann's CSV, the scope judge, decisions and the log.

Drafted by lane A as contract keeper, owned by lane C. Shiar reviews before the freeze.
Supplier and PurchaseLine are used by lane B (generator) and lane C (matching).
Columns follow docs/05_DATA_SCHEMA.md and docs/examples/bergmann_purchase_lines.csv.
Additions say so in a comment.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Annotated, Any, Literal

from pydantic import AwareDatetime, Field, StringConstraints, field_validator, model_validator

from trade_defence_desk.contracts.lane_b import CountryCode, _Contract, _digits_only

# text that is more than spaces
Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

# ------------------------------------------------------------------ importer


class Supplier(_Contract):
    """
    One supplier of the importer. Table `supplier`. The importer step builds it from the CSV.
    """

    supplier_id: str
    importer: str = Field(examples=["Bergmann"])
    name: Text
    city: str | None = None
    country: CountryCode  # two letters, as in the CSV


class PurchaseLine(_Contract):
    """
    One row of the importer's CSV, column for column. Table `purchase_line`.
    """

    line_id: str = Field(examples=["L01"])
    description: Text  # the goods in the importer's words
    cn_code: str | None = Field(default=None, pattern=r"^\d{8}$")  # L05 to L08 have none
    taric_code: str | None = Field(default=None, pattern=r"^\d{10}$")  # may be missing
    supplier_name: Text
    supplier_country: CountryCode
    producer_name: Text  # the producer named on the invoice
    origin: CountryCode  # made in
    country_of_dispatch: CountryCode  # sent from
    invoice_declaration_present: bool  # "yes" or "no" in the CSV
    annual_customs_value_eur: Decimal = Field(ge=0)
    in_transit_value_eur: Decimal = Field(default=Decimal(0), ge=0)
    incoterm: str | None = Field(default=None, examples=["FOB"])
    # in the schema, not in the CSV yet
    net_weight_kg: Decimal | None = Field(default=None, ge=0)
    quantity: Decimal | None = Field(default=None, ge=0)
    quantity_unit: str | None = None

    @field_validator("cn_code", "taric_code", mode="before")
    @classmethod
    def _strip_spaces(cls, value: str | None) -> str | None:
        if value is None or not value.strip():
            return None
        return _digits_only(value)


# ------------------------------------------------------------------ scope judge

Verdict = Literal["excluded", "not_excluded", "abstain"]


class ScopeJudgement(_Contract):
    """
    The scope judge's proposal for one match. A person confirms it.
    """

    match_id: str
    verdict: Verdict
    quote: Text | None = None  # word for word from the act
    section_id: str | None = None  # Added: where the quote is, for highlighting
    reason: Text
    model: str
    created_at: AwareDatetime
    confirmed_by: str | None = None  # Added: None until a person clicks

    @model_validator(mode="after")
    def _a_verdict_needs_a_quote(self) -> ScopeJudgement:
        if self.verdict != "abstain" and not self.quote:
            raise ValueError("only 'abstain' may come without a quote")
        if self.quote and not self.section_id:
            raise ValueError("a quote needs its section_id")
        return self


# ------------------------------------------------------------------ decisions

Answer = Literal["yes", "no", "not_sure", "continue_unverified"]


class Decision(_Contract):
    """
    What a person settled. Table `decision`. Never edited, a new answer is a new row.
    """

    decision_id: str
    match_id: str
    question: str = Field(examples=["same_legal_entity"])
    answer: Answer
    reason: Text  # required, "yes" alone cannot be saved
    decided_by: str
    decided_at: AwareDatetime


class AuditEvent(_Contract):
    """
    One line of the log. Table `audit_event`. Nothing is ever deleted.
    """

    event_id: str
    ts: AwareDatetime
    actor: str = Field(examples=["thomas", "pipeline"])
    kind: str = Field(examples=["decision_made"])
    payload: dict[str, Any] = {}
