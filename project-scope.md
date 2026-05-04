# AI-Powered Financial Advisor

## Problem

I want to put part of my savings to work in trading, but I lack clarity on which tools to use and how to time entries and exits.
I need guidance to make more informed decisions and improve long-term returns.

## Solution

Build a **personal trading advisor** (web app, for my own use — not a product for third parties) that turns market analysis into concrete guidance aligned with the Problem above: which instruments to consider, how much capital to allocate to each, and when to enter or exit positions.

The system proposes a **small, focused set of instruments** (typically two or three) rather than an open-ended watchlist, so decisions stay actionable. It stays current by aggregating signals from **trusted financial news and data sources**, and it grounds recommendations in a **curated knowledge base** on markets, products, and risk—not only on day-to-day headlines.

## Scope & Constraints

- **Audience:** personal use only (single user: me).
- **Instruments:** ETFs, ETCs, ETNs, bonds, options.
- **Markets:** EU and US.
- **Time horizon:** swing trading (days to weeks).
- **Execution model:** advisory only for v1. Autonomous execution via broker API is a possible future direction, not in scope now.
- **Data sources:** free tiers for v1. Paid / real-time market data feeds may be added later.
- **Delivery surface:** web app.

## Architecture (high level)

- **Hybrid approach:** LLM-driven reasoning combined with quantitative models for signals and risk.
- **Multi-agent design:** specialised agents collaborate (e.g. market intelligence, technical/quantitative analysis, allocation, rationale generation).
- **RAG-backed knowledge base:** curated documents on products, mechanics, and risk grounded via retrieval.
- **Self-grading loop:** the system records its own prior recommendations, evaluates them against realised outcomes, and uses that feedback to update the model and/or KB over time.

## Features

### MVP (v1)

1. **Shortlist of instruments (2–3)** — Rank and explain why a small set of assets or products fits the profile and current context.
2. **Allocation guidance** — Suggest how to split capital across the shortlist with rationale (e.g. diversification, volatility, liquidity).
3. **Entry / exit signals** — Clear buy, hold, or sell-style recommendations with timing context (not only "now" but what would change the view).
4. **Multi-source market intelligence** — Ingest and reconcile news, macro data, and market feeds from configurable trusted (free-tier) sources.

### Post-MVP

5. **Investor profile & constraints** — Capture risk tolerance, horizon, jurisdiction, and capital available so suggestions stay within stated boundaries.
6. **Knowledge-base grounding** — Retrieve and cite concepts from a curated KB (products, mechanics, risk) so advice is explainable and consistent.
7. **Narrative rationale** — Human-readable summary linking each recommendation to evidence (sources + KB), for learning and audit.
8. **Change detection & refresh** — Detect material new information and refresh or flag stale guidance instead of silent drift.
9. **Alerts & digest** — Optional notifications or periodic digests when the shortlist or thesis changes meaningfully.
10. **Compliance & safety rails** — Personal guardrails (e.g. concentration limits, leverage caps) and disclaimers against advice outside an appropriate scope.

## Open Questions

These decisions are deferred until we start designing the relevant component, but each will need an answer:

- **Conflict reconciliation** — how to resolve disagreements across data/news sources (e.g. bullish news vs. bearish technicals).
- **Validation strategy** — backtesting, paper-trading, or both, before trusting recommendations.
- **Free-tier data coverage gaps** — especially EU ETCs/ETNs and option chains, where free APIs are weak.
- **Tax handling** — whether the advisor reasons about realised gains, holding periods, or wash-sale-equivalent rules.
- **Hard compliance floors** — concrete personal rules the system must never violate (leverage cap, max single-position concentration, excluded instruments).
- **Multi-agent framework** — LangGraph, CrewAI, custom orchestration, or other.
- **Self-grading mechanics** — what counts as a "wrong call", over what window, and how aggressively the model/KB should adapt without overfitting to short-term noise.
