"""
Lane C and shared contracts, checked against the example files. Bergmann is [INVENTED].
"""

import csv
import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from trade_defence_desk.contracts.lane_c import (
    AuditEvent,
    Decision,
    PurchaseLine,
    ScopeJudgement,
    Supplier,
)
from trade_defence_desk.contracts.shared import Run, RunEvent

FIXTURES = Path(__file__).parent / "fixtures" / "contracts"
CSV = Path(__file__).parents[1] / "docs" / "examples" / "bergmann_purchase_lines.csv"
NOW = datetime(2026, 11, 27, 8, tzinfo=UTC)


def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_example_files_fit():
    [Supplier(**s) for s in load("suppliers_bergmann.json")]
    [ScopeJudgement(**j) for j in load("scope_judgements.json")]
    both = load("decision_and_audit.json")
    Decision(**both["decision"])
    AuditEvent(**both["audit_event"])
    runs = load("run_events.json")
    Run(**runs["run"])
    [RunEvent(**e) for e in runs["events"]]


def test_the_real_csv_fits():
    with CSV.open(encoding="utf-8", newline="") as f:
        lines = [PurchaseLine(**row) for row in csv.DictReader(f)]
    assert len(lines) == 9
    assert lines[0].invoice_declaration_present is True
    assert lines[1].invoice_declaration_present is False
    assert lines[0].taric_code == "5603148070"
    assert {line.origin for line in lines} == {"CN", "BR", "VN"}


def test_codes_with_spaces_and_an_empty_taric_code():
    with CSV.open(encoding="utf-8", newline="") as f:
        row = next(csv.DictReader(f))
    line = PurchaseLine(**{**row, "cn_code": "5603 14 80", "taric_code": ""})
    assert (line.cn_code, line.taric_code) == ("56031480", None)


def test_a_verdict_needs_a_quote():
    with pytest.raises(ValidationError):
        ScopeJudgement(match_id="M03", verdict="excluded", reason="r", model="m", created_at=NOW)


def test_a_quote_needs_its_section():
    with pytest.raises(ValidationError):
        ScopeJudgement(
            match_id="M03", verdict="excluded", quote="q", reason="r", model="m", created_at=NOW
        )


def test_time_needs_a_timezone():
    with pytest.raises(ValidationError):
        ScopeJudgement(
            match_id="M09",
            verdict="abstain",
            reason="r",
            model="m",
            created_at=datetime(2026, 1, 1),
        )


def test_abstain_needs_no_quote():
    ScopeJudgement(match_id="M09", verdict="abstain", reason="r", model="m", created_at=NOW)


def test_decision_needs_a_reason():
    with pytest.raises(ValidationError):
        Decision(
            decision_id="1",
            match_id="M01",
            question="same_legal_entity",
            answer="yes",
            reason="   ",
            decided_by="thomas",
            decided_at=NOW,
        )


def test_run_ends_after_it_starts():
    with pytest.raises(ValidationError):
        Run(run_id="R1", kind="daily", started_at=NOW, finished_at=datetime(2026, 1, 1, tzinfo=UTC))


def test_negative_time_is_an_error():
    with pytest.raises(ValidationError, match="greater than or equal"):
        RunEvent(run_id="R1", ts=NOW, step="normalise", status="ok", ms=-1)


def test_event_time_needs_a_zone():
    with pytest.raises(ValidationError, match="timezone"):
        RunEvent(run_id="R1", ts=datetime(2026, 11, 27, 8), step="normalise", status="ok", ms=1)
