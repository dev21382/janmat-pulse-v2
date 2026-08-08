# Janmat Pulse v2 — Political Intelligence Platform (Phase 0 + 1a + 1b)

Builds on [janmat-pulse](https://github.com/dev21382/janmat-pulse) — live sentiment tracking on Indian
political topics, a forecast trained on that real data, and manifesto intelligence over the 2024 Lok
Sabha party manifestos — and extends it toward the full [Political Intelligence Platform
PRD](ROADMAP.md) this project is scoped against: a trust-first sentiment score legend, ML-classified
promise-atom-level manifesto RAG across five parties, and a Promise-to-Performance scorecard. See
[ROADMAP.md](ROADMAP.md) for exactly what's built vs. explicitly deferred, and why.

**Live app**: deployed on Render — see repo description for the current link. Free-tier hosting, so the
first request after idle time can take ~50s to wake up.

## New in this revision

Three rounds of changes so far: the trust layer + manifesto/scorecard structure (Phase 0 + 1a), then
replacing rule-based/keyword approximation with real ML models and expanding the ingested data, then
Phase 1b's open search and evidence panel:

- **Open search + evidence panel (Phase 1b, A8/A10)** — a free-text search bar not limited to the six
  curated dashboard topics. Queries are expanded via a hand-curated India-politics synonym/
  transliteration/hashtag dictionary (e.g. "GST" also matches "जीएसटी") before fanning out live to
  Reddit + Google News, each capped at an 8-second timeout budget with a size-bounded 15-minute cache.
  Results include an evidence panel of the top-2-by-reach items per sentiment bucket — reach is a real
  engagement percentile for Reddit, an honestly-labeled recency percentile for News (no fabricated
  engagement numbers for sources that don't have any). GDELT is deliberately excluded from this live
  path since it self-throttles and stays a scheduled-ingestion-only source.

- **Real ML sentiment classification** — [`cardiffnlp/twitter-roberta-base-sentiment-latest`](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest)
  via Hugging Face's free Inference API is now the primary classifier (a supervised transformer, not a
  rule-based scorer), used when `HF_API_TOKEN` is set. VADER remains as the offline fallback — every
  stored item is tagged with which method actually scored it (`hf_roberta` or `vader`), never silently
  blended.
- **Real LLM-based promise taxonomy tagging** — Groq (`GROQ_API_KEY`, the same key already used for
  generative RAG) classifies each promise-atom into the fixed 10-category taxonomy via batched chat
  completions. Keyword matching is kept only as the offline fallback, and every atom is tagged with
  which method classified it (`llm` or `keyword`).
- **Manifesto corpus expanded from 3 parties to 5** — added TMC and DMK, and fixed BJP's manifesto
  (bjp.org itself times out for automated fetches from every network tested; the same document is
  mirrored reliably on [data.opencity.in](https://data.opencity.in)'s public elections-data catalog).
  BJP text extraction and page structure were verified before switching sources.
- **GDELT added as a second live news source** — the product spec's own top-recommended free source
  ("100+ languages, 15-minute refresh, genuinely free, no key, no cap") alongside Google News RSS.

## What's actually live vs. documented as a limitation

This is a working prototype, not a demo with mocked data. Everything below is real and running;
the limitations are stated plainly rather than papered over.

| Piece | Status |
|---|---|
| Reddit ingestion | Real, via Reddit's public unauthenticated `.json` search endpoint. Some cloud networks get rate-limited/blocked by Reddit's anti-bot measures — the pipeline degrades to News/GDELT-only when that happens, rather than faking posts. |
| News ingestion | Real, two independent sources: Google News RSS and GDELT's DOC 2.0 API, both scoped per topic. No API key needed for either. |
| X / Twitter | **Not included.** X's API is paid-only; rather than fake it, it's omitted. |
| Sentiment scoring | Real ML classification (`cardiffnlp/twitter-roberta-base-sentiment-latest` via Hugging Face's free Inference API) when `HF_API_TOKEN` is set; VADER (rule-based) otherwise. Every item stores which method scored it. |
| Forecast | A linear-trend estimate by default. The codebase also has a small PyTorch LSTM (`ENABLE_LSTM=true`) trained per-topic on the real accumulated daily sentiment history — disabled by default because torch's RSS footprint exceeds the 512MB ceiling on free-tier hosting (confirmed by an OOM kill in production). Enable it if you deploy somewhere with ~1GB+ RAM. |
| Manifesto RAG — retrieval | Real. Five parties' official 2024 manifesto PDFs (BJP, INC, CPI(M), TMC, DMK), chunked and ranked with TF-IDF + cosine similarity (scikit-learn) — chosen over transformer embeddings for the same memory-budget reason as the forecaster. |
| Manifesto RAG — generation | Real when a free Groq API key is configured (see below); otherwise the app serves ranked, cited excerpts directly with no generation step — still fully functional, just without prose synthesis. |
| Promise-atom extraction | Real. Regex-based extraction on each manifesto's own numbered lists, page-cited. Only produces atoms where the source document actually numbers its commitments — INC, CPI(M) and DMK do; BJP's manifesto is written as flowing prose (zero numbered markers in the extracted text) and TMC's uses non-numeric bullets, so those two contribute few or no atoms. That's a real property of those documents, not a gap in extraction — both are still fully covered by the whole-document RAG chat. |
| Promise-atom taxonomy tagging | Real LLM classification (Groq, batched) into the fixed 10-category taxonomy when `GROQ_API_KEY` is set; keyword-matching fallback otherwise (matched keywords shown for auditability either way). Every atom is tagged with which method classified it. |
| Cross-party promise comparison | Real. Side-by-side view per taxonomy category across parties whose manifesto structure yields promise-atoms, built directly from the extracted data. |
| Sentiment score legend + confidence bands | Real, always visible, same methodology applied to every topic. |
| Delivery Scorecard | Real data model; a small **hand-curated, independently-sourced seed dataset** (4 entries, each cited to PIB/CAG/PRS), not a live budget/PFMS/CAG ingestion pipeline — see [ROADMAP.md](ROADMAP.md). |
| Open search (any topic, not just the curated 6) | Real, live, on-demand fan-out to Reddit + Google News with query expansion, per-source timeout budgets, and a bounded 15-minute cache. GDELT is excluded from this live path (self-throttled, ingestion-only). |
| Evidence panel (top-2-by-reach per sentiment bucket) | Real. Reach is a genuine engagement percentile for Reddit (has upvotes); News items have no engagement metric at all, so their reach is an honestly-labeled recency percentile instead, never presented as equivalent to real engagement. Not CIB-filtered (see ROADMAP.md — no bot-laden source to filter yet). |

## Architecture

```
frontend/   React + Vite + TypeScript + Tailwind — Dashboard, Search, Manifesto Chat, Compare, Scorecard
backend/    FastAPI — ingestion (Reddit/News/GDELT), sentiment (ML + fallback), forecast, RAG
            pipeline (retrieval + promise-atoms + LLM taxonomy), scorecard, on-demand search
            (query expansion + evidence panel), REST API
Dockerfile  Multi-stage build: builds the frontend, serves it as static files from FastAPI
```

One container, one process, one URL — the frontend is served by the same FastAPI app as the
API, so there's nothing to configure across origins.

## Running locally

```bash
# backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# frontend (separate terminal)
cd frontend
npm install
npm run dev
```

The Vite dev server proxies `/api` to `localhost:8000`. Open `http://localhost:5173`.

To enable the PyTorch LSTM forecaster instead of the linear-trend default (needs more RAM):

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
ENABLE_LSTM=true uvicorn app.main:app --reload --port 8000
```

## Enabling the ML tiers

All three of these default to a fully functional non-ML fallback with zero configuration. Each one
upgrades independently when its key is set — none of them depend on each other.

| Feature | Env var | Free key from |
|---|---|---|
| Generative RAG answers (vs. cited excerpts) | `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) — 14,400 req/day, no card |
| LLM promise-taxonomy tagging (vs. keyword matching) | `GROQ_API_KEY` (same key) | same as above |
| ML sentiment classification (vs. VADER) | `HF_API_TOKEN` | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) — free, no card |

Set these in your deployment platform's secrets (Render → Environment). Never commit them to git —
see `.env.example`.

## Data sources

- Reddit: `r/india`, `r/IndianPolitics`, `r/IndiaSpeaks`, `r/worldnews` via public search JSON.
- News: Google News RSS + GDELT DOC 2.0 API, both scoped per topic, India edition.
- Manifestos (2024 Lok Sabha, official documents): [BJP Sankalp Patra](https://data.opencity.in/dataset/76e54184-f294-44e4-a40c-8594ccb410c8/resource/6210fb78-c1c3-4700-a61f-ed01daee9aff/download/7377fce3-f32d-4dba-8d1c-4969c25a3add.pdf),
  [INC Nyay Patra](https://manifesto.inc.in/assets/Congress-Manifesto-English-2024-Dyoxp_4E.pdf),
  [CPI(M) Manifesto](https://cpim.org/wp-content/uploads/old/documents/election_manifesto_english_april_2024.pdf),
  [TMC Didir Shopoth](https://data.opencity.in/dataset/76e54184-f294-44e4-a40c-8594ccb410c8/resource/628261ee-a164-4760-a475-7a7e10d78d44/download/5e073a4f-f293-4cb0-90f1-bf5847a0015b.pdf),
  [DMK Manifesto](https://data.opencity.in/dataset/76e54184-f294-44e4-a40c-8594ccb410c8/resource/c86a0519-1a32-407c-8381-41659734f9a2/download/a7964b61-ee79-4f84-9e1b-e3e28be52e04.pdf).
