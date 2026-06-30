#!/usr/bin/env python3
"""
Auto-research engine — knowledge-base maintenance pass.

A config-driven, stdlib-only pass over the LLM Wiki in knowledge/ (see CLAUDE.md §4).
Driven by knowledge/topic.json, it runs four beats each cycle:

  1. LINT       — deterministic audit: stale claims (past the freshness window),
                  orphan pages (no inbound links), and gaps (seeded/pending sources,
                  unverified benchmark rows). Pure Python, no API needed.
  2. VERIFY     — for each seeded source, Gemini (with Google Search grounding) finds the
                  primary URL and confirms the figure...
  3. CROSS-CHECK— ...then a second, adversarial Gemini call tries to REFUTE it. A claim is
                  only `verified` if confirmed AND not refuted; otherwise `contested`.
  4. DISCOVER   — runs the topic's discovery queries to find NEW publications from the
                  sanctioned sources, dedupes against what's already known, and files
                  genuinely new candidates into knowledge/sources/inbox.md for an agent
                  to compile into wiki pages. This is what makes the wiki compound.

Finally it writes a human-readable knowledge/DIGEST.md ("what's new / changed / re-check")
and appends one LINT line to knowledge/log.md. Edits are committed by the workflow's PR step.

Env:
  GEMINI_API_KEY  free key from https://aistudio.google.com/apikey (required unless DRY_RUN)
  GEMINI_MODEL    default gemini-2.0-flash
  DRY_RUN         "1" to run LINT + DIGEST only (no API calls) — used for CI smoke tests
  SCOPE           informational; recorded in the log line
"""
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone, date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # knowledge/
TOPIC = os.path.join(ROOT, "topic.json")
REGISTRY = os.path.join(ROOT, "sources", "registry.md")
INBOX = os.path.join(ROOT, "sources", "inbox.md")
BENCHMARKS = os.path.join(ROOT, "wiki", "benchmarks.md")
WIKI = os.path.join(ROOT, "wiki")
LOG = os.path.join(ROOT, "log.md")
DIGEST = os.path.join(ROOT, "DIGEST.md")

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash").strip()
DRY_RUN = os.environ.get("DRY_RUN", "").strip() in ("1", "true", "yes")
SCOPE = os.environ.get("SCOPE", "all").strip() or "all"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
ENDPOINT = ("https://generativelanguage.googleapis.com/v1beta/models/"
            f"{MODEL}:generateContent?key={API_KEY}")


# ---------------------------------------------------------------- Gemini helpers
def gemini(prompt, search=True):
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.0}}
    if search:
        body["tools"] = [{"google_search": {}}]
    req = urllib.request.Request(ENDPOINT, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=90) as r:
        data = json.loads(r.read().decode())
    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    return "".join(p.get("text", "") for p in parts).strip()


def gemini_json(prompt, search=True):
    txt = gemini(prompt, search=search)
    m = re.search(r"\{.*\}|\[.*\]", txt, re.DOTALL)
    if not m:
        raise ValueError(f"no JSON in reply: {txt[:160]!r}")
    return json.loads(m.group(0))


# ---------------------------------------------------------------- markdown utils
def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def front_matter(text):
    """Parse a leading --- ... --- block into a dict (minimal, not full YAML)."""
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    fm = {}
    if not m:
        return fm
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
        fm[k.strip()] = v
    return fm


def wiki_files():
    out = []
    for dp, _, fns in os.walk(WIKI):
        for fn in fns:
            if fn.endswith(".md"):
                out.append(os.path.join(dp, fn))
    return out


def registry_rows(lines):
    for i, ln in enumerate(lines):
        if ln.strip().startswith("| src-"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) == 7:
                yield i, cells


