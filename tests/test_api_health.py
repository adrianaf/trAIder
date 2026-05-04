"""Tests for the /health endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient

from traider import __version__
from traider.api.app import app

client = TestClient(app)


def test_health_returns_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": __version__}


def test_openapi_schema_available() -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "trAIder API"
    assert "/health" in schema["paths"]
