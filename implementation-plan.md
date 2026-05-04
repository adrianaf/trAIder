# Implementation Plan

Each task is sized to roughly a single commit / PR (≤1 day) with a clear, testable outcome. Phases are ordered so each completed phase delivers working value, and the early phases get to an end-to-end thin slice fast before broadening.

## Phase 0 — Foundation
- **0.1** Initialize Python project with `uv` (pyproject, lockfile).
- **0.2** Wire tooling: ruff, mypy, pytest, pre-commit. CI on push.
- **0.3** Docker Compose: Postgres 16 + pgvector extension.
- **0.4** Pydantic Settings module loading from `.env`.
- **0.5** Alembic init + empty baseline migration.
- **0.6** Pytest skeleton with smoke test (`assert app boots`).
- **0.7** FastAPI scaffold: `app.py` factory, `/health` route, `traider-api` dev runner, TestClient route test.

## Phase 1 — Instruments & price data
- **1.1** Schema: `instruments` (symbol, market, type, currency, name).
- **1.2** Seed script: ~20 ETFs across EU + US.
- **1.3** Schema: `price_bars` (instrument_id, ts, OHLCV, source).
- **1.4** `yfinance` client wrapper with retries + on-disk cache.
- **1.5** Stooq client for EU gaps.
- **1.6** Source-priority resolver (yfinance → Stooq fallback).
- **1.7** Daily price-ingest CLI: `ingest-prices`.
- **1.8** Tests with VCR.py-recorded responses.
- **1.9** API endpoints: `GET /instruments`, `GET /instruments/{symbol}`, `GET /instruments/{symbol}/prices?from&to`.

## Phase 2 — Signal engine (thin slice)
- **2.1** Indicator module wrapping `pandas-ta`.
- **2.2** SMA-crossover signal → `(instrument, action, strength, ts)`.
- **2.3** RSI signal.
- **2.4** MACD signal.
- **2.5** Signal aggregator → per-instrument composite score.
- **2.6** Indicator tests on fixed-price fixtures.
- **2.7** API endpoint: `GET /signals/{symbol}` returning latest signal values.

## Phase 3 — Backtest harness
- **3.1** `vectorbt` wrapper: signal series + prices → returns.
- **3.2** Walk-forward evaluator.
- **3.3** Metrics: Sharpe, max drawdown, hit rate, avg holding period.
- **3.4** CLI: `backtest <signal> <universe> <window>`.
- **3.5** Tests asserting expected metrics on synthetic series.
- **3.6** API endpoint: `POST /backtests` (signal + universe + window) → metrics.

## Phase 4 — First end-to-end recommendation (single agent)
- **4.1** Anthropic SDK wrapper with prompt caching enabled.
- **4.2** Prompt template: signals + price summary → shortlist (2–3) + allocation % + entry/exit rationale.
- **4.3** Single-agent pipeline (deterministic inputs).
- **4.4** Schema: `recommendations` (run_id, ts, shortlist json, rationale, model, prompt_hash).
- **4.5** CLI: `advise` — runs pipeline and persists.
- **4.6** Snapshot tests for prompt construction.
- **4.7** API endpoints: `POST /advise` (triggers pipeline), `GET /recommendations`, `GET /recommendations/{run_id}`.

## Phase 5 — Multi-agent decomposition (LangGraph)
- **5.1** Pydantic state schema for the graph.
- **5.2** Market-intel agent (regime summary).
- **5.3** Technical-analysis agent (consumes signal engine).
- **5.4** Allocation agent (shortlist + risk → weights).
- **5.5** Synthesizer agent (final rec + rationale).
- **5.6** LangGraph wiring of the four nodes.
- **5.7** Replace single-agent pipeline with the graph.
- **5.8** Per-agent unit tests with mocked LLM responses.
- **5.9** Streaming variant of `POST /advise` (SSE) emitting per-agent progress events.

## Phase 6 — News & macro intelligence
- **6.1** RSS fetcher with configurable feed list.
- **6.2** GDELT events client.
- **6.3** FRED macro client (curated indicator list).
- **6.4** News dedupe + per-instrument tagging.
- **6.5** Conflict reconciliation (weight by source trust + recency).
- **6.6** Wire outputs into market-intel agent.

## Phase 7 — RAG knowledge base
- **7.1** Schemas: `kb_documents`, `kb_chunks` (with pgvector column).
- **7.2** LlamaIndex ingestion pipeline.
- **7.3** Voyage embeddings client.
- **7.4** Seed KB: 5–10 curated docs (ETF mechanics, options basics, swing-trading risk).
- **7.5** Retrieval tool exposed to agents.
- **7.6** Synthesizer grounds rationale in retrieved chunks with citations.
- **7.7** Persist citations on recommendation rows.
- **7.8** API endpoints: `GET /kb/documents`, `POST /kb/search` (debug/inspection).

