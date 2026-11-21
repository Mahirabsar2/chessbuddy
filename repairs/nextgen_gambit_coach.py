#!/usr/bin/env python3
"""Add an interactive opening/gambit coach and selectable chess start modes."""
from pathlib import Path

def replace_once(path, old, new, label):
    p = Path(path)
    source = p.read_text(encoding="utf-8")
    if new in source:
        return
    if old not in source:
        raise SystemExit("Gambit Coach patch could not find " + label + " in " + path)
    p.write_text(source.replace(old, new, 1), encoding="utf-8")

variant_markup = r'''        <section class="card variant-setup" id="variantSetupCard">
          <div class="content-head"><div><span class="eyebrow">GAME SETUP</span><h3>Choose your starting position</h3></div><span class="chip">PLAY</span></div>
          <div class="field"><label for="variantStartMode">Game type</label>
            <select id="variantStartMode">
              <option value="standard">Standard chess</option>
              <option value="custom">Custom FEN position</option>
              <option value="chess960">Chess960 · random back rank (beta)</option>
              <option value="threecheck">3-Check chess</option>
              <option value="koth">King of the Hill</option>
            </select>
          </div>
          <div class="field" id="variantFenField" hidden><label for="variantFenInput">Custom position FEN</label>
            <textarea id="variantFenInput" rows="2" spellcheck="false" autocapitalize="off" autocomplete="off" placeholder="Paste a valid FEN position here"></textarea>
          </div>
          <div class="field" id="variant960SeedField" hidden><label for="variant960Seed">Chess960 seed (0–959, blank = random)</label>
            <input id="variant960Seed" type="number" min="0" max="959" step="1" inputmode="numeric" placeholder="Random seed" />
          </div>
          <p class="muted tiny" id="variantSetupHelp">Standard chess with the normal starting position and rules.</p>
          <button class="btn primary" id="btnStartVariantGame" type="button">START VS SELECTED BOT</button>
          <div class="variant-support-note">Available here: Standard, custom FEN, 3-Check and King of the Hill. Chess960 layout is playable in beta; castling from randomized rook/king files is not enabled yet. Other variants need their own rules engine before they can be called playable.</div>
        </section>'''
replace_once(
    "app/src/main/assets/index.html",
    '        <button class="row-btn" id="rowOnline" type="button"><span class="ri" id="riOnline"></span><span class="rt"><b>Play Online</b><small>See friends online and send direct challenges</small></span><span class="rc" data-ic="chev"></span></button>\n      </div>',
    '        <button class="row-btn" id="rowOnline" type="button"><span class="ri" id="riOnline"></span><span class="rt"><b>Play Online</b><small>See friends online and send direct challenges</small></span><span class="rc" data-ic="chev"></span></button>\n' + variant_markup + '\n      </div>',
    "Play lobby game setup card"
)

gambit_markup = r'''      <section class="card gambit-coach-lab" id="gambitCoachLab" aria-label="Opening and gambit practice">
        <div class="content-head"><div><span class="eyebrow">OPENING &amp; GAMBIT COACH</span><h3>Practice any line</h3></div><span class="chip">COACH MODE</span></div>
        <p class="muted tiny">Browse the ChessBuddy opening book and dedicated gambit lines. The coach can demonstrate both sides, play the opponent's replies while you practice, or make the next book move for you.</p>
        <div class="field"><label for="gambitSearch">Search openings and gambits</label><input id="gambitSearch" type="search" placeholder="Alien Gambit, King's Gambit, Sicilian…" autocomplete="off" /></div>
        <div class="field"><label for="gambitCourseSelect">Repertoire line</label><select id="gambitCourseSelect"></select></div>
        <div class="gambit-course-meta" id="gambitCourseMeta"></div>
        <div class="grid2">
          <div class="field"><label for="gambitPracticeSide">You play</label><select id="gambitPracticeSide"><option value="w">White</option><option value="b">Black</option></select></div>
          <div class="field"><label for="gambitPracticeMode">Practice mode</label><select id="gambitPracticeMode"><option value="practice">I play the line</option><option value="demo">Coach demonstrates both sides</option></select></div>
        </div>
        <div class="gambit-board-wrap"><div id="gambitCoachBoard" class="board" role="grid" aria-label="Opening and gambit practice board"></div></div>
        <div class="gambit-progress-card">
          <div class="content-head"><span class="eyebrow" id="gambitMoveCount">READY</span><b id="gambitStarScore">☆☆☆</b></div>
          <b id="gambitCoachStatus">Choose a line to begin.</b>
          <p class="muted tiny" id="gambitCoachExplanation">The coach explains the idea behind the selected opening or gambit.</p>
        </div>
        <div class="gambit-move-list" id="gambitMoveList"></div>
        <div class="gambit-controls">
          <button class="btn primary" id="btnGambitPractice" type="button">START PRACTICE</button>
          <button class="btn" id="btnGambitDemo" type="button">COACH DEMO</button>
          <button class="btn" id="btnGambitCoachMove" type="button">COACH MOVE</button>
          <button class="btn" id="btnGambitUndo" type="button" disabled>UNDO</button>
          <button class="btn" id="btnGambitRestart" type="button">RESTART</button>
        </div>
        <div class="gambit-rating-row"><span class="muted tiny" id="gambitPersonalBest">Line stars: ☆☆☆</span><span class="muted tiny" id="gambitCatalogCount"></span></div>
        <div class="notice" id="gambitCoachNotice" role="status" aria-live="polite">Select a repertoire line, choose your colour, then start practice or watch the coach demonstrate it.</div>
        <div class="variant-support-note">The library includes the Alien Gambit and many classical and offbeat gambits. Gambit evaluations are not guarantees: some sharp gambits are objectively unsound and are included for study.</div>
      </section>'''
