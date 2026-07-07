#!/usr/bin/env python3
"""
Build dashboard.html from the knowledge base.

Reads the wiki's markdown (topic.json, sources/registry.md, wiki/benchmarks.md, log.md) and
emits a single self-contained dashboard.html at the repo root: a knowledge-base **overview**
(source verification status, benchmark ledger, the ABL-vs-pure-LLM cost divergence) plus a
no-backend document **intake** panel that turns a pasted document/URL into a ready-to-commit
`sources/documents/` file + `registry.md` row, with a deep-link to GitHub's upload UI.

Stdlib only. Run: python knowledge/scripts/build_dashboard.py
Env: REPO_SLUG (default Anurag160596/Auto-research) for the GitHub deep-links.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # knowledge/
REPO = os.path.dirname(ROOT)                                        # repo root
TOPIC = os.path.join(ROOT, "topic.json")
REGISTRY = os.path.join(ROOT, "sources", "registry.md")
BENCHMARKS = os.path.join(ROOT, "wiki", "benchmarks.md")
LOG = os.path.join(ROOT, "log.md")
OUT = os.path.join(REPO, "dashboard.html")
SLUG = os.environ.get("REPO_SLUG", "Anurag160596/Auto-research").strip("/")
STATUSES = ("verified", "contested", "seeded", "pending", "superseded")


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def rows(text, prefix=None, ncells=None):
    for ln in text.splitlines():
        s = ln.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if prefix and not (cells and cells[0].startswith(prefix)):
            continue
        if ncells and len(cells) != ncells:
            continue
        yield cells


def parse_sources():
    out = []
    for c in rows(read(REGISTRY), prefix="src-", ncells=7):
        out.append({"id": c[0], "source": c[1], "finding": c[2], "date": c[3],
                    "type": c[4], "url": c[5] if c[5].startswith("http") else "",
                    "status": c[6]})
    return out


def parse_benchmarks():
    out = []
    for c in rows(read(BENCHMARKS), ncells=6):
        ver = c[5].lower()
        if not any(st in ver for st in STATUSES):
            continue
        st = next(st for st in STATUSES if st in ver)
        out.append({"metric": re.sub(r"[*~`]", "", c[0]), "value": re.sub(r"[*~`]", "", c[1]),
                    "source": re.sub(r"\[[^\]]*\]|[⚠]", "", c[2]).strip(),
                    "date": c[3], "confidence": c[4], "status": st})
    return out


def last_pass():
    for ln in reversed(read(LOG).splitlines()):
        if "| LINT" in ln or "| INGEST" in ln:
            m = re.match(r"(\d{4}-\d{2}-\d{2})", ln.strip())
            return m.group(1) if m else "—"
    return "—"


def main():
    topic = json.loads(read(TOPIC))
    srcs = parse_sources()
    bench = parse_benchmarks()
    counts = {s: sum(1 for x in srcs if x["status"] == s) for s in STATUSES}
    data = {
        "topic": topic.get("name", "Knowledge base"),
        "repo": SLUG,
        "lastPass": last_pass(),
        "counts": counts,
        "nSources": len(srcs),
        "nBench": len(bench),
        "nVerified": sum(1 for b in bench if b["status"] == "verified"),
        "sources": srcs,
        "benchmarks": bench,
        # ABL-vs-pure-LLM cost/resolution divergence (illustrative, per the value thesis):
        # ABL stays near the ~$0.20 deterministic floor; pure-LLM rises past Gartner's >$3 by 2030.
        "chart": {
            "years": [2024, 2025, 2026, 2027, 2028, 2029, 2030],
            "abl":   [0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28],
            "rival": [0.90, 1.15, 1.45, 1.85, 2.30, 2.75, 3.20],
            "threshold": 3.0,
        },
    }
    html = TEMPLATE.replace("/*__DATA__*/0", json.dumps(data))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"wrote {OUT} ({len(html)} bytes) — {len(srcs)} sources, {len(bench)} benchmarks")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<title>Auto-research — Knowledge Base Dashboard</title>
<style>
  :root{
    --bg:#0a0f1f;--bg2:#0e1526;--card:#121b30;--card2:#0f1728;--ink:#e8eefc;--ink2:#b7c3de;
    --muted:#8595b6;--faint:#5f6f92;--line:#1e2a45;--line2:#172238;
    --teal:#2dd4bf;--amber:#f59e0b;--grey:#94a3b8;--blue:#5b8def;
    --good:#2dd4bf;--warn:#f59e0b;--bad:#f87171;--seed:#8595b6;
    --mono:'SFMono-Regular',ui-monospace,'JetBrains Mono',Menlo,Consolas,monospace;
    --sans:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;
  }
  *{box-sizing:border-box}
  body{margin:0;background:
     radial-gradient(1100px 500px at 90% -10%,rgba(45,212,191,.06),transparent 60%),
     radial-gradient(900px 500px at -10% 0%,rgba(91,141,239,.07),transparent 55%),var(--bg);
     color:var(--ink);font-family:var(--sans);-webkit-font-smoothing:antialiased}
  .mono{font-family:var(--mono);font-variant-numeric:tabular-nums}
  a{color:var(--teal);text-decoration:none} a:hover{text-decoration:underline}
  .wrap{max-width:1180px;margin:0 auto;padding:22px 20px 90px}
  header.top{display:flex;align-items:center;gap:13px;flex-wrap:wrap;border-bottom:1px solid var(--line);padding-bottom:16px}
  .mark{width:34px;height:34px;border-radius:9px;background:linear-gradient(135deg,var(--teal),#0ea5a0);display:flex;align-items:center;justify-content:center;color:#04231f;font-weight:900;font-size:18px}
  header h1{font-size:17px;margin:0;font-weight:800;letter-spacing:-.2px}
  header .sub{font-size:12px;color:var(--muted);margin-top:2px}
  header .sp{flex:1}
  .chip{font-size:11px;color:var(--ink2);background:var(--card);border:1px solid var(--line);border-radius:999px;padding:6px 12px}
  h2.sec{font-size:12px;text-transform:uppercase;letter-spacing:.7px;color:var(--muted);font-weight:700;margin:30px 0 14px;display:flex;align-items:center;gap:9px}
  h2.sec::after{content:"";flex:1;height:1px;background:var(--line)}
  /* KPI */
  .kpis{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-top:18px}
  .kpi{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px}
  .kpi .l{font-size:10px;text-transform:uppercase;letter-spacing:.6px;color:var(--muted);font-weight:700}
  .kpi .v{font-size:26px;font-weight:820;margin-top:6px;letter-spacing:-.5px}
  .kpi.g .v{color:var(--teal)} .kpi.w .v{color:var(--amber)} .kpi.s .v{color:var(--grey)}
  /* card + chart */
  .card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px}
  canvas{display:block;width:100%}
  .legend{display:flex;gap:16px;flex-wrap:wrap;margin-top:12px;font-size:12px;color:var(--ink2)}
  .legend i{display:inline-block;width:20px;height:3px;border-radius:2px;margin-right:7px;vertical-align:3px}
  .note{font-size:11px;color:var(--faint);margin-top:10px;line-height:1.6}
  /* tables */
  .tbl{overflow-x:auto} table{width:100%;border-collapse:collapse;font-size:12.5px;min-width:560px}
  th,td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line2);vertical-align:top}
  thead th{color:var(--muted);font-weight:600;font-size:10px;text-transform:uppercase;letter-spacing:.5px}
  tbody tr:hover td{background:var(--card2)}
  td.r,th.r{text-align:right}
  .pill{display:inline-flex;align-items:center;gap:5px;font-size:10.5px;font-weight:700;padding:3px 9px;border-radius:999px;text-transform:uppercase;letter-spacing:.3px;white-space:nowrap}
  .pill::before{content:"";width:6px;height:6px;border-radius:50%;background:currentColor}
  .pill.verified{color:var(--good);background:rgba(45,212,191,.12)}
  .pill.contested{color:var(--bad);background:rgba(248,113,113,.12)}
  .pill.seeded,.pill.pending{color:var(--seed);background:rgba(133,149,182,.14)}
  .pill.superseded{color:var(--faint);background:rgba(95,111,146,.14)}
  .conf{font-size:10px;color:var(--faint);text-transform:uppercase;letter-spacing:.4px}
  /* intake */
  .intake{display:grid;grid-template-columns:1fr 1fr;gap:18px}
  .drop{border:1.5px dashed var(--line);border-radius:12px;padding:16px;background:var(--card2);transition:.15s}
  .drop.drag{border-color:var(--teal);background:rgba(45,212,191,.06)}
  .fld{margin-bottom:11px} .fld label{display:block;font-size:11px;color:var(--muted);font-weight:600;margin-bottom:5px}
  .fld input,.fld select,.fld textarea{width:100%;background:var(--bg2);border:1px solid var(--line);border-radius:9px;color:var(--ink);
    padding:9px 11px;font-size:13px;font-family:var(--sans)}
  .fld textarea{min-height:78px;resize:vertical;font-family:var(--mono);font-size:12px}
  .fld input:focus,.fld select:focus,.fld textarea:focus{outline:none;border-color:var(--teal)}
  .btn{appearance:none;border:none;border-radius:10px;padding:10px 15px;font-size:13px;font-weight:750;cursor:pointer;transition:.15s}
  .btn.primary{background:var(--teal);color:#04231f} .btn.primary:hover{filter:brightness(1.08)}
  .btn.ghost{background:transparent;border:1px solid var(--line);color:var(--ink2)} .btn.ghost:hover{border-color:var(--teal);color:var(--ink)}
  .out{margin-top:10px} .out label{display:flex;justify-content:space-between;align-items:center;font-size:11px;color:var(--muted);font-weight:600;margin-bottom:5px}
  .out textarea{width:100%;background:var(--bg2);border:1px solid var(--line);border-radius:9px;color:var(--ink2);padding:10px;font-family:var(--mono);font-size:11.5px;min-height:70px}
  .copy{font-size:10.5px;color:var(--teal);cursor:pointer;font-weight:700;background:none;border:none}
  .steps{font-size:12px;color:var(--ink2);line-height:1.7;padding-left:18px;margin:2px 0}
  .steps code{background:var(--bg2);border:1px solid var(--line);border-radius:5px;padding:1px 5px;font-size:11px}
  .ghlink{display:inline-flex;align-items:center;gap:7px;margin:4px 8px 4px 0;background:var(--card);border:1px solid var(--line);border-radius:9px;padding:8px 13px;font-size:12.5px;font-weight:700;color:var(--ink);cursor:pointer}
  .ghlink:hover{border-color:var(--teal);text-decoration:none}
  footer{margin-top:34px;font-size:11px;color:var(--faint);line-height:1.7;border-top:1px solid var(--line);padding-top:14px}
  .toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%) translateY(18px);background:#04231f;color:var(--teal);border:1px solid var(--teal);
    padding:10px 17px;border-radius:11px;font-size:13px;font-weight:700;opacity:0;pointer-events:none;transition:.25s;z-index:60}
  .toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
  @media(max-width:820px){.kpis{grid-template-columns:repeat(2,1fr)}.intake{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <div class="mark">◆</div>
    <div><h1>Auto-research — Knowledge Base</h1><div class="sub" id="topicSub">—</div></div>
    <div class="sp"></div>
    <span class="chip">Last pass: <b id="lastPass" class="mono">—</b></span>
    <a class="chip" id="repoLink" target="_blank" rel="noopener">View repo ↗</a>
  </header>

  <div class="kpis" id="kpis"></div>

  <h2 class="sec">Cost per resolution — the divergence</h2>
  <div class="card">
    <canvas id="chart" height="300"></canvas>
    <div class="legend">
      <span><i style="background:var(--teal)"></i>ABL (deterministic) — flat near the platform floor</span>
      <span><i style="background:var(--amber)"></i>Pure-LLM rival — rising to &gt;$3 by 2030</span>
      <span><i style="background:var(--grey)"></i>Gartner $3 threshold (2030)</span>
    </div>
    <div class="note">Illustrative of the value thesis: ABL resolves routine work without an LLM call, so its cost/resolution stays near the ~$0.20 deterministic floor, while pure-LLM cost tracks Gartner's forecast of &gt;$3 per resolution by 2030. Benchmarks below are the sourced evidence.</div>
  </div>

  <h2 class="sec">Document intake — add a source</h2>
  <div class="card">
    <div class="intake">
      <div>
        <div class="drop" id="drop">
          <div class="fld"><label>Drop a text/markdown file here, or fill the fields</label></div>
          <div class="fld"><label>Source</label><select id="f_source"><option>Gartner</option><option>McKinsey</option><option>Forrester</option><option>Other</option></select></div>
          <div class="fld"><label>Key finding (one line)</label><input id="f_finding" placeholder="e.g. 80% of routine issues autonomously resolved by 2029"/></div>
          <div class="fld" style="display:flex;gap:10px">
            <div style="flex:1"><label>Date (YYYY-MM)</label><input id="f_date" placeholder="2026-01"/></div>
            <div style="flex:1"><label>Short slug</label><input id="f_slug" placeholder="cost-per-resolution"/></div>
          </div>
          <div class="fld"><label>Source URL (optional)</label><input id="f_url" placeholder="https://…"/></div>
          <div class="fld"><label>Document text / extract (optional)</label><textarea id="f_text" placeholder="Paste the article/report text or key quotes…"></textarea></div>
          <button class="btn primary" id="gen">Generate commit-ready entry</button>
        </div>
      </div>
      <div>
        <div class="out"><label>1 · Row for <code>sources/registry.md</code> <button class="copy" data-copy="o_row">copy</button></label><textarea id="o_row" readonly></textarea></div>
        <div class="out"><label>2 · File <code>sources/documents/<span id="o_fname">…</span></code> <button class="copy" data-copy="o_doc">copy</button></label><textarea id="o_doc" readonly></textarea></div>
        <div style="margin-top:12px">
          <div class="steps">Then, on GitHub:</div>
          <a class="ghlink" id="lnkUpload" target="_blank" rel="noopener">⬆ Upload file to documents/</a>
          <a class="ghlink" id="lnkRegistry" target="_blank" rel="noopener">✎ Paste the row into registry.md</a>
          <div class="note">No backend needed — the dashboard formats the entry; GitHub stores it. On the next ingest pass the engine compiles it into the wiki.</div>
        </div>
      </div>
    </div>
  </div>

  <h2 class="sec">Benchmark ledger <span id="benchCount" class="conf" style="text-transform:none"></span></h2>
  <div class="card tbl"><table id="benchTbl"><thead><tr><th>Metric</th><th class="r">Value</th><th>Source</th><th>Date</th><th>Conf.</th><th>Status</th></tr></thead><tbody></tbody></table></div>

  <h2 class="sec">Sources <span id="srcCount" class="conf" style="text-transform:none"></span></h2>
  <div class="card tbl"><table id="srcTbl"><thead><tr><th>ID</th><th>Source</th><th>Finding</th><th>Date</th><th>Status</th></tr></thead><tbody></tbody></table></div>

  <footer id="foot">—</footer>
</div>
<div class="toast" id="toast">Copied</div>

<script>
"use strict";
const DATA = /*__DATA__*/0;

/* ---------- header + KPIs ---------- */
document.getElementById('topicSub').textContent = DATA.topic + ' · self-maintaining LLM Wiki';
document.getElementById('lastPass').textContent = DATA.lastPass;
document.getElementById('repoLink').href = 'https://github.com/' + DATA.repo;
document.getElementById('benchCount').textContent = '· ' + DATA.nVerified + ' of ' + DATA.nBench + ' verified';
document.getElementById('srcCount').textContent = '· ' + DATA.nSources + ' total';
document.getElementById('foot').innerHTML = 'Generated from <code>knowledge/</code> by build_dashboard.py · ' +
  DATA.topic + ' · sources verified against Gartner / McKinsey / Forrester. Every figure links to its primary source in the registry.';
const K = DATA.counts;
document.getElementById('kpis').innerHTML = [
  ['g','Verified', K.verified],['w','Contested', K.contested],['s','Seeded', K.seeded],
  ['','Benchmarks', DATA.nBench],['','Sources', DATA.nSources]
].map(function(k){return '<div class="kpi '+k[0]+'"><div class="l">'+k[1]+'</div><div class="v mono">'+k[2]+'</div></div>';}).join('');

/* ---------- tables ---------- */
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function pill(s){return '<span class="pill '+s+'">'+s+'</span>';}
document.querySelector('#benchTbl tbody').innerHTML = DATA.benchmarks.map(function(b){
  return '<tr><td>'+esc(b.metric)+'</td><td class="r mono">'+esc(b.value)+'</td><td>'+esc(b.source)+
    '</td><td class="mono">'+esc(b.date)+'</td><td class="conf">'+esc(b.confidence)+'</td><td>'+pill(b.status)+'</td></tr>';}).join('');
document.querySelector('#srcTbl tbody').innerHTML = DATA.sources.map(function(s){
  var id = s.url ? '<a href="'+esc(s.url)+'" target="_blank" rel="noopener">'+esc(s.id)+'</a>' : esc(s.id);
  return '<tr><td class="mono">'+id+'</td><td>'+esc(s.source)+'</td><td>'+esc(s.finding)+
    '</td><td class="mono">'+esc(s.date)+'</td><td>'+pill(s.status)+'</td></tr>';}).join('');

/* ---------- divergence chart (canvas, no deps) ---------- */
var C = DATA.chart, cv = document.getElementById('chart'), ctx = cv.getContext('2d');
function css(v){return getComputedStyle(document.documentElement).getPropertyValue(v).trim();}
var hover = -1;
function draw(){
  var dpr = window.devicePixelRatio||1, w = cv.clientWidth, h = 300;
  cv.width = w*dpr; cv.height = h*dpr; cv.style.height = h+'px'; ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,w,h);
  var pL=46,pR=104,pT=16,pB=34, pw=w-pL-pR, ph=h-pT-pB, maxY=3.6;
  var xs=function(i){return pL + pw*i/(C.years.length-1);}, ys=function(v){return pT + ph*(1-v/maxY);};
  // gridlines + y labels
  ctx.font='11px '+css('--mono'); ctx.textBaseline='middle';
  for(var g=0;g<=4;g++){var v=maxY*g/4, y=ys(v);
    ctx.strokeStyle=css('--line2'); ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(pL,y); ctx.lineTo(w-pR,y); ctx.stroke();
    ctx.fillStyle=css('--faint'); ctx.textAlign='right'; ctx.fillText('$'+v.toFixed(1),pL-8,y);}
  // $3 threshold
  var ty=ys(C.threshold); ctx.strokeStyle=css('--grey'); ctx.setLineDash([5,4]); ctx.lineWidth=1.5;
  ctx.beginPath(); ctx.moveTo(pL,ty); ctx.lineTo(w-pR,ty); ctx.stroke(); ctx.setLineDash([]);
  ctx.fillStyle=css('--grey'); ctx.textAlign='left'; ctx.fillText('$3 by 2030',w-pR+8,ty);
  // x labels
  ctx.textAlign='center'; ctx.textBaseline='top'; ctx.fillStyle=css('--faint');
  C.years.forEach(function(yr,i){ctx.fillText(yr,xs(i),pT+ph+10);});
  // series
  function line(arr,color,label){
    ctx.strokeStyle=color; ctx.lineWidth=2.5; ctx.beginPath();
    arr.forEach(function(v,i){var x=xs(i),y=ys(v); i?ctx.lineTo(x,y):ctx.moveTo(x,y);}); ctx.stroke();
    var lx=xs(arr.length-1), ly=ys(arr[arr.length-1]);
    ctx.fillStyle=color; ctx.beginPath(); ctx.arc(lx,ly,4,0,7); ctx.fill();
    ctx.textAlign='left'; ctx.textBaseline='middle'; ctx.font='700 11px '+css('--sans');
    ctx.fillText(label,lx+9,ly + (label[0]==='A'?12:-2));
    ctx.font='11px '+css('--mono');
  }
  line(C.rival,css('--amber'),'Pure-LLM');
  line(C.abl,css('--teal'),'ABL');
  // hover
  if(hover>=0){var hx=xs(hover);
    ctx.strokeStyle=css('--line'); ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(hx,pT); ctx.lineTo(hx,pT+ph); ctx.stroke();
    [['ABL',C.abl[hover],css('--teal')],['Pure-LLM',C.rival[hover],css('--amber')]].forEach(function(d){
      var y=ys(d[1]); ctx.fillStyle=d[2]; ctx.beginPath(); ctx.arc(hx,y,4.5,0,7); ctx.fill();});
    var bx=Math.min(hx+10,w-pR-96), by=pT+6;
    ctx.fillStyle=css('--bg2'); ctx.strokeStyle=css('--line'); ctx.lineWidth=1;
    ctx.beginPath(); ctx.rect(bx,by,150,52); ctx.fill(); ctx.stroke();
    ctx.textAlign='left'; ctx.textBaseline='top'; ctx.fillStyle=css('--ink'); ctx.font='700 11px '+css('--sans');
    ctx.fillText(C.years[hover],bx+10,by+7);
    ctx.font='11px '+css('--mono');
    ctx.fillStyle=css('--teal'); ctx.fillText('ABL   $'+C.abl[hover].toFixed(2),bx+10,by+23);
    ctx.fillStyle=css('--amber'); ctx.fillText('Rival $'+C.rival[hover].toFixed(2),bx+10,by+37);
  }
}
cv.addEventListener('mousemove',function(e){
  var r=cv.getBoundingClientRect(), w=cv.clientWidth, pL=46,pR=104,pw=w-pL-pR;
  var i=Math.round((e.clientX-r.left-pL)/pw*(C.years.length-1));
  hover=(i>=0&&i<C.years.length)?i:-1; draw();});
cv.addEventListener('mouseleave',function(){hover=-1;draw();});
window.addEventListener('resize',draw); draw();

/* ---------- intake ---------- */
function slugify(s){return String(s).toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,40);}
function val(id){return document.getElementById(id).value.trim();}
function gen(){
  var src=val('f_source'), find=val('f_finding'), date=val('f_date')||'unknown',
      slug=val('f_slug')||slugify(find)||'source', url=val('f_url'), text=val('f_text');
  var id='src-'+slugify(src)+'-'+(date.replace(/[^0-9]/g,'').slice(0,6)||'x')+'-'+slug;
  var fname=id.replace(/^src-/,'')+'.md';
  var row='| '+id+' | '+src+' | '+(find||'—')+' | '+date+' | '+(/gartner|mckinsey|forrester/i.test(src)?'analyst':'other')+' | '+(url||'_pending_')+' | seeded |';
  var doc='# '+(find||slug)+'\n\n- **Source:** '+src+'\n- **Date:** '+date+'\n- **URL:** '+(url||'—')+'\n- **Registry id:** `'+id+'`\n\n---\n\n'+(text||'(paste the document text or key quotes here)')+'\n';
  document.getElementById('o_row').value=row;
  document.getElementById('o_doc').value=doc;
  document.getElementById('o_fname').textContent=fname;
  var base='https://github.com/'+DATA.repo;
  document.getElementById('lnkUpload').href=base+'/upload/main/knowledge/sources/documents';
  document.getElementById('lnkRegistry').href=base+'/edit/main/knowledge/sources/registry.md';
}
document.getElementById('gen').addEventListener('click',gen);
gen();
// drag-drop a text file into the notes box
var drop=document.getElementById('drop');
['dragover','dragenter'].forEach(function(ev){drop.addEventListener(ev,function(e){e.preventDefault();drop.classList.add('drag');});});
['dragleave','drop'].forEach(function(ev){drop.addEventListener(ev,function(e){e.preventDefault();drop.classList.remove('drag');});});
drop.addEventListener('drop',function(e){var f=e.dataTransfer.files[0]; if(!f)return;
  if(!val('f_slug')) document.getElementById('f_slug').value=slugify(f.name.replace(/\.[^.]+$/,''));
  if(/\.(txt|md|csv|json|html?)$/i.test(f.name)){var rd=new FileReader(); rd.onload=function(){document.getElementById('f_text').value=String(rd.result).slice(0,6000); gen();}; rd.readAsText(f);}
  else{document.getElementById('f_text').value='[binary file: '+f.name+'] — upload the file itself via the GitHub link below.'; gen();}});
// copy buttons
function toast(t){var el=document.getElementById('toast'); el.textContent=t; el.classList.add('show'); clearTimeout(el._t); el._t=setTimeout(function(){el.classList.remove('show');},1600);}
document.querySelectorAll('.copy').forEach(function(b){b.addEventListener('click',function(){
  var ta=document.getElementById(b.dataset.copy); ta.select();
  navigator.clipboard&&navigator.clipboard.writeText(ta.value).then(function(){toast('Copied ✓');},function(){document.execCommand('copy');toast('Copied ✓');});});});
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
