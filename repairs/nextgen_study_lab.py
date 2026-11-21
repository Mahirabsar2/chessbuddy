#!/usr/bin/env python3
"""Add an offline, legality-checked opening repertoire trainer to Learn."""
from pathlib import Path

def replace_once(path, old, new, label):
    p = Path(path)
    source = p.read_text(encoding="utf-8")
    if new in source:
        return
    if old not in source:
        raise SystemExit("Opening Lab patch could not find " + label + " in " + path)
    p.write_text(source.replace(old, new, 1), encoding="utf-8")

markup = r'''      <section class="card cb-opening-lab" id="openingLab" aria-label="Opening repertoire trainer">
        <div class="content-head">
          <div><span class="eyebrow">OPENING REPERTOIRE</span><h3>Opening Lab</h3></div>
          <span class="chip">OFFLINE</span>
        </div>
        <p class="muted tiny">Learn practical main lines from both sides. Every line is checked for legal moves before it is shown.</p>
        <div class="field">
          <label for="openingCourseSelect">Choose an opening</label>
          <select id="openingCourseSelect"></select>
        </div>
        <div class="opening-course-meta" id="openingCourseMeta"></div>
        <div class="opening-board-wrap"><div id="openingBoard" class="board" role="grid" aria-label="Opening study chessboard"></div></div>
        <div class="opening-step-card">
          <div class="content-head"><span class="eyebrow" id="openingMoveCount">START POSITION</span><span class="chip" id="openingCompletion">NOT STARTED</span></div>
          <b id="openingNextMove">Ready to study</b>
          <p class="muted tiny" id="openingExplanation">Choose an opening to begin the guided line.</p>
        </div>
        <div class="opening-move-list" id="openingMoveList" aria-label="Moves played in the opening line"></div>
        <div class="opening-controls">
          <button class="btn" id="btnOpeningBack" type="button" disabled>BACK</button>
          <button class="btn primary" id="btnOpeningNext" type="button">NEXT MOVE</button>
          <button class="btn" id="btnOpeningRestart" type="button">RESTART</button>
        </div>
        <p class="muted tiny" id="openingLabStatus" role="status" aria-live="polite">Opening lines are stored locally and work offline.</p>
        <div class="opening-record" id="openingRecord"></div>
        <div class="opening-explorer">
          <div class="content-head"><div><span class="eyebrow">MASTER GAME DATABASE</span><b>Opening Explorer</b></div><button class="btn small" id="btnOpeningExplore" type="button">EXPLORE</button></div>
          <p class="muted tiny">Look up master-game move choices and results from this exact position.</p>
          <div id="openingExplorerStatus" class="muted tiny" role="status" aria-live="polite">Open a position, then tap Explore.</div>
          <div id="openingExplorerResults"></div>
        </div>
      </section>'''
endgameMarkup = r'''      <section class="card cb-endgame-lab" id="endgameLab" aria-label="Endgame tablebase lab">
        <div class="content-head"><div><span class="eyebrow">ENDGAME STUDY</span><h3>Endgame Lab</h3></div><span class="chip">TABLEBASE</span></div>
        <p class="muted tiny">Load a sample or paste a FEN. ChessBuddy validates the position, then queries perfect-play tablebase results for positions with seven pieces or fewer.</p>
        <div class="field"><label for="endgamePreset">Sample position</label><select id="endgamePreset"></select></div>
        <div class="field"><label for="endgameFen">Position FEN</label><input id="endgameFen" type="text" spellcheck="false" autocapitalize="off" autocomplete="off" /></div>
        <div class="endgame-board-wrap"><div id="endgameBoard" class="board" role="grid" aria-label="Endgame tablebase board"></div></div>
        <div class="endgame-controls">
          <button class="btn" id="btnLoadEndgame" type="button">LOAD POSITION</button>
          <button class="btn primary" id="btnLookupEndgame" type="button">LOOK UP TABLEBASE</button>
          <button class="btn" id="btnPlayEndgameBest" type="button" disabled>PLAY BEST MOVE</button>
        </div>
        <div id="endgameStatus" class="notice" role="status" aria-live="polite">Choose a sample endgame or paste a FEN.</div>
        <div id="endgameResults"></div>
      </section>'''