replace_once(
    "app/src/main/assets/index.html",
    '    </section>\n\n    <!-- ================= WATCH',
    gambit_markup + '\n    </section>\n\n    <!-- ================= WATCH',
    "Learn page Gambit Coach panel"
)

# Add state for the active start mode and variant-aware engine options.
replace_once(
    "app/src/main/assets/js/app.js",
    "  let game = new Chess();\n  const makeClock",
    "  let game = new Chess();\n  let activeGameVariant = 'standard', activeGameOptions = null, variantChecks = { w: 0, b: 0 };\n  const makeClock",
    "active game variant state"
)
replace_once(
    "app/src/main/assets/js/app.js",
    "  const baseOptions = () => ({ Threads: settings.engine.threads, Hash: settings.engine.hash, 'Move Overhead': 30 });",
    "  const baseOptions = () => ({ Threads: settings.engine.threads, Hash: settings.engine.hash, 'Move Overhead': 30, UCI_Chess960: activeGameVariant === 'chess960' });",
    "variant-aware engine options"
)

# Add special win conditions and count checks after each committed move.
replace_once(
    "app/src/main/assets/js/app.js",
    "  function computeOver() {\n    const loser = game.turn(), winner = loser === 'w' ? 'b' : 'w', nm = winner === 'w' ? 'White' : 'Black';",
    """  function computeOver() {
    if (activeGameVariant === 'threecheck') {
      if (variantChecks.w >= 3) return { type: 'variant', winner: 'w', text: '3-Check — White delivered three checks' };
      if (variantChecks.b >= 3) return { type: 'variant', winner: 'b', text: '3-Check — Black delivered three checks' };
    }
    if (activeGameVariant === 'koth') {
      const center = ['d4', 'e4', 'd5', 'e5'];
      if (center.some(sq => { const p = game.get(sq); return p && p.type === 'k' && p.color === 'w'; }))
        return { type: 'variant', winner: 'w', text: 'King of the Hill — White reached the center' };
      if (center.some(sq => { const p = game.get(sq); return p && p.type === 'k' && p.color === 'b'; }))
        return { type: 'variant', winner: 'b', text: 'King of the Hill — Black reached the center' };
    }
    const loser = game.turn(), winner = loser === 'w' ? 'b' : 'w', nm = winner === 'w' ? 'White' : 'Black';""",
    "variant win conditions"
)
replace_once(
    "app/src/main/assets/js/app.js",
    "    over = computeOver();\n    soundForMove(m);",
    "    if (activeGameVariant === 'threecheck' && game.inCheck()) variantChecks[m.color] = Math.min(3, Number(variantChecks[m.color] || 0) + 1);\n    over = computeOver();\n    soundForMove(m);",
    "3-Check counter update"
)

# Start custom FEN / Chess960 positions while preserving existing callers and rematches.
replace_once(
    "app/src/main/assets/js/app.js",
    "  function startGame(players) {\n    const modelIds",
    "  function startGame(players, options) {\n    options = options || null;\n    const modelIds",
    "startGame optional options"
)
replace_once(
    "app/src/main/assets/js/app.js",
    "    if (!modelIds.length) return startGameNow(players);",
    "    if (!modelIds.length) return startGameNow(players, options);",
    "startGame direct options handoff"
)
replace_once(
    "app/src/main/assets/js/app.js",
    "    (async () => { for (const id of modelIds) { if (!await ensureMaiaModel(id)) return; } startGameNow(players); })()",
    "    (async () => { for (const id of modelIds) { if (!await ensureMaiaModel(id)) return; } startGameNow(players, options); })()",
    "Maia start options handoff"
)
replace_once(
    "app/src/main/assets/js/app.js",
    "  function startGameNow(players) {\n    Native.logEvent",
    "  function startGameNow(players, options) {\n    options = options || {};\n    Native.logEvent",
    "startGameNow optional options"
)
replace_once(
    "app/src/main/assets/js/app.js",
    "    game = new Chess(); ctx = newCtx(players); if (ctx.clock) ctx.clock.start('w', performance.now());",
    """    activeGameVariant = options.variant || 'standard';
    activeGameOptions = options.startFen ? { variant: activeGameVariant, startFen: options.startFen } : { variant: activeGameVariant };
    variantChecks = { w: 0, b: 0 };
    game = options.startFen ? new Chess(options.startFen) : new Chess();
    ctx = newCtx(players); if (ctx.clock) ctx.clock.start('w', performance.now());""",
    "custom start FEN initialization"
)
replace_once(
    "app/src/main/assets/js/app.js",
    "    setHeaders(); saveCurrent();\n    showPlayScreen('game'); render();",
    """    setHeaders();
    if (options.startFen) { game.setHeader('SetUp', '1'); game.setHeader('FEN', options.startFen); }
    if (activeGameVariant !== 'standard') game.setHeader('Variant', activeGameVariant === 'chess960' ? 'Chess960 setup (castling disabled beta)' : activeGameVariant);
    saveCurrent();
    showPlayScreen('game'); render();""",
    "start headers for custom/variant game"
)
replace_once(
    "app/src/main/assets/js/app.js",
    "  const rematch = () => startGame({ w: ctx.players.b, b: ctx.players.w });",
    "  const rematch = () => startGame({ w: ctx.players.b, b: ctx.players.w }, activeGameOptions);",
    "variant-aware rematch"
)

