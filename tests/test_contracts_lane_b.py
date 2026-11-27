"""Lane B contracts, filled with the real duty table of act 2026/2393 (Article 1).

The act data is real. The invoice names in the NameMatch tests come from
docs/examples/04_WHOSE_NAME_IS_IT.md; Bergmann's invoices are [INVENTED].
"""

from datetime import UTC, date, datetime
from decimal import Decimal
from typing import get_args

import pytest
from pydantic import ValidationError

from trade_defence_desk.contracts import (
    Act,
    CompanyAlias,
    Measure,
    MeasureEvent,
    MeasureProduct,
    MeasureRate,
    NameMatch,
)
from trade_defence_desk.contracts.lane_b import ActType
from trade_defence_desk.triage import ACT_TYPES

BASIS = "net, free-at-Union-frontier price, before duty"
M = "AD-2026-2393"


def test_act_types_match_triage():
    assert set(get_args(ActType)) == set(ACT_TYPES)


def test_act_from_the_download():
    act = Act(
        celex="32026R2393",
        kind="regulation",
        title="imposing a definitive anti-dumping duty ... PET Spunbond ...",
        act_type="definitive",
        type_confidence="high",
        date_document=date(2026, 10, 29),
        date_publication=date(2026, 10, 30),
        applicable_from=date(2026, 10, 31),
        source_url="http://publications.europa.eu/resource/celex/32026R2393",
        sha256="0" * 64,
        bytes=232_083,
        fetched_at=datetime(2026, 11, 23, tzinfo=UTC),
    )
    assert act.is_holdout_hidden is False


def test_unknown_field_is_an_error():
    with pytest.raises(ValidationError):
        CompanyAlias(rate_id="r1", name="x", typo_field=1)


def test_measure_2393():
    m = Measure(
        measure_id=M,
        kind="AD",
        stage="definitive",
        product_text="certain non-woven needle-punched sheets of polyester filaments ...",
        origin_countries=["CN"],
        legal_act_celex="32026R2393",
        valid_from=date(2026, 10, 31),
        valid_to_basis="expected_5y",
        status="in_force",
    )
    assert m.valid_to is None


def test_no_computed_end_date():
    with pytest.raises(ValidationError, match="valid_to"):
        Measure(
            measure_id=M,
            kind="AD",
            stage="definitive",
            product_text="x",
            origin_countries=["CN"],
            legal_act_celex="32026R2393",
            valid_to=date(2031, 10, 31),
            valid_to_basis="expected_5y",
            status="in_force",
        )


def test_registered_only_needs_registration_stage():
    with pytest.raises(ValidationError, match="registered_only"):
        Measure(
            measure_id=M,
            kind="AD",
            stage="definitive",
            product_text="x",
            origin_countries=["CN"],
            legal_act_celex="32026R2393",
            status="registered_only",
        )


def test_duty_table_2393_with_grouped_cell():
    rates = [
        MeasureRate(
            rate_id="r1",
            measure_id=M,
            origin_country="CN",
            taric_additional_code="88CB",
            rate_category="individual",
            rate_pct=Decimal("39.8"),
            basis=BASIS,
        ),
        MeasureRate(
            rate_id="r2",
            measure_id=M,
            origin_country="CN",
            taric_additional_code="88CC",
            rate_category="individual",
            rate_pct=Decimal("48.1"),
            basis=BASIS,
        ),
        MeasureRate(
            rate_id="r3",
            measure_id=M,
            origin_country="CN",
            rate_category="cooperating_not_sampled",
            rate_pct=Decimal("47.1"),
            basis=BASIS,
        ),
        MeasureRate(
            rate_id="r4",
            measure_id=M,
            origin_country="CN",
            taric_additional_code="8999",
            rate_category="residual",
            rate_pct=Decimal("48.1"),
            basis=BASIS,
        ),
    ]
    aliases = [
        CompanyAlias(rate_id="r1", name="Hubei Unibon nonwovens Co Ltd"),
        CompanyAlias(rate_id="r2", name="Changde Tiandingfeng Nonwovens Co Ltd"),
        CompanyAlias(rate_id="r2", name="Tiandingfeng Nonwovens Co Ltd"),
    ]
    assert rates[0].rate_pct == Decimal("39.8")
    assert sum(a.rate_id == "r2" for a in aliases) == 2  # one row, two names


