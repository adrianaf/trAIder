"""Phase 0 smoke tests: app boots, settings load, DB is reachable."""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine, text

from traider import __version__
from traider.settings import Settings, get_settings


def test_version_is_set() -> None:
    assert __version__ == "0.1.0"


def test_settings_load() -> None:
    settings = get_settings()
    assert isinstance(settings, Settings)
    assert settings.database_url.startswith("postgresql+psycopg://")


def test_get_settings_is_cached() -> None:
    assert get_settings() is get_settings()


@pytest.mark.integration
def test_database_is_reachable() -> None:
    engine = create_engine(get_settings().database_url)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar_one()
    assert result == 1


@pytest.mark.integration
def test_pgvector_extension_available() -> None:
    engine = create_engine(get_settings().database_url)
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT extname FROM pg_extension WHERE extname = 'vector'")
        ).scalar()
    assert result == "vector"