gambit_controller = r'''
  /* ================= Opening & Gambit Coach ================= */
  const GAMBIT_COURSES = [
    { id:'alien-gambit', name:'Alien Gambit · Caro-Kann', eco:'B12', side:'w', level:'Sharp / risky', idea:'White sacrifices a knight on f7 to drag the black king into the open. Black can decline the attack by returning the king to safety and consolidating the extra material.', moves:'e4 c6 d4 d5 Nd2 dxe4 Nxe4 Nf6 Ng5 h6 Nxf7 Kxf7 Nf3 c5' },
    { id:'kings-gambit-accepted', name:'King’s Gambit Accepted', eco:'C34', side:'w', level:'Aggressive', idea:'White gives a flank pawn to open the f-file and gain rapid development. Black can hold the extra pawn but must defend accurately.', moves:'e4 e5 f4 exf4 Nf3 g5 h4 g4' },
    { id:'kings-gambit-falkbeer', name:'King’s Gambit Declined · Falkbeer Countergambit', eco:'C31', side:'b', level:'Countergambit', idea:'Black strikes in the center immediately instead of accepting the f-pawn.', moves:'e4 e5 f4 d5 exd5 e4' },
    { id:'evans-gambit', name:'Evans Gambit', eco:'C52', side:'w', level:'Attacking', idea:'White offers the b-pawn to gain tempi with c3 and d4, opening the center while Black is still developing.', moves:'e4 e5 Nf3 Nc6 Bc4 Bc5 b4 Bxb4 c3 Ba5 d4 exd4 O-O' },
    { id:'danish-gambit', name:'Danish Gambit', eco:'C21', side:'w', level:'Sacrificial', idea:'White offers one or two central pawns for open diagonals and fast development.', moves:'e4 e5 d4 exd4 c3 dxc3 Bc4 cxb2 Bxb2' },
    { id:'scotch-gambit', name:'Scotch Gambit', eco:'C44', side:'w', level:'Open game', idea:'White gives up the d-pawn to develop the bishop actively and attack before Black completes development.', moves:'e4 e5 Nf3 Nc6 d4 exd4 Bc4' },
    { id:'vienna-gambit', name:'Vienna Gambit', eco:'C29', side:'w', level:'Attacking', idea:'White uses f4 to challenge e5 and build a quick kingside initiative.', moves:'e4 e5 Nc3 Nf6 f4' },
    { id:'halloween-gambit', name:'Halloween Gambit', eco:'C47', side:'w', level:'Wild / unsound', idea:'White sacrifices a knight for two central pawns and space. Black should return material only when it improves king safety.', moves:'e4 e5 Nf3 Nc6 Nc3 Nf6 Nxe5' },
    { id:'smith-morra', name:'Smith–Morra Gambit', eco:'B21', side:'w', level:'Sicilian attack', idea:'White offers the d-pawn for open files, quick piece development and pressure against the queenside.', moves:'e4 c5 d4 cxd4 c3 dxc3 Nxc3' },
    { id:'blackmar-diemer', name:'Blackmar–Diemer Gambit', eco:'D00', side:'w', level:'Attacking', idea:'White gives a central pawn for rapid development and open lines toward the black king.', moves:'d4 d5 e4 dxe4 Nc3 Nf6 f3' },
    { id:'budapest', name:'Budapest Gambit', eco:'A52', side:'b', level:'Surprise defense', idea:'Black gives a pawn to develop quickly and put pressure on e5 and the center.', moves:'d4 Nf6 c4 e5 dxe5 Ng4' },
    { id:'albin-counter', name:'Albin Countergambit', eco:'D08', side:'b', level:'Counterattack', idea:'Black sacrifices a pawn to gain space with the advanced d-pawn and create tactical chances.', moves:'d4 d5 c4 e5 dxe5 d4' },
    { id:'benko', name:'Benko Gambit', eco:'A57', side:'b', level:'Positional sacrifice', idea:'Black sacrifices a queenside pawn for long-term pressure on the a- and b-files and active bishops.', moves:'d4 Nf6 c4 c5 d5 b5 cxb5 a6 bxa6 Bxa6' },
    { id:'englund', name:'Englund Gambit', eco:'A40', side:'b', level:'Tricky / risky', idea:'Black offers a central pawn to pull White away from normal development and create tactical chances.', moves:'d4 e5 dxe5 Nc6 Nf3 Qe7' },
    { id:'latvian', name:'Latvian Gambit', eco:'C40', side:'b', level:'Wild / unsound', idea:'Black offers the f-pawn for rapid, direct counterplay. It is risky but useful for tactical practice.', moves:'e4 e5 Nf3 f5' },
    { id:'elephant', name:'Elephant Gambit', eco:'C40', side:'b', level:'Offbeat', idea:'Black challenges the center with ...d5 and tries to create active piece play after the exchange.', moves:'e4 e5 Nf3 d5 exd5 e4' },
    { id:'stafford', name:'Stafford Gambit', eco:'C42', side:'b', level:'Tricky / risky', idea:'Black sacrifices a pawn for fast development and tactical threats against f2 and the white king.', moves:'e4 e5 Nf3 Nf6 Nxe5 Nc6' },
    { id:'rousseau', name:'Rousseau Gambit', eco:'C50', side:'b', level:'Offbeat', idea:'Black pushes ...f5 early to challenge the center and create attacking chances.', moves:'e4 e5 Nf3 Nc6 Bc4 f5' },
    { id:'from', name:'From’s Gambit', eco:'A02', side:'b', level:'Sharp', idea:'Black responds to Bird’s Opening with ...e5 and attacks the f-pawn to open lines.', moves:'f4 e5 fxe5 d6' },
    { id:'blumenfeld', name:'Blumenfeld Countergambit', eco:'E10', side:'b', level:'Positional sacrifice', idea:'Black gives a queenside pawn for central control and pressure against White’s center.', moves:'d4 Nf6 c4 e6 Nf3 b6 d5 c6' },
    { id:'cochrane', name:'Cochrane Gambit', eco:'C42', side:'w', level:'Endgame gamble', idea:'White sacrifices a knight to expose the black king. Accurate defense can leave Black with a material edge.', moves:'e4 e5 Nf3 Nf6 Nxe5 d6 Nxf7' },
    { id:'shilling', name:'Shilling Gambit', eco:'C50', side:'b', level:'Trap line', idea:'Black offers a pawn with ...Nd4, hoping White grabs material and overlooks a tactical queen attack.', moves:'e4 e5 Nf3 Nc6 Bc4 Nd4' },
    { id:'tennison', name:'Tennison Gambit', eco:'A06', side:'w', level:'Offbeat', idea:'White offers the e-pawn for rapid development and attacking chances on the kingside.', moves:'Nf3 d5 e4 dxe4 Ng5' },
    { id:'goring', name:'Göring Gambit', eco:'C44', side:'w', level:'Open game', idea:'White offers the c-pawn after the Scotch move order to open files and develop quickly.', moves:'e4 e5 Nf3 Nc6 d4 exd4 c3' },
    { id:'urussov', name:'Urussov Gambit', eco:'C24', side:'w', level:'Open game', idea:'White uses d4 after the Bishop’s Opening to open the center before Black castles.', moves:'e4 e5 Bc4 Nf6 d4' },
    { id:'muzio', name:'Muzio Gambit', eco:'C37', side:'w', level:'Extreme attack', idea:'White sacrifices a knight on f3’s support and castles quickly for a dangerous kingside attack.', moves:'e4 e5 f4 exf4 Nf3 g5 Bc4 g4 O-O' },
    { id:'allgaier', name:'Allgaier Gambit', eco:'C39', side:'w', level:'Extreme attack', idea:'White sacrifices the knight on g5 to rip open the black king’s position in the King’s Gambit.', moves:'e4 e5 f4 exf4 Nf3 g5 h4 g4 Ng5' },
    { id:'kieseritzky', name:'Kieseritzky Gambit', eco:'C39', side:'w', level:'Classical attack', idea:'White sacrifices a pawn and uses Ne5 to build an initiative against Black’s exposed kingside.', moves:'e4 e5 f4 exf4 Nf3 g5 h4 g4 Ne5' },
    { id:'falkbeer', name:'Falkbeer Countergambit', eco:'C31', side:'b', level:'Counterattack', idea:'Black returns the central blow immediately with ...d5 instead of passively defending e5.', moves:'e4 e5 f4 d5' },
    { id:'blackmar', name:'Blackmar Gambit', eco:'D00', side:'w', level:'Offbeat', idea:'White opens the center with e4 and invites a central pawn capture for quick development.', moves:'d4 d5 e4' },
    { id:'qga', name:'Queen’s Gambit Accepted', eco:'D20', side:'w', level:'Classical', idea:'White offers the c-pawn for central control and quick development. It is a long-standing, sound opening.', moves:'d4 d5 c4 dxc4 e3 Nf6 Bxc4' }
  ];

  let gambitRun = null, gambitCatalog = [], gambitSelected = 'alien-gambit', gambitSelectedMoves = [];
  function gambitCourseList() {
    const gambits = GAMBIT_COURSES.map(c => Object.assign({ kind:'gambit' }, c));
    const book = (Openings.LINES || []).map((line, i) => ({
      id:'opening-book-' + i, name:line[0], eco:'Opening book', kind:'opening', side:'w',
      level:'Opening repertoire', idea:'Common opening line from the ChessBuddy opening book.', moves:line[1]
    }));
    const seen = new Set(gambits.map(c => c.name.toLowerCase()));
    return gambits.concat(book.filter(c => !seen.has(c.name.toLowerCase())));
  }
  function buildGambitLine(course) {
    const tokens = String(course.moves || '').trim().split(/\s+/).filter(Boolean);
    const board = new Chess(), uci = [], san = [], positions = [board.fen()];
    if (!tokens.length) throw new Error('This course does not contain a move line yet.');
    tokens.forEach((token, i) => {
      let move;
      try { move = board.move(token); } catch (e) { throw new Error(course.name + ' has an invalid move at step ' + (i + 1) + ': ' + token); }
      if (!move) throw new Error(course.name + ' has an illegal move at step ' + (i + 1) + ': ' + token);
      uci.push(move.from + move.to + (move.promotion || ''));
      san.push(move.san);
      positions.push(board.fen());
    });
    return { course:course, uci:uci, san:san, positions:positions };
  }
  function gambitLineFor(id) {
    const course = gambitCourseList().find(c => c.id === id);
    if (!course) throw new Error('Choose an opening or gambit from the repertoire list.');
    return buildGambitLine(course);
  }
  function gambitStars(id) {
    const stars = settings.progress.gambitStars || {};
    return Math.max(0, Math.min(3, Number(stars[id] || 0)));
  }
  function starText(value) { return '★'.repeat(value) + '☆'.repeat(3 - value); }
  function updateGambitCourseInfo() {
    const line = gambitLineFor(gambitSelected), c = line.course;
    gambitSelectedMoves = line.san;
    $('gambitCourseMeta').textContent = (c.kind === 'gambit' ? 'GAMBIT' : 'OPENING') + ' · ' + c.eco + ' · ' + c.level + ' · ' + line.uci.length + ' half-moves';
    $('gambitCoachExplanation').textContent = c.idea;
    $('gambitPersonalBest').textContent = 'Your best: ' + starText(gambitStars(c.id));
    $('gambitSearch').value = $('gambitSearch').value || '';
  }
  function populateGambitCourseSelect(query) {
    const select = $('gambitCourseSelect');
    if (!select) return;
    const q = String(query || '').trim().toLowerCase(), courses = gambitCourseList();
    const matches = courses.filter(c => !q || (c.name + ' ' + c.eco + ' ' + c.kind + ' ' + c.idea).toLowerCase().includes(q));
    select.innerHTML = matches.map(c => '<option value="' + c.id + '">' + (c.kind === 'gambit' ? '♜ ' : '♟ ') + esc(c.name) + '</option>').join('');
    if (!matches.some(c => c.id === gambitSelected)) gambitSelected = (matches[0] || { id:'' }).id;
    select.value = gambitSelected;
    $('gambitCatalogCount').textContent = matches.length + ' / ' + courses.length + ' lines';
    if (gambitSelected) updateGambitCourseInfo();
    else $('gambitCoachNotice').textContent = 'No matching opening or gambit. Try another search.';
  }
  function setGambitNotice(message, kind) {
    const el = $('gambitCoachNotice');
    el.textContent = message;
    el.className = 'notice' + (kind ? ' ' + kind : '');
  }
  function renderGambitCoach() {
    const run = gambitRun;
    if (!run) return;
    const host = $('gambitCoachBoard'), board = run.game, legal = {}, captures = {};
    if (run.selected) board.moves({ square:run.selected, verbose:true }).forEach(m => {
      legal[m.to] = true; if (m.captured || m.flags.indexOf('e') >= 0) captures[m.to] = true;
    });
    Board.draw(host, board, { flipped:run.mode === 'practice' && run.userSide === 'b', selected:run.selected, legal:legal, captures:captures,
      last:run.lastMove, coords:true, check:Board.checkSquare(board) });
    Board.arrow(host, run.hintFrom || null, run.hintTo || null, run.mode === 'practice' && run.userSide === 'b');
    const total = run.uci.length, count = run.mode === 'demo' ? run.index : run.index;
    $('gambitMoveCount').textContent = 'MOVE ' + count + ' / ' + total;
    $('gambitCoachStatus').textContent = run.done ? 'Line completed' : (run.offBook ? 'Free play · Stockfish continuation' : (run.mode === 'demo' ? 'Coach demonstration' : 'Practice as ' + (run.userSide === 'w' ? 'White' : 'Black')));
    $('gambitMoveList').innerHTML = run.san.slice(0, run.index).map((m, i) =>
      '<span class="gambit-move' + (i === run.index - 1 ? ' current' : '') + '">' +
      (i % 2 === 0 ? (Math.floor(i / 2) + 1) + '. ' : '') + esc(m) + '</span>').join(' ') || '<span class="muted tiny">The move list will appear as the line is played.</span>';
    $('btnGambitUndo').disabled = !board.history().length || run.busy;
    const stars = gambitStars(run.course.id);
    $('gambitStarScore').textContent = starText(stars);
    $('gambitPersonalBest').textContent = 'Your best: ' + starText(stars);
    $('btnGambitPractice').disabled = run.busy;
    $('btnGambitDemo').disabled = run.busy;
    $('btnGambitCoachMove').disabled = run.busy || run.done;
  }
  function finishGambitPractice() {
    if (!gambitRun || gambitRun.done) return;
    const run = gambitRun;
    run.done = true;
    if (run.mode === 'practice') {
      const awarded = run.deviations === 0 ? 3 : run.deviations === 1 ? 2 : 1;
      settings.progress.gambitStars = settings.progress.gambitStars || {};
      settings.progress.gambitStars[run.course.id] = Math.max(gambitStars(run.course.id), awarded);
      settings.progress.gambitCompleted = Number(settings.progress.gambitCompleted || 0) + 1;
      saveSettings();
      setGambitNotice('Line completed. You earned ' + starText(awarded) + (run.deviations ? ' — ' + run.deviations + ' off-book move(s).' : ' — perfect repertoire play!'), 'ok');
    } else setGambitNotice('Coach demonstration completed. Switch to practice mode to earn stars.', 'ok');
    renderGambitCoach();
  }
  function gambitApplyBookMove() {
    const run = gambitRun;
    if (!run || run.done || run.index >= run.uci.length) { if (run) finishGambitPractice(); return false; }
    const uci = run.uci[run.index], m = run.game.move({ from:uci.slice(0,2), to:uci.slice(2,4), promotion:uci.length > 4 ? uci[4] : undefined });
    if (!m) { setGambitNotice('The saved repertoire move was not legal in the current position.', 'bad'); return false; }
    run.index++;
    run.lastMove = { from:m.from, to:m.to }; run.selected = null; run.hintFrom = null; run.hintTo = null;
    return true;
  }
  async function gambitEngineReply() {
    const run = gambitRun;
    if (!run || run.done || run.busy || run.game.isGameOver()) return;
    run.busy = true; renderGambitCoach(); setGambitNotice('Stockfish is finding a legal continuation from your deviation…');
    try {
      await engine.useProvider('stockfish', '');
      const res = await engine.search({ startFen:Eng.START_FEN, moves:Eng.uciMovesFromHistory(run.game.history({ verbose:true })),
        movetime:650, options:analysisOptions(1) });
      if (gambitRun !== run || res.cancelled) return;
      if (!res.bestmove) throw new Error('Stockfish did not return a move.');
      const uci = res.bestmove, move = run.game.move({ from:uci.slice(0,2), to:uci.slice(2,4), promotion:uci.length > 4 ? uci[4] : undefined });
      if (!move) throw new Error('Stockfish returned a move the board rejected.');
      run.lastMove = { from:move.from, to:move.to };
      if (run.game.isGameOver()) { run.done = true; setGambitNotice('The practice game ended: ' + (run.game.isCheckmate() ? 'checkmate' : 'draw') + '.', 'ok'); }
      else setGambitNotice('Stockfish played ' + move.san + '. Keep playing from this position.');
    } catch (e) {
      setGambitNotice('Engine continuation unavailable: ' + (e.message || 'unknown engine error') + '. Your position is preserved.', 'warn');
    } finally {
      if (gambitRun === run) { run.busy = false; renderGambitCoach(); }
    }
  }
  async function gambitCoachReplies() {
    const run = gambitRun;
    if (!run || run.done || run.mode !== 'practice') return;
    run.busy = true;
    try {
      while (run.index < run.uci.length && run.game.turn() !== run.userSide) {
        if (!gambitApplyBookMove()) break;
      }
      if (run.index >= run.uci.length) finishGambitPractice();
      else setGambitNotice('Your turn as ' + (run.userSide === 'w' ? 'White' : 'Black') + '. Play the next move in the line, or let the coach make it for you.');
    } finally {
      if (gambitRun === run) { run.busy = false; renderGambitCoach(); }
    }
  }
  function startGambitPractice(mode) {
    let line;
    try { line = gambitLineFor(gambitSelected); }
    catch (e) { setGambitNotice(e.message, 'bad'); return; }
    const userSide = $('gambitPracticeSide').value === 'b' ? 'b' : 'w';
    gambitRun = { course:line.course, game:new Chess(), uci:line.uci, san:line.san, index:0, mode:mode,
      userSide:userSide, selected:null, lastMove:null, hintFrom:null, hintTo:null, deviations:0, offBook:false, busy:false, done:false };
    renderGambitCoach();
    setGambitNotice(mode === 'demo' ? 'Coach demonstration: tap COACH MOVE to step through both sides.' :
      'Practice started. The coach will play the opposing side’s prepared replies. You can also tap COACH MOVE to play the next book move for you.');
    if (mode === 'practice') gambitCoachReplies();
  }
  function gambitCoachMove() {
    const run = gambitRun;
    if (!run || run.done || run.busy || run.offBook) return;
    if (!gambitApplyBookMove()) return;
    renderGambitCoach();
    if (run.mode === 'practice') gambitCoachReplies();
    else if (run.index >= run.uci.length) finishGambitPractice();
    else setGambitNotice('Coach played ' + run.san[run.index - 1] + '. Tap COACH MOVE for the next move.');
  }
  function gambitSquareTap(event) {
    const run = gambitRun;
    const el = event.target && event.target.closest ? event.target.closest('.sq[data-sq]') : null;
    if (!run || run.mode !== 'practice' || run.done || run.busy || run.offBook || !el || run.game.turn() !== run.userSide) return;
    const sq = el.getAttribute('data-sq'), piece = run.game.get(sq);
    if (!run.selected) {
      if (piece && piece.color === run.userSide) { run.selected = sq; renderGambitCoach(); }
      return;
    }
    const legal = run.game.moves({ square:run.selected, verbose:true });
    const candidate = legal.find(m => m.to === sq);
    if (!candidate) {
      if (piece && piece.color === run.userSide) { run.selected = sq; renderGambitCoach(); }
      else { run.selected = null; renderGambitCoach(); }
      return;
    }
    const uci = candidate.from + candidate.to + (candidate.promotion || '');
    const expected = run.uci[run.index];
    const correct = expected === uci;
    const move = run.game.move({ from:candidate.from, to:candidate.to, promotion:candidate.promotion || 'q' });
    if (!move) { setGambitNotice('That move was not legal.'); return; }
    run.selected = null; run.lastMove = { from:move.from, to:move.to };
    if (correct) {
      run.index++;
      setGambitNotice('Correct repertoire move: ' + move.san + '. The coach is preparing the reply.', 'ok');
      if (run.game.isGameOver()) finishGambitPractice();
      else gambitCoachReplies();
    } else {
      run.deviations++; run.offBook = true;
      setGambitNotice('You chose ' + move.san + ' instead of the prepared line. Free practice is on — Stockfish will continue from your position.', 'warn');
      renderGambitCoach();
      gambitEngineReply();
    }
    renderGambitCoach();
  }
  function undoGambitMove() {
    const run = gambitRun;
    if (!run || run.busy || !run.game.history().length) return;
    run.game.undo(); run.lastMove = null; run.done = false; run.offBook = false;
    const historyLength = run.game.history().length;
    run.index = Math.min(run.uci.length, historyLength);
    if (run.mode === 'practice' && run.game.turn() !== run.userSide) gambitCoachReplies();
    else { renderGambitCoach(); setGambitNotice('Move undone. Continue the line from this position.'); }
  }
  function restartGambitRun() {
    if (!gambitRun) return startGambitPractice($('gambitPracticeMode').value);
    const id = gambitRun.course.id, mode = gambitRun.mode, side = gambitRun.userSide;
    gambitSelected = id; $('gambitPracticeSide').value = side; $('gambitPracticeMode').value = mode;
    startGambitPractice(mode);
  }
  function initializeGambitCoach() {
    populateGambitCourseSelect('');
    const select = $('gambitCourseSelect');
    if (select && GAMBIT_COURSES.some(c => c.id === 'alien-gambit')) select.value = gambitSelected;
    if (select) gambitSelected = select.value;
    try { updateGambitCourseInfo(); } catch (e) { setGambitNotice(e.message, 'warn'); }
    if ($('gambitCoachBoard')) {
      const preview = new Chess();
      Board.draw($('gambitCoachBoard'), preview, { coords:true });
    }
  }

  /* ================= Start-position variants ================= */
  function chess960BackRank(seed) {
    let n = Math.max(0, Math.min(959, Number(seed) | 0));
    const row = Array(8).fill(null);
    const darkBishop = (n % 4) * 2 + 1; n = Math.floor(n / 4);
    const lightBishop = (n % 4) * 2; n = Math.floor(n / 4);
    row[darkBishop] = 'b'; row[lightBishop] = 'b';
    let empty = row.map((p,i) => p ? -1 : i).filter(i => i >= 0);
    const queenAt = n % 6; n = Math.floor(n / 6);
    row[empty[queenAt]] = 'q';
    empty = row.map((p,i) => p ? -1 : i).filter(i => i >= 0);
    const pairs = [];
    for (let a = 0; a < 5; a++) for (let b = a + 1; b < 5; b++) pairs.push([a,b]);
    const pair = pairs[n % 10];
    row[empty[pair[0]]] = 'n'; row[empty[pair[1]]] = 'n';
    empty = row.map((p,i) => p ? -1 : i).filter(i => i >= 0);
    row[empty[0]] = 'r'; row[empty[1]] = 'k'; row[empty[2]] = 'r';
    return row.join('');
  }
  function chess960Fen(seed) {
    const lower = chess960BackRank(seed);
    const upper = lower.toUpperCase();
    return lower + '/pppppppp/8/8/8/8/PPPPPPPP/' + upper + ' w - - 0 1';
  }
  function renderVariantSetup() {
    const mode = $('variantStartMode').value;
    $('variantFenField').hidden = mode !== 'custom';
    $('variant960SeedField').hidden = mode !== 'chess960';
    const help = {
      standard:'Standard chess with the normal starting position and rules.',
      custom:'Paste any valid six-field FEN to play from a custom position using standard chess rules.',
      chess960:'Generates one of the 960 legal back-rank layouts. Beta note: randomized Chess960 castling is disabled until the board rules layer supports Fischer-Random castling.',
      threecheck:'Win by giving check three times. Normal chess moves apply; the app tracks the check counter.',
      koth:'Win by moving your king onto d4, e4, d5 or e5. Normal chess moves apply.'
    };
    $('variantSetupHelp').textContent = help[mode] || help.standard;
  }
  function startSelectedVariantGame() {
    const mode = $('variantStartMode').value;
    let options = { variant:mode }, fen = '';
    if (mode === 'custom') {
      fen = $('variantFenInput').value.trim();
      if (!fen) { toast('Paste a FEN position first.'); return; }
      try { new Chess(fen); } catch (e) { toast('Invalid FEN: ' + e.message); return; }
      options.startFen = fen;
    } else if (mode === 'chess960') {
      const raw = $('variant960Seed').value.trim();
      const seed = raw === '' ? Math.floor(Math.random() * 960) : Number(raw);
      if (!Number.isInteger(seed) || seed < 0 || seed > 959) { toast('Chess960 seed must be from 0 to 959.'); return; }
      fen = chess960Fen(seed);
      options.startFen = fen; options.variant = 'chess960';
      toast('Chess960 layout seed ' + seed + '. Castling is disabled in this beta.');
    }
    const bot = Str.botById(selBot) || Str.botById('marlow') || Str.BOTS[0];
    if (!bot) { toast('No Stockfish bot is available.'); return; }
    const p = botPlayer(bot), c = settings.play.color === 'r' ? (Math.random() < 0.5 ? 'w' : 'b') : settings.play.color;
    startGame(c === 'w' ? { w:HUMAN, b:p } : { w:p, b:HUMAN }, options);
  }
'''
replace_once(
    "app/src/main/assets/js/app.js",
    "  const LESSON_LEVELS = ['New to Chess','Beginner','Intermediate','Advanced'];",
    gambit_controller + "\n  const LESSON_LEVELS = ['New to Chess','Beginner','Intermediate','Advanced'];",
    "Gambit Coach and variant controllers"
)

