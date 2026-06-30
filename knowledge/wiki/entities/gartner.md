---
title: Gartner
type: entity
status: verified
updated: 2026-06-25
sources: [src-gartner-2025-automation, src-gartner-2026-cost, src-gartner-2022-labor, src-gartner-2024-selfservice, src-gartner-2024-costbenchmarks, src-gartner-2025-cancellations]
links: [benchmarks, concepts/token-economics, concepts/deflection-quality-haircut, syntheses/contact-center-ai-value-thesis]
---

# Gartner

Industry analyst firm. Primary external source for the **automation ceiling**, the **rising
AI-cost curve**, and the **labor-cost structure** of contact centers in this value model.

## Claims sourced to Gartner

- **~80% of common customer-service issues will be autonomously resolved by agentic AI by
  2029**, with ~30% opex reduction [src-gartner-2025-automation]. → sets the upper bound on
  automatable volume.
- **AI cost per resolution will exceed $3 by 2030** as token/compute costs rise
  [src-gartner-2026-cost]. → the engine of the [deterministic-vs-pure-LLM divergence](../comparisons/deterministic-vs-pure-llm.md).
- **Labor is up to 95% of contact-center cost**; **~$80B labor displacement by 2026**
  [src-gartner-2022-labor]. → why value concentrates in seat reduction / deflection.
- **Only ~14% of issues fully self-resolve today** [src-gartner-2024-selfservice]. → grounds
  the [quality haircut](../concepts/deflection-quality-haircut.md): headline automation rates
  must be discounted for failed containment and repeats.
- **Cost per contact: ~$13.50 assisted vs ~$1.84 self-service** (median, Feb 2024)
  [src-gartner-2024-costbenchmarks]. → the sanctioned anchor for the model's
  `human_cost_per_resolution`, replacing the misattributed $7.16. Offshore B2C resolution
  runs **$2–$4** [src-gartner-2026-cost] — the floor that pure-LLM cost (>$3 by 2030) is set
  to cross. See [benchmarks](../benchmarks.md).

## Tension to watch
The 80%-by-2029 ceiling and the $3-by-2030 cost both point at agentic AI, but they cut
opposite ways: automation rises while *per-resolution* cost rises for pure-LLM approaches.
The model's thesis lives in that gap — see [the synthesis](../syntheses/contact-center-ai-value-thesis.md).
Note the 2026 cost note frames it precisely as GenAI cost/resolution exceeding **offshore
human-agent** cost, driven by data-center costs, vendor pivot to profitability, and
token-heavy complex use cases.

## Credibility caveat (added 2026-06-25)
Gartner also predicts **>40% of agentic-AI projects will be cancelled by end of 2027**
[src-gartner-2025-cancellations] — escalating costs, unclear business value, inadequate risk
controls. This does not contradict the 80%-by-2029 ceiling (which is directionally sound) but
underscores that **realized** value depends on execution. Carry this caveat into board
materials so the case reads as credible rather than hype.

## Verification (2026-06-25)
All four core Gartner claims located and confirmed against primary press releases (see the
[registry](../../sources/registry.md)). The 2022 labor note adds useful context: only ~1 in
10 interactions automated by 2026, against ~17M agents worldwide — i.e. the $80B comes from a
modest automation rate applied to a labor-heavy cost base.

## Open items
- `src-gartner-2025-cancellations` entered `seeded`; confirm the exact press-release URL/date.
