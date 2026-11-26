"""Triage: the type of an act, from fixed rules on its title.

Lane B. Backlog item B-05. Due: written Thu 26 Nov, frozen Fri 27 Nov, before the sealed
exam is drawn. After the freeze these rules change only with a pull request that says
why, so the exam result is never tuned on the exam.

Run it on every stored document:

    uv run python -m trade_defence_desk.triage --report reports/b05_triage.md

How it reads a title
--------------------
A regulation or decision title names its main action right after its date:

    "Commission Implementing Regulation (EU) 2026/2393 of 29 October 2026
     imposing a definitive anti-dumping duty and definitively collecting ..."

The words after the date ("imposing a definitive ...") are the "operative phrase". The
rules look at how it STARTS, not at words anywhere in the title. That matters: a title
can say "imposing a definitive countervailing duty ... and amending Regulation X". That
act is a definitive duty, not an amendment.

Notices have no date in the title, so their rules read the whole title.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

RULES_VERSION = "b05-2026-11-26"

Confidence = Literal["high", "low"]
Route = Literal["full_extraction", "person", "list_only"]

# Types an act can get. "after an expiry review" is its own type (docs/examples/08).
ACT_TYPES = (
    "registration",
    "initiation",
    "provisional",
    "definitive",
    "definitive_expiry_review",
    "extension",
    "amendment",
    "correction",
    "repeal",
    "termination",
    "undertaking",
    "exemption",
    "safeguard",
    "other",
)

# Types a notice can get. The first six are the `notice_type` values in
# docs/05_DATA_SCHEMA.md. "safeguard" and "correction" are added for the same reasons
# as for acts.
NOTICE_TYPES = (
    "initiation",
    "expiry_review",
    "interim_review",
    "impending_expiry",
    "expiry",
    "other",
    "safeguard",
    "correction",
)

# Decision D-20: these are shown and sent to a person, never handled silently.
TO_PERSON = {"amendment", "correction", "undertaking", "exemption", "other"}


class Triage(BaseModel):
    act_type: str
    confidence: Confidence
    route: Route  # what happens next with this document
    to_person: bool  # D-20: a person looks at it
    rule: str  # which rule decided, so a person can check it


# One rule: (name, pattern on the operative phrase, type, confidence).
# The first rule that matches wins, so the order matters. Each pattern is anchored with
# "^": it must match the START of the operative phrase.
ACT_RULES: list[tuple[str, str, str, Confidence]] = [
    # Out of scope, but shown (D-20). First, so that "amending ... a definitive safeguard
    # measure" is a safeguard and not an amendment.
    ("safeguard", r"safeguard (measure|clause|investigation)", "safeguard", "high"),
    ("correcting", r"^(amending and )?correcting\b", "correction", "high"),
    ("amending", r"^amending\b", "amendment", "high"),
    ("repealing", r"^repealing\b", "repeal", "high"),
    ("terminating", r"^terminating\b", "termination", "high"),
    ("accepting undertaking", r"^accepting (an )?undertaking", "undertaking", "high"),
    ("registration", r"^making imports .* subject to registration", "registration", "high"),
    # "initiating an investigation concerning possible circumvention ... and making such
    # imports subject to registration": an initiation that ALSO starts registration.
    ("initiating", r"^initiating\b", "initiation", "high"),
    ("extending", r"^extending\b", "extension", "high"),
    ("provisional", r"^imposing (a )?provisional\b", "provisional", "high"),
    (
        "definitive after expiry review",
        r"^imposing (a )?definitive\b.*\bfollowing an expiry review\b",
        "definitive_expiry_review",
        "high",
    ),
    ("definitive", r"^imposing (a )?definitive\b", "definitive", "high"),
    # Re-imposing a duty after a court judgment: a definitive duty, but unusual.
    ("reimposing", r"^re-?imposing (a )?definitive\b", "definitive", "low"),
    ("exemption", r"^(revoking the exemption|concerning exemptions?)\b", "exemption", "high"),
]

NOTICE_RULES: list[tuple[str, str, str, Confidence]] = [
    ("notice correction", r"^corrigendum\b", "correction", "high"),
    ("notice safeguard", r"safeguard (measure|investigation)", "safeguard", "high"),
    (
        "notice impending expiry",
        r"^notice of (the )?impending expiry\b",
        "impending_expiry",
        "high",
    ),
    ("notice expiry", r"^notice of (the )?expiry\b", "expiry", "high"),
    (
        "notice expiry review",
        r"^notice of initiation of an expiry review\b",
        "expiry_review",
        "high",
    ),
    (
        "notice interim review",
        r"^notice of initiation of (a |an )?(partial )?interim review\b",
        "interim_review",
        "high",
    ),
    (
        "notice proceeding",
        r"^notice of initiation of an? (anti-dumping|anti-subsidy) proceeding\b",
        "initiation",
        "high",
    ),
    # Reopening, amending a notice, a review after a court or WTO ruling: real events,
    # but each one is different. A person reads them.
    ("notice other", r"^notice\b", "other", "low"),
]

# "... of 29 October 2026 imposing ..." -> "imposing ..."
_DATE = re.compile(
    r"\bof \d{1,2} (January|February|March|April|May|June|July|August|September|October"
    r"|November|December) \d{4},? (?P<rest>.+)$",
    re.IGNORECASE,
)


def operative_phrase(title: str) -> str | None:
    """The words after the act's own date, in lower case. None if there is no date."""
    match = _DATE.search(" ".join(title.split()))
    return match.group("rest").lower() if match else None


