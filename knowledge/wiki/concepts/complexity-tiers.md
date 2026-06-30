---
title: Complexity tiers
type: concept
status: seeded
updated: 2026-06-24
sources: [src-mck-2025-transactional]
links: [concepts/token-economics, concepts/deflection-quality-haircut, entities/mckinsey, benchmarks]
---

# Complexity tiers (Low / Medium / High)

Interactions are split into three complexity tiers. Each carries a volume-mix %, an
automation rate, and an [LLM call build-up](./token-economics.md). The tiering is what makes
the value **durable**: it concentrates in the low-complexity tier, which is both the cheapest
to automate (no LLM call) and the largest by volume.

| tier | default automation rate | LLM calls | cost driver |
|---|---|---|---|
| Low | 90% | 0 (deterministic) | platform floor only |
| Medium | 60% | 1 | floor + modest tokens |
| High | 25% | 4 | floor + heavy tokens |

## Links to the evidence
- McKinsey's **50–60% transactional** share [src-mck-2025-transactional] maps to the low/medium
  tiers — the automation-eligible majority.
- The **High-complexity** answer auto-distributes the remainder to low/medium at ~2:1 in the
  dashboards (an engineering convention, not a benchmark).

## Open items
- Review the Low/Medium/High split and per-tier automation rates with Product.
