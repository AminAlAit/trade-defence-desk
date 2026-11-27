"""Small reusable types for the lane C contracts.

Owner: lane C. Used by importer.py, scope.py and decisions.py.
If lane A keeps a shared types module, these move there in the freeze pull request.
"""

from __future__ import annotations

import re
from decimal import Decimal
from typing import Annotated

from pydantic import AfterValidator, BeforeValidator, Field

_SPACES = re.compile(r"[\s\u00a0\u202f.]+")


def _strip_code(value: object) -> object:
    """Accept '5603 14 80' or '5603.14.80' and keep only the digits."""
    if value is None:
        return None
    if isinstance(value, int):
        value = str(value)
    if isinstance(value, str):
        cleaned = _SPACES.sub("", value)
        return cleaned or None
    return value


def _upper_country(value: object) -> object:
    if isinstance(value, str):
        return value.strip().upper()
    return value


def _check_country(value: str) -> str:
    # EL is the EU's own code for Greece; XK is used for Kosovo. Both are valid here.
    if not re.fullmatch(r"[A-Z]{2}", value):
        raise ValueError("country must be a two-letter ISO code, for example CN")
    return value


CountryCode = Annotated[str, BeforeValidator(_upper_country), AfterValidator(_check_country)]
"""ISO 3166-1 alpha-2 code, upper case: CN, VN, BR."""

CnCode = Annotated[
    str,
    BeforeValidator(_strip_code),
    Field(
        pattern=r"^\d{8}$",
        description="8-digit Combined Nomenclature code, digits only",
    ),
]

TaricCode = Annotated[
    str,
    BeforeValidator(_strip_code),
    Field(pattern=r"^\d{10}$", description="10-digit TARIC code, digits only"),
]

Eur = Annotated[
    Decimal,
    Field(
        ge=Decimal("0"),
        max_digits=14,
        decimal_places=2,
        description="euros, never a float",
    ),
]
"""Money is Decimal. 0.1 + 0.2 must stay 0.3 on Thomas's screen."""


def _strip_text(value: object) -> object:
    if isinstance(value, str):
        return " ".join(value.split())
    return value


CleanText = Annotated[str, BeforeValidator(_strip_text), Field(min_length=1)]
"""Text with outer spaces removed and inner runs of spaces collapsed. Never empty."""
