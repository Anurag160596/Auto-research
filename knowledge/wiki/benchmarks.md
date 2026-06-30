---
title: Benchmark ledger
type: concept
status: verified
updated: 2026-06-25
sources: [src-gartner-2025-automation, src-gartner-2026-cost, src-gartner-2022-labor, src-gartner-2024-selfservice, src-gartner-2025-cancellations, src-mck-2023-genai, src-mck-2025-transactional, src-mck-2024-qa, src-mck-callcost, src-contactbabel-callcost, src-forrester-tei]
links: [syntheses/contact-center-ai-value-thesis, concepts/token-economics]
---

# Benchmark ledger

Every **quantitative** claim the value model is allowed to use. Downstream artifacts (the
ROI calculator, Excel models, dashboards) should trace each number to a row here. Client
deal inputs (volume, headcount, cost/agent) are **not** benchmarks — they belong in the deal,
not in this ledger.

| metric | value | source | date | confidence | verification |
|---|---|---|---|---|---|
| Routine issues autonomously resolvable by 2029 | ~80% | Gartner [src-gartner-2025-automation] | 2025-03 | high | verified |
| Opex reduction from agentic CC AI | ~30% | Gartner [src-gartner-2025-automation] | 2025-03 | med | verified |
| Agentic-AI projects cancelled by end 2027 | > 40% | Gartner [src-gartner-2025-cancellations] | 2025-06 | med | seeded |
| AI cost per resolution by 2030 | > $3.00 | Gartner [src-gartner-2026-cost] | 2026-01 | med | verified |
| Labor share of contact-center cost | up to 95% | Gartner [src-gartner-2022-labor] | 2022-08 | high | verified |
| Agent labor cost reduced by conversational AI in 2026 | ~$80B | Gartner [src-gartner-2022-labor] | 2022-08 | med | verified |
| Issues that fully self-resolve today | ~14% | Gartner [src-gartner-2024-selfservice] | 2024-08 | high | verified |
| Human-serviced contact reduction (gen AI) | up to 50% | McKinsey [src-mck-2023-genai] | 2023-06 | high | verified |
| Productivity value (share of function cost) | 30–45% | McKinsey [src-mck-2023-genai] | 2023-06 | med | verified |
| AHT compression — measured (field results) | ~9% to >25% | McKinsey [src-mck-2023-genai] | 2023-06 | med | contested |
| Transactional (automation-eligible) share | 50–60% | McKinsey [src-mck-2025-transactional] | 2025-03 | high | verified |
| QA savings from gen-AI quality review | > 50% | McKinsey [src-mck-2024-qa] | 2024-07 | med | verified |
| Median cost per **assisted** (live) contact | $13.50 | Gartner [src-gartner-2024-costbenchmarks] | 2024-02 | high | verified |
| Median cost per **self-service** contact | $1.84 | Gartner [src-gartner-2024-costbenchmarks] | 2024-02 | high | verified |
| Offshore B2C human cost per resolution | $2–$4 | Gartner [src-gartner-2026-cost] | 2026-01 | med | verified |
| ~~Avg cost per inbound call $7.16~~ (superseded) | $7.16 | ⚠ ContactBabel, not McKinsey — replaced by Gartner row above [src-mck-callcost] | 2025 | low | superseded |
| Forrester TEI ROI range | ~210–391% | Forrester [src-forrester-tei] | 2024 | med | verified |
| Forrester TEI NPV (composite, top end) | up to ~$19.9M | Forrester [src-forrester-tei] | 2024 | med | verified |
| Forrester TEI payback | ~6–12 months | Forrester [src-forrester-tei] | 2024 | low | contested |

> **Verification notes (2026-06-25 pass):**
> - **AHT compression** — the seeded "~9% measured" understates published field results;
>   McKinsey case studies cite 15% (banking, 100 days) to >25% (telecom). Re-scoped to a
>   ~9%→>25% range and marked `contested` pending a single canonical figure.
> - **$7.16 per call** — widely cited as McKinsey but the primary source appears to be
>   **ContactBabel** (2025 US Contact Center Decision-Makers' Guide), which is *not* a
>   sanctioned benchmark firm. Treat as directional only; confirm or replace with a
>   Gartner/McKinsey/Forrester figure before using in a board case.
> - **Forrester payback** — the seeded "5.4 months median" could not be tied to a specific
>   study; published composites range ~6–12 months (boost.ai <12mo, Sprinklr/Dynamics <6mo).

## Model-internal assumptions (not external benchmarks)

These are engineering defaults of the value model, **not** sourced benchmarks. They need
validation against ABL production telemetry, not analyst reports.

| assumption | default | owner to confirm |
|---|---|---|
| Platform cost per interaction (deterministic floor) | $0.20 | Finance |
| Frontier token price — input | $3.00 / M | Pricing |
| Frontier token price — output | $15.00 / M | Pricing |
| Failed-containment haircut | 12% | Product |
| Repeat-contact drag | 6% | Product |
| Automation rates Low / Med / High | 90 / 60 / 25 % | Product |
| Human cost per resolution — voice (calculator default) | $6 | conservative vs Gartner $13.50 assisted |
| Human cost per resolution — chat (calculator default) | $4 | conservative vs Gartner $13.50 assisted |

> **Cost-per-contact anchor (2026-06-25):** the human-cost multiplier is now anchored to
> Gartner's **$13.50 median per assisted contact** [src-gartner-2024-costbenchmarks], not the
> superseded $7.16. The ROI calculator's per-channel defaults ($6 voice / $4 chat) sit
> *below* that, so the value case is conservative; a board case could justify raising them
> toward the Gartner benchmark.

> **Caveat (carry into every artifact):** external benchmarks are projections; realized
> value depends on execution. Every `pending` row is a task for the next [lint pass](../CLAUDE.md#4-operations).
