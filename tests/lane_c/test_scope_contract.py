import json

import pytest
from pydantic import ValidationError

from trade_defence_desk.contracts.scope import (
    QuoteStatus,
    ScopeJudgement,
    ScopeJudgeOutput,
    ScopeLimitKind,
    ScopeVerdict,
)


def test_l03_fixture_is_valid_and_usable(fixtures):
    j = ScopeJudgement.model_validate(
        json.loads((fixtures / "scope_judgement_L03.json").read_text())
    )
    assert j.verdict is ScopeVerdict.OUTSIDE_SCOPE
    assert j.usable


def test_l09_not_sure_needs_no_quote(fixtures):
    j = ScopeJudgement.model_validate(
        json.loads((fixtures / "scope_judgement_L09.json").read_text())
    )
    assert j.quote is None and j.usable


def test_quote_digits_are_fine_but_explanation_digits_are_not():
    ScopeJudgeOutput(
        verdict="outside_scope",
        limit_kind="description_limit",
        quote="of a thickness exceeding 0,5 mm but not exceeding 1,8 mm",
        explanation="The line states a thickness above the quoted range.",
    )
    with pytest.raises(ValidationError, match="number guard"):
        ScopeJudgeOutput(
            verdict="outside_scope",
            limit_kind="description_limit",
            quote="of a thickness exceeding 0,5 mm but not exceeding 1,8 mm",
            explanation="The line is 3 mm thick, above 1,8 mm.",
        )


def test_number_words_are_caught_too():
    with pytest.raises(ValidationError, match="number guard"):
        ScopeJudgeOutput(
            verdict="not_sure",
            limit_kind="none",
            explanation="It weighs three hundred grams.",
        )


def test_outside_scope_without_quote_is_refused():
    with pytest.raises(ValidationError, match="needs a quote"):
        ScopeJudgeOutput(
            verdict="outside_scope",
            limit_kind="description_limit",
            explanation="Too thick.",
        )


def test_outside_scope_must_name_its_limit():
    with pytest.raises(ValidationError, match="kind of limit"):
        ScopeJudgeOutput(
            verdict="outside_scope",
            limit_kind="none",
            quote="x",
            explanation="Too thick.",
        )


def test_quote_not_found_is_stored_but_not_usable(fixtures):
    data = json.loads((fixtures / "scope_judgement_L03.json").read_text())
    data["quote_status"] = "not_found"
    data["section_id"] = None
    j = ScopeJudgement.model_validate(data)
    assert not j.usable


def test_found_quote_must_point_at_a_section(fixtures):
    data = json.loads((fixtures / "scope_judgement_L03.json").read_text())
    data["section_id"] = None
    with pytest.raises(ValidationError, match="section_id"):
        ScopeJudgement.model_validate(data)


def test_from_output_keeps_the_model_answer(fixtures):
    out = ScopeJudgeOutput(
        verdict="not_sure", limit_kind="none", explanation="No thickness is given."
    )
    j = ScopeJudgement.from_output(
        out,
        match_id=9,
        purchase_line_id="L09",
        measure_id=1,
        celex="32026R2393",
        quote_status=QuoteStatus.NO_QUOTE,
        section_id=None,
        provider="groq",
        model="openai/gpt-oss-120b",
        prompt_version="scope-v1",
        created_at=__import__("datetime").datetime.fromisoformat("2026-11-02T08:55:00+01:00"),
    )
    assert j.limit_kind is ScopeLimitKind.NONE


def test_naive_datetime_is_refused(fixtures):
    data = json.loads((fixtures / "scope_judgement_L03.json").read_text())
    data["created_at"] = "2026-11-02T08:55:00"
    with pytest.raises(ValidationError):
        ScopeJudgement.model_validate(data)
