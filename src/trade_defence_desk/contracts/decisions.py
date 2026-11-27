"""Contracts for what a person settles, and the log that remembers it.

Owner: lane C.  Used by: all lanes (C-05 decisions list and log, C-12 proof export,
A reads them for the report, B reads them when a decision touches the ledger).

Two rules from docs/examples/10_FROM_A_CLICK_TO_THE_PROOF.md shape everything here:

1. A decision always has a reason. "Yes" without a reason cannot be saved.
2. Add a row, never rewrite one. A change of mind is a NEW decision that points at the
   old one with `replaces_decision_id`. The audit log is append-only.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any, Self

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, model_validator

from ._lane_c_types import CleanText, Eur


class QuestionKind(StrEnum):
    """Every kind of question the desk can put to a person. One list for all lanes."""

    SAME_LEGAL_ENTITY = "same_legal_entity"  # name matcher tier 3 (lane B), example 04
    OUTSIDE_SCOPE = "outside_scope"  # scope judge proposal (lane C), example 05
    FIELD_NOT_VERIFIED = "field_not_verified"  # amber FieldCheck (lane A), example 03
    PARSER_MODEL_DISAGREE = "parser_model_disagree"  # rule 2 of the AI rules (lane A)
    EXTENDED_MEASURE = "extended_measure"  # liability_basis = consignment, example 07
    MEASURE_NEEDS_REVIEW = "measure_needs_review"  # Measure.needs_review (lane B)
    INVOICE_DECLARATION = "invoice_declaration"  # low rate needs the declaration, example 06


class Answer(StrEnum):
    YES = "yes"
    NO = "no"
    NOT_SURE = "not_sure"
    CONTINUE_UNVERIFIED = "continue_unverified"  # carry the risk on purpose; range stays


# Which answers make sense for which question. The API refuses anything else.
ALLOWED_ANSWERS: dict[QuestionKind, frozenset[Answer]] = {
    QuestionKind.SAME_LEGAL_ENTITY: frozenset(Answer),
    QuestionKind.OUTSIDE_SCOPE: frozenset(Answer),
    QuestionKind.FIELD_NOT_VERIFIED: frozenset({Answer.YES, Answer.NO, Answer.CONTINUE_UNVERIFIED}),
    QuestionKind.PARSER_MODEL_DISAGREE: frozenset(
        {Answer.YES, Answer.NO, Answer.CONTINUE_UNVERIFIED}
    ),
    QuestionKind.EXTENDED_MEASURE: frozenset(
        {Answer.YES, Answer.NO, Answer.NOT_SURE, Answer.CONTINUE_UNVERIFIED}
    ),
    QuestionKind.MEASURE_NEEDS_REVIEW: frozenset(
        {Answer.YES, Answer.NO, Answer.CONTINUE_UNVERIFIED}
    ),
    QuestionKind.INVOICE_DECLARATION: frozenset({Answer.YES, Answer.NO, Answer.NOT_SURE}),
}

# For questions about the act itself, the answer must say which value is right.
_NEEDS_CHOSEN_VALUE = {QuestionKind.PARSER_MODEL_DISAGREE}


class Decision(BaseModel):
    """One answer of one person to one question. Never edited after it is saved."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: int | None = Field(default=None, description="set by the database")

    question: QuestionKind
    # What the question is about. Exactly one of the two is set.
    match_id: int | None = Field(default=None, description="a purchase line against a measure")
    field_check_id: int | None = Field(default=None, description="a field of an act extraction")

    answer: Answer
    chosen_value: str | None = Field(
        default=None,
        description="for parser_model_disagree: the value the person confirms",
    )
    reason: CleanText = Field(min_length=5, max_length=2000)
    decided_by: CleanText = Field(examples=["thomas"])
    decided_at: AwareDatetime

    replaces_decision_id: int | None = Field(
        default=None, description="set when this answer changes an earlier one"
    )

    @model_validator(mode="after")
    def _rules(self) -> Self:
        if (self.match_id is None) == (self.field_check_id is None):
            raise ValueError("set exactly one of match_id or field_check_id")
        if self.answer not in ALLOWED_ANSWERS[self.question]:
            raise ValueError(f"answer {self.answer} is not allowed for {self.question}")
        if (
            self.question in _NEEDS_CHOSEN_VALUE
            and self.answer is Answer.YES
            and not self.chosen_value
        ):
            raise ValueError("say which value is right in chosen_value")
        if self.replaces_decision_id is not None and self.replaces_decision_id == self.id:
            raise ValueError("a decision cannot replace itself")
        return self

    @property
    def closes_question(self) -> bool:
        """Does this answer close the question? not_sure keeps it open on the list.
        continue_unverified closes it, but the case keeps showing the accepted risk."""
        return self.answer is not Answer.NOT_SURE