# Add the new UI event handlers beside the existing Learn controls.
replace_once(
    "app/src/main/assets/js/app.js",
    "    $('btnOpeningExplore').onclick = loadOpeningExplorer;",
    """    $('btnOpeningExplore').onclick = loadOpeningExplorer;
    $('gambitSearch').oninput = e => populateGambitCourseSelect(e.target.value);
    $('gambitCourseSelect').onchange = e => { gambitSelected = e.target.value; gambitRun = null; updateGambitCourseInfo(); renderGambitCoach(); };
    $('gambitPracticeSide').onchange = () => { if (gambitRun) startGambitPractice('practice'); };
    $('gambitPracticeMode').onchange = () => { if (gambitRun) startGambitPractice($('gambitPracticeMode').value); };
    $('btnGambitPractice').onclick = () => { $('gambitPracticeMode').value = 'practice'; startGambitPractice('practice'); };
    $('btnGambitDemo').onclick = () => { $('gambitPracticeMode').value = 'demo'; startGambitPractice('demo'); };
    $('btnGambitCoachMove').onclick = gambitCoachMove;
    $('btnGambitUndo').onclick = undoGambitMove;
    $('btnGambitRestart').onclick = restartGambitRun;
    $('gambitCoachBoard').addEventListener('click', gambitSquareTap);
    $('variantStartMode').onchange = renderVariantSetup;
    $('btnStartVariantGame').onclick = startSelectedVariantGame;
    renderVariantSetup();
    initializeGambitCoach();""",
    "Gambit Coach and variant event handlers"
)

