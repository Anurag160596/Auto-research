---
title: McKinsey
type: entity
status: verified
updated: 2026-06-25
sources: [src-mck-2023-genai, src-mck-2025-transactional, src-mck-2024-qa, src-mck-callcost, src-contactbabel-callcost]
links: [benchmarks, concepts/complexity-tiers, concepts/deflection-quality-haircut, syntheses/contact-center-ai-value-thesis]
---

# McKinsey

Management consultancy. Primary external source for **contact-reduction potential**,
**productivity value**, the **transactional share** that bounds automation, and the
**per-call cost** the value model monetizes.

## Claims sourced to McKinsey

- **Gen AI can cut human-serviced contacts up to 50%**; productivity value **30–45% of
  function cost**; **AHT compression ~9% measured**, up to **>25% in full transformation**
  [src-mck-2023-genai]. → the agent-assist (handle-time) benefit line.
- **50–60% of interactions are transactional** and therefore automation-eligible
  [src-mck-2025-transactional]. → an upper cap on deflectable volume; some Excel models cap
  effective deflection by this share.
- **>50% QA savings** from gen-AI-assisted quality review [src-mck-2024-qa].
- ~~**~$7.16 average fully-loaded cost per inbound call** [src-mck-callcost].~~ ⚠ **Superseded
  (2026-06-25):** this figure is widely *attributed* to McKinsey but the primary source is
  **ContactBabel** (2025 US Contact Center Decision-Makers' Guide)
  [src-contactbabel-callcost], not a sanctioned benchmark firm. The cost-per-resolution
  anchor is now **Gartner's $13.50 median per assisted contact** (Feb 2024) — see the
  [Gartner page](./gartner.md) and [benchmarks](../benchmarks.md). $7.16 is no longer used.

## How these feed the model
The transactional share (50–60%) and the [complexity tiers](../concepts/complexity-tiers.md)
describe the same thing from two angles: the low-complexity, transactional tier is where
deterministic automation is both feasible and durable.

## Verification (2026-06-25)
Contact-reduction (up to 50%), productivity (30–45%), transactional share (50–60%), and QA
savings (>50%) all confirmed against McKinsey primary articles (see the
[registry](../../sources/registry.md)). The seeded "~9% measured AHT" understates published
field results (15% banking / >25% telecom) and is re-scoped + flagged in
[benchmarks](../benchmarks.md).

## Open items
- Replace or re-source the `$7.16` per-call figure (currently `contested`, traced to
  ContactBabel rather than McKinsey).
