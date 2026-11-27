import json
from datetime import datetime

import pytest
from pydantic import ValidationError

from trade_defence_desk.contracts.decisions import (
    Answer,
    AuditEvent,
    AuditKind,
    Decision,
    ExposureSnapshot,
)

T = datetime.fromisoformat("2026-11-02T09:14:31+01:00")


def _decision(**over):
    base = dict(
        id=41,
        question="same_legal_entity",
        match_id=7,
        answer="yes",
        reason="Licence number matches.",
        decided_by="thomas",
        decided_at=T,
    )
    base.update(over)
    return Decision(**base)


def test_fixtures_from_example_10_are_valid(fixtures):
    d = Decision.model_validate(json.loads((fixtures / "decision_41.json").read_text()))
    e = AuditEvent.model_validate(json.loads((fixtures / "audit_event_1203.json").read_text()))
    assert d.answer is Answer.YES and e.decision_id == d.id


def test_a_reason_is_required():
    with pytest.raises(ValidationError):
        _decision(reason="  ")


def test_exactly_one_subject():
    with pytest.raises(ValidationError, match="exactly one"):
        _decision(field_check_id=3)
    with pytest.raises(ValidationError, match="exactly one"):
        _decision(match_id=None)


def test_answer_must_fit_the_question():
    with pytest.raises(ValidationError, match="not allowed"):
        _decision(
            question="field_not_verified",
            match_id=None,
            field_check_id=3,
            answer="not_sure",
        )


def test_disagreement_needs_the_chosen_value():
    with pytest.raises(ValidationError, match="chosen_value"):
        _decision(question="parser_model_disagree", match_id=None, field_check_id=3)


def test_not_sure_keeps_the_question_open():
    assert not _decision(answer="not_sure").closes_question
    assert _decision(answer="continue_unverified").closes_question


def test_a_change_of_mind_is_a_new_row_and_logs_as_replaced():
    first = _decision()
    second = _decision(
        id=42,
        answer="no",
        reason="Supplier moved to a sister factory.",
        replaces_decision_id=first.id,
    )
    event = AuditEvent.for_decision(
        second,
        line_id="L01",
        measure_label="AD, PET spunbond, China (32026R2393)",
        before=ExposureSnapshot(low_eur=159200, high_eur=159200),
        after=ExposureSnapshot(low_eur=159200, high_eur=192400),
    )
    assert event.kind is AuditKind.DECISION_REPLACED
    assert event.payload["replaces_decision_id"] == 41
    assert event.payload["after"] == {"low_eur": "159200", "high_eur": "192400"}


def test_log_line_needs_a_saved_decision():
    with pytest.raises(ValueError, match="save the decision first"):
        AuditEvent.for_decision(
            _decision(id=None),
            line_id="L01",
            measure_label=None,
            before=None,
            after=None,
        )


def test_audit_event_is_frozen(fixtures):
    e = AuditEvent.model_validate(json.loads((fixtures / "audit_event_1203.json").read_text()))
    with pytest.raises(ValidationError):
        e.actor = "someone else"


def test_range_cannot_be_upside_down():
    with pytest.raises(ValidationError):
        ExposureSnapshot(low_eur=2, high_eur=1)
