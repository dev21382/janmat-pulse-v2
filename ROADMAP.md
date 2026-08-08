# Roadmap

This repo implements a deliberately scoped slice of the full [Political Intelligence Platform
PRD](#the-full-prd) it's built against: **Phase 0 (trust foundations) + Phase 1a (Manifesto RAG
upgrade + Scorecard v1)**, in the PRD's own prioritization order. Everything below is what's
*not* built, and why — so this reads as a scoped plan, not a silent gap.

## What v2 actually adds over v1

- **Phase 0 — trust foundations**: sentiment score legend (always visible, -100..+100, 5 bands)
  and confidence badges tied to mention volume (High/Medium/Low), applied identically to every
  topic (the "equal-treatment protocol").
- **Phase 1a — Manifesto RAG upgrade**: promise-atom extraction (splits on the manifesto's own
  numbered commitments instead of fixed-width chunks), each atom tagged to the PRD's fixed
  10-category taxonomy and flagged quantified vs. directional, plus a cross-party comparison view.
- **Phase 1a — Scorecard v1**: the real data model (Allocation Ratio / Utilization Rate /
  Delivery Index / Status, including "Goalpost Moved" and "Not Proven" as first-class statuses)
  with a small, independently-sourced seed dataset — not a live pipeline (see below).

## Deferred, and why

| Deferred item | Why it's not in v2 |
|---|---|
| **CIB / bot filtering (A5)** | Our only social source (Reddit) is blocked from most cloud IPs, so we have no bot-laden social volume to filter in the first place. Building a filter with nothing real to filter would be theater, not a feature. Revisit once a real social source is licensed. |
| **Multilingual / code-mixed NLP (A2)** | Needs a self-hosted IndicBERT-family model or a paid inference API — real memory/compute cost incompatible with free-tier hosting (see [janmat-pulse's own README](https://github.com/dev21382/janmat-pulse) for the OOM lesson that shaped this project's whole approach to resource budgets). |
| **Multimodal ingestion — OCR/Whisper (A11)** | Same free-tier memory constraint; async transcription queues need their own worker process and storage, which is a real infra project, not an add-on. |
| **Full continuous sentiment pipeline (Phase 1b/2)** | GDELT/YouTube ingestion at the PRD's specified cadence needs a scheduler and quota-aware fetcher beyond what a single free web service can run continuously. |
| **Poll aggregation (B3)** | Needs a maintained, licensed feed of published polls with a track-record weighting scheme — no free source exists; this is a real data-partnership problem, not an engineering one. |
| **Seat projection / Monte Carlo forecasting (Pillar B)** | Explicitly gated by the PRD itself on backtesting against 2019/2024 before going live — shipping an unvalidated forecaster would violate the PRD's own non-negotiable rule, not just skip a nice-to-have. |
| **Live PFMS/CAG/budget-document pipeline (D1, beyond the seed set)** | PFMS and CAG don't expose clean public APIs — real ingestion means parsing scheme-level PDFs and portals per ministry, a multi-week data-engineering effort on its own. The seed dataset demonstrates the target methodology; it is not a substitute for that pipeline. |
| **IT Rules 2026 / ECI labelling, silence-period cutoffs, multi-tenant data walls** | Real legal/compliance requirements for a live client-facing product, but they're operational controls, not code that makes sense to half-build against zero actual clients or actual AI-generated content in this repo yet. |

## The full PRD

The complete product requirements document this roadmap is scoped against is kept out of this
repo (it's an internal planning document, not shipped code) — ask the maintainer if you need the
full text to plan the next phase.
