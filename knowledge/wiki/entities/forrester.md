---
title: Forrester
type: entity
status: verified
updated: 2026-06-25
sources: [src-forrester-tei]
links: [benchmarks, syntheses/contact-center-ai-value-thesis]
---

# Forrester

Industry analyst firm. Source of the **Total Economic Impact (TEI)** composites used to
sanity-check the model's returns (NPV / ROI / payback) against third-party deployments.

## Claims sourced to Forrester

The composites span several published conversational-AI TEI studies [src-forrester-tei]:
- **boost.ai** — 293% ROI, $19.9M NPV, payback < 12 months.
- **PolyAI** — 391% ROI, $11.3M NPV, $14.2M benefits over 3 years.
- **Sprinklr** — 210% ROI, payback < 6 months.

Rolled up: **ROI ~210–391%**, **NPV up to ~$19.9M**, **payback ~6–12 months**.

## Role in the model
These are the external reasonableness band for the dashboards' computed NPV / ROI / payback.
If the model's outputs land far outside this band on a comparable profile, that's a flag to
re-check inputs (WACC, ramp, implementation cost) — not evidence the benchmark is wrong.

## Verification (2026-06-25)
ROI and NPV ranges confirmed against published vendor TEI studies (boost.ai, PolyAI,
Sprinklr). One correction: the seeded **"5.4-month median payback"** could not be tied to a
specific study — published paybacks range ~6–12 months — so it is re-scoped and flagged
`contested` in [benchmarks](../benchmarks.md).

## Open items
- Locate a single authoritative Forrester composite (or name the specific TEI) if a precise
  median payback is needed for a board case.