# ---------------------------------------------------------------- 1. LINT
def lint(cfg):
    fresh = int(cfg.get("freshness_days", 180))
    stale, orphans, gaps = [], [], []

    files = wiki_files()
    targets = set()       # internal link targets that exist
    rel = {f: os.path.relpath(f, WIKI) for f in files}
    for f in files:
        d = os.path.dirname(f)
        for m in re.finditer(r"\]\((\.{1,2}/[^)#]+)", read(f)):
            tgt = os.path.normpath(os.path.join(d, m.group(1)))
            targets.add(tgt)
    # also count links from index.md / log.md (entry points)
    for entry in (os.path.join(ROOT, "index.md"), LOG):
        if os.path.exists(entry):
            d = os.path.dirname(entry)
            for m in re.finditer(r"\]\((\.{1,2}/[^)#]+|wiki/[^)#]+)", read(entry)):
                targets.add(os.path.normpath(os.path.join(d, m.group(1))))

    for f in files:
        fm = front_matter(read(f))
        # stale by updated date
        up = fm.get("updated", "")
        if re.match(r"\d{4}-\d{2}-\d{2}", str(up)):
            try:
                age = (date.fromisoformat(up) - date.today()).days * -1
                if age > fresh:
                    stale.append(f"{rel[f]} (updated {up}, {age}d old)")
            except ValueError:
                pass
        # orphan: not a link target from anywhere, and not benchmarks (a hub)
        if f not in targets and os.path.basename(f) != "benchmarks.md":
            orphans.append(rel[f])

    # gaps: sources still awaiting verification (seeded/pending) — superseded/contested
    # rows are intentional end-states, not gaps.
    for _, c in registry_rows(read(REGISTRY).splitlines()):
        if c[6] in ("seeded", "pending"):
            gaps.append(f"source {c[0]} — status {c[6]}, url {c[5]}")
    for ln in read(BENCHMARKS).splitlines():
        if ln.strip().startswith("|") and re.search(r"\b(pending|seeded)\b", ln):
            cells = [x.strip() for x in ln.strip().strip("|").split("|")]
            if cells and cells[0] and cells[0].lower() not in ("metric", "assumption", ":---", "---"):
                gaps.append(f"benchmark '{cells[0][:48]}' unverified")
    return {"stale": stale, "orphans": orphans, "gaps": gaps}


# ---------------------------------------------------------------- 2+3. VERIFY + CROSS-CHECK
def verify_one(cfg, source, finding, date_s):
    allow = ", ".join(cfg["sanctioned_sources"])
    confirm = gemini_json(
        f"Verify a research citation for: {cfg['name']}. Authoritative sources: {allow}.\n"
        f'Claim: "{finding}"\nAttributed to: {source} (approx {date_s})\n'
        "Find the single most authoritative primary URL and judge whether the figure is "
        "essentially confirmed. Reply ONLY compact JSON: "
        '{"found":bool,"url":"","confirmed":bool,"published":"YYYY-MM or empty","note":"<=15 words"}')
    res = {"found": bool(confirm.get("found")), "url": (confirm.get("url") or "").strip(),
           "confirmed": bool(confirm.get("confirmed")), "published": confirm.get("published", ""),
           "refuted": False, "note": confirm.get("note", "")}
    # adversarial cross-check only if the first pass confirmed it
    if res["confirmed"] and res["url"]:
        time.sleep(1.2)
        ref = gemini_json(
            f'Adversarially fact-check this claim attributed to {source}: "{finding}". '
            "Search for any evidence it is FALSE, outdated, superseded, or misattributed. "
            "Default to refuted=true if you find a credible conflicting figure or it cannot be "
            'stood up. Reply ONLY compact JSON: {"refuted":bool,"note":"<=15 words"}')
        res["refuted"] = bool(ref.get("refuted"))
        if res["refuted"]:
            res["note"] = (res["note"] + " | refute: " + str(ref.get("note", ""))).strip(" |")
    return res


