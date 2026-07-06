# Documents — put your source files here

**This is where you put all the documents.** Drop any raw research material here — PDFs,
articles saved as `.md`/`.txt`/`.html`, screenshots, reports, exported notes.

This folder is **Layer 1 (raw sources)** of the LLM Wiki (see [`../../CLAUDE.md`](../../CLAUDE.md)).
Documents dropped here are **immutable inputs**: the LLM reads them and *compiles* their
content into the wiki pages under `../../wiki/`. You never edit the wiki by hand — you add
documents here, and an ingest pass turns them into pages.

## How to add a document
1. Put the file in this folder (e.g. `documents/gartner-2026-cost.pdf`).
2. Add one row to [`../registry.md`](../registry.md) with a new `src-…` id, the source, the
   key finding, the date, and (if online) the URL.
3. On the next **ingest** pass (run by an agent, or the automated engine picking it up), the
   document is read and its takeaways are written into the relevant entity/concept pages and
   the benchmark ledger — with a `LINT`/`INGEST` line appended to [`../../log.md`](../../log.md).

## Naming
Use short, dated, lowercase-hyphenated names so the id and file line up:
`documents/<source>-<year>-<topic>.<ext>` → e.g. `mckinsey-2023-genai-economic-potential.pdf`.

## Notes
- Keep documents to research/reference material — no secrets or credentials.
- Large binaries bloat the repo; prefer a saved `.md`/`.txt` extract plus the source URL in
  `registry.md` when the original is huge or paywalled.
