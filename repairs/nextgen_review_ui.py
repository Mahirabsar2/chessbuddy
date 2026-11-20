from pathlib import Path

p = Path("app/src/main/assets/js/app.js")
s = p.read_text(encoding="utf-8")
old = """    $('modalCard').innerHTML = '<div class="rv-top">' + coachAv(co) + '<div class="rv-say">' + esc(say) + '</div></div>' +
      '<div class="rv-accs">' + ['w', 'b'].map(c => '<div class="rv-acc"><b>' + s[c].accuracy + '</b><span>' + esc(labelOf(c)) + '<br>accuracy · est. ' + (s[c].rating || '–') + '</span></div>').join('') + '</div>' +
      reviewGraph(r) + (r.opening ? '<p class="muted center">Opening: <b>' + esc(r.opening) + '</b></p>' : '') + '<table class="rv-tbl">' + rows + '</table>' +
      '<div class="controls"><button class="btn primary" id="rvStart" type="button"><span data-ic="play"></span> Start review</button><button class="btn" id="rvExplain" type="button"><span data-ic="spark"></span> Explain with ' + esc(co.name) + '</button><button class="btn" id="rvClose" type="button"><span data-ic="exit"></span> Close</button></div>';
"""
new = """    $('modalCard').innerHTML = '<div class="rv-summary-head"><div><div class="rv-kicker">GAME REVIEW</div><h3>Review Summary</h3></div><button class="btn rv-close" id="rvClose" type="button" aria-label="Close review summary" title="Close"><span data-ic="exit"></span><span>Close</span></button></div>' +
      '<div class="rv-top">' + coachAv(co) + '<div class="rv-say">' + esc(say) + '</div></div>' +
      '<div class="rv-accs">' + ['w', 'b'].map(c => '<div class="rv-acc"><b>' + s[c].accuracy + '</b><span>' + esc(labelOf(c)) + '<br>Accuracy · Est. ' + (s[c].rating || '–') + '</span></div>').join('') + '</div>' +
      reviewGraph(r) + (r.opening ? '<p class="muted center rv-opening">Opening: <b>' + esc(r.opening) + '</b></p>' : '') + '<table class="rv-tbl"><thead><tr><th scope="col">Move Classification</th><th scope="col">' + esc(labelOf('w')) + '</th><th scope="col">' + esc(labelOf('b')) + '</th></tr></thead><tbody>' + rows + '</tbody></table>' +
      '<div class="rv-summary-actions"><button class="btn primary rv-action" id="rvStart" type="button"><span class="rv-action-icon" data-ic="play"></span><span>Start Review</span></button><button class="btn rv-action" id="rvExplain" type="button"><span class="rv-action-icon" data-ic="spark"></span><span>Explain with ' + esc(co.name) + '</span></button></div>';
"""
if new not in s:
    if old not in s:
        raise SystemExit("Expected Game Review summary markup not found.")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")

