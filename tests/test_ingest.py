"""Tests for B-01, B-02 and B-03. None of them uses the internet."""

import gzip
from datetime import UTC, date, datetime

from trade_defence_desk.ingest import (
    FoundDocument,
    act_url,
    file_name,
    fingerprint,
    kind_of,
    parse_sparql_result,
    read_index,
    store_act,
    write_index,
)

NOW = datetime(2026, 11, 25, 12, 0, tzinfo=UTC)


def _row(celex: str, day: str, title: str) -> dict:
    return {
        "celex": {"value": celex},
        "date": {"value": day},
        "title": {"value": title},
    }


def test_kind_of_reads_the_celex_number():
    assert kind_of("32026R2393") == "regulation"
    assert kind_of("32026R2138R(01)") == "regulation"
    assert kind_of("32025D1234") == "decision"
    assert kind_of("52026XC05408") == "notice"


def test_act_url_encodes_the_brackets_of_a_correction():
    base = "http://publications.europa.eu/resource/celex/"
    assert act_url("32026R2393") == base + "32026R2393"
    assert act_url("32025R0074R(01)") == base + "32025R0074R%2801%29"


def test_parse_keeps_one_row_per_celex_and_cleans_spaces():
    data = {
        "results": {
            "bindings": [
                _row("32026R2393", "2026-10-29", "Regulation of 29 October 2026"),
                _row("32026R2393", "2026-10-29", "a second title for the same act"),
                _row("52026XC05408", "2026-10-16", "Notice of initiation"),
            ]
        }
    }
    found = parse_sparql_result(data)
    assert [d.celex for d in found] == ["52026XC05408", "32026R2393"]  # sorted by date
    assert found[1].title == "Regulation of 29 October 2026"
    assert found[1].date_document == date(2026, 10, 29)


def test_same_act_fetched_twice_is_stored_once(tmp_path):
    doc = FoundDocument(
        celex="32026R2393", kind="regulation", title="t", date_document=date(2026, 10, 29)
    )
    content = b"<html>the act</html>"
    first = store_act(tmp_path, doc, content, NOW)
    write_index(tmp_path, {doc.celex: first})
    stored_file = tmp_path / file_name(doc.celex)
    written_at = stored_file.stat().st_mtime_ns

    later = datetime(2026, 11, 26, tzinfo=UTC)
    second = store_act(tmp_path, doc, content, later)

    assert second == first  # same fingerprint, so the first record stays
    assert stored_file.stat().st_mtime_ns == written_at  # file not written again
    assert first.sha256 == fingerprint(content)
    assert first.bytes == len(content)
    assert gzip.decompress(stored_file.read_bytes()) == content  # stored unchanged


def test_compressed_file_is_the_same_every_time(tmp_path):
    doc = FoundDocument(celex="32026R1", kind="regulation", title="t", date_document=NOW.date())
    store_act(tmp_path / "a", doc, b"same text", NOW)
    store_act(tmp_path / "b", doc, b"same text", NOW)
    a = (tmp_path / "a" / file_name(doc.celex)).read_bytes()
    b = (tmp_path / "b" / file_name(doc.celex)).read_bytes()
    assert a == b  # no time stamp inside, so git sees no change on a re-run


def test_index_round_trip(tmp_path):
    doc = FoundDocument(celex="32026R1", kind="regulation", title="a, b", date_document=NOW.date())
    act = store_act(tmp_path, doc, b"x", NOW)
    write_index(tmp_path, {act.celex: act})
    assert read_index(tmp_path) == {act.celex: act}