replace_once(
    "app/src/main/assets/index.html",
    '      <div id="learnPaths"></div>',
    '      <div id="learnPaths"></div>\n' + markup + '\n' + endgameMarkup,
    "Learn page opening lab mount"
)

controller = r'''
  /* ================= Offline Opening Lab ================= */
  const OPENING_COURSES = [
    { id:'italian', name:'Italian Game', eco:'C50', side:'White & Black', level:'Beginner', focus:'Rapid development, central control and the f7 pressure point.', moves:[
      ['e2e4','Claim the center and open the bishop and queen.'],['e7e5','Black mirrors the central claim.'],['g1f3','Develop while attacking e5.'],['b8c6','Defend e5 and develop a knight.'],['f1c4','Develop the bishop toward f7.'],['f8c5','Black develops actively and contests the diagonal.'],['c2c3','Prepare d4 and build a strong center.'],['g8f6','Develop and attack e4.'],['d2d4','Challenge the center immediately.'],['e5d4','Black captures the central pawn.'],['c3d4','Recapture and establish a broad pawn center.'],['c5b4','The bishop checks along the diagonal.'],['c1d2','Block the check and develop.'],['b4d2','Black trades the active bishop.'],['b1d2','Recapture with development.']
    ]},
    { id:'ruy', name:'Ruy Lopez', eco:'C60', side:'White & Black', level:'Intermediate', focus:'Pressure on the c6-knight and long-term central play.', moves:[
      ['e2e4','Occupy the center.'],['e7e5','Contest the center.'],['g1f3','Attack e5.'],['b8c6','Defend the pawn.'],['f1b5','Pin the knight that supports e5.'],['a7a6','Ask the bishop to decide.'],['b5a4','Keep the pinning pressure.'],['g8f6','Develop and counterattack e4.'],['e1g1','Castle and secure the king.'],['f8e7','Prepare to castle.'],['f1e1','Support the e-pawn and central play.'],['b7b5','Gain space and question the bishop.'],['a4b3','Retreat to the long diagonal.'],['d7d6','Reinforce e5.'],['c2c3','Prepare d4.'],['e8g8','Black castles to safety.'],['h2h3','Give the bishop a retreat square and limit pins.']
    ]},
    { id:'sicilian', name:'Sicilian Defense · Najdorf setup', eco:'B90', side:'Black', level:'Advanced', focus:'Asymmetrical positions, queenside space and dynamic counterplay.', moves:[
      ['e2e4','White takes central space.'],['c7c5','Black challenges the center from the flank.'],['g1f3','Develop and prepare d4.'],['d7d6','Support the c5-pawn and control e5.'],['d2d4','Open the center.'],['c5d4','Capture the d-pawn.'],['f3d4','Recapture with a developed knight.'],['g8f6','Attack e4 and develop.'],['b1c3','Defend e4 and develop.'],['a7a6','The Najdorf move: prepare ...b5 and control b5.'],['c1e3','Develop and prepare queenside castling.'],['e7e5','Gain central space and question the knight.'],['d4b3','Retreat to a useful square.'],['c8e6','Develop the bishop and contest the queenside.']
    ]},
    { id:'french', name:'French Defense · Winawer structure', eco:'C15', side:'Black', level:'Intermediate', focus:'A locked center, pawn-chain strategy and piece activity.', moves:[
      ['e2e4','Claim the center.'],['e7e6','Prepare ...d5 and build a solid structure.'],['d2d4','Support the center.'],['d7d5','Challenge e4.'],['b1c3','Develop and defend e4.'],['f8b4','Pin the knight and increase pressure.'],['e4e5','Gain space and close the center.'],['c7c5','Attack the base of White’s pawn chain.'],['a2a3','Ask the bishop to decide.'],['b4c3','Trade the bishop for the knight.'],['b2c3','Recapture while opening the b-file.'],['g8e7','Develop toward f5 or g6.']
    ]},
    { id:'caro', name:'Caro-Kann Defense · Classical setup', eco:'B12', side:'Black', level:'Intermediate', focus:'A resilient pawn structure and active light-squared bishop.', moves:[
      ['e2e4','White claims central space.'],['c7c6','Prepare a supported ...d5.'],['d2d4','Build a two-pawn center.'],['d7d5','Challenge the center.'],['b1c3','Develop and defend e4.'],['d5e4','Capture the e-pawn.'],['c3e4','Recapture with the knight.'],['c8f5','Develop the bishop outside the pawn chain.'],['e4g3','Retreat while keeping central influence.'],['f5g6','Maintain the active bishop.'],['h2h4','Gain space on the kingside.'],['h7h6','Ask the pawn to clarify its intention.'],['g1f3','Develop toward the center.'],['b8d7','Develop and support future central play.']
    ]},
    { id:'qgd', name:'Queen’s Gambit Declined', eco:'D30', side:'White & Black', level:'Beginner', focus:'Central tension, piece development and a sound pawn structure.', moves:[
      ['d2d4','Claim the center.'],['d7d5','Mirror the central claim.'],['c2c4','Challenge d5 and offer the c-pawn.'],['e7e6','Support d5 and keep the center solid.'],['b1c3','Develop and increase pressure on d5.'],['g8f6','Develop and contest e4.'],['c1g5','Pin the knight to the queen.'],['f8e7','Break the pin and prepare to castle.'],['e2e3','Support the center and open the bishop.'],['e8g8','Castle to safety.'],['g1f3','Complete development.'],['h7h6','Ask the bishop to decide.'],['g5h4','Keep the bishop active.']
    ]},
    { id:'london', name:'London System', eco:'D02', side:'White', level:'Beginner', focus:'A repeatable setup with a strong light-squared bishop.', moves:[
      ['d2d4','Claim central space.'],['d7d5','Black mirrors the claim.'],['c1f4','Develop the bishop outside the pawn chain.'],['g8f6','Develop and control e4.'],['e2e3','Support the center and free the dark-squared bishop.'],['c7c5','Challenge d4.'],['c2c3','Build a stable pawn chain.'],['b8c6','Develop and increase central pressure.'],['g1f3','Develop toward the center.'],['e7e6','Support d5.'],['b1d2','Develop and reinforce e4.'],['f8d6','Challenge the active bishop.'],['f4g3','Preserve the bishop pair.'],['e8g8','Castle to safety.']
    ]},
    { id:'kingsindian', name:'King’s Indian Defense', eco:'E60', side:'Black', level:'Advanced', focus:'Allow a broad white center, then challenge it dynamically.', moves:[
      ['d2d4','White claims central space.'],['g8f6','Develop and control e4.'],['c2c4','Support the center.'],['g7g6','Prepare a fianchetto.'],['b1c3','Develop and support e4.'],['f8g7','Fianchetto the bishop toward the center.'],['e2e4','Build a broad center.'],['d7d6','Support e5 and keep the center flexible.'],['g1f3','Develop and control e5.'],['e8g8','Castle and prepare the central break.'],['f1e2','Develop and prepare to castle.'],['e7e5','Challenge the center.'],['e1g1','White castles.'],['b8c6','Develop and increase pressure on d4.'],['d4d5','Close the center and gain space.']
    ]},
    { id:'pirc', name:'Pirc Defense', eco:'B07', side:'Black', level:'Intermediate', focus:'A flexible hypermodern setup that invites a central pawn center.', moves:[
      ['e2e4','White takes central space.'],['d7d6','Keep the center flexible.'],['d2d4','Build a broad center.'],['g8f6','Attack e4 and develop.'],['b1c3','Defend e4.'],['g7g6','Prepare a kingside fianchetto.'],['c1e3','Develop and support central control.'],['f8g7','Fianchetto the bishop.'],['d1d2','Connect the rooks and prepare long castling.'],['e8g8','Castle to safety.'],['e1c1','White castles queenside.'],['c7c6','Prepare ...b5 and control d5.'],['f2f3','Support the center and prepare g4.'],['b7b5','Gain queenside space.']
    ]}
  ];
  let openingStudy = { id:'italian', snapshots:[], played:[], index:0, error:'' };
  let openingExplorerFen = '', openingExplorerBusy = false;
  const ENDGAME_PRESETS = [
    { id:'kqk', name:'King + Queen vs King', fen:'7k/8/5KQ1/8/8/8/8/8 w - - 0 1' },
    { id:'krk', name:'King + Rook vs King', fen:'7k/8/5K2/8/8/8/8/5R2 w - - 0 1' },
    { id:'kpk', name:'King + Pawn vs King', fen:'8/8/8/8/4P3/4K3/8/7k w - - 0 1' },
    { id:'kbbk', name:'King + Two Bishops vs King', fen:'7k/8/5K2/8/4B3/8/2B5/8 w - - 0 1' }
  ];
  let endgameGame = null, endgameData = null, endgameLookupFen = '';
  function openingUciMove(game, uci) {
    if (typeof uci !== 'string' || !/^[a-h][1-8][a-h][1-8][qrbn]?$/.test(uci)) throw new Error('Invalid UCI move in the opening course.');
    return game.move({ from:uci.slice(0,2), to:uci.slice(2,4), promotion:uci.length > 4 ? uci[4] : undefined });
  }
  function buildOpeningStudy(course) {
    const game = new Chess(), snapshots = [game.fen()], played = [];
    course.moves.forEach((entry, i) => {
      const move = openingUciMove(game, entry[0]);
      if (!move) throw new Error(course.name + ' has an illegal move at step ' + (i + 1) + ': ' + entry[0]);
      played.push({ san:move.san, from:move.from, to:move.to, color:move.color, note:entry[1] });
      snapshots.push(game.fen());
    });
    return { id:course.id, snapshots:snapshots, played:played, index:0, error:'' };
  }
  function openingCourse() { return OPENING_COURSES.find(c => c.id === openingStudy.id) || OPENING_COURSES[0]; }
  function renderOpeningLab() {
    const course = openingCourse(), host = $('openingBoard');
    if (!host) return;
    const game = new Chess(openingStudy.snapshots[openingStudy.index] || new Chess().fen());
    const last = openingStudy.played[openingStudy.index - 1];
    const currentFen = openingStudy.snapshots[openingStudy.index];
    Board.draw(host, game, { coords:true, last:last ? { from:last.from, to:last.to } : null });
    if (openingExplorerFen && openingExplorerFen !== currentFen) {
      openingExplorerFen = '';
      $('openingExplorerStatus').textContent = 'Position changed. Tap Explore to load fresh master-game data.';
      $('openingExplorerResults').innerHTML = '';
    }
    const total = course.moves.length, complete = openingStudy.index >= total;
    $('openingCourseSelect').value = course.id;
    $('openingCourseMeta').textContent = course.eco + ' · ' + course.level + ' · ' + course.side + ' · ' + total + ' half-moves';
    $('openingMoveCount').textContent = complete ? 'LINE COMPLETE' : openingStudy.index === 0 ? 'START POSITION' : 'MOVE ' + openingStudy.index + ' OF ' + total;
    $('openingCompletion').textContent = complete ? 'COMPLETED' : openingStudy.index ? 'IN PROGRESS' : 'NOT STARTED';
    $('openingNextMove').textContent = complete ? 'Opening line completed' : 'Next: ' + (Math.floor(openingStudy.index / 2) + 1) + (openingStudy.index % 2 ? '… ' : '. ') + (openingStudy.played[openingStudy.index] ? openingStudy.played[openingStudy.index].san : '');
    $('openingExplanation').textContent = complete ? 'You reached the end of this main line. Restart to review it again.' : openingStudy.index ? openingStudy.played[openingStudy.index - 1].note : course.focus;
    $('btnOpeningBack').disabled = openingStudy.index === 0;
    $('btnOpeningNext').disabled = complete;
    $('btnOpeningNext').textContent = complete ? 'LINE COMPLETE' : 'NEXT MOVE';
    $('openingMoveList').innerHTML = openingStudy.played.slice(0, openingStudy.index).map((m, i) =>
      '<span class="opening-move ' + (i === openingStudy.index - 1 ? 'current' : '') + '">' +
      (m.color === 'w' ? (Math.floor(i / 2) + 1) + '. ' : '') + esc(m.san) + '</span>').join(' ') ||
      '<span class="muted tiny">Move list will appear here as you advance.</span>';
    const done = settings.progress.completedOpenings || [];
    $('openingRecord').textContent = done.length + '/' + OPENING_COURSES.length + ' opening lines completed · ' + done.join(', ');
  }
  function loadOpeningCourse(id) {
    const course = OPENING_COURSES.find(c => c.id === id) || OPENING_COURSES[0];
    try {
      openingStudy = buildOpeningStudy(course);
      $('openingLabStatus').textContent = 'Validated ' + course.moves.length + ' legal half-moves. Use Next Move to step through the line.';
      renderOpeningLab();
    } catch (e) {
      openingStudy.error = e.message || 'This opening line could not be validated.';
      $('openingLabStatus').textContent = openingStudy.error;
      $('openingNextMove').textContent = 'Course validation failed';
      $('btnOpeningNext').disabled = true;
    }
  }
  function advanceOpening() {
    if (openingStudy.index >= openingStudy.played.length) return;
    openingStudy.index++;
    if (openingStudy.index === openingStudy.played.length) {
      const done = settings.progress.completedOpenings || [];
      if (done.indexOf(openingStudy.id) < 0) done.push(openingStudy.id);
      settings.progress.completedOpenings = done;
      settings.progress.openingHalfMoves = Number(settings.progress.openingHalfMoves || 0) + openingStudy.played.length;
      saveSettings();
    }
    renderOpeningLab();
  }
  function stepBackOpening() {
    if (openingStudy.index > 0) openingStudy.index--;
    renderOpeningLab();
  }
  function restartOpening() {
    openingStudy.index = 0;
    renderOpeningLab();
  }
  async function loadOpeningExplorer() {
    if (openingExplorerBusy) return;
    const fen = openingStudy.snapshots[openingStudy.index];
    if (!fen || !Lichess || typeof Lichess.explorer !== 'function') {
      $('openingExplorerStatus').textContent = 'The Lichess Masters explorer is unavailable in this build.';
      return;
    }
    openingExplorerBusy = true;
    $('btnOpeningExplore').disabled = true;
    $('openingExplorerStatus').textContent = 'Loading master-game statistics for this position…';
    try {
      const data = await Lichess.explorer(fen);
      if (openingStudy.snapshots[openingStudy.index] !== fen) return;
      const moves = Array.isArray(data && data.moves) ? data.moves.slice().sort((a,b) =>
        (Number(b.white||0)+Number(b.draws||0)+Number(b.black||0)) -
        (Number(a.white||0)+Number(a.draws||0)+Number(a.black||0))).slice(0,8) : [];
      if (!moves.length) {
        $('openingExplorerStatus').textContent = 'No master games were found for this exact position. Try an earlier move.';
        $('openingExplorerResults').innerHTML = '';
        openingExplorerFen = fen;
        return;
      }
      const games = Number(data.white||0) + Number(data.draws||0) + Number(data.black||0);
      $('openingExplorerStatus').textContent = Number(games).toLocaleString() + ' master games · Top ' + moves.length + ' continuations';
      $('openingExplorerResults').innerHTML = '<div class="opening-explorer-table">' + moves.map(m => {
        const w = Number(m.white||0), d = Number(m.draws||0), b = Number(m.black||0), n = w+d+b;
        const pct = x => n ? Math.round(x*100/n) + '%' : '—';
        return '<div class="opening-explorer-row"><b>' + esc(m.san||m.uci||'Move') + '</b><span>' + n.toLocaleString() + ' games</span><small>W ' + pct(w) + ' · D ' + pct(d) + ' · B ' + pct(b) + '</small><small>Avg. rating ' + Number(m.averageRating||0).toLocaleString() + '</small></div>';
      }).join('') + '</div>';
      openingExplorerFen = fen;
    } catch (e) {
      $('openingExplorerStatus').textContent = e.message || 'Master-game data is offline. Your opening lesson still works.';
      $('openingExplorerResults').innerHTML = '';
    } finally {
      openingExplorerBusy = false;
      $('btnOpeningExplore').disabled = false;
    }
  }
  function endgamePieceCount(fen) {
    const board = String(fen || '').trim().split(/\s+/)[0] || '';
    return board.replace(/[1-8/]/g, '').length;
  }
  function setEndgameStatus(message, kind) {
    const el = $('endgameStatus');
    if (!el) return;
    el.textContent = message;
    el.className = 'notice' + (kind ? ' ' + kind : '');
  }
  function renderEndgameBoard() {
    if (!endgameGame || !$('endgameBoard')) return;
    Board.draw($('endgameBoard'), endgameGame, { coords:true });
    const count = endgamePieceCount(endgameGame.fen());
    $('btnLookupEndgame').disabled = count > 7;
    $('btnPlayEndgameBest').disabled = !(endgameData && endgameData.moves && endgameData.moves.length);
  }
  function loadEndgamePosition(fen) {
    try {
      const game = new Chess(String(fen || '').trim());
      endgameGame = game;
      endgameData = null;
      endgameLookupFen = '';
      $('endgameFen').value = game.fen();
      $('endgameResults').innerHTML = '';
      const count = endgamePieceCount(game.fen());
      renderEndgameBoard();
      if (count > 7) setEndgameStatus('Valid chess position · ' + count + ' pieces. Tablebase lookup supports up to 7 pieces.', 'warn');
      else setEndgameStatus('Valid chess position · ' + count + ' pieces. Ready for perfect-play lookup.', 'ok');
      return true;
    } catch (e) {
      endgameGame = null; endgameData = null; endgameLookupFen = '';
      $('endgameBoard').innerHTML = '';
      $('btnLookupEndgame').disabled = true;
      $('btnPlayEndgameBest').disabled = true;
      setEndgameStatus('Invalid FEN: ' + (e.message || 'position could not be loaded.'), 'bad');
      return false;
    }
  }
  async function lookupEndgameTablebase() {
    if (!endgameGame || endgamePieceCount(endgameGame.fen()) > 7) {
      setEndgameStatus('Load a valid position with seven pieces or fewer before using the tablebase.', 'warn');
      return;
    }
    const fen = endgameGame.fen();
    $('btnLookupEndgame').disabled = true;
    setEndgameStatus('Querying the Lichess Syzygy tablebase…');
    try {
      const data = await Lichess.tablebase(fen);
      if (!endgameGame || endgameGame.fen() !== fen) return;
      if (!data || !Array.isArray(data.moves)) throw new Error('No tablebase result was returned for this position.');
      endgameData = data; endgameLookupFen = fen;
      const category = String(data.category || (data.moves[0] && data.moves[0].category) || 'unknown');
      const dtz = data.dtz == null ? '—' : String(data.dtz);
      $('endgameResults').innerHTML = '<div class="endgame-result-head"><b>Perfect-play result: ' + esc(category.toUpperCase()) + '</b><span>DTZ ' + esc(dtz) + '</span></div>' +
        '<div class="endgame-move-list">' + data.moves.slice(0,6).map((m,i) =>
          '<div class="endgame-move"><b>' + (i+1) + '. ' + esc(m.san || m.uci || 'Move') + '</b><span>' + esc(String(m.category || category)) + '</span><small>DTZ ' + esc(m.dtz == null ? '—' : String(m.dtz)) + '</small></div>'
        ).join('') + '</div>';
      setEndgameStatus('Tablebase result loaded. These results are based on perfect play for the supported endgame.', 'ok');
      $('btnPlayEndgameBest').disabled = !data.moves.length;
    } catch (e) {
      endgameData = null; endgameLookupFen = '';
      $('endgameResults').innerHTML = '';
      setEndgameStatus(e.message || 'Tablebase data is unavailable. Your saved position is unchanged.', 'warn');
      $('btnPlayEndgameBest').disabled = true;
    } finally {
      $('btnLookupEndgame').disabled = !endgameGame || endgamePieceCount(endgameGame.fen()) > 7;
    }
  }
  function playBestEndgameMove() {
    if (!endgameData || !endgameData.moves || !endgameData.moves.length || !endgameGame || endgameLookupFen !== endgameGame.fen()) return;
    const uci = String(endgameData.moves[0].uci || '');
    if (!/^[a-h][1-8][a-h][1-8][qrbn]?$/.test(uci)) {
      setEndgameStatus('The tablebase did not provide a valid best-move coordinate.', 'bad');
      return;
    }
    const move = endgameGame.move({ from:uci.slice(0,2), to:uci.slice(2,4), promotion:uci.length > 4 ? uci[4] : undefined });
    if (!move) {
      setEndgameStatus('The suggested tablebase move was not legal in this position.', 'bad');
      return;
    }
    const fen = endgameGame.fen();
    endgameData = null; endgameLookupFen = '';
    $('endgameFen').value = fen;
    $('endgameResults').innerHTML = '';
    renderEndgameBoard();
    setEndgameStatus('Played ' + move.san + '. Look up the new position to continue.', 'ok');
  }
  function populateEndgameLab() {
    const select = $('endgamePreset');
    if (!select) return;
    select.innerHTML = ENDGAME_PRESETS.map(p => '<option value="' + p.id + '">' + esc(p.name) + '</option>').join('');
    loadEndgamePosition(ENDGAME_PRESETS[0].fen);
  }
  function populateOpeningLab() {
    const select = $('openingCourseSelect');
    if (!select) return;
    select.innerHTML = OPENING_COURSES.map(c => '<option value="' + c.id + '">' + esc(c.name) + '</option>').join('');
    loadOpeningCourse(openingStudy.id);
    if (!$('endgamePreset').options.length) populateEndgameLab();
  }

'''
anchor = "  const LESSON_LEVELS = ['New to Chess','Beginner','Intermediate','Advanced'];\n"
replace_once(
    "app/src/main/assets/js/app.js",
    anchor,
    controller + anchor,
    "opening course controller insertion"
)

