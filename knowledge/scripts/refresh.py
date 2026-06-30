#!/usr/bin/env python3
"""
Knowledge-base refresh — free-Gemini edition.

Runs the "refresh / verify" half of the LLM Wiki lint pass (see knowledge/CLAUDE.md §4)
using the free Google Gemini API with Google Search grounding. For every source still
marked `status: seeded` with a `_pending_` url in knowledge/sources/registry.md, it asks
Gemini to find the authoritative primary URL and confirm the figure, then:

  * confirmed + url found  -> status: verified, url filled
  * found but figure differs -> status: contested, url filled
  * nothing credible found  -> left seeded (counted as unresolved)

It then propagates each source's new status into the verification column of any
knowledge/wiki/benchmarks.md row that cites that source id, and appends one LINT line to
knowledge/log.md. Edits are committed by the workflow's PR step, not here.

Stdlib only (urllib) — no pip install needed. Env:
  GEMINI_API_KEY  (required)   free key from https://aistudio.google.com/apikey
  GEMINI_MODEL    (optional)   default gemini-2.0-flash
  SCOPE           (optional)   informational only; recorded in the log line
"""
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # knowledge/
REGISTRY = os.path.join(ROOT, "sources", "registry.md")
BENCHMARKS = os.path.join(ROOT, "wiki", "benchmarks.md")
LOG = os.path.join(ROOT, "log.md")

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash").strip()
SCOPE = os.environ.get("SCOPE", "all").strip() or "all"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{MODEL}:generateContent?key={API_KEY}"
)


def gemini_verify(source, finding, date):
    """Ask Gemini (with Search grounding) to verify one citation. Returns a dict."""
    prompt = (
        "You are verifying a research citation used in a contact-center AI value model. "
        "Only Gartner, McKinsey, and Forrester count as authoritative for benchmarks.\n\n"
        f"Claim: \"{finding}\"\n"
        f"Attributed to: {source} (approx date: {date})\n\n"
        "Using web search, find the single most authoritative primary/official URL for this "
        "claim and judge whether the figure is essentially confirmed by that source.\n"
        "Respond with ONLY compact JSON, no prose, no code fences:\n"
        '{"found": true|false, "url": "<best url or empty>", '
        '"confirmed": true|false, "published": "YYYY-MM or empty", "note": "<=15 words"}'
    )
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"google_search": {}}],
        "generationConfig": {"temperature": 0.0},
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    text = "".join(p.get("text", "") for p in parts).strip()
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        raise ValueError(f"no JSON in model reply: {text[:160]!r}")
    return json.loads(m.group(0))


def parse_registry_rows(lines):
    """Yield (index, cells) for data rows of the source table (id starts with 'src-')."""
    for i, ln in enumerate(lines):
        if ln.strip().startswith("| src-"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) == 7:
                yield i, cells


def main():
    if not API_KEY:
        sys.exit("ERROR: GEMINI_API_KEY is not set. Add it as a repo secret "
                 "(get a free key at https://aistudio.google.com/apikey).")

    with open(REGISTRY, encoding="utf-8") as f:
        reg_lines = f.read().splitlines()

    verified, contested, unresolved, errors = [], [], [], []
    status_by_id = {}

    for idx, cells in parse_registry_rows(reg_lines):
        sid, source, finding, date, typ, url, status = cells
        if status != "seeded" or url not in ("_pending_", ""):
            continue  # only touch unverified rows
        try:
            r = gemini_verify(source, finding, date)
        except Exception as e:  # network / parse / quota — skip this row, keep going
            errors.append(f"{sid}: {e}")
            continue
        new_url = (r.get("url") or "").strip() or "_pending_"
        if r.get("found") and r.get("confirmed") and new_url != "_pending_":
            status, verified, status_by_id[sid] = "verified", verified + [sid], "verified"
        elif r.get("found") and new_url != "_pending_":
            status, contested, status_by_id[sid] = "contested", contested + [sid], "contested"
        else:
            unresolved.append(sid)
            time.sleep(1.5)
            continue
        cells[5], cells[6] = new_url, status
        reg_lines[idx] = "| " + " | ".join(cells) + " |"
        time.sleep(1.5)  # stay under free-tier RPM

    if status_by_id:
        with open(REGISTRY, "w", encoding="utf-8") as f:
            f.write("\n".join(reg_lines) + "\n")

        # Propagate status into benchmarks.md verification column for rows citing the source.
        with open(BENCHMARKS, encoding="utf-8") as f:
            bench = f.read().splitlines()
        for i, ln in enumerate(bench):
            if not ln.strip().startswith("|") or "pending" not in ln:
                continue
            for sid, st in status_by_id.items():
                if f"[{sid}]" in ln:
                    bench[i] = re.sub(r"\bpending\b", st, ln, count=1)
                    break
        with open(BENCHMARKS, "w", encoding="utf-8") as f:
            f.write("\n".join(bench) + "\n")

    # Append one LINT line to the log.
    note = f"Gemini ({MODEL}) source-verification pass"
    if errors:
        note += f"; {len(errors)} API/parse errors"
    log_line = (f"{TODAY} | LINT | scope={SCOPE} | "
                f"verified={len(verified)} contested={len(contested)} "
                f"unresolved={len(unresolved)} | {note}\n")
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(log_line)

    print(log_line.strip())
    if verified:
        print("  verified:", ", ".join(verified))
    if contested:
        print("  contested:", ", ".join(contested))
    if errors:
        print("  errors:", "; ".join(errors))
    # Success even if nothing changed — the PR step simply finds no diff.


if __name__ == "__main__":
    main()
