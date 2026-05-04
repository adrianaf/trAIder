"""Application settings loaded from environment / `.env`."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    database_url: str = Field(
        default="postgresql+psycopg://traider:traider@localhost:5432/traider",
        description="SQLAlchemy URL for the primary Postgres database.",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
