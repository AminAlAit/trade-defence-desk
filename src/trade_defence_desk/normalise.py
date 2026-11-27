"""
Cuts an act's XHTML into sections: title, citations, recitals, articles, annexes, final.

Every section gets a stable id (see contracts.lane_a.SECTION_ID), so a quote can point at it.
Text is kept as written. Only spaces are cleaned and footnote markers dropped.
Left out on purpose: headings ("3.5. Dumping margins", "Article 1"), "Whereas:",
"HAS ADOPTED THIS REGULATION:", the "(n)" recital numbers and footnote texts.
A quote never needs them.
"""

from __future__ import annotations

import gzip
import re
from decimal import Decimal
from pathlib import Path

from lxml import etree  # ty: ignore[missing-module-member]

from trade_defence_desk.contracts.lane_a import ActSection, SectionKind

X = "{http://www.w3.org/1999/xhtml}"
SAMPLE_ACTS = Path(__file__).resolve().parents[2] / "data" / "sample_acts"

# block elements get a space around their text, inline ones do not ("g/m" + "2")
BLOCK = {"p", "div", "td", "th", "tr", "table", "tbody", "br", "li"}
GAP = "\x00"  # where a footnote marker was, so the space before it goes too
SPACES = re.compile(r"[\s\u00a0\u2009\u202f\u2007]+")


def load_sample(celex: str) -> bytes:
    """
    The raw XHTML of one act in data/sample_acts.
    """
    return gzip.decompress((SAMPLE_ACTS / f"{celex}.xhtml.gz").read_bytes())


def clean(text: str) -> str:
    """
    All kinds of spaces become one normal space.
    """
    return SPACES.sub(" ", text).strip()


def to_decimal(text: str) -> Decimal:
    """
    '39,8 ' becomes Decimal('39.8'). The text itself stays as written.
    """
    return Decimal(clean(text).replace(",", "."))


def _is_note_marker(el: etree._Element) -> bool:
    # a footnote reference: <a href="#ntr2-...">(<span class="oj-note-tag">2</span>)</a>
    return (el.get("href") or "").startswith("#ntr") or "oj-note-tag" in (el.get("class") or "")


def text_of(el: etree._Element) -> str:
    """
    The readable text of one element, footnote markers left out.
    """
    parts: list[str] = []

    def walk(node: etree._Element) -> None:
        block = etree.QName(node).localname in BLOCK
        if block:
            parts.append(" ")
        if node.text:
            parts.append(node.text)
        for child in node:
            if not isinstance(child.tag, str):
                pass  # comments
            elif _is_note_marker(child):
                parts.append(GAP)
            else:
                walk(child)
            if child.tail:
                parts.append(child.tail)
        if block:
            parts.append(" ")

    walk(el)
    return clean(re.sub(rf"\s*{GAP}", "", "".join(parts)))


def _one(root: etree._Element, id_: str) -> etree._Element | None:
    found = root.xpath(f"//*[@id='{id_}']")
    return found[0] if found else None


def _first_cell(table: etree._Element) -> etree._Element | None:
    row = table.find(f"{X}tbody/{X}tr")
    if row is None:
        row = table.find(f"{X}tr")
    return None if row is None else row.find(f"{X}td")


def _recitals(preamble: etree._Element) -> list[tuple[int, str]]:
    out = []
    for table in preamble.findall(f"{X}table"):
        cell = _first_cell(table)
        if cell is None:
            continue
        number = re.fullmatch(r"\((\d+)\)", text_of(cell))
        if number:
            body = cell.getnext()
            out.append((int(number.group(1)), text_of(body) if body is not None else ""))
    return out


def _article_paragraphs(article: etree._Element) -> list[tuple[int, str]]:
    # numbered paragraphs sit in divs with ids like 001.002
    numbered = [d for d in article if re.fullmatch(r"\d{3}\.\d{3}", d.get("id") or "")]
    rest = [c for c in article if c not in numbered and "oj-ti-art" not in (c.get("class") or "")]
    if numbered:
        if any(text_of(c) for c in rest):
            raise ValueError(f"{article.get('id')}: text outside its numbered paragraphs")
        return [(int(d.get("id").split(".")[1]), text_of(d)) for d in numbered]
    text = clean(" ".join(text_of(c) for c in rest))
    return [(1, text)] if text else []


def annex_parts(annex: etree._Element) -> list[etree._Element]:
    """
    The parts of an annex after its "ANNEX" heading. Part 1 is anx_N.1. The parser uses this too.
    """
    kids = [c for c in annex if text_of(c)]
    if kids and text_of(kids[0]).upper().startswith("ANNEX"):
        kids = kids[1:]
    return kids


def numbered(root: etree._Element, prefix: str) -> list[tuple[int, etree._Element]]:
    """
    Every element with an id like art_1, art_2, in number order. A gap in the numbers is fine.
    """
    found = []
    for el in root.iter():
        match = (
            re.fullmatch(rf"{prefix}_(\d+)", el.get("id") or "")
            if isinstance(el.tag, str)
            else None
        )
        if match:
            found.append((int(match.group(1)), el))
    return sorted(found, key=lambda pair: pair[0])


def normalise(raw: bytes, celex: str) -> list[ActSection]:
    """
    The act as a list of sections, in reading order.
    """
    root = etree.fromstring(raw)
    rows: list[tuple[str, SectionKind, str]] = []

    title = _one(root, "tit_1")
    if title is not None:
        rows.append(("tit", "title", text_of(title)))

    rows += [(f"cit_{n}", "citation", text_of(el)) for n, el in numbered(root, "cit")]

    preamble = _one(root, "pbl_1")
    if preamble is not None:
        rows += [(f"rct_{i}", "recital", t) for i, t in _recitals(preamble)]

    for n, art in numbered(root, "art"):
        rows += [(f"art_{n}.{p}", "article", t) for p, t in _article_paragraphs(art)]

    final = _one(root, "fnp_1")
    if final is not None:
        rows.append(("fin_1", "final", text_of(final)))

    for n, anx in numbered(root, "anx"):
        rows += [(f"anx_{n}.{p}", "annex", text_of(c)) for p, c in enumerate(annex_parts(anx), 1)]

    kept = [row for row in rows if row[2]]
    ids = [sid for sid, _, _ in kept]
    if len(ids) != len(set(ids)):
        raise ValueError(f"{celex}: two sections with the same id")
    return [
        ActSection(celex=celex, section_id=sid, kind=kind, order=i, text=text)
        for i, (sid, kind, text) in enumerate(kept)
    ]
