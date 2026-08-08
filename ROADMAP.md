# Roadmap

This repo implements a deliberately scoped slice of the full Political Intelligence Platform PRD
it's built against, in the PRD's own prioritization order: **Phase 0 (trust foundations) → Phase 1a
(Manifesto RAG upgrade + Scorecard v1) → Phase 1b (search + evidence panel)**. Everything below is
what's *not* built, and why — so this reads as a scoped plan, not a silent gap.

## What's built, by phase

- **Phase 0 — trust foundations**: sentiment score legend (always visible, -100..+100, 5 bands)
  and confidence badges tied to mention volume (High/Medium/Low), applied identically to every
  topic (the "equal-treatment protocol").
- **Phase 1a — Manifesto RAG upgrade**: promise-atom extraction (splits on each manifesto's own
  numbered commitments instead of fixed-width chunks) across five parties, each atom tagged to the
  PRD's fixed 10-category taxonomy — via real LLM classification (Groq) when configured, keyword
  matching as the labeled fallback — flagged quantified vs. directional, plus a cross-party
  comparison view.
- **Phase 1a — Scorecard v1**: the real data model (Allocation Ratio / Utilization Rate /
  Delivery Index / Status, including "Goalpost Moved" and "Not Proven" as first-class statuses)
  with a small, independently-sourced seed dataset — not a live pipeline (see below).
- **Phase 1a follow-up — real ML tiers + wider data**: real transformer sentiment classification
  (HF Inference API) alongside VADER, the manifesto corpus expanded from 3 to 5 parties (BJP, INC,
  CPI(M), TMC, DMK), and GDELT added as a second scheduled news source alongside Google News RSS.
- **Phase 1b — search + evidence panel (A8/A10)**: an open free-text search bar (not limited to
  the six curated dashboard topics) with real query expansion (a hand-curated India-politics
  synonym/transliteration/hashtag dictionary — "GST" also matches "जीएसटी" — not a general
  translation model, see below), fanning out live to Reddit + Google News with an 8-second
  per-source timeout budget and a size-bounded 15-minute cache. Results include an evidence panel
  of the top-2-by-reach items per sentiment bucket — reach is a real engagement percentile for
  Reddit (has upvotes) and an honestly-labeled recency percentile for News (which has no
  engagement metric at all, so nothing is fabricated there).

## Deferred, and why

| Deferred item | Why it's not in yet |
|---|---|
| **CIB / bot filtering (A5)** | Our only social source (Reddit) is blocked from most cloud IPs, so we have no bot-laden social volume to filter in the first place. Building a filter with nothing real to filter would be theater, not a feature. Revisit once a real social source is licensed. The evidence panel's "top reach" is therefore not bot-filtered — worth knowing if this ever needs to survive real scrutiny. |
| **Multilingual / code-mixed NLP (A2)** | The search query-expansion dictionary covers ~30 hand-picked terms; it is not the IndicBERT-family model the PRD calls for, which needs self-hosting or a paid inference API — real memory/compute cost incompatible with free-tier hosting (see [janmat-pulse's own README](https://github.com/dev21382/janmat-pulse) for the OOM lesson that shaped this project's whole approach to resource budgets). |
| **Multimodal ingestion — OCR/Whisper (A11)** | Same free-tier memory constraint; async transcription queues need their own worker process and storage, which is a real infra project, not an add-on. |
| **YouTube ingestion** | Free but quota-capped (10,000 units/day per the PRD) — not wired up yet; GDELT and RSS covered more ground per engineering hour spent so far. |
| **Poll aggregation (B3)** | Needs a maintained, licensed feed of published polls with a track-record weighting scheme — no free source exists; this is a real data-partnership problem, not an engineering one. Still blocked as of Phase 1b. |
| **Seat projection / Monte Carlo forecasting (Pillar B)** | Explicitly gated by the PRD itself on backtesting against 2019/2024 before going live — shipping an unvalidated forecaster would violate the PRD's own non-negotiable rule, not just skip a nice-to-have. |
| **Live PFMS/CAG/budget-document pipeline (D1, beyond the seed set)** | PFMS and CAG don't expose clean public APIs — real ingestion means parsing scheme-level PDFs and portals per ministry, a multi-week data-engineering effort on its own. The seed dataset demonstrates the target methodology; it is not a substitute for that pipeline. |
| **IT Rules 2026 / ECI labelling, silence-period cutoffs, multi-tenant data walls** | Real legal/compliance requirements for a live client-facing product, but they're operational controls, not code that makes sense to half-build against zero actual clients or actual AI-generated content in this repo yet. |

## The full PRD

The complete product requirements document this roadmap is scoped against is kept out of this
repo (it's an internal planning document, not shipped code) — ask the maintainer if you need the
full text to plan the next phase.