## Phase 8 — Self-grading loop
- **8.1** Schema: `evaluations` (rec_id, horizon, realised_return, hit, evaluated_at).
- **8.2** Outcome evaluator: fetches T+horizon prices, scores recommendations.
- **8.3** Aggregated performance views (per signal, per prompt/agent version).
- **8.4** Periodic evaluator job.
- **8.5** Surface recent evaluations into synthesizer prompt as feedback context.
- **8.6** KB-update flow on systematic failure patterns (human-approved initially).
- **8.7** API endpoints: `GET /evaluations`, `GET /performance/summary` (aggregates).

## Phase 9 — Web UI (Next.js + FastAPI)
- **9.1** API hardening for UI consumption: CORS config, OpenAPI tags, consistent error envelope.
- **9.2** Next.js 15 App Router scaffold with Tailwind + shadcn/ui + TanStack Query.
- **9.3** Typed API client generated from OpenAPI schema.
- **9.4** Shortlist view: instruments, allocation, action.
- **9.5** Detail view: signals, news inputs, citations (links into KB).
- **9.6** Performance view: recommendations + outcomes over time (lightweight-charts).
- **9.7** "Run new advisory" action — calls streaming `POST /advise`, renders agent progress live.
- **9.8** Auth: single-user token guard on the API (env-configured).

## Phase 10 — Scheduling & observability
- **10.1** APScheduler integration.
- **10.2** Daily price-ingest schedule.
- **10.3** Weekly recommendation schedule.
- **10.4** Langfuse setup for agent traces + prompt versions.
- **10.5** Cost tracking per pipeline run.

## Phase 11 — Hardening
- **11.1** Rate-limit-aware data clients (token bucket per provider).
- **11.2** Centralised error handler with email/Telegram alerts.
- **11.3** Secrets handling review (no secrets in repo, `.env` in a password manager).
- **11.4** DB backup script + restore drill.
- **11.5** README with full local-run instructions.

---

## Sequencing rationale

Three principles drove the order:

### 1. Get to an end-to-end working slice as fast as possible (Phases 0–4)
The biggest risk in a multi-agent + RAG + quant project is integration surprises — agent contracts not matching, data shapes wrong, prompts not behaving as expected. So Phases 0–4 build the *thinnest possible vertical slice*: foundation → real prices → one signal family → one LLM call producing a real recommendation. That gives something runnable and gradeable in ~2 weeks. Everything after is *replacing parts of a working system* rather than betting on a big-bang integration much later.

### 2. Lower-risk, higher-determinism work goes first
- Data plumbing (Phase 1) and quant signals (Phase 2) are deterministic, easy to test, and have well-known failure modes. Doing them first means the LLM agents in later phases are debugging *agent logic*, not "is my data wrong?"
- Backtesting (Phase 3) before LLM agents (Phase 4) so signals can be validated for predictive value *before* building narrative on top of them. If a signal is garbage, no rationale will save it.
- Single agent (Phase 4) before multi-agent (Phase 5) because graph orchestration is hard to debug; a working baseline gives a comparison point when decomposing.

### 3. Each phase produces something independently usable
- After Phase 1: a price database and CLI ingest.
- After Phase 3: a backtester — useful as a research tool by itself.
- After Phase 4: an `advise` CLI runnable weekly today, even with no UI or KB.
- After Phase 8: the system grades itself, even if interaction is still via CLI.
- The Next.js UI (Phase 9) lands late on purpose — it consumes a FastAPI surface that's been growing alongside features, and building screens earlier risks designing them around recommendations that are still wrong.

### Why specific later orderings
- **Multi-agent (5) before news/macro (6):** the agent boundaries drawn in Phase 5 dictate where news inputs go. Building news ingestion before knowing the agent topology means refactoring it once.
- **News (6) before RAG (7):** news is structured fetching with clear schemas; RAG involves chunking, embeddings, and retrieval-quality tuning. Doing the simpler ingestion first builds data-flow muscle and lets the synthesizer be tested with real inputs before adding retrieval as another variable.
- **Self-grading (8) before UI (9):** the most valuable thing the UI shows is performance over time. Building the UI before evaluations exist means the most interesting screen is empty.
- **Scheduling and observability (10) late:** running the pipeline manually is fine while iterating on agents and prompts. Automating an unstable pipeline just means automated failures.
- **Hardening (11) last:** rate-limit handling, alerting, and backups only matter once the system is doing work worth protecting. Doing them earlier is premature.

### Assumption
This ordering assumes active iteration on the system after MVP. If it needed to "just run unattended" from day 1, scheduling and hardening would move much earlier.
