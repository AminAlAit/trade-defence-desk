"""
Reads the duty table from the operative part of an act. Python only, no model.

One DutyRow per TARIC additional code. A "See Annex" row becomes one row per company in
that annex. A grouped cell gives one row with several names. Tables in the reasons are
never read, so the 57,5 underselling margin in 2026/2393 can't leak in.

Anything it doesn't recognise raises ValueError, so the act goes to a person. It never
guesses a row. An act without duty rows (a registration) gives an empty list.
"""

from __future__ import annotations

import re

from lxml import etree  # ty: ignore[missing-module-member]

from trade_defence_desk.contracts.lane_a import DutyRow
from trade_defence_desk.contracts.lane_b import RateCategory
from trade_defence_desk.normalise import X, annex_parts, numbered, text_of, to_decimal

CODE_HEADER = "taric additional code"
CODE = re.compile(r"[A-Z0-9]{4}")
SEE_ANNEX = re.compile(r"see annex(?: ([IVX]+|\d+))?", re.IGNORECASE)
RATE = re.compile(r"(\d+(?:,\d+)?) ?%?")
NAMES_A_RATE = re.compile(r"rates? of the [a-z -]{0,40}duty", re.IGNORECASE)
COUNTRY_WIDE = re.compile(
    r"rate of the (?:definitive|provisional) (?:anti-dumping|countervailing) duty .*?"
    r"shall be (\d+(?:,\d+)?) ?%",
    re.IGNORECASE,
)
ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10}


def _rows(table: etree._Element) -> list[etree._Element]:
    body = table.find(f"{X}tbody")
    return list((body if body is not None else table).findall(f"{X}tr"))


def _cells(row: etree._Element) -> list[etree._Element]:
    return row.findall(f"{X}td")


def _column(header: list[str], *words: str) -> int:
    for i, cell in enumerate(header):
        if all(w in cell.lower() for w in words):
            return i
    raise ValueError(f"no column with {words} in header {header}")


def _names(cell: etree._Element) -> list[str]:
    """
    A grouped cell holds one small table per name, a dash in front. Else the cell is the name.
    """
    inner = cell.findall(f".//{X}table")
    if not inner:
        return [text_of(cell)]
    return [text_of(_cells(_rows(table)[0])[-1]) for table in inner]


def _category(label: str, see_annex: bool) -> RateCategory:
    low = label.lower()
    if low.startswith("all other"):
        return "residual"
    if low.startswith("other cooperating") or see_annex:
        return "cooperating_not_sampled"
    if "other" in low or "compan" in low:
        raise ValueError(f"unknown kind of row: {label!r}")
    return "individual"


def _is_duty_table(table: etree._Element) -> bool:
    rows = _rows(table)
    # the outer table only; its header cells may sit in small tables of their own
    return (
        table.get("class") == "oj-table" and bool(rows) and CODE_HEADER in text_of(rows[0]).lower()
    )


def _article_paragraph_id(el: etree._Element) -> str:
    article = paragraph = None
    for up in [el, *el.iterancestors()]:
        id_ = up.get("id") or ""
        if paragraph is None and re.fullmatch(r"\d{3}\.\d{3}", id_):
            paragraph = int(id_.split(".")[1])
        if re.fullmatch(r"art_\d+", id_):
            article = int(id_.split("_")[1])
            break
    if article is None:
        raise ValueError("duty table outside an article")
    return f"art_{article}.{paragraph or 1}"


def _rate(rate_text: str) -> dict:
    """
    A simple percentage becomes rate_pct. Anything else goes to a person, as written.
    """
    number = RATE.fullmatch(rate_text)
    if number:
        return {"rate_pct": to_decimal(number.group(1)), "rate_text": number.group(1)}
    return {"rate_text": rate_text, "formula_text": rate_text, "needs_review": True}


