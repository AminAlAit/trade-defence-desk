from decimal import Decimal

import pytest
from pydantic import ValidationError

from trade_defence_desk.contracts.importer import PurchaseLine, Supplier, supplier_id_for


def _line(**over):
    base = dict(
        id="L01",
        importer_id="bergmann",
        supplier_id="cn-hubei-unibon",
        description="Root-barrier fleece, polyester, 180 g/m2",
        cn_code="5603 14 80",
        taric_code="5603 14 80 70",
        origin="cn",
        country_of_dispatch="CN",
        producer_name="Hubei Unibon Non-Woven Co., Ltd.",
        invoice_declaration_present=True,
        annual_customs_value_eur="400000",
        in_transit_value_eur="36000",
        incoterm="FOB",
    )
    base.update(over)
    return PurchaseLine(**base)


def test_codes_are_cleaned_and_country_upper_cased():
    line = _line()
    assert line.cn_code == "56031480"
    assert line.taric_code == "5603148070"
    assert line.origin == "CN"


def test_money_is_decimal_not_float():
    assert _line().annual_customs_value_eur == Decimal("400000")


def test_taric_must_extend_the_cn_code():
    with pytest.raises(ValidationError, match="does not start with"):
        _line(taric_code="5603139070")


def test_cn_code_taken_from_taric_when_missing():
    assert _line(cn_code=None).effective_cn_code == "56031480"


def test_no_codes_is_allowed_but_has_no_effective_code():
    line = _line(cn_code=None, taric_code=None)
    assert line.effective_cn_code is None


def test_negative_value_is_refused():
    with pytest.raises(ValidationError):
        _line(annual_customs_value_eur="-1")


def test_in_transit_cannot_exceed_the_year():
    with pytest.raises(ValidationError, match="larger than the whole year"):
        _line(in_transit_value_eur="500000")


def test_unknown_field_is_refused():
    with pytest.raises(ValidationError):
        _line(tax_rate="10")


def test_line_is_frozen():
    line = _line()
    with pytest.raises(ValidationError):
        line.origin = "VN"


def test_supplier_id_is_stable():
    a = Supplier.from_name("bergmann", "Ningbo Seaway Trading Co., Ltd.", "CN")
    b = Supplier.from_name("bergmann", "  Ningbo Seaway Trading Co., Ltd.", "cn")
    assert a.id == supplier_id_for("Ningbo Seaway Trading Co., Ltd.", "CN")
    assert a.id == "cn-ningbo-seaway-trading-co-ltd"
    assert b.country == "CN"
