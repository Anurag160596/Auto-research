---
title: Deterministic vs pure-LLM cost
type: comparison
status: seeded
updated: 2026-06-24
sources: [src-gartner-2026-cost, src-gartner-2025-automation]
links: [concepts/token-economics, entities/gartner, entities/kore-ai, syntheses/contact-center-ai-value-thesis]
---

# Deterministic (ABL) vs pure-LLM cost per resolution

The signature chart of the whole project: ABL's cost stays roughly **flat**; the pure-LLM
rival's cost **rises** toward 2030.

| | ABL (deterministic) | Pure-LLM rival |
|---|---|---|
| Cost basis | platform floor (~$0.20), tokens only when an LLM is called | tokens on **every** resolution |
| Low-complexity tier | $0.20 floor, **no** LLM call | full token cost every time |
| Trajectory to 2030 | flat (infra floor) | rising toward **>$3 / resolution** [src-gartner-2026-cost] |
| Durability | high — value sits in the low tier | erodes as token/compute cost climbs |

## The mechanism
Both approaches can hit [Gartner's ~80% automation ceiling](../entities/gartner.md)
[src-gartner-2025-automation]. The difference is **unit cost at that ceiling**: the
deterministic path resolves the routine majority with zero token spend, so rising token
prices barely move its blended cost; the pure-LLM path pays tokens on everything and tracks
the rising curve. See the arithmetic in [token economics](../concepts/token-economics.md).

## Design note (for the dashboards)
Render ABL in teal (`#2dd4bf`, flat) and the pure-LLM rival in amber (`#f59e0b`, rising) —
the divergence is the centerpiece visual. (Kept here so the narrative and the chart stay in
sync.)

## Open items
- Verify the $3-by-2030 figure against the primary Gartner note; confirm whether it is a
  blended or worst-case per-resolution number.
