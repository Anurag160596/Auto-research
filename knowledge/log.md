# Knowledge base — activity log

Append-only. One line per operation. Format (see [schema](./CLAUDE.md#5-log-line-format-logmd-append-only)):

```
DATE | OP | target | changes | note
```
`OP` ∈ `INGEST` | `QUERY` | `LINT`. Newest at the bottom.

**Active auto-update cadence:** every 72 hours (every 3rd day-of-month, 06:23 UTC) via
GitHub Actions running `knowledge/scripts/refresh.py` (free Gemini + Search grounding) →
opens a review PR. See
[CLAUDE.md §6](./CLAUDE.md#6-how-the-auto-update-runs).

---

2026-06-24 | INGEST | bootstrap | +schema, +index, +9 wiki pages, +registry(9 sources), +benchmarks(16) | Seeded the wiki from the project's root CLAUDE.md (§1 thesis, §7 sources). All claims status=seeded; source URLs pending. Next: a LINT pass to locate primary sources and flip seeded → verified.
2026-06-25 | LINT   | scope=all | verified=7 contested=3 seeded=1 | Manual ingest pass: located primary URLs for 4 Gartner + 3 McKinsey claims and Forrester TEI composites; flipped registry+benchmarks to verified. Flagged $7.16/call (ContactBabel, not McKinsey), AHT ~9% (understated vs field 15–25%), Forrester 5.4mo payback (untraceable) as contested. Ingested new Gartner caveat: >40% agentic-AI projects cancelled by 2027 (src-gartner-2025-cancellations, seeded).
2026-06-25 | INGEST | src-gartner-2024-costbenchmarks | +1 source, benchmarks +3 rows, +calculator citation | Tracked down a sanctioned replacement for the contested $7.16/call: Gartner "Benchmarks to Assess Your Customer Service Costs" (Feb 2024) — $13.50 median assisted / $1.84 self-service. Marked $7.16 (src-mck-callcost) superseded. Anchored human_cost_per_resolution to Gartner; noted calculator defaults ($6 voice/$4 chat) are conservative below it (no value change). Fixed misattribution in root CLAUDE.md §3/§7 and added Gartner citation to the calculator footer.
