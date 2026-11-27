"""
Shapes every lane writes: one run, and one event per step. The replay plays these.
"""

from __future__ import annotations

from typing import Literal

from pydantic import AwareDatetime, Field, model_validator

from trade_defence_desk.contracts.lane_b import _Contract

RunKind = Literal["backfill", "daily", "replay", "live"]


class Run(_Contract):
    """
    One run of the pipeline. Table `run`.
    """

    run_id: str
    kind: RunKind
    started_at: AwareDatetime
    finished_at: AwareDatetime | None = None

    @model_validator(mode="after")
    def _ends_after_it_starts(self) -> Run:
        if self.finished_at is not None and self.finished_at < self.started_at:
            raise ValueError("finished_at is before started_at")
        return self


class RunEvent(_Contract):
    """
    One step of one run. Table `run_event`.
    """

    run_id: str
    ts: AwareDatetime  # Added: when the step started, so the replay can order events
    step: str = Field(examples=["normalise", "parse_tables"])
    celex: str | None = None  # Added: which act, when the step works on one
    status: Literal["ok", "failed", "skipped"]
    detail: str = ""
    ms: int = Field(ge=0)
