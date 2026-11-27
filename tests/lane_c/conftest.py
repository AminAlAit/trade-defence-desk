from pathlib import Path

import pytest

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "lane_c"


@pytest.fixture
def fixtures() -> Path:
    return FIXTURES
