"""Find trade defence documents in the EU catalogue, download them, store them unchanged.

Lane B. Backlog items B-01 (find), B-02 (download and store) and B-03 (backfill and counts).

Run it:

    uv run python -m trade_defence_desk.ingest backfill --months 24

Rule for week 1 (docs/09_ROADMAP.md): until the sealed exam is drawn, only downloading
and title rules run on these acts. Nothing in this file reads the act text.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import re
import time
from collections import Counter
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Literal
from urllib.parse import quote

import httpx
from pydantic import BaseModel

from trade_defence_desk.triage import RULES_VERSION, triage

SPARQL_URL = "https://publications.europa.eu/webapi/rdf/sparql"
ACT_URL = "http://publications.europa.eu/resource/celex/{celex}"
STORE_DIR = Path("data/acts")
INDEX_NAME = "index.csv"

Kind = Literal["regulation", "decision", "notice"]

# B-01: the query. It asks the catalogue for every English document in a date window
# whose CELEX number is a regulation (3YYYYR...), a decision (3YYYYD...) or a notice
# in the C series (5YYYYXC...), and whose title names a trade defence instrument.
# Safeguards are out of our scope, but the desk shows them (decision D-20), so we find
# them too. The bare word "safeguard" is too wide: it also finds foreign policy decisions
# ("to safeguard freedom of navigation"), Euratom nuclear safeguards and a central bank
# decision [MEASURED 2026-11-26]. So we ask for "safeguard measure", "safeguard
# investigation" and "safeguard clause". Corrections ("corrigenda") have CELEX numbers
# like 32026R2138R(01) and are found by the same pattern.
QUERY = """
PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT DISTINCT ?celex ?date ?title WHERE {
  ?work cdm:resource_legal_id_celex ?celex ;
        cdm:work_date_document ?date .
  ?exp cdm:expression_belongs_to_work ?work ;
       cdm:expression_title ?title ;
       cdm:expression_uses_language
         <http://publications.europa.eu/resource/authority/language/ENG> .
  FILTER(?date >= "$start"^^xsd:date && ?date <= "$end"^^xsd:date)
  FILTER(REGEX(STR(?celex), "^(3[0-9]{4}[RD]|5[0-9]{4}XC)"))
  FILTER(CONTAINS(LCASE(STR(?title)), "anti-dumping")
      || CONTAINS(LCASE(STR(?title)), "countervailing")
      || CONTAINS(LCASE(STR(?title)), "anti-subsidy")
      || CONTAINS(LCASE(STR(?title)), "safeguard measure")
      || CONTAINS(LCASE(STR(?title)), "safeguard investigation")
      || CONTAINS(LCASE(STR(?title)), "safeguard clause"))
}
"""


class FoundDocument(BaseModel):
    """One document the catalogue lists. Nothing downloaded yet."""

    celex: str
    kind: Kind
    title: str
    date_document: date


class StoredAct(BaseModel):
    """One row of data/acts/index.csv: what we found, plus the download facts."""

    celex: str
    kind: Kind
    title: str
    date_document: date
    source_url: str
    language: str = "eng"
    sha256: str = ""  # fingerprint of the unpacked text; empty for notices (not downloaded)
    bytes: int = 0  # size of the unpacked text
    fetched_at: str = ""  # when we downloaded it, UTC


# ---------------------------------------------------------------- B-01: find


def kind_of(celex: str) -> Kind:
    """Tell the kind of document from its CELEX number."""
    if celex.startswith("5"):
        return "notice"
    if celex[5] == "D":
        return "decision"
    return "regulation"


def clean_title(title: str) -> str:
    """The catalogue uses non-breaking spaces. Make them normal spaces for the index."""
    return re.sub(r"\s+", " ", title.replace(" ", " ")).strip()


def parse_sparql_result(data: dict) -> list[FoundDocument]:
    """Turn the catalogue's JSON answer into a list, one entry per CELEX number."""
    found: dict[str, FoundDocument] = {}
    for row in data["results"]["bindings"]:
        celex = row["celex"]["value"]
        if celex in found:  # the same work can come back with two titles
            continue
        found[celex] = FoundDocument(
            celex=celex,
            kind=kind_of(celex),
            title=clean_title(row["title"]["value"]),
            date_document=date.fromisoformat(row["date"]["value"][:10]),
        )
    return sorted(found.values(), key=lambda d: (d.date_document, d.celex))


def find_documents(client: httpx.Client, start: date, end: date) -> list[FoundDocument]:
    """Ask the catalogue which trade defence documents are dated from start to end."""
    query = QUERY.replace("$start", start.isoformat()).replace("$end", end.isoformat())
    response = client.post(
        SPARQL_URL,
        data={"query": query},
        headers={"Accept": "application/sparql-results+json"},
        timeout=120,
    )
    response.raise_for_status()
    return parse_sparql_result(response.json())


# ---------------------------------------------------- B-02: download and store


def act_url(celex: str) -> str:
    """The address of one act's text.

    A correction has a CELEX number like 32025R0074R(01). The server answers 404 when the
    brackets are sent as they are, and 200 when they are encoded as %28 and %29
    [MEASURED 2026-11-25].
    """
    return ACT_URL.format(celex=quote(celex, safe=""))