class AuditKind(StrEnum):
    DECISION_MADE = "decision_made"
    DECISION_REPLACED = "decision_replaced"
    CONTINUED_UNVERIFIED = "continued_unverified"
    IMPORTER_UPLOADED = "importer_uploaded"
    SCOPE_JUDGED = "scope_judged"
    EVIDENCE_EXPORTED = "evidence_exported"
    ASSUMPTION_CHANGED = "assumption_changed"  # for example the freight uplift on a line


class ExposureSnapshot(BaseModel):
    """The euro range at one moment, so the log can show before and after."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    low_eur: Eur
    high_eur: Eur

    @model_validator(mode="after")
    def _ordered(self) -> Self:
        if self.low_eur > self.high_eur:
            raise ValueError("low_eur is above high_eur")
        return self


class AuditEvent(BaseModel):
    """One line of the log. Append-only: the database refuses UPDATE and DELETE.

    `payload` is free JSON, so each kind can carry what it needs. For decisions it
    holds `before` and `after` as ExposureSnapshot, which the proof export prints.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: int | None = Field(default=None, description="set by the database")
    ts: AwareDatetime
    actor: CleanText = Field(examples=["thomas", "system:upload", "system:scope_judge"])
    kind: AuditKind
    decision_id: int | None = None
    match_id: int | None = None
    payload: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _decision_events_point_at_decision(self) -> Self:
        decision_kinds = {
            AuditKind.DECISION_MADE,
            AuditKind.DECISION_REPLACED,
            AuditKind.CONTINUED_UNVERIFIED,
        }
        if self.kind in decision_kinds and self.decision_id is None:
            raise ValueError(f"{self.kind} needs decision_id")
        return self

    @classmethod
    def for_decision(
        cls,
        decision: Decision,
        *,
        line_id: str | None,
        measure_label: str | None,
        before: ExposureSnapshot | None,
        after: ExposureSnapshot | None,
    ) -> AuditEvent:
        """Build the log line for a saved decision. The decision must already have its id."""
        if decision.id is None:
            raise ValueError("save the decision first, so the log can point at its id")
        if decision.replaces_decision_id is not None:
            kind = AuditKind.DECISION_REPLACED
        elif decision.answer is Answer.CONTINUE_UNVERIFIED:
            kind = AuditKind.CONTINUED_UNVERIFIED
        else:
            kind = AuditKind.DECISION_MADE
        payload: dict[str, Any] = {
            "question": decision.question.value,
            "answer": decision.answer.value,
            "line": line_id,
            "measure": measure_label,
        }
        if decision.replaces_decision_id is not None:
            payload["replaces_decision_id"] = decision.replaces_decision_id
        if before is not None:
            payload["before"] = before.model_dump(mode="json")
        if after is not None:
            payload["after"] = after.model_dump(mode="json")
        return cls(
            ts=decision.decided_at,
            actor=decision.decided_by,
            kind=kind,
            decision_id=decision.id,
            match_id=decision.match_id,
            payload=payload,
        )
