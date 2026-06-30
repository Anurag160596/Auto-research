---
title: Token economics (cost build-up)
type: concept
status: seeded
updated: 2026-06-24
sources: [src-gartner-2026-cost]
links: [concepts/complexity-tiers, comparisons/deterministic-vs-pure-llm, benchmarks, entities/kore-ai]
---

# Token economics — the cost build-up

The per-resolution cost of an automated interaction, built from a deterministic platform
floor plus any LLM token cost stacked on top **only where an LLM is actually called**.

```
ABL cost/resolution = platform_cost_per_interaction + LLM_token_cost
LLM_token_cost      = calls × (input_tokens × input_price + output_tokens × output_price) / 1,000,000
```

## Defaults (model-internal — see [benchmarks](../benchmarks.md))
- Platform cost: **$0.20 / interaction** — all-in deterministic floor.
- Token prices: **$3.00 / M input, $15.00 / M output** (frontier rates).
- **Low tier:** 0 LLM calls (pure deterministic) → cost = platform floor only.
- **Medium:** 1 call, 2,000 in / 500 out.
- **High:** 4 calls, 4,000 in / 1,000 out.

## Why it matters
Because the low tier makes **zero** LLM calls, its cost is fixed at the platform floor and
does not move with token prices. Pure-LLM approaches pay tokens on *every* resolution, so
their cost rises with [Gartner's $3-by-2030 curve](../entities/gartner.md). This is the
arithmetic behind the [divergence](../comparisons/deterministic-vs-pure-llm.md).

## Open items
- Validate calls/tokens per tier against ABL production telemetry.
- Confirm the $0.20 platform floor with Finance.
