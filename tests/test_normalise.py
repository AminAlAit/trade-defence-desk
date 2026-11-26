"""
The normaliser on the two example acts, 2026/2393 and 2026/2311.
"""

import hashlib
from collections import Counter
from decimal import Decimal

import pytest

from trade_defence_desk.normalise import clean, load_sample, normalise, to_decimal

# from data/sample_acts/README.md
SHA256 = {
    "32026R2393": "4ad071c2ee03262acbd24ef42f3046de3669e5b15e96e7c85b5263f929fd92f3",
    "32026R2311": "3d11a229e6e09be7c698bfb90a2faef143c39368e517288540bd301f84727970",
}


def sections(celex):
    return {s.section_id: s for s in normalise(load_sample(celex), celex)}


@pytest.mark.parametrize("celex", SHA256)
def test_sample_act_unchanged(celex):
    assert hashlib.sha256(load_sample(celex)).hexdigest() == SHA256[celex]


@pytest.mark.parametrize(
    "celex, counts",
    [
        (
            "32026R2393",
            {"title": 1, "citation": 2, "recital": 170, "article": 7, "final": 1, "annex": 2},
        ),
        ("32026R2311", {"title": 1, "citation": 2, "recital": 134, "article": 4, "final": 1}),
    ],
)
def test_parts(celex, counts):
    assert Counter(s.kind for s in sections(celex).values()) == counts


@pytest.mark.parametrize("celex", SHA256)
def test_ids_unique_and_in_order(celex):
    found = normalise(load_sample(celex), celex)
    assert len({s.section_id for s in found}) == len(found)
    assert [s.order for s in found] == list(range(len(found)))


@pytest.mark.parametrize("celex", SHA256)
def test_same_ids_every_run(celex):
    raw = load_sample(celex)
    assert normalise(raw, celex) == normalise(raw, celex)


def test_recitals_numbered_from_the_act():
    found = sections("32026R2393")
    assert found["rct_1"].text.startswith("On 15 September 2025")
    assert "rct_170" in found and "rct_171" not in found


def test_article_paragraphs():
    found = sections("32026R2393")
    assert found["art_1.2"].text.startswith("2. The rates of the definitive anti-dumping duty")
    assert "Hubei Unibon nonwovens Co Ltd 39,8 88CB" in found["art_1.2"].text
    assert found["art_4.1"].text.startswith("This Regulation shall enter into force")


def test_annex_without_its_heading():
    found = sections("32026R2393")
    assert found["anx_1.1"].text.startswith("People")
    assert "Jiangyin Huasicheng Nonwoven Co., Ltd. 88CH" in found["anx_1.2"].text


def test_footnote_markers_dropped():
    assert "2020/1524, the European Commission" in sections("32026R2311")["rct_1"].text


def test_superscript_stays_in_the_word():
    assert "70 g/m2," in sections("32026R2393")["art_1.1"].text


def test_numbers_kept_as_written():
    assert "0,5 mm but not exceeding 1,8 mm" in sections("32026R2393")["art_1.1"].text


def test_no_odd_spaces_left():
    for s in sections("32026R2393").values():
        assert " " not in s.text and "  " not in s.text


def test_clean_and_decimal():
    assert clean(" 5603 14 80 ") == "5603 14 80"
    assert clean("39,8 % ") == "39,8 %"
    assert to_decimal("39,8 ") == Decimal("39.8")
    assert to_decimal("15,8") == Decimal("15.8")
