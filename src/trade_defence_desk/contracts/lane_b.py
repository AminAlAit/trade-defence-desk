"""Lane B contracts: the act, the ledger, and the name match. Issue X-04, draft v1.

Made by lane B, used by lane A (Act) and lane C (everything else).
See docs/04_ARCHITECTURE.md ("Where the lanes meet") and docs/05_DATA_SCHEMA.md.

The column names follow docs/05_DATA_SCHEMA.md. Where this file adds or changes
something, a comment says so, so all three can check it before the freeze.

Rules from docs/05_DATA_SCHEMA.md ("Six rules the ledger follows") that a shape can
enforce on its own are checked here:

- rule 1: no computed end date;
- rule 5: hard cases go to a person.

Rates are Decimal, never float, so 39,8 stays exactly 39.8.
"""

from __future__ import annotations

import re
from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

# ------------------------------------------------------------------ shared types

# The act types triage gives (src/trade_defence_desk/triage.py, ACT_TYPES).
# A test checks that this list and the triage list stay the same.
ActType = Literal[
    "registration",
    "initiation",
    "provisional",
    "definitive",
    "definitive_expiry_review",
    "extension",
    "amendment",
    "correction",
    "repeal",
    "termination",
    "undertaking",
    "exemption",
    "safeguard",
    "other",
]

# Two letters, ISO 3166 (CN for China). QUESTION FOR THE FREEZE: the schema example
# writes "China"; lane C's PurchaseLine must use the same form, or matching breaks.
CountryCode = str


def _digits_only(value: str) -> str:
    """'5603 14 80' with normal or non-breaking spaces becomes '56031480'."""
    return re.sub(r"[\s  ]", "", value)


class _Contract(BaseModel):
    """Common settings: unknown fields are an error, so a typo never passes silently."""

    model_config = ConfigDict(extra="forbid")


# ------------------------------------------------------------------ group 1: acts


class Act(_Contract):
    """One published act. Table `act`. Made by lane B (download and triage)."""

    celex: str = Field(examples=["32026R2393"])
    # Added: what kind of document. Notices have their own table, but the download
    # index holds all three kinds, so the field says which one this is.
    kind: Literal["regulation", "decision", "notice"]
    title: str
    act_type: ActType
    type_confidence: Literal["high", "low"]
    oj_ref: str | None = Field(default=None, examples=["OJ L, 2026/2393"])
    date_document: date
    date_publication: date | None = None
    applicable_from: date | None = None
    language: str = "eng"
    source_url: str
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    bytes: int = Field(gt=0)
    fetched_at: datetime
    is_holdout_hidden: bool = False


# --------------------------------------------------------------- group 2: ledger

Stage = Literal["registration", "provisional", "definitive"]
MeasureStatus = Literal[
    "in_force",
    "under_review",
    "suspended",
    "registered_only",
    "expired",
    "repealed",
    "superseded",
]
ValidToBasis = Literal["stated", "expected_5y", "provisional_max", "unknown"]


class Measure(_Contract):
    """One duty on one product from one country or group of countries. Table `measure`."""

    measure_id: str
    kind: Literal["AD", "CVD"]  # anti-dumping or anti-subsidy
    stage: Stage
    product_text: str  # the product in the act's own words
    origin_countries: list[CountryCode] = Field(min_length=1)
    liability_basis: Literal["origin", "consignment"] = "origin"
    extends_measure_id: str | None = None
    legal_act_celex: str
    valid_from: date | None = None
    valid_from_basis: str | None = None  # where we read the start date
    valid_to: date | None = None
    valid_to_basis: ValidToBasis = "unknown"
    status: MeasureStatus
    superseded_by: str | None = None
    has_open_event: bool = False
    needs_review: bool = False

    @model_validator(mode="after")
    def _no_computed_end_date(self) -> Measure:
        # Rule 1: valid_to is filled only when an act or a notice states the date.
        if self.valid_to is not None and self.valid_to_basis != "stated":
            raise ValueError("valid_to may only be set when valid_to_basis is 'stated'")
        return self

    @model_validator(mode="after")
    def _registration_is_a_state(self) -> Measure:
        # Rule 2: registration is a state, not a duty.
        if self.status == "registered_only" and self.stage != "registration":
            raise ValueError("status 'registered_only' needs stage 'registration'")
        return self


