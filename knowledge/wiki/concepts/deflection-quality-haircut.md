---
title: Deflection quality haircut
type: concept
status: seeded
updated: 2026-06-24
sources: [src-gartner-2024-selfservice]
links: [concepts/complexity-tiers, entities/gartner, benchmarks]
---

# Deflection quality haircut

Headline automation rates overstate realized deflection, because some contained interactions
fail (escalate later) and some customers come back. The model discounts the raw rate:

```
effective = automation_rate × (1 − failed_containment) × (1 − repeat_drag)
```

## Defaults (model-internal — see [benchmarks](../benchmarks.md))
- `failed_containment` = **12%**
- `repeat_drag` = **6%**

## Why these defaults are defensible
Gartner finds **only ~14% of issues fully self-resolve today** [src-gartner-2024-selfservice].
That low real-world self-resolution rate is the justification for haircutting optimistic
automation assumptions rather than taking them at face value.

## Interaction with tiers
Some Excel models additionally **cap** effective deflection by the McKinsey transactional
share (50–60%) — you cannot deflect more than the automation-eligible volume. See
[complexity tiers](./complexity-tiers.md).

## Open items
- Calibrate `failed_containment` and `repeat_drag` against ABL containment telemetry.
