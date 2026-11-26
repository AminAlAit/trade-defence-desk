"""
Lane A contracts, checked against the example files from 2026/2393 and 2026/2311.
"""

import json
from decimal import Decimal
from pathlib import Path

import pytest
from pydantic import ValidationError

from trade_defence_desk.contracts.lane_a import (
    ActExtraction,
    ActSection,
    DutyRow,
    FieldCheck,
    Quoted,
)

FIXTURES = Path(__file__).parent / "fixtures" / "contracts"


def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


@pytest.mark.parametrize("celex", ["32026R2393", "32026R2311"])
def test_example_files_fit(celex):
    sections = [ActSection(**s) for s in load(f"sections_{celex}.json")]
    assert {s.celex for s in sections} == {celex}
    ActExtraction(**load(f"extraction_{celex}_parser.json"))
    ActExtraction(**load(f"extraction_{celex}_llm_example.json"))


def test_example_quotes_are_in_the_sections():
    text = {s["section_id"]: s["text"] for s in load("sections_32026R2393.json")}
    ex = ActExtraction(**load("extraction_32026R2393_llm_example.json"))
    conditions = ex.conditions
    assert conditions is not None
    quoted = [ex.stage, ex.applies_from_rule, ex.previous_act, *ex.origins, *ex.cn_codes]
    quoted += [conditions.invoice_declaration, conditions.provisional_collection]
    quoted += [conditions.new_exporter_clause]
    for field in quoted:
        assert field is not None
        assert field.quote in text[field.section_id]
        assert field.value in field.quote


def test_2393_parser_example_has_eight_rows():
    ex = ActExtraction(**load("extraction_32026R2393_parser.json"))
    assert len(ex.duty_rows) == 8
    assert ex.duty_rows[0].rate_pct == Decimal("39.8")
    assert ex.duty_rows[1].names == [
        "Changde Tiandingfeng Nonwovens Co Ltd",
        "Tiandingfeng Nonwovens Co Ltd",
    ]


def test_field_checks_fit():
    checks = [FieldCheck(**c) for c in load("field_checks_32026R2393.json")]
    assert [c.status for c in checks] == ["checked_by_program", "quote_found", "not_verified"]


@pytest.mark.parametrize(
    "section_id, kind",
    [
        ("rct_12", "recital"),
        ("art_1.2", "article"),
        ("anx_1.2", "annex"),
        ("tit", "title"),
    ],
)
def test_section_ids(section_id, kind):
    ActSection(celex="32026R2393", section_id=section_id, kind=kind, order=0, text="x")


@pytest.mark.parametrize(
    "section_id, kind",
    [
        ("art_1", "article"),  # no paragraph
        ("rct_12", "article"),  # wrong kind
        ("Article 1", "article"),
    ],
)
def test_bad_section_ids(section_id, kind):
    with pytest.raises(ValidationError):
        ActSection(celex="32026R2393", section_id=section_id, kind=kind, order=0, text="x")


def test_model_reading_names_its_model():
    with pytest.raises(ValidationError):
        ActExtraction(extraction_id="e1", celex="32026R2393", system="llm")


def test_same_code_twice_is_an_error():
    row = DutyRow(
        taric_additional_code="88CB",
        category="individual",
        rate_pct=Decimal("39.8"),
        rate_text="39,8",
        section_id="art_1.2",
    )
    with pytest.raises(ValidationError):
        ActExtraction(extraction_id="e1", celex="32026R2393", system="parser", duty_rows=[row, row])


def test_model_answers_are_kept_for_the_verifier():
    # an odd stage or a doubled row from the model is flagged later, not refused here
    row = DutyRow(
        category="residual", rate_pct=Decimal("48.1"), rate_text="48,1", section_id="art_1.2"
    )
    ActExtraction(
        extraction_id="e1",
        celex="32026R2393",
        system="llm",
        provider="groq",
        model="openai/gpt-oss-120b",
        stage=Quoted(value="Definitive", quote="A definitive", section_id="art_1.1"),
        duty_rows=[row, row],
    )


def test_rate_without_percentage_goes_to_a_person():
    with pytest.raises(ValidationError):
        DutyRow(category="individual", rate_text="EUR 12/t", section_id="art_1.2")
    DutyRow(
        category="individual",
        rate_text="EUR 12/t",
        formula_text="EUR 12/t",
        needs_review=True,
        section_id="art_1.2",
    )


def test_quote_found_needs_the_quote():
    with pytest.raises(ValidationError):
        FieldCheck(extraction_id="e1", field_path="stage", status="quote_found")