# Populate the selector once at boot, and bind all controls to real state transitions.
replace_once(
    "app/src/main/assets/js/app.js",
    "    $('learnPaths').addEventListener('click', e => { const b = e.target.closest('[data-lesson]'); if (b) openLearnLesson(b.getAttribute('data-lesson')); });",
    """    $('learnPaths').addEventListener('click', e => { const b = e.target.closest('[data-lesson]'); if (b) openLearnLesson(b.getAttribute('data-lesson')); });
    $('openingCourseSelect').onchange = e => loadOpeningCourse(e.target.value);
    $('btnOpeningNext').onclick = advanceOpening;
    $('btnOpeningBack').onclick = stepBackOpening;
    $('btnOpeningRestart').onclick = restartOpening;
    $('btnOpeningExplore').onclick = loadOpeningExplorer;
    $('endgamePreset').onchange = e => { const preset = ENDGAME_PRESETS.find(p => p.id === e.target.value); if (preset) loadEndgamePosition(preset.fen); };
    $('btnLoadEndgame').onclick = () => loadEndgamePosition($('endgameFen').value);
    $('btnLookupEndgame').onclick = lookupEndgameTablebase;
    $('btnPlayEndgameBest').onclick = playBestEndgameMove;""",
    "opening lab controls"
)

