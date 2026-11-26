"""
The API, first cut: health, the acts and their text. The screens come later.
"""

from __future__ import annotations

from typing import LiteralString

import psycopg
from fastapi import FastAPI, HTTPException
from psycopg.rows import dict_row

from trade_defence_desk.db import database_url

app = FastAPI(title="Trade Defence Desk")


def _rows(sql: LiteralString, params: list | None = None) -> list[dict]:
    with psycopg.connect(database_url(), connect_timeout=3) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            return cur.execute(sql, params or []).fetchall()


@app.get("/health")
def health() -> dict:
    try:
        _rows("SELECT 1")
        db = "ok"
    except psycopg.Error:
        db = "down"
    return {"status": "ok", "db": db}


@app.get("/acts")
def acts() -> list[dict]:
    return _rows(
        "SELECT celex, title, act_type, date_publication, applicable_from FROM act "
        "WHERE NOT is_holdout_hidden ORDER BY date_publication DESC"
    )


def _visible(celex: str) -> None:
    if not _rows("SELECT 1 FROM act WHERE celex = %s AND NOT is_holdout_hidden", [celex]):
        raise HTTPException(404, f"no act {celex}")


@app.get("/acts/{celex}/text")
def act_text(celex: str, section: str | None = None) -> list[dict]:
    _visible(celex)
    sql = 'SELECT section_id, kind, "order", text FROM act_section WHERE celex = %s'
    params = [celex]
    if section:
        sql += " AND section_id = %s"
        params.append(section)
    return _rows(sql + ' ORDER BY "order"', params)
