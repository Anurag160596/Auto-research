# knowledge/ — LLM Wiki (Karpathy pattern)

This directory is a **self-maintaining knowledge base** built the way Andrej Karpathy
described in his April-2026 *LLM Knowledge Base / LLM Wiki* note: instead of RAG, an LLM
**compiles** raw research into a directory of dense, interlinked markdown pages, updates
those pages as new sources arrive, and periodically audits them for contradictions and
gaps. You read the wiki; the AI owns and maintains it.

> Reference: Karpathy, "LLM Knowledge Bases" (gist `442a6bf…`), VentureBeat coverage
> "Karpathy shares 'LLM Knowledge Base' architecture that bypasses RAG", April 2026.

**This wiki's topic:** the research and evidence base behind the ABL / Kore.ai
contact-center value model in this repo (see the root `CLAUDE.md`). Its job is to be the
single, sourced source-of-truth for every benchmark and assumption the dashboards rely on.

---

## 1. Three layers

1. **Raw sources** (`sources/`) — immutable. The original articles, reports, PDFs,
   screenshots, and quotes. Never edited after capture; only appended to. Each source gets
   a stable id and a one-line provenance entry in `sources/registry.md`.
2. **The wiki** (`wiki/`) — LLM-generated, LLM-owned markdown. Dense, synthesized,
   cross-linked. This is the layer you read and that downstream artifacts cite.
3. **The schema** (this file) — the rules below. Defines page types, conventions, and the
   three operations: **ingest**, **query**, **lint**.

Plus two control files at the root of `knowledge/`:
- `index.md` — content catalog, by category, one line per page, with links.
- `log.md` — append-only chronological record of every ingest / query / lint pass.

---

## 2. Page types (under `wiki/`)

| Folder | Page type | Holds |
|---|---|---|
| `entities/` | **Entity page** | One organization, vendor, product, or person (e.g. Gartner, McKinsey, Forrester, Kore.ai). Stable facts + every claim that entity is the source of. |
| `concepts/` | **Concept page** | One idea or mechanism (token economics, complexity tiers, the quality haircut, seat-decay). Definition, math, evidence, open questions. |
| `comparisons/` | **Comparison page** | A head-to-head (deterministic vs pure-LLM cost; seat vs consumption pricing). |
| `syntheses/` | **Synthesis page** | A cross-cutting argument assembled from many pages (the overall value thesis). |
| `benchmarks.md` | **Benchmark ledger** | One table: every *quantitative* claim, with number, source entity, date, confidence, and verification status. The numbers the model is allowed to use live here. |

---

## 3. Page conventions

Every wiki page starts with YAML front-matter:

```yaml
---
title: McKinsey
type: entity            # entity | concept | comparison | synthesis
status: verified        # verified | seeded | stale | contested
updated: 2026-06-24     # ISO date of last edit (pass in via the run; do not invent)
sources: [src-mck-2023-genai, src-mck-2025-transactional]
links: [concepts/token-economics, benchmarks]
---
```

Rules:
- **Markdown only.** No vendor lock-in; any text editor must be able to read it.
- **Every quantitative claim cites a source id** from `sources/registry.md` inline, e.g.
  `AHT compression ~9% measured [src-mck-2023-genai]`.
- **Cross-link generously.** Reference other pages by relative path. From a page in
  `wiki/entities/`, a concept link looks like `[token economics] -> ../concepts/token-economics.md`.
  A page with no inbound links is an
  orphan and the lint pass will flag it.
- **Honesty over polish.** Mark unverified material `status: seeded` and say so in the body.
  Note contradictions explicitly rather than smoothing them over.
- **No date invention.** Dates come from the source or from the run's supplied "today"; if
  unknown, write `date: unknown`.

---

## 4. Operations

### Ingest (add a source)
1. Capture the raw source into `sources/` (or record its URL + key quotes there) and add a
   line to `sources/registry.md` with a new `src-…` id.
2. Read it. Extract the key takeaways.
3. Write or update the relevant **entity** and **concept** pages. Add any quantitative claim
   to `benchmarks.md`.
4. If the new source **contradicts** an existing claim, do not overwrite silently — record
   both, mark the older `status: contested`, and note the conflict in the body.
5. Update `index.md`. Append an `INGEST` line to `log.md`.

### Query (answer from the wiki)
1. Read the relevant wiki pages (not the raw sources) first.
2. Answer **with citations** back to source ids / pages.
3. If the answer is durable and reusable, file it back as a new synthesis/concept page —
   "explorations become permanent knowledge." Append a `QUERY` line to `log.md`.

### Lint (periodic health check) — this is the auto-update beat
Run on a schedule. Each pass:
1. **Contradictions** — claims that disagree across pages → reconcile or mark `contested`.
2. **Stale claims** — anything older than the freshness window (default **180 days**) or
   superseded by a newer report → mark `status: stale` and queue a refresh search.
3. **Orphans** — pages with no inbound links → link them in or retire them.
4. **Gaps** — concepts referenced but with no page; benchmarks with `verification: pending`.
5. **Refresh** — for each stale/pending item, run a web search for newer figures and
   **ingest** what's found.
6. Append a `LINT` line to `log.md` summarizing what changed.

---

## 5. Log line format (`log.md`, append-only)

```
2026-06-24 | INGEST | src-mck-2025-transactional | +concepts/complexity-tiers, +benchmarks(2) | McKinsey 50–60% transactional
2026-06-24 | LINT   | scope=all | stale=3 orphan=1 contradictions=0 refreshed=2
2026-06-24 | QUERY  | "what is the deterministic cost floor?" | filed synthesis/cost-floor
```
Consistent leading prefixes (`INGEST` / `QUERY` / `LINT`) keep the log machine-parseable.

---

## 6. How the auto-update runs

**Active transport:** GitHub Actions — `.github/workflows/knowledge-refresh.yml`, which runs
`knowledge/scripts/refresh.py`.
**Cadence:** every 72 hours (every 3rd day-of-month, 06:23 UTC) + manual `Run workflow`.

Each run executes a stdlib-only Python script that uses the **free Google Gemini API with
Google Search grounding** to verify seeded sources — filling primary-source URLs, flipping
`seeded → verified` (or `contested`), and propagating status into
[`benchmarks.md`](./wiki/benchmarks.md). It appends a `LINT` line to [`log.md`](./log.md) and
opens a pull request (`auto/knowledge-refresh`) so AI-assisted edits are reviewed before they
land on `main`.

One-time setup (repo admin) — no paid key, no GitHub App required:
1. Get a free Gemini key: <https://aistudio.google.com/apikey>
2. Add the `GEMINI_API_KEY` repo secret (Settings → Secrets and variables → Actions).
3. Settings → Actions → General → enable "Allow GitHub Actions to create and approve pull
   requests."

> Deeper passes (page-level `status` upkeep, orphan/contradiction reconciliation, ingesting
> brand-new sources) still benefit from a full LLM agent — any Claude session pointed at
> `knowledge/` with this schema as context can do them by hand per §4. The Gemini script
> covers the recurring source-verification beat for free.
