# trAIder

Personal AI-powered swing-trading advisor for **EU and US** markets. The goal is a small web app (single-user) that suggests a **focused set of instruments** (typically ETFs, ETCs, ETNs, bonds, or options), **capital allocation**, and **entry/exit** ideas—grounded in trusted news/data and a **curated knowledge base**, not headlines alone. **Advisory only** in v1; no broker execution yet.

## Status

Early foundation: Python package, FastAPI scaffold (`GET /health`), Postgres + pgvector via Docker Compose, Alembic migrations, and pytest. Agents, RAG, and frontend are planned in later phases.

## Requirements

- **Python 3.12+**
- [**uv**](https://docs.astral.sh/uv/) for dependencies
- **Docker** (for local Postgres)

## Quick start

```bash
git clone <your-fork-or-repo-url>
cd trAIder
uv sync
```

Copy [`.env.example`](.env.example) to `.env` and adjust if needed (defaults match `docker-compose.yml`).

```bash
docker compose up -d
uv run alembic upgrade head
uv run traider-api
```

- API: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
- OpenAPI docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

```bash
uv run traider          # CLI (prints version)
```

## Development

```bash
uv run pytest
uv run pytest -m "not integration"   # skip tests that need DB/network
uv run ruff check . && uv run ruff format --check .
uv run mypy
uv run pre-commit run --all-files
```

Database helpers:

```bash
docker compose up -d
uv run alembic upgrade head
uv run alembic revision -m "describe change"
uv run alembic downgrade -1
```

## Layout

| Path | Purpose |
|------|---------|
| `src/traider/` | Main package (`settings`, `cli`) |
| `src/traider/api/` | FastAPI app, routes, `traider-api` entry |
| `alembic/` | Migrations (`env.py` uses `traider.settings`) |
| `tests/` | pytest (use `@pytest.mark.integration` for DB/network) |
| `docker-compose.yml` | Postgres 16 + pgvector |

## Disclaimer

This project is for **personal experimentation and learning**. It is **not** investment, tax, or legal advice. Trading involves risk; you are responsible for your own decisions.
