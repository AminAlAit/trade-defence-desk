"""
Stores one sample act in Postgres: the act, its sections, its measure and its duty rows.

M1 only. Later Suma's ingest writes `act` and her ledger (B-06) writes the measure tables.
Run it with: uv run python -m trade_defence_desk.store 32026R2393
"""

from __future__ import annotations

import hashlib
import re
import sys
from datetime import UTC, date, datetime, timedelta
from typing import NamedTuple

import psycopg
from psycopg import sql

from trade_defence_desk.contracts.lane_a import ActSection, DutyRow
from trade_defence_desk.contracts.lane_b import Act, CompanyAlias, Measure, MeasureRate, Stage
from trade_defence_desk.db import database_url
from trade_defence_desk.normalise import load_sample, normalise
from trade_defence_desk.parse_tables import parse_duty_rows
from trade_defence_desk.triage import triage


class Sample(NamedTuple):
    signed: date
    published: date
    origin: str


# From data/sample_acts/README.md. The fixed example acts only.
SAMPLES = {
    "32026R2393": Sample(date(2026, 10, 29), date(2026, 10, 30), "CN"),
    "32026R2311": Sample(date(2026, 10, 19), date(2026, 10, 20), "KR"),
}
FETCHED = datetime(2026, 11, 23, tzinfo=UTC)
BASIS = re.compile(r"applicable to the (net, free-at-Union-frontier price, before duty)")


def build_act(celex: str, raw: bytes, sections: list[ActSection]) -> Act:
    """
    The act row, from the file and the sample README.
    """
    meta = SAMPLES[celex]
    title = next(s.text for s in sections if s.kind == "title")
    kind = triage(celex, title)
    return Act.model_validate(
        {
            "celex": celex,
            "kind": "regulation",
            "title": title,
            "act_type": kind.act_type,
            "type_confidence": kind.confidence,
            "oj_ref": f"OJ L, {celex[1:5]}/{int(celex[6:])}",
            "date_document": meta.signed,
            "date_publication": meta.published,
            # both acts enter into force "on the day following that of its publication"
            "applicable_from": meta.published + timedelta(days=1),
            "source_url": f"http://publications.europa.eu/resource/celex/{celex}",
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "fetched_at": FETCHED,
        }
    )


def build_measure(act: Act, sections: list[ActSection]) -> Measure:
    """
    One measure card for the act. Lane B's ledger builds these after M1.
    """
    stage: Stage = "definitive" if act.act_type.startswith("definitive") else "provisional"
    product = next(s.text for s in sections if s.section_id == "art_1.1")
    return Measure(
        measure_id=act.celex,  # agreed with Suma for M1: the act's celex
        kind="AD",
        stage=stage,
        product_text=product,
        origin_countries=[SAMPLES[act.celex].origin],
        legal_act_celex=act.celex,
        valid_from=act.applicable_from,
        valid_from_basis="art_4.1" if act.celex == "32026R2393" else "art_2.1",
        status="in_force",
    )


def duty_basis(sections: list[ActSection]) -> str:
    """
    The price base the rates apply to, in the act's words.
    """
    for s in sections:
        if s.kind == "article" and (found := BASIS.search(s.text)):
            return found.group(1)
    raise ValueError("no price base found in the articles")


def to_ledger(
    measure: Measure, rows: list[DutyRow], basis: str
) -> tuple[list[MeasureRate], list[CompanyAlias]]:
    """
    Parser rows as lane B's MeasureRate and CompanyAlias. One rate per code.
    """
    rates, aliases = [], []
    for row in rows:
        rate_id = f"{measure.measure_id}-{row.taric_additional_code or 'all'}"
        rates.append(
            MeasureRate(
                rate_id=rate_id,
                measure_id=measure.measure_id,
                origin_country=measure.origin_countries[0],
                taric_additional_code=row.taric_additional_code,
                rate_category=row.category,
                rate_pct=row.rate_pct,
                basis=basis,
                valid_from=measure.valid_from,
            )
        )
        aliases += [CompanyAlias(rate_id=rate_id, name=name) for name in row.names]
    return rates, aliases


def _insert(cur: psycopg.Cursor, table: str, row: dict) -> None:
    query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        sql.Identifier(table),
        sql.SQL(", ").join(map(sql.Identifier, row)),
        sql.SQL(", ").join(sql.Placeholder() * len(row)),
    )
    cur.execute(query, list(row.values()))


def save(conn: psycopg.Connection, celex: str) -> dict[str, int]:
    """
    Writes one sample act and everything parsed from it. Running it twice gives the same rows.
    """
    raw = load_sample(celex)
    sections = normalise(raw, celex)
    act = build_act(celex, raw, sections)
    measure = build_measure(act, sections)
    rates, aliases = to_ledger(measure, parse_duty_rows(raw), duty_basis(sections))

    with conn.transaction(), conn.cursor() as cur:
        cur.execute(
            "DELETE FROM company_alias WHERE rate_id IN "
            "(SELECT rate_id FROM measure_rate WHERE measure_id = %s)",
            [measure.measure_id],
        )
        cur.execute("DELETE FROM measure_rate WHERE measure_id = %s", [measure.measure_id])
        cur.execute("DELETE FROM measure WHERE legal_act_celex = %s", [celex])
        cur.execute("DELETE FROM act_section WHERE celex = %s", [celex])
        cur.execute("DELETE FROM act WHERE celex = %s", [celex])
        _insert(cur, "act", act.model_dump())
        for s in sections:
            _insert(cur, "act_section", s.model_dump())
        _insert(cur, "measure", measure.model_dump())
        for r in rates:
            _insert(cur, "measure_rate", r.model_dump())
        for a in aliases:
            _insert(cur, "company_alias", a.model_dump())
    return {"sections": len(sections), "rates": len(rates), "aliases": len(aliases)}


def main(argv: list[str] | None = None) -> None:
    celexes = (argv if argv is not None else sys.argv[1:]) or list(SAMPLES)
    with psycopg.connect(database_url()) as conn:
        for celex in celexes:
            print(celex, save(conn, celex))


if __name__ == "__main__":
    main()