css = """
/* Next Gen: responsive Game Review summary and predictable icon sizing */
.sheet.full {
  height: 94vh;
  max-height: 94vh;
  max-height: calc(100dvh - env(safe-area-inset-top, 0px));
  min-height: 0;
  padding: 14px 14px calc(18px + env(safe-area-inset-bottom, 0px));
  overflow-x: hidden;
  overscroll-behavior: contain;
}
.sheet.full > * { min-width: 0; }
.rv-summary-head {
  display:flex; align-items:center; justify-content:space-between;
  gap:12px; min-height:42px; margin:0 0 10px;
}
.rv-summary-head h3 { margin:0; font-size:18px; line-height:1.2; }
.rv-kicker { color:var(--muted); font-size:10px; font-weight:900; letter-spacing:1.2px; margin-bottom:3px; }
.rv-close {
  flex:none; min-width:76px; min-height:38px; height:38px; padding:0 10px;
  display:inline-flex; align-items:center; justify-content:center; gap:6px; font-size:12px;
}
.rv-close svg { width:17px; height:17px; flex:none; }
.rv-top { min-width:0; }
.rv-say { min-width:0; overflow-wrap:anywhere; }
.rv-accs { grid-template-columns:repeat(2,minmax(0,1fr)); }
.rv-acc { min-width:0; padding:10px 8px; }
.rv-acc b { font-size:clamp(22px,6vw,27px); line-height:1.15; }
.rv-acc span { overflow-wrap:anywhere; }
.rv-graph { width:100%; height:clamp(62px,18vw,86px); }
.rv-tbl { width:100%; table-layout:fixed; border-collapse:collapse; margin:8px 0 14px; }
.rv-tbl th {
  color:var(--muted); font-size:10px; font-weight:800; letter-spacing:.35px;
  text-transform:uppercase; text-align:center; padding:5px 3px; border-bottom:1px solid var(--line);
}
.rv-tbl th:first-child { text-align:left; }
.rv-tbl th:nth-child(2),.rv-tbl th:nth-child(3) { width:48px; }
.rv-tbl td { padding:6px 3px; border-bottom:1px solid var(--line); font-size:13px; line-height:1.25; vertical-align:middle; overflow-wrap:anywhere; }
.rv-tbl td:first-child { padding-right:6px; }
.rv-tbl td:nth-child(2),.rv-tbl td:nth-child(3) { width:48px; text-align:center; font-weight:800; font-variant-numeric:tabular-nums; }
.rv-tbl .rv-dot { width:22px; min-width:22px; height:22px; margin-right:6px; vertical-align:middle; }
.rv-tbl .rv-grade-icon { width:14px; height:14px; }
.rv-opening { overflow-wrap:anywhere; margin:8px 0; }
.rv-summary-actions { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:9px; margin:12px 0 4px; }
.rv-action {
  display:flex; align-items:center; justify-content:center; gap:8px;
  min-width:0; min-height:50px; height:auto; padding:9px 10px;
  font-size:clamp(11px,3.35vw,13px); line-height:1.2; text-align:center; overflow-wrap:anywhere;
}
.rv-action > span:last-child { min-width:0; }
.rv-action-icon { display:inline-flex; align-items:center; justify-content:center; flex:none; width:20px; height:20px; }
.rv-action-icon svg { display:block; width:20px; height:20px; max-width:20px; max-height:20px; }
.controls > .btn { min-width:0; max-width:100%; overflow-wrap:anywhere; }
@media (max-width:380px) {
  .sheet.full { padding-left:11px; padding-right:11px; }
  .rv-top { gap:8px; }
  .rv-top .avatar { width:44px; height:44px; }
  .rv-say { padding:9px 10px; font-size:13px; }
  .rv-tbl td { font-size:12px; }
  .rv-tbl th:nth-child(2),.rv-tbl th:nth-child(3),
  .rv-tbl td:nth-child(2),.rv-tbl td:nth-child(3) { width:42px; }
  .rv-action { gap:6px; padding:8px 6px; }
  .rv-action-icon,.rv-action-icon svg { width:18px; height:18px; max-width:18px; max-height:18px; }
}
@media (max-height:620px) {
  .sheet.full { height:96vh; max-height:96vh; max-height:calc(100dvh - env(safe-area-inset-top,0px)); }
  .rv-top { margin-bottom:7px; }
  .rv-accs { margin:7px 0; }
  .rv-graph { height:58px; }
  .rv-tbl { margin:5px 0 8px; }
  .rv-tbl td { padding:4px 3px; }
}
"""
p = Path("app/src/main/assets/css/app.css")
s = p.read_text(encoding="utf-8")
marker = "/* Next Gen: responsive Game Review summary and predictable icon sizing */"
if marker not in s:
    p.write_text(s + "\n" + css + "\n", encoding="utf-8")
print("Responsive Game Review UI patch applied.")