RateCategory = Literal[
    "individual",  # one named producer or group
    "cooperating_not_sampled",  # "other cooperating companies", listed in the annex
    "residual",  # "all other imports"
    "country_wide",  # one rate for a whole country, no company rows
    "undertaking",  # a price undertaking; stays empty in our four weeks
]


class MeasureRate(_Contract):
    """One row of a duty table: one measure and one TARIC additional code."""

    rate_id: str
    measure_id: str
    origin_country: CountryCode
    # Optional: the "other cooperating companies" row says "See Annex", one code per
    # company there, so the row itself may have no single code.
    taric_additional_code: str | None = Field(default=None, examples=["88CB"])
    rate_category: RateCategory
    rate_pct: Decimal | None = Field(default=None, ge=0, le=100)
    amount: Decimal | None = None
    unit: str | None = None
    currency: str | None = None
    formula_text: str | None = None
    basis: str  # the price base, in the act's words
    valid_from: date | None = None
    valid_to: date | None = None
    needs_review: bool = False

    @model_validator(mode="after")
    def _not_a_simple_percentage_goes_to_a_person(self) -> MeasureRate:
        # Rule 5: a rate that is not a simple percentage is shown, not applied.
        if self.rate_pct is None and not self.needs_review:
            raise ValueError("a rate without rate_pct must have needs_review = True")
        return self


class CompanyAlias(_Contract):
    """One name written in one row. A grouped cell gives several names for one rate_id."""

    rate_id: str
    name: str = Field(min_length=1)  # exactly as the act writes it
    city: str | None = None
    role: Literal["producer", "exporter", "related"] = "producer"


class MeasureProduct(_Contract):
    """One product code a measure covers. Codes are stored as digits only."""

    measure_id: str
    cn_code: str = Field(pattern=r"^\d{8}$", examples=["56031480"])
    is_ex_code: bool  # "ex": only part of the code is covered
    taric_code: str | None = Field(default=None, pattern=r"^\d{10}$")

    @field_validator("cn_code", "taric_code", mode="before")
    @classmethod
    def _strip_spaces(cls, value: str | None) -> str | None:
        return None if value is None else _digits_only(value)


EventType = Literal[
    "review_started",
    "extended",
    "amended",
    "suspended",
    "reinstated",
    "repealed",
    "corrected",
    "undertaking_accepted",
    "undertaking_withdrawn",
    "expiry_notice",
]

# Rule 5 and B-07: these always mark the measure for a person.
EVENTS_FOR_A_PERSON = {
    "amended",
    "corrected",
    "suspended",
    "undertaking_accepted",
    "undertaking_withdrawn",
}


class MeasureEvent(_Contract):
    """Something that happened to a measure later. Table `measure_event`."""

    measure_id: str
    celex: str  # the act or notice that says so
    event_type: EventType
    effective_date: date | None = None
    quote: str = Field(min_length=1)
    needs_review: bool = False

    @model_validator(mode="after")
    def _hard_cases_go_to_a_person(self) -> MeasureEvent:
        if self.event_type in EVENTS_FOR_A_PERSON and not self.needs_review:
            raise ValueError(f"event '{self.event_type}' must have needs_review = True")
        return self


# ------------------------------------------------------- group 4: name matching

# Working proposal from docs/examples/04_WHOSE_NAME_IS_IT.md, marked [INVENTED] there.
# Issue B-10 fixes the tier names and cut-offs.
NameTier = Literal["identical", "very_likely", "uncertain", "no_match"]


class NameMatch(_Contract):
    """The name matcher's answer for one invoice name. Made by lane B, used by lane C.

    The schema stores only name_tier and name_score on `match`. This shape carries a
    little more, so the case page can show which names were compared.
    """

    invoice_name: str  # the producer named on the invoice
    rate_id: str | None = None  # the duty table row it matched; None for no_match
    act_name: str | None = None  # the CompanyAlias name it was compared with
    tier: NameTier
    # 0 to 1. The trained model gives a probability. The baseline's 0 to 100 spelling
    # score is divided by 100.
    score: float = Field(ge=0, le=1)
    matcher_version: str  # for example "baseline-rapidfuzz-v1"
    # "no match, but one name in the act looks related" (example 04, pair 7).
    related_name_hint: str | None = None

    @model_validator(mode="after")
    def _a_match_names_its_row(self) -> NameMatch:
        if self.tier != "no_match" and self.rate_id is None:
            raise ValueError("every tier except 'no_match' needs a rate_id")
        if self.tier == "no_match" and self.rate_id is not None:
            raise ValueError("'no_match' must not point at a rate_id")
        return self