def _annex_rows(root: etree._Element, which: str | None, rate_text: str) -> list[DutyRow]:
    """
    The companies listed in the annex a "See Annex" row points at, all at that row's rate.
    """
    annexes = numbered(root, "anx")
    if which:
        n = ROMAN.get(which.upper()) or int(which)
        annexes = [(k, a) for k, a in annexes if k == n]
    if len(annexes) != 1:
        raise ValueError(f"'See Annex {which or ''}' fits {len(annexes)} annexes")
    n, annex = annexes[0]

    found = []
    for p, part in enumerate(annex_parts(annex), start=1):
        tables = [part] if etree.QName(part).localname == "table" else part.findall(f".//{X}table")
        found += [(p, t) for t in tables if _is_duty_table(t)]
    if len(found) != 1:
        raise ValueError(f"annex {n} has {len(found)} tables with TARIC additional codes")
    p, table = found[0]

    rows = _rows(table)
    header = [text_of(c) for c in _cells(rows[0])]
    name_col, code_col = _column(header, "name"), _column(header, "taric")
    out = []
    for row in rows[1:]:
        cells = _cells(row)
        if len(cells) != len(header):
            raise ValueError(f"annex {n}: a row with {len(cells)} cells, header has {len(header)}")
        code = text_of(cells[code_col])
        if not CODE.fullmatch(code):
            raise ValueError(f"annex {n}: not a TARIC additional code: {code!r}")
        out.append(
            DutyRow(
                taric_additional_code=code,
                category="cooperating_not_sampled",
                names=[text_of(cells[name_col])],
                section_id=f"anx_{n}.{p}",
                **_rate(rate_text),
            )
        )
    if not out:
        raise ValueError(f"annex {n}: the table has no companies")
    return out


def _table_rows(root: etree._Element, table: etree._Element) -> list[DutyRow]:
    section_id = _article_paragraph_id(table)
    rows = _rows(table)
    header = [text_of(c) for c in _cells(rows[0])]
    code_col = _column(header, "taric")
    rate_col = _column(header, "%")
    out: list[DutyRow] = []
    for row in rows[1:]:
        cells = _cells(row)
        if len(cells) != len(header):
            raise ValueError(
                f"{section_id}: a row with {len(cells)} cells, header has {len(header)}"
            )
        label, rate_text, code = (
            text_of(cells[0]),
            text_of(cells[rate_col]),
            text_of(cells[code_col]),
        )
        see_annex = SEE_ANNEX.fullmatch(code)
        category = _category(label, bool(see_annex))
        if see_annex:
            number = RATE.fullmatch(rate_text)
            out += _annex_rows(root, see_annex.group(1), number.group(1) if number else rate_text)
            continue
        if not CODE.fullmatch(code):
            raise ValueError(f"{section_id}: not a TARIC additional code: {code!r}")
        out.append(
            DutyRow(
                taric_additional_code=code,
                category=category,
                names=[] if category == "residual" else _names(cells[0]),
                section_id=section_id,
                **_rate(rate_text),
            )
        )
    return out


def _country_wide(operative: etree._Element) -> list[DutyRow]:
    """
    One rate for the whole country and no company table, as in 2026/2311.
    """
    found = []
    for div in operative.iter(f"{X}div"):
        if re.fullmatch(r"\d{3}\.\d{3}", div.get("id") or ""):
            found += [(div, m) for m in COUNTRY_WIDE.finditer(text_of(div))]
    if len(found) > 1:
        raise ValueError("more than one country-wide rate, a person reads this act")
    if not found:
        return []
    div, match = found[0]
    rate_text = match.group(1)
    return [
        DutyRow(
            category="country_wide",
            rate_pct=to_decimal(rate_text),
            rate_text=rate_text,
            section_id=_article_paragraph_id(div),
        )
    ]


def parse_duty_rows(raw: bytes) -> list[DutyRow]:
    """
    All duty rows of the act's operative part, in the order the act gives them.
    """
    root = etree.fromstring(raw)
    enacting = root.xpath("//*[@id='enc_1']")
    if not enacting:
        raise ValueError("no operative part (enc_1) in this file")
    operative = enacting[0]

    rows: list[DutyRow] = []
    for table in operative.iter(f"{X}table"):
        if _is_duty_table(table):
            rows += _table_rows(root, table)
    if not rows:
        rows = _country_wide(operative)

    text = text_of(operative)
    if not rows and (CODE_HEADER in text.lower() or NAMES_A_RATE.search(text)):
        raise ValueError("the articles name a duty, but no rate was read")
    return rows