# Show a descriptive variant in game metadata and preserve it in archive rows.
replace_once(
    "app/src/main/assets/js/app.js",
    "      plies: game.history().length, pgn: game.pgn(), fen: game.fen(), done: !!over });",
    "      plies: game.history().length, pgn: game.pgn(), fen: game.fen(), variant:activeGameVariant, done: !!over });",
    "archive variant label"
)

css = r'''
/* Gambit Coach and game setup */
.variant-setup { margin-top:14px; }
.variant-setup .btn { width:100%; }
.variant-support-note { color:var(--muted); font-size:11px; line-height:1.45; margin-top:9px; }
.gambit-coach-lab { margin-top:14px; }
.gambit-course-meta { color:var(--muted); font-size:12px; margin:8px 0 12px; }
.gambit-board-wrap { width:min(100%,360px); margin:12px auto; }
#gambitCoachBoard { width:100%; max-width:360px; aspect-ratio:1; }
.gambit-progress-card { padding:12px; border-radius:12px; background:var(--surface2); margin:10px 0; }
.gambit-progress-card>b { display:block; margin:5px 0; }
#gambitStarScore { color:#e8bf58; letter-spacing:1px; }
.gambit-move-list { display:flex; flex-wrap:wrap; gap:5px; min-height:24px; margin:10px 0; }
.gambit-move { padding:4px 7px; border-radius:6px; background:var(--surface2); font-size:12px; }
.gambit-move.current { outline:1px solid var(--accent,#c5a45a); font-weight:700; }
.gambit-controls { display:grid; grid-template-columns:1fr 1fr; gap:7px; }
.gambit-controls .btn { min-width:0; padding:10px 5px; }
.gambit-rating-row { display:flex; align-items:center; justify-content:space-between; gap:8px; flex-wrap:wrap; margin:9px 0; }
@media(max-width:380px) { .gambit-controls { grid-template-columns:1fr 1fr; } }
'''
css_anchor = "/* Offline Opening Lab */"
replace_once(
    "app/src/main/assets/css/app.css",
    css_anchor,
    css_anchor + "\n" + css,
    "Gambit Coach and variant styles"
)

print("Gambit Coach, complete opening-book picker, three-star mastery, custom FEN, Chess960 layout, 3-Check and King of the Hill applied.")
