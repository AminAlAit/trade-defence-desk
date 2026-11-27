"""Contracts for the importer side: Supplier and PurchaseLine.

Owner: lane C.  Used by: lane B (the synthetic importer generator, B-09),
lane C (CSV upload C-13, product matching C-04, euro engine C-03, scope judge C-07).

See docs/05_DATA_SCHEMA.md, "Group 3: the importer", and
docs/examples/bergmann_purchase_lines.csv for the CSV these shapes come from.

Everything here describes a synthetic importer. No real customer data, ever (D-12).
"""

from __future__ import annotations

import re
from enum import StrEnum
from typing import Self
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, model_validator

from ._lane_c_types import CleanText, CnCode, CountryCode, Eur, TaricCode

_ID = r"^[A-Za-z0-9][A-Za-z0-9_\-]{0,63}$"


class Incoterm(StrEnum):
    """Incoterms 2020. Shown to Thomas; the euro engine reads `value_basis`, not this."""

    EXW = "EXW"
    FCA = "FCA"
    FAS = "FAS"
    FOB = "FOB"
    CFR = "CFR"
    CIF = "CIF"
    CPT = "CPT"
    CIP = "CIP"
    DAP = "DAP"
    DPU = "DPU"
    DDP = "DDP"


class ValueBasis(StrEnum):
    """What the yearly value on the line means.

    customs_value: the price at the EU border, the base the duty is computed on.
    invoice_value: only the price paid; the euro engine adds a labelled freight and
    insurance assumption (example 06, sum 5) and shows it next to the figure.
    """

    CUSTOMS_VALUE = "customs_value"
    INVOICE_VALUE = "invoice_value"


def supplier_id_for(name: str, country: str) -> str:
    """A stable id from name and country, so the same supplier in two uploads is one row."""
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:48]
    return f"{country.lower()}-{slug}"


class Supplier(BaseModel):
    """The company Bergmann buys from. Can be a factory or a trader.

    The duty rate does NOT follow the supplier. It follows the producer named on the
    invoice (D-21). That is why PurchaseLine carries `producer_name` separately.
    """

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    id: str = Field(pattern=_ID, examples=["cn-hubei-unibon-non-woven-co-ltd"])
    importer_id: str = Field(pattern=_ID, examples=["bergmann"])
    name: CleanText = Field(examples=["Ningbo Seaway Trading Co., Ltd."])
    country: CountryCode = Field(examples=["CN"])
    city: CleanText | None = None

    @classmethod
    def from_name(
        cls, importer_id: str, name: str, country: str, city: str | None = None
    ) -> Supplier:
        return cls(
            id=supplier_id_for(name, country),
            importer_id=importer_id,
            name=name,
            country=country,
            city=city,
        )


class PurchaseLine(BaseModel):
    """One product, bought from one supplier, made by one producer, over the last year.

    Codes are optional on purpose: a real importer file often has gaps, and the
    desk must say "unsure" rather than guess (C-04, example 05).
    """

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    id: str = Field(pattern=_ID, examples=["L01"])
    importer_id: str = Field(pattern=_ID, examples=["bergmann"])
    supplier_id: str = Field(pattern=_ID)

    description: CleanText = Field(
        examples=["Root-barrier fleece, polyester, 180 g/m2, 1.2 mm thick, with binder"],
        description="the goods in the importer's own words; the scope judge reads this",
    )
    cn_code: CnCode | None = Field(default=None, examples=["56031480"])
    taric_code: TaricCode | None = Field(default=None, examples=["5603148070"])

    origin: CountryCode = Field(description="where the goods were made", examples=["CN"])
    country_of_dispatch: CountryCode = Field(
        description="where the goods were sent from; decides extended measures (example 07)",
        examples=["CN"],
    )

    producer_name: CleanText | None = Field(
        default=None,
        description="the producer named on the invoice; the name matcher compares this",
        examples=["Hubei Unibon Non-Woven Co., Ltd."],
    )
    invoice_declaration_present: bool = Field(
        description="is the act's signed declaration on the invoice? (Art 1(3) of 2026/2393)",
    )

    annual_customs_value_eur: Eur = Field(description="last year's purchases on this line")
    value_basis: ValueBasis = ValueBasis.CUSTOMS_VALUE
    in_transit_value_eur: Eur = Field(default=Decimal(0), description="shipped, not yet released by customs")

    incoterm: Incoterm | None = None
    net_weight_kg: Eur | None = Field(default=None, description="kilograms; Decimal like money")
    quantity: Eur | None = None
    quantity_unit: CleanText | None = None

    @model_validator(mode="after")
    def _codes_agree(self) -> Self:
        if self.taric_code and self.cn_code and not self.taric_code.startswith(self.cn_code):
            raise ValueError(
                f"taric_code {self.taric_code} does not start with cn_code {self.cn_code}"
            )
        return self

    @model_validator(mode="after")
    def _transit_not_above_year(self) -> Self:
        if self.in_transit_value_eur > self.annual_customs_value_eur:
            raise ValueError("in_transit_value_eur is larger than the whole year's value")
        return self

    @property
    def effective_cn_code(self) -> str | None:
        """The 8-digit code, taken from the TARIC code when only that is given."""
        if self.cn_code:
            return self.cn_code
        return self.taric_code[:8] if self.taric_code else None

    @property
    def name_to_match(self) -> str | None:
        """The producer if the invoice names one. Otherwise None: the matcher then falls
        back to the supplier, and the case page must say so (example 04, "The trader")."""
        return self.producer_name
