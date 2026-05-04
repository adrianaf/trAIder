# Tech Stack

Stack tuned to project constraints: personal use, swing horizon, free-tier data, multi-agent + RAG, web app.

## Recommended Stack

### Language & runtime
- **Python 3.12** for backend, agents, quant, RAG. Non-negotiable — finance + ML + LLM ecosystem lives here.
- **TypeScript + Next.js 15 (App Router)** for the web frontend if going the real-UI route.

### Multi-agent orchestration
- **LangGraph** as primary. Stateful graphs fit a multi-agent system with a self-grading loop better than CrewAI's role-based abstraction. Plays well with checkpointing (replay/inspect agent runs — important for grading).
- *Alternative:* **PydanticAI** if stricter typing and lighter abstractions are preferred; less mature for complex graphs.

### LLM
- **Claude (Anthropic SDK)** as primary reasoner — Sonnet 4.6 for most agents, Opus 4.7 for the synthesizer/rationale agent.
- Use **prompt caching** — re-passing the same KB chunks and instrument metadata across agents makes this materially cheaper.
- Keep the model choice behind a thin abstraction to enable A/B testing.

### Quantitative layer
- **pandas, numpy, scipy** — table stakes.
- **pandas-ta** (or TA-Lib for C-speed indicators) for technicals.
- **vectorbt** for backtesting and signal evaluation. Fast, vectorised, fits swing-horizon work better than backtrader.
- **statsmodels / scikit-learn** for any regression/classification overlays.

### Market data (free-tier)
- **yfinance** — broad US + many EU tickers, fine for swing.
- **Stooq** — free EU historical, especially for ETFs/ETNs that yfinance misses.
- **Alpha Vantage** free tier — fundamentals and FX (rate-limited; cache aggressively).
- **FRED** (via `fredapi`) — macro series, free and reliable.
- **Finnhub** free tier — earnings calendar, basic news.

**Options data is the weak spot.** yfinance has US chains (delayed, sometimes stale); EU options are largely paywalled. Plan for **Tradier sandbox** (US, free, delayed) and budget paid feeds (EODHD or similar) once options become central. Consider deferring options entirely from MVP.

### News & events
- RSS feeds (free, reliable) + **GDELT** for global event signals.
- **NewsAPI** free tier for prototyping; not production-grade.

### RAG / knowledge base
- **PostgreSQL + pgvector** — single store for app data *and* embeddings. Simpler than a separate vector DB at personal scale.
- **LlamaIndex** for ingestion, chunking, retrieval. More RAG-focused than LangChain; easier to swap retrievers.
- **Voyage AI embeddings** (`voyage-3`) — Anthropic's recommended embedding partner, strong on financial/technical text. Open-source fallback: `BAAI/bge-large-en-v1.5`.

### Backend API
- **FastAPI** + **SQLModel** (Pydantic + SQLAlchemy) + **Alembic** migrations.
- **Pydantic** everywhere — typed agent inputs/outputs catch a lot of multi-agent bugs early.

### Frontend
- **Next.js 15 (App Router) + React + Tailwind + shadcn/ui** + **TanStack Query** for data fetching.
- Charts: **Recharts** for simple, **lightweight-charts** (TradingView's OSS lib) for candlesticks.
- Typed API client **generated from FastAPI's OpenAPI schema** so the frontend stays in sync as endpoints evolve.

### Scheduling & background jobs
- **APScheduler** (in-process) for v1 — swing horizon doesn't need anything heavier.
- Graduate to **Prefect** when self-grading workflows get complex.

### Observability for LLM / agent runs
- **Langfuse** (self-hostable, OSS) — trace agent calls, prompt versions, costs. Critical for debugging multi-agent behaviour and feeding the self-grading loop.

### Storage of recommendations & outcomes
- Postgres tables: `recommendations`, `prices_snapshot`, `evaluations`. Time-series of (recommendation → realised outcome at horizon T) is the substrate for self-grading.

### Dev tooling
- **uv** for Python package management (fast).
- **ruff** + **mypy** + **pytest**.
- **Docker Compose** for Postgres + app locally.

### Deployment
- **Fly.io** or **Railway** — single small VM, Postgres add-on, deploy from Git. Cheapest path that survives.

## Tradeoffs to revisit

1. **pgvector vs dedicated vector DB.** pgvector is fast enough at personal scale (likely <100k chunks). Don't reach for Qdrant/Weaviate until outgrown.
2. **Sync vs async FastAPI.** Starting sync with SQLAlchemy 2.0 sync engine — simpler to debug. Re-evaluate once Phase 5+ endpoints fan out to multiple LLM/data calls per request and concurrency starts paying off.
