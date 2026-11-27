"""
Where the database is. Compose sets DATABASE_URL, a laptop run falls back to localhost.
"""

import os

DEFAULT_URL = "postgresql://tdd:tdd@localhost:5432/tdd"


def database_url() -> str:
    return os.environ.get("DATABASE_URL", DEFAULT_URL)