def verify(cfg):
    lines = read(REGISTRY).splitlines()
    verified, contested = [], []
    status_by_id = {}
    for idx, c in registry_rows(lines):
        sid, source, finding, date_s, typ, url, status = c
        if status != "seeded" or url not in ("_pending_", ""):
            continue
        try:
            r = verify_one(cfg, source, finding, date_s)
        except Exception as e:
            print(f"  verify error {sid}: {e}")
            continue
        new_url = r["url"] or "_pending_"
        if r["found"] and r["confirmed"] and not r["refuted"] and new_url != "_pending_":
            status, status_by_id[sid] = "verified", "verified"; verified.append(sid)
        elif r["found"] and new_url != "_pending_":
            status, status_by_id[sid] = "contested", "contested"; contested.append(f"{sid} ({r['note']})")
        else:
            time.sleep(1.2); continue
        c[5], c[6] = new_url, status
        lines[idx] = "| " + " | ".join(c) + " |"
        time.sleep(1.2)
    if status_by_id:
        with open(REGISTRY, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        b = read(BENCHMARKS).splitlines()
        for i, ln in enumerate(b):
            if ln.strip().startswith("|") and "pending" in ln:
                for sid, st in status_by_id.items():
                    if f"[{sid}]" in ln:
                        b[i] = re.sub(r"\bpending\b", st, ln, count=1); break
        with open(BENCHMARKS, "w", encoding="utf-8") as f:
            f.write("\n".join(b) + "\n")
    return {"verified": verified, "contested": contested}


# ---------------------------------------------------------------- 4. DISCOVER
def known_urls():
    urls = set()
    for ln in read(REGISTRY).splitlines():
        for m in re.finditer(r"https?://[^\s|]+", ln):
            urls.add(m.group(0).rstrip("/"))
    if os.path.exists(INBOX):
        for m in re.finditer(r"https?://[^\s|)]+", read(INBOX)):
            urls.add(m.group(0).rstrip("/"))
    return urls


def discover(cfg, cap=8):
    allow = ", ".join(cfg["sanctioned_sources"])
    seen = known_urls()
    found = []
    for q in cfg.get("discovery_queries", []):
        try:
            items = gemini_json(
                f"Topic: {cfg['name']}. Only these sources count: {allow}.\n"
                f'Search the web for RECENT (last ~12 months) publications matching: "{q}". '
                "Return ONLY a compact JSON array of up to 3 NEW findings, each: "
                '{"claim":"<=25 words","source":"Gartner|McKinsey|Forrester","url":"","date":"YYYY-MM"}. '
                "Only include items from the allowed sources with a real URL.")
        except Exception as e:
            print(f"  discover error: {e}")
            continue
        for it in (items if isinstance(items, list) else []):
            url = (it.get("url") or "").strip().rstrip("/")
            src = (it.get("source") or "").strip()
            if not url or url in seen:
                continue
            if not any(s.lower() in src.lower() for s in cfg["sanctioned_sources"]):
                continue
            seen.add(url)
            found.append({"claim": (it.get("claim") or "").strip(), "source": src,
                          "url": url, "date": (it.get("date") or "").strip()})
            if len(found) >= cap:
                break
        time.sleep(1.2)
        if len(found) >= cap:
            break
    if found:
        head = "" if os.path.exists(INBOX) else (
            "# Discovery inbox\n\nNew candidate sources surfaced by the auto-research "
            "discovery beat (see CLAUDE.md §4). Each row is raw capture awaiting compilation "
            "into a wiki page + a registry id by the next agent ingest pass.\n\n"
            "| found | source | candidate finding | date | url |\n|---|---|---|---|---|\n")
        with open(INBOX, "a", encoding="utf-8") as f:
            if head:
                f.write(head)
            for it in found:
                f.write(f"| {TODAY} | {it['source']} | {it['claim']} | {it['date']} | {it['url']} |\n")
    return found


# ---------------------------------------------------------------- DIGEST + log
def write_digest(cfg, L, V, D):
    def block(title, items, empty="— none"):
        body = "\n".join(f"- {x}" for x in items) if items else empty
        return f"### {title}\n{body}\n"
    out = (f"# Knowledge-base digest — {TODAY}\n\n"
           f"_Topic: **{cfg['name']}**. Auto-generated by the {MODEL} research pass"
           f"{' (DRY RUN — lint only)' if DRY_RUN else ''}._\n\n"
           "## What's new\n"
           + block("Discovered (filed to sources/inbox.md)",
                   [f"{d['source']}: {d['claim']} — {d['url']}" for d in D["discovered"]]) +
           "\n## What changed\n"
           + block("Newly verified", V["verified"])
           + block("Now contested", V["contested"]) +
           "\n## What to re-check\n"
           + block("Stale (past freshness window)", L["stale"])
           + block("Orphan pages (no inbound links)", L["orphans"])
           + block("Gaps (unverified sources / benchmarks)", L["gaps"][:20]
                   + ([f"...and {len(L['gaps'])-20} more"] if len(L["gaps"]) > 20 else [])))
    with open(DIGEST, "w", encoding="utf-8") as f:
        f.write(out)


def main():
    cfg = json.loads(read(TOPIC))
    if not API_KEY and not DRY_RUN:
        sys.exit("ERROR: GEMINI_API_KEY not set (free key: https://aistudio.google.com/apikey). "
                 "Or set DRY_RUN=1 for a lint-only pass.")
    print(f"topic: {cfg['name']} | model: {MODEL} | dry_run: {DRY_RUN}")

    L = lint(cfg)
    print(f"lint: stale={len(L['stale'])} orphans={len(L['orphans'])} gaps={len(L['gaps'])}")

    V = {"verified": [], "contested": []}
    D = {"discovered": []}
    if not DRY_RUN:
        V = verify(cfg)
        print(f"verify: verified={len(V['verified'])} contested={len(V['contested'])}")
        D = {"discovered": discover(cfg)}
        print(f"discover: new={len(D['discovered'])}")

    write_digest(cfg, L, V, D)
    line = (f"{TODAY} | LINT   | scope={SCOPE} | "
            f"verified={len(V['verified'])} contested={len(V['contested'])} "
            f"discovered={len(D['discovered'])} stale={len(L['stale'])} "
            f"orphans={len(L['orphans'])} gaps={len(L['gaps'])} | "
            f"{MODEL} research pass{' (dry-run)' if DRY_RUN else ''}\n")
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line)
    print(line.strip())


if __name__ == "__main__":
    main()