# Render the opening board when the Learn destination is opened.
replace_once(
    "app/src/main/assets/js/app.js",
    "    if (name === 'learn') renderLearn();",
    "    if (name === 'learn') { renderLearn(); if (!$('openingCourseSelect').options.length) populateOpeningLab(); else renderOpeningLab(); }",
    "opening lab tab lifecycle"
)

css = r'''
/* Offline Opening Lab */
.cb-opening-lab { margin-top:14px; }
.opening-course-meta { color:var(--muted); font-size:12px; margin:8px 0 12px; }
.opening-board-wrap { width:min(100%,360px); margin:12px auto; }
#openingBoard { width:100%; max-width:360px; aspect-ratio:1; }
.opening-step-card { padding:12px; border-radius:12px; background:var(--surface2); margin:10px 0; }
.opening-step-card>b { display:block; margin:5px 0; font-size:16px; }
.opening-step-card p { margin:5px 0 0; }
.opening-move-list { display:flex; flex-wrap:wrap; gap:5px; min-height:24px; margin:10px 0; }
.opening-move { padding:4px 7px; border-radius:6px; background:var(--surface2); font-size:12px; }
.opening-move.current { outline:1px solid var(--accent,#c5a45a); font-weight:700; }
.opening-controls { display:grid; grid-template-columns:1fr 1.3fr 1fr; gap:7px; }
.opening-controls .btn { min-width:0; padding:10px 5px; }
.opening-record { margin-top:9px; color:var(--muted); font-size:11px; overflow-wrap:anywhere; }
.cb-endgame-lab { margin-top:14px; }
.endgame-board-wrap { width:min(100%,320px); margin:12px auto; }
#endgameBoard { width:100%; max-width:320px; aspect-ratio:1; }
.endgame-controls { display:grid; grid-template-columns:1fr 1fr; gap:7px; }
.endgame-controls #btnPlayEndgameBest { grid-column:1/-1; }
.endgame-controls .btn { min-width:0; padding:10px 5px; }
.endgame-result-head { display:flex; justify-content:space-between; gap:8px; flex-wrap:wrap; padding:10px; margin:10px 0 7px; border-radius:10px; background:var(--surface2); }
.endgame-move-list { display:grid; gap:6px; }
.endgame-move { display:grid; grid-template-columns:1fr auto; gap:3px 8px; padding:9px 10px; border-radius:9px; background:var(--surface2); }
.endgame-move span,.endgame-move small { color:var(--muted); font-size:11px; text-align:right; }
.endgame-move small { grid-column:1/-1; text-align:left; }
.opening-explorer { margin-top:14px; padding-top:12px; border-top:1px solid var(--border,#ffffff18); }
.opening-explorer-table { display:grid; gap:6px; margin-top:9px; }
.opening-explorer-row { display:grid; grid-template-columns:1fr auto; gap:3px 10px; align-items:center; padding:9px 10px; border-radius:9px; background:var(--surface2); min-width:0; }
.opening-explorer-row b { font-size:14px; }
.opening-explorer-row span,.opening-explorer-row small { color:var(--muted); font-size:11px; text-align:right; }
.opening-explorer-row small:first-of-type { grid-column:1/-1; text-align:left; }
'''
p = Path("app/src/main/assets/css/app.css")
css_source = p.read_text(encoding="utf-8")
if "/* Offline Opening Lab */" not in css_source:
    p.write_text(css_source + "\n" + css, encoding="utf-8")

print("Offline Opening Lab added with eight validated main-line courses, reversible navigation and saved completion records.")
