"""Contracts for the scope judge (C-07): is this purchase line outside the act's scope?

Owner: lane C.  Used by: lane C (case page, decisions list, euro engine),
lane A (the report and the traces).

"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Self

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, model_validator

from ..guards.number_guard import assert_no_free_numbers
from ._lane_c_types import CleanText


class ScopeVerdict(StrEnum):
    """Three answers, nothing else.

    docs/05_DATA_SCHEMA.md calls them excluded, not excluded, abstain.
    docs/04_ARCHITECTURE.md calls them outside scope, inside scope, not sure.
    We propose the second set for the freeze: it follows the wording rules.
    """

    OUTSIDE_SCOPE = "outside_scope"
    INSIDE_SCOPE = "inside_scope"
    NOT_SURE = "not_sure"


class ScopeLimitKind(StrEnum):
    """Which kind of limit the judge relied on (example 05, "Two kinds of outside")."""

    DESCRIPTION_LIMIT = "description_limit"  # a condition in the product sentence
    EXPLICIT_EXCLUSION = "explicit_exclusion"  # a list of products the act leaves out
    NONE = "none"  # the verdict rests on no single limit (inside scope, or not sure)


class ScopeJudgeOutput(BaseModel):
    """The model's answer. Used as the PydanticAI output type.

    The explanation may not contain a single digit or number word: the guard below
    runs inside the model's own retry loop, so a bad answer is sent back, not stored.
    """

    model_config = ConfigDict(extra="forbid")

    verdict: ScopeVerdict
    limit_kind: ScopeLimitKind
    quote: str | None = Field(
        default=None,
        description="one sentence part of the act, copied word for word; required "
        "unless the verdict is not_sure",
    )
    explanation: CleanText = Field(
        max_length=400,
        description="one or two plain sentences, with no numbers in them",
    )

    @model_validator(mode="after")
    def _rules(self) -> Self:
        if self.verdict is not ScopeVerdict.NOT_SURE and not self.quote:
            raise ValueError("a verdict other than not_sure needs a quote from the act")
        if self.verdict is ScopeVerdict.OUTSIDE_SCOPE and self.limit_kind is ScopeLimitKind.NONE:
            raise ValueError("outside_scope must name the kind of limit it relies on")
        assert_no_free_numbers(self.explanation)
        return self


class QuoteStatus(StrEnum):
    """Set by Python after the model answers, never by the model."""

    FOUND = "found"  # the quote is in the act, word for word, after normalising spaces
    NOT_FOUND = "not_found"  # shown amber; the verdict cannot be trusted
    NO_QUOTE = "no_quote"  # only allowed with not_sure


class ScopeJudgement(BaseModel):
    """One stored proposal of the scope judge for one match (purchase line x measure)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: int | None = Field(default=None, description="set by the database")
    match_id: int
    purchase_line_id: str = Field(examples=["L03"])
    measure_id: int
    celex: str = Field(pattern=r"^3\d{4}[A-Z]\d{4}$", examples=["32026R2393"])

    verdict: ScopeVerdict
    limit_kind: ScopeLimitKind
    quote: str | None = None
    quote_status: QuoteStatus
    section_id: str | None = Field(
        default=None,
        description="the ActSection the quote was found in, for highlighting",
    )
    explanation: CleanText

    provider: str = Field(examples=["groq"])
    model: str = Field(examples=["openai/gpt-oss-120b"])
    prompt_version: str = Field(examples=["scope-v1"])
    llm_cache_key: str | None = None
    created_at: AwareDatetime

    @model_validator(mode="after")
    def _consistent(self) -> Self:
        if self.quote is None and self.quote_status is not QuoteStatus.NO_QUOTE:
            raise ValueError("quote_status must be no_quote when there is no quote")
        if self.quote is not None and self.quote_status is QuoteStatus.NO_QUOTE:
            raise ValueError("quote_status no_quote, but a quote is present")
        if self.verdict is not ScopeVerdict.NOT_SURE and self.quote is None:
            raise ValueError("a verdict other than not_sure needs a quote")
        if self.quote_status is QuoteStatus.FOUND and not self.section_id:
            raise ValueError("a found quote must point at its section_id")
        assert_no_free_numbers(self.explanation)
        return self

    @property
    def usable(self) -> bool:
        """May the decisions list show this as the desk's proposal?

        Only if the quote was found in the act, or the judge honestly said not_sure.
        Usable never means decided: Thomas still confirms.
        """
        return self.quote_status is QuoteStatus.FOUND or self.verdict is ScopeVerdict.NOT_SURE

    @classmethod
    def from_output(
        cls,
        output: ScopeJudgeOutput,
        *,
        match_id: int,
        purchase_line_id: str,
        measure_id: int,
        celex: str,
        quote_status: QuoteStatus,
        section_id: str | None,
        provider: str,
        model: str,
        prompt_version: str,
        created_at: datetime,
        llm_cache_key: str | None = None,
    ) -> ScopeJudgement:
        """Wrap the model's answer with what Python found out about it."""
        return cls(
            match_id=match_id,
            purchase_line_id=purchase_line_id,
            measure_id=measure_id,
            celex=celex,
            verdict=output.verdict,
            limit_kind=output.limit_kind,
            quote=output.quote,
            quote_status=quote_status,
            section_id=section_id,
            explanation=output.explanation,
            provider=provider,
            model=model,
            prompt_version=prompt_version,
            llm_cache_key=llm_cache_key,
            created_at=created_at,
        )
