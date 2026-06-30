---
title: Contact-center AI value thesis
type: synthesis
status: seeded
updated: 2026-06-24
sources: [src-gartner-2025-automation, src-gartner-2026-cost, src-gartner-2022-labor, src-gartner-2024-selfservice, src-mck-2023-genai, src-mck-2025-transactional, src-mck-callcost, src-forrester-tei]
links: [comparisons/deterministic-vs-pure-llm, concepts/token-economics, concepts/complexity-tiers, concepts/deflection-quality-haircut, concepts/seat-decay-contradiction, benchmarks]
---

# The contact-center AI value thesis

The one-page argument the whole repo exists to make. Keep this intact across every artifact.

1. **The automation wave is real and large.** Agentic AI will autonomously resolve **~80% of
   common service issues by 2029** [src-gartner-2025-automation], and gen AI can cut
   human-serviced contacts **up to 50%** [src-mck-2023-genai]. **50–60% of interactions are
   transactional** and automation-eligible [src-mck-2025-transactional].

2. **Labor is the prize.** Contact-center cost is **up to 95% labor**
   [src-gartner-2022-labor]; an assisted (live) contact costs a **~$13.50 median**
   [src-gartner-2024-costbenchmarks] vs $1.84 in self-service. Value = deflected/assisted
   volume × that cost. (The model uses conservative per-channel defaults below the Gartner
   median; the discredited "$7.16 McKinsey" figure is superseded — see
   [benchmarks](../benchmarks.md).)

3. **But pure-LLM economics get worse over time.** AI cost per resolution will exceed
   **$3 by 2030** [src-gartner-2026-cost] as token/compute costs rise.

4. **ABL's deterministic moat.** Because ABL resolves routine work **without an LLM call**,
   its marginal cost stays near a ~$0.20 floor while rivals track the rising curve — the
   [divergence](../comparisons/deterministic-vs-pure-llm.md). The value is **durable** because
   it concentrates in the [low-complexity tier](../concepts/complexity-tiers.md).

5. **Discount for reality.** Only **~14% of issues fully self-resolve today**
   [src-gartner-2024-selfservice]; apply the [quality haircut](../concepts/deflection-quality-haircut.md)
   so the case survives scrutiny.

6. **Align the commercial model.** Consumption/outcome pricing resolves the
   [seat-decay contradiction](../concepts/seat-decay-contradiction.md) — savings stay with
   the customer as seats fall.

7. **Sanity-check the returns.** Computed NPV / ROI / payback should sit within Forrester's
   TEI band (ROI 208–391%, payback ~5.4 months) [src-forrester-tei] for a comparable profile.

**Standing caveat:** these are external projections; realized value depends on execution.
State this on every artifact.

## Reference case
100M annual interactions · 20,000 agents · $45k fully-loaded cost / agent. (Deal inputs, not
benchmarks.)
