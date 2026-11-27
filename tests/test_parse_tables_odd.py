"""
The parser on small hand-written tables. Each odd case must stop the act, never guess a row.
"""

from decimal import Decimal

import pytest

from trade_defence_desk.parse_tables import parse_duty_rows

HEAD = (
    '<html xmlns="http://www.w3.org/1999/xhtml"><body>'
    '<div id="enc_1"><div id="art_1"><p class="oj-ti-art">Article 1</p><div id="001.002">'
    "<p>2. The rates of the definitive anti-dumping duty shall be as follows:</p>"
)
TABLE_HEAD = (
    '<table class="oj-table"><tbody><tr><td>Company</td>'
    "<td>Definitive anti-dumping duty (%)</td><td>TARIC additional code</td></tr>"
)
ANNEX = (
    '<div id="anx_1"><p>ANNEX</p><table class="oj-table"><tbody>'
    "<tr><td>Name</td><td>TARIC additional code</td></tr>"
    "<tr><td>Alpha Co., Ltd.</td><td>A001</td></tr>"
    "</tbody></table></div>"
)


def act(*rows: str, annex: str = "") -> bytes:
    body = "".join(f"<tr>{''.join(f'<td>{c}</td>' for c in row)}</tr>" for row in rows)
    end = "</tbody></table></div></div></div>"
    return (HEAD + TABLE_HEAD + body + end + annex + "</body></html>").encode()


def test_simple_rows():
    rows = parse_duty_rows(
        act(["Beta Co Ltd", "12,5", "B001"], ["All other imports", "30,0", "8999"])
    )
    assert [(r.taric_additional_code, r.category, r.rate_pct) for r in rows] == [
        ("B001", "individual", Decimal("12.5")),
        ("8999", "residual", Decimal("30.0")),
    ]


def test_see_annex_one():
    rows = parse_duty_rows(act(["Other cooperating companies", "20,0", "See Annex I"], annex=ANNEX))
    assert [(r.taric_additional_code, r.names) for r in rows] == [("A001", ["Alpha Co., Ltd."])]


def test_see_annex_without_an_annex():
    with pytest.raises(ValueError, match="fits 0 annexes"):
        parse_duty_rows(act(["Other cooperating companies", "20,0", "See Annex"]))


def test_annex_named_but_missing():
    with pytest.raises(ValueError):
        parse_duty_rows(act(["Other cooperating companies", "20,0", "See Annex II"], annex=ANNEX))


def test_code_that_is_not_a_code():
    with pytest.raises(ValueError, match="not a TARIC additional code"):
        parse_duty_rows(act(["Beta Co Ltd", "12,5", "see note 3"]))


def test_unknown_kind_of_row():
    with pytest.raises(ValueError, match="unknown kind of row"):
        parse_duty_rows(act(["Any other company", "30,0", "8999"]))


def test_row_with_a_missing_cell():
    with pytest.raises(ValueError, match="cells"):
        parse_duty_rows(act(["Beta Co Ltd", "12,5"]))


def test_rate_that_is_not_a_percentage_goes_to_a_person():
    [row] = parse_duty_rows(act(["Beta Co Ltd", "EUR 12,5 per tonne", "B001"]))
    assert row.rate_pct is None
    assert row.needs_review
    assert row.formula_text == "EUR 12,5 per tonne"


def test_no_operative_part():
    with pytest.raises(ValueError, match="no operative part"):
        parse_duty_rows(b'<html xmlns="http://www.w3.org/1999/xhtml"><body></body></html>')


def test_a_rate_named_but_not_read():
    raw = (
        HEAD.replace("shall be as follows:", "shall be fifteen per cent.")
        + "</div></div></div></body></html>"
    ).encode()
    with pytest.raises(ValueError, match="no rate was read"):
        parse_duty_rows(raw)


def test_registration_has_no_rows():
    raw = (
        b'<html xmlns="http://www.w3.org/1999/xhtml"><body><div id="enc_1"><div id="art_1">'
        b"<p>Customs authorities shall register imports of the product.</p>"
        b"</div></div></body></html>"
    )
    assert parse_duty_rows(raw) == []