def download_text(client: httpx.Client, celex: str) -> bytes:
    """Download the English XHTML text of one act, exactly as the server sends it."""
    response = client.get(
        act_url(celex),
        headers={"Accept": "application/xhtml+xml", "Accept-Language": "eng"},
        follow_redirects=True,
        timeout=120,
    )
    response.raise_for_status()
    return response.content


def fingerprint(content: bytes) -> str:
    """SHA-256 of the unpacked text, the same fingerprint as data/sample_acts/README.md."""
    return hashlib.sha256(content).hexdigest()


def file_name(celex: str) -> str:
    return f"{celex}.xhtml.gz"


def save_compressed(path: Path, content: bytes) -> None:
    """Write gzip with a fixed time stamp, so the same text always gives the same file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as gz:
        gz.write(content)


def read_index(store: Path) -> dict[str, StoredAct]:
    index = store / INDEX_NAME
    if not index.exists():
        return {}
    with index.open(encoding="utf-8", newline="") as fh:
        return {row["celex"]: StoredAct.model_validate(row) for row in csv.DictReader(fh)}


def write_index(store: Path, acts: dict[str, StoredAct]) -> None:
    store.mkdir(parents=True, exist_ok=True)
    fields = list(StoredAct.model_fields)
    with (store / INDEX_NAME).open("w", encoding="utf-8", newline="\n") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for act in sorted(acts.values(), key=lambda a: (a.date_document, a.celex)):
            writer.writerow(act.model_dump(mode="json"))


def store_act(store: Path, doc: FoundDocument, content: bytes, now: datetime) -> StoredAct:
    """Store one downloaded text unchanged, with fingerprint, size and time.

    If the same text is already stored, nothing is written again (B-02: the same act
    fetched twice is stored once).
    """
    digest = fingerprint(content)
    known = read_index(store).get(doc.celex)
    if known is not None and known.sha256 == digest and (store / file_name(doc.celex)).exists():
        return known
    save_compressed(store / file_name(doc.celex), content)
    return StoredAct(
        celex=doc.celex,
        kind=doc.kind,
        title=doc.title,
        date_document=doc.date_document,
        source_url=act_url(doc.celex),
        sha256=digest,
        bytes=len(content),
        fetched_at=now.isoformat(timespec="seconds"),
    )


# ------------------------------------------------------- B-03: count by type


def count_report(acts: list[StoredAct], start: date, end: date) -> str:
    """A short Markdown report: how many documents of each kind and type."""
    by_kind = Counter(a.kind for a in acts)
    by_type = Counter((a.kind, triage(a.celex, a.title).act_type) for a in acts)
    lines = [
        f"# Counts per act type, {start} to {end}",
        "",
        "Made by `uv run python -m trade_defence_desk.ingest backfill` (B-03).",
        "Window: the date of the document, as the catalogue records it.",
        f"Types come from the triage title rules of B-05, version {RULES_VERSION}.",
        "",
        "| Kind | Count |",
        "|---|---|",
        *[f"| {k} | {by_kind[k]} |" for k in ("regulation", "decision", "notice")],
        f"| **all** | **{len(acts)}** |",
        "",
        "| Kind | Type | Count |",
        "|---|---|---|",
        *[f"| {k} | {t} | {n} |" for (k, t), n in sorted(by_type.items())],
        "",
    ]
    return "\n".join(lines)


# ------------------------------------------------------------------ commands


def backfill(months: int, store: Path, report: Path | None, pause: float = 1.0) -> None:
    end = datetime.now(UTC).date()
    start = end - timedelta(days=round(months * 365.25 / 12))
    acts = read_index(store)
    with httpx.Client(headers={"User-Agent": "trade-defence-desk (student project)"}) as client:
        found = find_documents(client, start, end)
        print(f"found {len(found)} documents from {start} to {end}")
        failed: list[str] = []
        for i, doc in enumerate(found, 1):
            if doc.kind == "notice":
                # Notices are listed, not downloaded: the ledger needs only their title
                # and date (docs/05_DATA_SCHEMA.md, table `notice`).
                acts[doc.celex] = StoredAct(**doc.model_dump(), source_url=act_url(doc.celex))
                continue
            if doc.celex in acts and (store / file_name(doc.celex)).exists():
                continue  # already stored; a re-run does not download it again
            try:
                content = download_text(client, doc.celex)
            except httpx.HTTPError as error:
                failed.append(f"{doc.celex}: {error}")
                continue
            acts[doc.celex] = store_act(store, doc, content, datetime.now(UTC))
            write_index(store, acts)  # save after each act, so a crash loses little
            print(f"{i}/{len(found)} {doc.celex} {len(content):,} bytes")
            time.sleep(pause)  # be polite to the server
    write_index(store, acts)
    window = [a for a in acts.values() if start <= a.date_document <= end]
    text = count_report(window, start, end)
    if failed:
        text += "\n## Not downloaded\n\n" + "\n".join(f"- {f}" for f in failed) + "\n"
    print(text)
    if report is not None:
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(text, encoding="utf-8", newline="\n")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="python -m trade_defence_desk.ingest")
    commands = parser.add_subparsers(dest="command", required=True)
    cmd = commands.add_parser("backfill", help="find, download and count the last N months")
    cmd.add_argument("--months", type=int, default=24)
    cmd.add_argument("--store", type=Path, default=STORE_DIR)
    cmd.add_argument("--report", type=Path, default=None)
    args = parser.parse_args(argv)
    if args.command == "backfill":
        backfill(args.months, args.store, args.report)


if __name__ == "__main__":
    main()
