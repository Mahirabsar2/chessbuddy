from pathlib import Path

def edit(path, pairs):
    p = Path(path)
    source = p.read_text(encoding="utf-8")
    for old, new in pairs:
        if new in source:
            continue
        if old not in source:
            raise SystemExit("Next Gen patch could not find expected source in " + path + ": " + old[:100].replace("\n", "\\n"))
        source = source.replace(old, new, 1)
    p.write_text(source, encoding="utf-8")

# Keep the live board and move legality instant; reduce engine work for first-pass analysis.
edit("app/src/main/assets/js/app.js", [
("engine: { threads: autoThreads(dev.cores || 4), hash: autoHash(dev.memMb || 0), analysisMs: 1500 },",
 "engine: { threads: autoThreads(dev.cores || 4), hash: autoHash(dev.memMb || 0), analysisMs: 900 },"),
("""  async function doAnalyze() {
    if (engine.state === 'dead' && !Native.available) throw new Eng.EngineError('dead', 'Stockfish only runs inside the Android app.');
    const fen = game.fen(); let latest = {};
    $('btnAnalyze').disabled = true; $('coachLines').innerHTML = '<div class=\"muted\">Stockfish is analysing…</div>';
    try {
      const res = await runAnalysis({ ms: settings.engine.analysisMs, multipv: 3, onInfo: (info, byPv) => {
        latest = byPv; if (!analyzeRaf) analyzeRaf = requestAnimationFrame(() => { analyzeRaf = 0; renderLines(fen, Object.keys(latest).map(k => latest[k]).sort((a, b) => a.multipv - b.multipv)); });
      } });
      if (res.cancelled) { $('coachLines').innerHTML = '<div class=\"muted\">Analysis interrupted.</div>'; return null; }
      renderLines(fen, res.lines); lastAnalysis = { fen, lines: res.lines }; renderCoachMini();
      return lastAnalysis;
    } finally { $('btnAnalyze').disabled = false; }
  }
""",
 """  async function doAnalyze() {
    if (engine.state === 'dead' && !Native.available) throw new Eng.EngineError('dead', 'Stockfish only runs inside the Android app.');
    const fen = game.fen(); let latest = {};
    // One principal variation reaches useful depth sooner than MultiPV=3 on phones.
    // Scores update as Stockfish thinks; users can request deeper analysis in Settings.
    $('btnAnalyze').disabled = true;
    $('coachLines').innerHTML = '<div class=\"muted\">Quick analysis started · legal moves are already verified</div>';
    try {
      const res = await runAnalysis({ ms: settings.engine.analysisMs, multipv: 1, onInfo: (info, byPv) => {
        latest = byPv;
        if (!analyzeRaf) analyzeRaf = requestAnimationFrame(() => {
          analyzeRaf = 0;
          const lines = Object.keys(latest).map(k => latest[k]).sort((a, b) => a.multipv - b.multipv);
          renderLines(fen, lines);
          const best = lines[0];
          if (best && $('coachLines')) $('coachLines').setAttribute('aria-label', 'Live Stockfish analysis, depth ' + (best.depth || 0));
        });
      } });
      if (res.cancelled) { $('coachLines').innerHTML = '<div class=\"muted\">Analysis interrupted by a position change.</div>'; return null; }
      if (game.fen() !== fen) return null;
      renderLines(fen, res.lines);
      lastAnalysis = { fen, lines: res.lines, elapsedMs: res.elapsedMs, depth: res.lines.reduce((n, l) => Math.max(n, l.depth || 0), 0) };
      renderCoachMini();
      return lastAnalysis;
    } finally { $('btnAnalyze').disabled = false; }
  }
"""),
("const my = ++reviewTok, quickMs = Math.max(65, Math.min(110, Math.round(settings.engine.analysisMs / 18)));\n    const deepMs = Math.max(220, Math.min(450, Math.round(settings.engine.analysisMs * 0.28)));",
 "const my = ++reviewTok, quickMs = Math.max(55, Math.min(90, Math.round(settings.engine.analysisMs / 12)));\n    const deepMs = Math.max(180, Math.min(320, Math.round(settings.engine.analysisMs * 0.24)));"),
("""      const forcing = !!(h[i].captured || h[i].promotion || h[i].san.indexOf('+') >= 0 || h[i].san.indexOf('#') >= 0);
      let cramped = false;
      try { cramped = new Chess(h[i].after).moves().length <= 4; } catch (e) { /* ignore malformed historic FEN */ }
      if (swing >= 0.04 || forcing || cramped) { deep.add(i); deep.add(i + 1); }
""",
 """      const checkOrPromotion = !!(h[i].promotion || h[i].san.indexOf('+') >= 0 || h[i].san.indexOf('#') >= 0);
      const captureWithSwing = !!h[i].captured && swing >= 0.025;
      let cramped = false;
      try { cramped = new Chess(h[i].after).moves().length <= 4; } catch (e) { /* ignore malformed historic FEN */ }
      // Do not deep-search every routine capture. Spend the second pass on material swings,
      // forcing checks/promotions, and genuinely constrained positions.
      if (swing >= 0.06 || checkOrPromotion || captureWithSwing || (cramped && swing >= 0.03)) { deep.add(i); deep.add(i + 1); }
""")
])

edit("app/src/main/assets/index.html", [
("""          <div class=\"field\"><label for=\"setAnalysisMs\">Coach analysis time</label><select id=\"setAnalysisMs\"><option value=\"1000\">1 s</option><option value=\"1500\">1.5 s</option><option value=\"3000\">3 s</option><option value=\"5000\">5 s</option></select></div>
""",
"""          <div class=\"field\"><label for=\"setAnalysisMs\">Analysis Quality / Time</label><select id=\"setAnalysisMs\"><option value=\"500\">Quick · 0.5 s</option><option value=\"900\">Balanced · 0.9 s</option><option value=\"1500\">Strong · 1.5 s</option><option value=\"3000\">Deep · 3 s</option><option value=\"5000\">Maximum · 5 s</option></select><small class=\"muted\">Legal-move checks are exact and instant. Engine evaluations improve with more search time.</small></div>
""")
])

edit("app/build.gradle", [("versionName '3.0.0'", "versionName '1.0.0'")])
edit("tests/logic/rebuild-smoke.test.js", [
("assert(/versionName '3\\.0\\.0'/.test(gradle), 'Android versionName must be 3.0.0');",
 "assert(/versionName '1\\.0\\.0'/.test(gradle), 'Android versionName must be 1.0.0');")
])
print("Next Gen 1.0.0 performance overlay applied.")