def test_rate_without_percentage_goes_to_a_person():
    with pytest.raises(ValidationError, match="needs_review"):
        MeasureRate(
            rate_id="r9",
            measure_id=M,
            origin_country="CN",
            rate_category="individual",
            amount=Decimal("120"),
            unit="tonne",
            currency="EUR",
            basis=BASIS,
        )


def test_product_codes_with_non_breaking_spaces():
    p = MeasureProduct(
        measure_id=M, cn_code="5603 14 80", is_ex_code=True, taric_code="5603 14 80 70"
    )
    assert p.cn_code == "56031480"
    assert p.taric_code == "5603148070"


def test_bad_product_code():
    with pytest.raises(ValidationError):
        MeasureProduct(measure_id=M, cn_code="5603 14", is_ex_code=False)


def test_amendment_goes_to_a_person():
    with pytest.raises(ValidationError, match="needs_review"):
        MeasureEvent(
            measure_id=M,
            celex="32027R0001",
            event_type="amended",
            quote="Article 1 is amended as follows",
        )
    ok = MeasureEvent(
        measure_id=M,
        celex="32027R0001",
        event_type="amended",
        quote="Article 1 is amended as follows",
        needs_review=True,
    )
    assert ok.needs_review


def test_name_match_tiers():
    hit = NameMatch(
        purchase_line_id="L01",
        matched_on="producer",
        invoice_name="Hubei Unibon Non-Woven Co., Ltd.",
        rate_id="r1",
        act_name="Hubei Unibon nonwovens Co Ltd",
        tier="uncertain",
        score=0.955,
        matcher_version="baseline-rapidfuzz-v1",
    )
    assert hit.rate_id == "r1"
    miss = NameMatch(
        purchase_line_id="L01",
        matched_on="producer",
        invoice_name="Hubei Unibon New Materials Co., Ltd.",
        tier="no_match",
        score=0.667,
        matcher_version="baseline-rapidfuzz-v1",
        related_name_hint="Hubei Unibon nonwovens Co Ltd",
    )
    assert miss.rate_id is None


def test_name_match_needs_row_unless_no_match():
    with pytest.raises(ValidationError, match="rate_id"):
        NameMatch(
            purchase_line_id="L01",
            matched_on="producer",
            invoice_name="x",
            tier="very_likely",
            score=0.98,
            matcher_version="v1",
        )


def test_score_is_zero_to_one():
    with pytest.raises(ValidationError):
        NameMatch(
            purchase_line_id="L01",
            matched_on="producer",
            invoice_name="x",
            tier="no_match",
            score=95.5,
            matcher_version="v1",
        )


def test_name_match_supplier_fallback():
    # Line L02 [INVENTED]: the invoice names no producer, so the matcher compares the
    # supplier, a trader. The case page must say that the supplier was compared.
    fallback = NameMatch(
        purchase_line_id="L02",
        matched_on="supplier",
        invoice_name="Ningbo Seaway Trading Co., Ltd.",
        tier="no_match",
        score=0.31,
        matcher_version="baseline-rapidfuzz-v1",
    )
    assert fallback.matched_on == "supplier"


def test_name_match_on_only_producer_or_supplier():
    with pytest.raises(ValidationError, match="matched_on"):
        NameMatch(
            purchase_line_id="L02",
            matched_on="seller",
            invoice_name="x",
            tier="no_match",
            score=0.1,
            matcher_version="v1",
        )


def test_name_match_needs_purchase_line():
    with pytest.raises(ValidationError, match="purchase_line_id"):
        NameMatch(
            matched_on="producer",
            invoice_name="x",
            tier="no_match",
            score=0.1,
            matcher_version="v1",
        )
