"""The number guard (C-17): model text shown to a user may hold no digit of its own.

Rule 1 of docs/06_AI_RULES.md: no number the user sees comes from free model text.
Digits are allowed only inside a word-for-word quote of the act, because then they are
the act's words, not the model's.

This module is pure Python with no dependencies, so every lane can import it and the
CI test can run it on every pull request.
"""

from __future__ import annotations

import re
import unicodedata

# Any Unicode decimal digit, not only 0-9: the model could write Arabic-Indic digits too.
_DIGIT = re.compile(r"\d", re.UNICODE)
# Spelled-out numbers are numbers too. Small list on purpose; extend in C-17.
_NUMBER_WORDS = re.compile(
    r"\b(zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|"
    r"percent|per cent)\b",
    re.IGNORECASE,
)


def _normalise(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    return " ".join(text.split())


def strip_quotes(text: str, quotes: list[str]) -> str:
    """Remove every allowed quote from the text before the digit check."""
    cleaned = _normalise(text)
    for quote in sorted((q for q in quotes if q), key=len, reverse=True):
        cleaned = cleaned.replace(_normalise(quote), " ")
    return cleaned


def find_numbers(text: str, quotes: list[str] | None = None) -> list[str]:
    """Return every digit or number word that sits outside the allowed quotes."""
    rest = strip_quotes(text, quotes or [])
    found = [m.group(0) for m in _DIGIT.finditer(rest)]
    found += [m.group(0) for m in _NUMBER_WORDS.finditer(rest)]
    return found


def assert_no_free_numbers(text: str, quotes: list[str] | None = None) -> str:
    """Raise ValueError if the text has a number outside the quotes. Return the text."""
    found = find_numbers(text, quotes)
    if found:
        raise ValueError(f"number guard: model text contains {found!r} outside a quote")
    return text
