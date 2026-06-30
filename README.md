# Knowledge-Base — self-maintaining LLM Wiki

A knowledge base built on **Andrej Karpathy's LLM Wiki pattern**: instead of RAG, an LLM
*compiles* raw research into a directory of dense, interlinked markdown pages and incrementally
maintains them. You read the wiki; the AI owns and updates it.

**Topic:** the research and evidence base behind a contact-center AI value model
(Gartner / McKinsey / Forrester benchmarks, token economics, the deterministic-vs-pure-LLM
cost divergence).

## Structure

```
knowledge/
  CLAUDE.md          # the schema — page types + ingest/query/lint operations
  index.md           # content catalog
  log.md             # append-only activity log
  sources/registry.md# provenance for every cited figure
  wiki/              # entity / concept / comparison / synthesis pages + benchmarks.md
.github/workflows/
  knowledge-refresh.yml  # 72h auto-refresh (free Gemini + Google Search grounding)
```

Read [`knowledge/CLAUDE.md`](knowledge/CLAUDE.md) first — it defines the conventions and the
three operations (ingest / query / lint).

## Auto-refresh (free)

Every 72 hours, a GitHub Action runs `knowledge/scripts/refresh.py`, which uses the **free
Google Gemini API with Google Search grounding** to verify seeded sources, fill primary-source
URLs, flip `seeded → verified` (or `contested`), and open a review PR.

### One-time setup
1. Free Gemini key: <https://aistudio.google.com/apikey>
2. Add repo secret **`GEMINI_API_KEY`** (Settings → Secrets and variables → Actions).
3. Settings → Actions → General → enable **"Allow GitHub Actions to create and approve pull requests."**

Then trigger it from the **Actions** tab → *Knowledge base — 72h refresh* → **Run workflow**.

## Provenance
Seeded from the value-modeling project's research notes; verified in a 2026-06-25 pass
(primary Gartner/McKinsey/Forrester URLs recorded). See `knowledge/log.md` for the history.
