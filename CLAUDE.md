# trAIder

Personal AI-powered swing-trading advisor (web app). Recommends 2–3 instruments (ETFs/ETCs/ETNs/bonds/options across EU + US) with allocation and entry/exit signals, via a multi-agent + RAG pipeline that grades its own past calls.

For details, see:
- `project-scope.md` — features, constraints, open questions.
- `tech-stack.md` — chosen libraries and rationale.
- `implementation-plan.md` — phased build plan and sequencing rationale.

## Tech stack (current)
- Python 3.12, managed with `uv`.
- FastAPI (sync) + SQLAlchemy 2.0 + Alembic + psycopg3.
- Postgres 16 + pgvector via Docker Compose.
- Pydantic v2 + pydantic-settings.
- pytest, ruff, mypy (strict), pre-commit.

Coming in later phases: LangGraph, Anthropic SDK, LlamaIndex + Voyage embeddings, vectorbt, pandas-ta, Next.js 15 + shadcn/ui + TanStack Query.

## Repo layout
- `src/traider/` — Python package.
  - `api/` — FastAPI app (`app.py`, `cli.py`, `routes/`).
  - `cli.py` — `traider` script entry.
  - `settings.py` — Pydantic Settings (single source of truth for config).
- `tests/` — pytest, `integration` marker for tests that touch DB or network.
- `alembic/` — DB migrations. `env.py` reads `database_url` from `traider.settings`.
- `docker-compose.yml` — Postgres + pgvector container.

## Common commands

```bash
# Setup
uv sync

# Database
docker compose up -d                      # start Postgres
uv run alembic upgrade head               # apply migrations
uv run alembic revision -m "msg"          # new empty migration
uv run alembic downgrade -1               # roll back one

# Dev runners
uv run traider                            # CLI (prints version for now)
uv run traider-api                        # FastAPI on http://127.0.0.1:8000

# Quality gates
uv run pytest                             # all tests
uv run pytest -m "not integration"        # skip DB-touching
uv run ruff check . && uv run ruff format --check .
uv run mypy
uv run pre-commit run --all-files
```

## Conventions
- **Strict mypy.** All public functions are typed; don't loosen settings.
- **Imports:** ruff handles isort; don't reorder by hand.
- **Config:** `traider.settings.get_settings()` is the single source. Never hardcode connection strings or API keys; add fields to `Settings` and document them in `.env.example`.
- **Migrations:** every schema change goes through Alembic. Don't `CREATE TABLE` in app code.
- **Testing:** anything that touches Postgres, the network, or external APIs is marked `@pytest.mark.integration`. Unit tests must run offline.
- **Pre-commit:** runs ruff (lint + format) and mypy. Don't bypass with `--no-verify`.
- **API:** one router module per resource under `src/traider/api/routes/`, registered in `app.create_app()`. Pydantic models for both request and response.
- **No comments explaining *what* the code does** — name things well instead. Comments only for non-obvious *why*.

## Library documentation: use Context7 MCP

For any question or code involving an external library, framework, SDK, CLI, or cloud service — *including familiar ones* — fetch current docs via **Context7 MCP** before answering or writing code. Training data lags behind real API changes.

Steps:
1. `resolve-library-id` with the library name (e.g. `fastapi`, `sqlalchemy`, `alembic`, `langgraph`, `llamaindex`, `vectorbt`, `next.js`, `shadcn-ui`).
2. Choose the best `/org/project` match (name fit, description, reputation, snippet count). Use a version-specific ID if the user mentions a version.
3. `query-docs` with that ID and the user's full question (not single keywords).
4. Answer using the fetched docs; cite the source where relevant.

**Skip Context7 only for:** refactoring, debugging business logic in this repo, code review, or general programming concepts unrelated to a specific library.

## Project status
Phase 0 (foundation) complete: uv project, tooling, Docker+Postgres+pgvector, Pydantic Settings, Alembic baseline, pytest smoke tests, FastAPI scaffold with `/health`. Next: Phase 1 — instruments & price data.
