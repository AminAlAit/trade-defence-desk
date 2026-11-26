"""
Storing 2026/2393. The conversion runs everywhere, the database part only with DATABASE_URL.
"""

import os
from datetime import date
from decimal import Decimal

import pytest

from trade_defence_desk.normalise import load_sample, normalise
from trade_defence_desk.parse_tables import parse_duty_rows
from trade_defence_desk.store import build_act, build_measure, duty_basis, save, to_ledger

CELEX = "32026R2393"


@pytest.fixture(scope="module")
def parts():
    raw = load_sample(CELEX)
    sections = normalise(raw, CELEX)
    act = build_act(CELEX, raw, sections)
    measure = build_measure(act, sections)
    rates, aliases = to_ledger(measure, parse_duty_rows(raw), duty_basis(sections))
    return act, measure, rates, aliases


def test_act_row(parts):
    act = parts[0]
    assert act.act_type == "definitive"
    assert act.applicable_from == date(2026, 10, 31)
    assert act.bytes == 232_083


def test_measure_row(parts):
    measure = parts[1]
    assert measure.measure_id == "AD-2026-2393"
    assert measure.origin_countries == ["CN"]
    assert measure.valid_to is None  # no computed end date


def test_eight_rates_eight_names(parts):
    rates, aliases = parts[2], parts[3]
    assert len(rates) == 8
    assert len(aliases) == 8
    assert rates[0].rate_pct == Decimal("39.8")
    assert rates[0].basis == "net, free-at-Union-frontier price, before duty"


def test_grouped_cell_shares_one_rate_id(parts):
    aliases = parts[3]
    assert sum(a.rate_id == "AD-2026-2393-88CC" for a in aliases) == 2


def test_country_wide_rate_for_2311():
    raw = load_sample("32026R2311")
    sections = normalise(raw, "32026R2311")
    measure = build_measure(build_act("32026R2311", raw, sections), sections)
    rates, aliases = to_ledger(measure, parse_duty_rows(raw), duty_basis(sections))
    assert [(r.rate_id, r.rate_category, r.rate_pct) for r in rates] == [
        ("AD-2026-2311-all", "country_wide", Decimal("15.8"))
    ]
    assert aliases == []


@pytest.mark.skipif("DATABASE_URL" not in os.environ, reason="needs Postgres")
def test_save_twice_same_rows():
    import psycopg

    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        first = save(conn, CELEX)
        second = save(conn, CELEX)
        count = conn.execute(
            "SELECT count(*) FROM measure_rate WHERE measure_id = 'AD-2026-2393'"
        ).fetchone()
    assert first == second == {"sections": 183, "rates": 8, "aliases": 8}
    assert count is not None and count[0] == 8