def triage(celex: str, title: str) -> Triage:
    """Give one document its type, confidence and route."""
    clean = " ".join(title.split()).lower()

    if celex.startswith("5"):  # a notice
        for name, pattern, act_type, confidence in NOTICE_RULES:
            if re.search(pattern, clean):
                return Triage(
                    act_type=act_type,
                    confidence=confidence,
                    route="list_only",  # notices are listed, not read in full
                    to_person=act_type in TO_PERSON | {"safeguard", "correction"}
                    or confidence == "low",
                    rule=name,
                )
        return Triage(
            act_type="other", confidence="low", route="list_only", to_person=True, rule="none"
        )

    # A corrigendum's title is "Corrigendum to ... Regulation X of DATE imposing ...". The
    # phrase after the date describes act X, not the corrigendum. So check this first.
    if clean.startswith("corrigendum"):
        return _act("correction", "high", "corrigendum")

    phrase = operative_phrase(title)
    if phrase is None:  # no date found: fall back to the whole title, and say so
        phrase = clean
        fallback = True
    else:
        fallback = False

    for name, pattern, act_type, confidence in ACT_RULES:
        # Without a date we cannot know where the phrase starts, so search anywhere.
        if re.search(pattern.removeprefix("^") if fallback else pattern, phrase):
            return _act(act_type, "low" if fallback else confidence, name)
    return _act("other", "low", "none")


def _act(act_type: str, confidence: Confidence, rule: str) -> Triage:
    # B-05: every act goes to full extraction, registrations and initiations included,
    # even though they usually have no duty table (docs/examples/01). Only safeguards,
    # which are out of scope, go straight to a person.
    route: Route = "person" if act_type == "safeguard" else "full_extraction"
    return Triage(
        act_type=act_type,
        confidence=confidence,
        route=route,
        to_person=act_type in TO_PERSON or act_type == "safeguard" or confidence == "low",
        rule=rule,
    )


# ------------------------------------------------------------------ command


def run(store: Path, report: Path | None) -> None:
    index = store / "index.csv"
    with index.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    results = []
    for row in rows:
        t = triage(row["celex"], row["title"])
        results.append({"celex": row["celex"], "kind": row["kind"], **t.model_dump()})

    out = store / "triage.csv"
    with out.open("w", encoding="utf-8", newline="\n") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(results[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)

    by_type = Counter((r["kind"], r["act_type"]) for r in results)
    low = [(r, row) for r, row in zip(results, rows, strict=True) if r["confidence"] == "low"]
    lines = [
        f"# Triage of {len(results)} documents (rules {RULES_VERSION})",
        "",
        "Made by `uv run python -m trade_defence_desk.triage` (B-05).",
        "Every row is in `data/acts/triage.csv`.",
        "",
        "| Kind | Type | Count |",
        "|---|---|---|",
        *[f"| {k} | {t} | {n} |" for (k, t), n in sorted(by_type.items())],
        "",
        f"## Low confidence: {len(low)}",
        "",
        "A person checks these.",
        "",
        "| CELEX | Type | Rule | Title |",
        "|---|---|---|---|",
        *[f"| {r['celex']} | {r['act_type']} | {r['rule']} | {row['title']} |" for r, row in low],
        "",
    ]
    text = "\n".join(lines)
    print(text)
    if report is not None:
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(text, encoding="utf-8", newline="\n")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="python -m trade_defence_desk.triage")
    parser.add_argument("--store", type=Path, default=Path("data/acts"))
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args(argv)
    run(args.store, args.report)


if __name__ == "__main__":
    main()
