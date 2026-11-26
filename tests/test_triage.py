"""Tests for B-05, the triage rules. Every title here is a real title from the catalogue."""

import pytest

from trade_defence_desk.triage import ACT_TYPES, NOTICE_TYPES, operative_phrase, triage

REG = "Commission Implementing Regulation (EU)"

# (celex, title, expected type)
CASES = [
    # the four titles in docs/examples/08_A_QUIET_DAY.md, "How triage reads a title"
    (
        "32025R2409",
        f"{REG} 2025/2409 of 1 December 2025 making imports of PET spunbond originating in "
        "the People's Republic of China subject to registration",
        "registration",
    ),
    (
        "32026R1063",
        f"{REG} 2026/1063 of 12 May 2026 imposing a provisional anti-dumping duty on imports "
        "of PET Spunbond originating in the People's Republic of China",
        "provisional",
    ),
    (
        "32026R2393",
        f"{REG} 2026/2393 of 29 October 2026 imposing a definitive anti-dumping duty and "
        "definitively collecting the provisional duty imposed on imports of PET Spunbond",
        "definitive",
    ),
    (
        "32026R2311",
        f"{REG} 2026/2311 of 19 October 2026 imposing a definitive anti-dumping duty on "
        "imports of certain heavyweight thermal paper originating in the Republic of Korea "
        "following an expiry review pursuant to Article 11(2)",
        "definitive_expiry_review",
    ),
    # the first verb decides, not a word later in the title
    (
        "32025R0796",
        f"{REG} 2025/796 of 24 April 2025 imposing a definitive countervailing duty on "
        "imports of mobile access equipment and amending Implementing Regulation (EU) 2025/45",
        "definitive",
    ),
    (
        "32025R1505",
        f"{REG} 2025/1505 of 25 July 2025 imposing a definitive anti-dumping duty and "
        "definitively collecting the provisional duty imposed on imports of epoxy resins "
        "and terminating the investigation on imports of epoxy resins originating in Thailand",
        "definitive",
    ),
    (
        "32026R2319",
        f"{REG} 2026/2319 of 19 October 2026 amending Implementing Regulation (EU) 2023/265 "
        "imposing a definitive anti-dumping duty on imports of ceramic tiles",
        "amendment",
    ),
    (
        "32025R0826",
        f"{REG} 2025/826 of 29 April 2025 correcting Implementing Regulation (EU) 2025/261 "
        "imposing a definitive anti-dumping duty on imports of biodiesel",
        "correction",
    ),
    (
        "32025R0074R(01)",
        f"Corrigendum to {REG} 2025/74 of 13 January 2025 imposing a provisional "
        "anti-dumping duty on imports of lysine",
        "correction",
    ),
    (
        "32026R2314",
        f"{REG} 2026/2314 of 19 October 2026 repealing definitive anti-dumping duty on "
        "imports of solar glass",
        "repeal",
    ),
    (
        "32025D1067",
        "Commission Implementing Decision (EU) 2025/1067 of 28 May 2025 terminating the "
        "anti-dumping investigation concerning imports of certain seamless pipes",
        "termination",
    ),
    (
        "32026D0328",
        "Commission Implementing Decision (EU) 2026/328 of 9 February 2026 accepting an "
        "undertaking offered in connection with the anti-subsidy measures",
        "undertaking",
    ),
    (
        "32026R1925",
        f"{REG} 2026/1925 of 6 August 2026 initiating an investigation concerning possible "
        "circumvention of the anti-dumping measures imposed by Implementing Regulation (EU) "
        "2024/357 and making such imports subject to registration",
        "initiation",
    ),
    (
        "32025R0698",
        f"{REG} 2025/698 of 9 April 2025 extending the definitive anti-dumping duty imposed "
        "by Implementing Regulation (EU) 2021/633 on imports of monosodium glutamate",
        "extension",
    ),
    (
        "32025R0329",
        f"{REG} 2025/329 of 19 February 2025 revoking the exemption from the anti-dumping "
        "duty on essential bicycle parts granted to Solo International Oy",
        "exemption",
    ),
    (
        "32026R2270",
        f"{REG} 2026/2270 of 15 October 2026 amending Implementing Regulation (EU) 2025/2351 "
        "imposing a definitive safeguard measure with regard to imports of ferro-alloying",
        "safeguard",
    ),
    # notices
    (
        "52026XC01506",
        "Notice of initiation of an anti-dumping proceeding concerning imports of copper tubes",
        "initiation",
    ),
    (
        "52025XC05537",
        "Notice of initiation of an expiry review of the anti-dumping measures applicable to "
        "imports of certain heavyweight thermal paper",
        "expiry_review",
    ),
    (
        "52025XC06545",
        "Notice of initiation of a partial interim review of the countervailing measures",
        "interim_review",
    ),
    (
        "52026XC03105",
        "Notice of initiation of interim review of the anti-dumping measures applicable to "
        "imports of aspartame",
        "interim_review",
    ),
    (
        "52026XC05566",
        "Notice of the impending expiry of certain anti-dumping measures",
        "impending_expiry",
    ),
    ("52026XC01375", "Notice of the expiry of certain anti-dumping measures", "expiry"),
    (
        "52026XC05780",
        "Notice of initiation of a safeguard investigation concerning imports of certain new "
        "hybrid vehicles",
        "safeguard",
    ),
    (
        "52026XC02557",
        "Notice of reopening the anti-dumping investigation concerning imports of lysine",
        "other",
    ),
]


@pytest.mark.parametrize(("celex", "title", "expected"), CASES)
def test_real_titles(celex, title, expected):
    assert triage(celex, title).act_type == expected


def test_registration_and_initiation_still_go_to_full_extraction():
    # B-05, "done when": registration and initiation regulations are not skipped
    for celex, title, expected in CASES:
        if expected in ("registration", "initiation") and not celex.startswith("5"):
            assert triage(celex, title).route == "full_extraction", celex


def test_notices_are_listed_not_read():
    assert triage("52026XC05566", "Notice of the impending expiry of ...").route == "list_only"


def test_safeguards_and_corrections_go_to_a_person():
    # D-20: shown and sent to a person
    for celex, title, expected in CASES:
        if expected in ("safeguard", "correction", "amendment", "undertaking", "exemption"):
            assert triage(celex, title).to_person, celex


def test_unknown_title_is_other_with_low_confidence():
    result = triage("32026R9999", f"{REG} 2026/9999 of 1 January 2026 doing something new")
    assert (result.act_type, result.confidence, result.to_person) == ("other", "low", True)


def test_title_without_a_date_falls_back_with_low_confidence():
    result = triage("32026R9998", "Regulation imposing a definitive anti-dumping duty")
    assert result.act_type == "definitive"
    assert result.confidence == "low"


def test_operative_phrase_starts_after_the_date():
    title = f"{REG} 2026/2497 of 10 November 2026 imposing a provisional anti-dumping duty"
    assert operative_phrase(title) == "imposing a provisional anti-dumping duty"


def test_every_expected_type_is_a_known_type():
    for celex, _, expected in CASES:
        known = NOTICE_TYPES if celex.startswith("5") else ACT_TYPES
        assert expected in known
