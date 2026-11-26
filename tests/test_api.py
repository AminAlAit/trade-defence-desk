"""
The API answers /health even when the database is down.
"""

from fastapi.testclient import TestClient

from trade_defence_desk.api import app


def test_health_without_database(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://nobody:x@127.0.0.1:1/none?connect_timeout=1")
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "db": "down"}
