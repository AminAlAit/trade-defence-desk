"""
The duty table parser, pinned on 2026/2393 (docs/examples/02_READING_THE_DUTY_TABLE.md)
and on 2026/2311, which has no company table.
"""

from decimal import Decimal

from lxml import etree  # ty: ignore[missing-module-member]

from trade_defence_desk.normalise import X, load_sample, normalise, text_of
from trade_defence_desk.parse_tables import parse_duty_rows

# the expected output in example 02, one row per code
EXPECTED_2393 = [
    ("88CB", "individual", "39.8", ["Hubei Unibon nonwovens Co Ltd"]),
    (
        "88CC",
        "individual",
        "48.1",
        ["Changde Tiandingfeng Nonwovens Co Ltd", "Tiandingfeng Nonwovens Co Ltd"],
    ),
    ("88CD", "cooperating_not_sampled", "47.1", ["Hebei Jinliu Chemical Fiber Co., Ltd."]),
    ("88CE", "cooperating_not_sampled", "47.1", ["Hebei Saikefu Nonwovens Co., Ltd."]),
    ("88CF", "cooperating_not_sampled", "47.1", ["Hubei Bushi Nonwovens Co., Ltd."]),
    ("88CG", "cooperating_not_sampled", "47.1", ["Shouguang Fada Cloth Co., Ltd."]),
    ("88CH", "cooperating_not_sampled", "47.1", ["Jiangyin Huasicheng Nonwoven Co., Ltd."]),
    ("8999", "residual", "48.1", []),
]


def rows_2393():
    return parse_duty_rows(load_sample("32026R2393"))


def test_2393_matches_example_02():
    got = [(r.taric_additional_code, r.category, str(r.rate_pct), r.names) for r in rows_2393()]
    assert got == EXPECTED_2393


def test_four_rows_become_eight():
    assert len(rows_2393()) == 8


def test_grouped_cell_is_two_names_on_one_rate():
    row = next(r for r in rows_2393() if r.taric_additional_code == "88CC")
    assert len(row.names) == 2
    assert row.rate_pct == Decimal("48.1")


def test_see_annex_expanded():
    annex = [r for r in rows_2393() if r.section_id.startswith("anx_")]
    assert [r.taric_additional_code for r in annex] == ["88CD", "88CE", "88CF", "88CG", "88CH"]
    assert {r.rate_pct for r in annex} == {Decimal("47.1")}


def test_rates_only_from_the_operative_part():
    # the trap: the reasons hold the same companies at 57,5 (underselling margin)
    root = etree.fromstring(load_sample("32026R2393"))
    reasons = root.xpath("//*[@id='pbl_1']")[0]
    assert "57,5" in text_of(reasons)
    assert len(root.findall(f".//{X}table")) == 196
    assert Decimal("57.5") not in {r.rate_pct for r in rows_2393()}
    assert all(r.section_id in ("art_1.2", "anx_1.2") for r in rows_2393())


def test_rates_kept_as_written():
    assert rows_2393()[0].rate_text == "39,8"


def test_every_row_points_at_its_text():
    text = {s.section_id: s.text for s in normalise(load_sample("32026R2393"), "32026R2393")}
    for row in rows_2393():
        # annex rows carry the rate of the "See Annex" row in Article 1(2)
        rate_home = "art_1.2" if row.section_id.startswith("anx_") else row.section_id
        assert row.rate_text in text[rate_home]
        assert row.taric_additional_code in text[row.section_id]
        for name in row.names:
            assert name in text[row.section_id]


def test_2311_one_rate_for_the_country():
    rows = parse_duty_rows(load_sample("32026R2311"))
    assert len(rows) == 1
    row = rows[0]
    assert (row.category, row.rate_pct, row.taric_additional_code) == (
        "country_wide",
        Decimal("15.8"),
        None,
    )
    assert row.names == []
    assert row.section_id == "art_1.2"
