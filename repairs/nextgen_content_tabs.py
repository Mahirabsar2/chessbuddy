from pathlib import Path

def replace_once(path, old, new, label):
    p = Path(path)
    s = p.read_text(encoding="utf-8")
    if new in s:
        return
    if old not in s:
        raise SystemExit("Core tabs patch could not find " + label + " in " + path)
    p.write_text(s.replace(old, new, 1), encoding="utf-8")

# The public Lichess API exposes a daily puzzle and TV channel index without credentials.
replace_once(
    "app/src/main/assets/js/lichess.js",
    """    function tablebase(fen) {
      return request('https://tablebase.lichess.org/standard?fen=' + encodeURIComponent(fen), 'tablebase:' + fen);
    }
    return { explorer: explorer, tablebase: tablebase, clearCache: function () { cache.clear(); } };
""",
    """    function tablebase(fen) {
      return request('https://tablebase.lichess.org/standard?fen=' + encodeURIComponent(fen), 'tablebase:' + fen);
    }
    function dailyPuzzle() { return request('https://lichess.org/api/puzzle/daily', 'puzzle:daily'); }
    function tvChannels() { return request('https://lichess.org/api/tv/channels', 'tv:channels'); }
    return { explorer: explorer, tablebase: tablebase, dailyPuzzle: dailyPuzzle, tvChannels: tvChannels, clearCache: function () { cache.clear(); } };
""",
    "Lichess API methods"
)

# Main navigation gets five real sections. Coach, Archive and Settings remain reachable from More.
replace_once(
    "app/src/main/assets/index.html",
    """  </main>

  <nav class="tabbar" aria-label="Main navigation">
    <button class="tab active" data-tab="play" type="button"><span data-ic="tPlay"></span><i>Play</i></button>
    <button class="tab" data-tab="coach" type="button"><span data-ic="tCoach"></span><i>Coach</i></button>
    <button class="tab" data-tab="history" type="button"><span data-ic="tHist"></span><i>Archive</i></button>
    <button class="tab" data-tab="settings" type="button"><span data-ic="tSet"></span><i>Settings</i></button>
  </nav>
""",
    """    <!-- ================= PUZZLES ================= -->
    <section id="view-puzzles" class="view" aria-label="Puzzles">
      <div class="content-hero"><span class="eyebrow">TACTICS STUDIO</span><h1>Puzzles</h1><p>Train pattern recognition with the official Lichess daily puzzle.</p></div>
      <div class="card">
        <div class="content-head"><div><span class="eyebrow">DAILY CHALLENGE</span><h3>Today's Puzzle</h3></div><span class="chip" id="puzzleRating">Not loaded</span></div>
        <p class="muted tiny" id="puzzleThemes">Load today's position to begin. Your moves are checked against the puzzle's published solution.</p>
        <div class="puzzle-board-wrap"><div id="puzzleBoard" class="board" role="grid" aria-label="Daily puzzle chessboard"></div></div>
        <div id="puzzleStatus" class="notice" role="status" aria-live="polite">Ready when you are.</div>
        <div class="puzzle-actions">
          <button class="btn primary" id="btnDailyPuzzle" type="button">Load Daily Puzzle</button>
          <button class="btn" id="btnPuzzleHint" type="button" disabled>Hint</button>
          <button class="btn" id="btnPuzzleReset" type="button" disabled>Reset</button>
        </div>
      </div>
      <div class="card"><h3>Training Progress</h3><div class="stat-strip"><div><b id="puzzlesSolvedCount">0</b><span>Puzzles Solved</span></div><div><b id="puzzleLessonsCount">0</b><span>Lessons Completed</span></div></div><p class="muted tiny">Puzzle history and ratings will remain local until a signed-in puzzle profile service is connected.</p></div>
    </section>

    <!-- ================= LEARN ================= -->
    <section id="view-learn" class="view" aria-label="Learn">
      <div class="content-hero learn-hero"><span class="eyebrow">IMPROVE YOUR CHESS</span><h1>Learn</h1><p>Short, structured lessons from first moves to advanced strategy. Your completed lessons are saved on this device.</p></div>
      <div class="learn-progress"><div><b id="learnProgressText">0 lessons completed</b><span class="muted tiny">Your learning path</span></div><div class="progress-track"><div id="learnProgressBar"></div></div></div>
      <div id="learnPaths"></div>
    </section>

    <!-- ================= WATCH ================= -->
    <section id="view-watch" class="view" aria-label="Watch">
      <div class="content-hero watch-hero"><span class="eyebrow">LIVE CHESS</span><h1>Watch</h1><p>Browse current public Lichess TV games and open a live board.</p></div>
      <div class="card">
        <div class="content-head"><div><span class="eyebrow">LIVE CHANNELS</span><h3>Playing Now</h3></div><button class="btn small" id="btnWatchRefresh" type="button">Refresh</button></div>
        <div id="watchStatus" class="muted tiny" role="status" aria-live="polite">Loading public TV channels…</div>
        <div id="watchChannels" class="watch-grid"></div>
      </div>
      <div class="card"><h3>Streams and events</h3><p class="muted tiny">The live channel list is supplied by Lichess. Tournament broadcasts and creator streams will be added as separate, verified feeds rather than invented entries.</p></div>
    </section>

    <!-- ================= MORE ================= -->
    <section id="view-more" class="view" aria-label="More">
      <div class="content-hero more-hero"><span class="eyebrow">YOUR CHESSBUDDY</span><h1>More</h1><p>Profile, performance, social play and app controls.</p></div>
      <div class="card">
        <div class="content-head"><div><span class="eyebrow">PLAYER PROFILE</span><h3 id="moreProfileName">Local Player</h3></div><span class="chip" id="moreAccountState">Offline</span></div>
        <p class="muted tiny" id="moreProfileSub">Sign in from Play Online to sync your player profile.</p>
        <div class="stat-strip"><div><b id="moreGames">0</b><span>Games</span></div><div><b id="moreWins">0</b><span>Wins</span></div><div><b id="moreLessons">0</b><span>Lessons</span></div></div>
      </div>
      <div class="card"><h3>Player Hub</h3>
        <button class="row-btn" id="moreOnline" type="button"><span class="ri" data-ic="users"></span><span class="rt"><b>Friends &amp; Online Play</b><small>Find players, manage challenges and view your online profile</small></span><span class="rc" data-ic="chev"></span></button>
        <button class="row-btn" id="moreCoach" type="button"><span class="ri" data-ic="spark"></span><span class="rt"><b>Coach &amp; Game Analysis</b><small>Review games, ask questions and explore positions</small></span><span class="rc" data-ic="chev"></span></button>
        <button class="row-btn" id="moreArchive" type="button"><span class="ri" data-ic="tHist"></span><span class="rt"><b>Game Archive</b><small>Replay, import, export and manage saved games</small></span><span class="rc" data-ic="chev"></span></button>
        <button class="row-btn" id="moreSettings" type="button"><span class="ri" data-ic="tSet"></span><span class="rt"><b>Settings &amp; Updates</b><small>Engines, board, sound, storage, privacy and updates</small></span><span class="rc" data-ic="chev"></span></button>
      </div>
      <div class="card"><h3>Achievements</h3><p class="muted tiny">Your local game and lesson progress is counted above. Verified badges and cross-device leaderboards will be enabled when the achievement service is added.</p></div>
    </section>
  </main>

  <nav class="tabbar" aria-label="Main navigation">
    <button class="tab active" data-tab="play" type="button"><span data-ic="tPlay"></span><i>Play</i></button>
    <button class="tab" data-tab="puzzles" type="button"><span data-ic="tPuzzle"></span><i>Puzzles</i></button>
    <button class="tab" data-tab="learn" type="button"><span data-ic="tLearn"></span><i>Learn</i></button>
    <button class="tab" data-tab="watch" type="button"><span data-ic="tWatch"></span><i>Watch</i></button>
    <button class="tab" data-tab="more" type="button"><span data-ic="tMore"></span><i>More</i></button>
  </nav>
""",
    "five-tab navigation markup"
)

# Make the new tab icon paths part of the app's original icon set.
replace_once(
    "app/src/main/assets/js/app.js",
    """    tCoach: '<path d="M12 3l2.1 5.6L20 11l-5.9 2.4L12 19l-2.1-5.6L4 11l5.9-2.4z" fill="currentColor"/>',
""",
    """    tPuzzle: '<path d="M9 4a2.5 2.5 0 1 1 4.9.7H17a2 2 0 0 1 2 2v3.1a2.5 2.5 0 1 1 0 4.9V18a2 2 0 0 1-2 2h-3.2a2.5 2.5 0 1 0-4.9 0H6a2 2 0 0 1-2-2v-3.2a2.5 2.5 0 1 0 0-4.9V6a2 2 0 0 1 2-2z"/>',
    tLearn: '<path d="M3 5.5c3.1-1.2 6.1-.9 9 1v13c-2.9-1.9-5.9-2.2-9-1zM21 5.5c-3.1-1.2-6.1-.9-9 1v13c2.9-1.9 5.9-2.2 9-1z"/>',
    tWatch: '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m10 9 5 3-5 3z" fill="currentColor"/>',
    tMore: '<circle cx="5" cy="5" r="1.6" fill="currentColor"/><circle cx="12" cy="5" r="1.6" fill="currentColor"/><circle cx="19" cy="5" r="1.6" fill="currentColor"/><circle cx="5" cy="12" r="1.6" fill="currentColor"/><circle cx="12" cy="12" r="1.6" fill="currentColor"/><circle cx="19" cy="12" r="1.6" fill="currentColor"/><circle cx="5" cy="19" r="1.6" fill="currentColor"/><circle cx="12" cy="19" r="1.6" fill="currentColor"/><circle cx="19" cy="19" r="1.6" fill="currentColor"/>',
    tCoach: '<path d="M12 3l2.1 5.6L20 11l-5.9 2.4L12 19l-2.1-5.6L4 11l5.9-2.4z" fill="currentColor"/>',
""",
    "navigation icons"
)

replace_once(
    "app/src/main/assets/js/app.js",
    "  const TAB_TITLES = { coach: 'Coach', history: 'Archive', settings: 'Settings' };",
    "  const TAB_TITLES = { puzzles: 'Puzzles', learn: 'Learn', watch: 'Watch', more: 'More', coach: 'Coach', history: 'Archive', settings: 'Settings' };",
    "tab titles"
)

replace_once(
    "app/src/main/assets/js/app.js",
    """    document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.getAttribute('data-tab') === name));
    if (name === 'coach') { renderCoachSettings(); renderCoachMini(); renderCoachBar(); }
    if (name === 'history') renderHistory();
    if (name === 'settings') renderSettings();
""",
    """    const navTab = ['coach', 'history', 'settings'].indexOf(name) >= 0 ? 'more' : name;
    document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.getAttribute('data-tab') === navTab));
    if (name === 'coach') { renderCoachSettings(); renderCoachMini(); renderCoachBar(); }
    if (name === 'history') renderHistory();
    if (name === 'settings') renderSettings();
    if (name === 'puzzles') { renderPuzzleProgress(); if (!puzzleSession && !puzzleLoading) loadDailyPuzzle(); }
    if (name === 'learn') renderLearn();
    if (name === 'watch') renderWatch();
    if (name === 'more') renderMore();
""",
    "tab routing"
)

# A native external-link bridge is restricted to the official Lichess TV and game paths.
replace_once(
    "app/src/main/java/com/chessbuddy/NativeBridge.java",
    """        return true;
    }

    @JavascriptInterface
    public void logEvent(String event, String detail) {
""",
    """        return true;
    }

    /** Open only official public Lichess TV or game pages from an explicit user tap. */
    @JavascriptInterface
    public boolean openExternalUrl(final String raw) {
        if (raw == null || raw.length() > 1024) return false;
        final Uri uri;
        try { uri = Uri.parse(raw); } catch (Exception e) { return false; }
        String path = uri.getPath();
        boolean allowedPath = path != null && ("/tv".equals(path) || path.startsWith("/tv/")
            || path.matches("^/game/[A-Za-z0-9]{6,16}$"));
        if (!"https".equalsIgnoreCase(uri.getScheme()) || !"lichess.org".equalsIgnoreCase(uri.getHost())
            || uri.getUserInfo() != null || uri.getPort() != -1 || !allowedPath) return false;
        main.post(new Runnable() { @Override public void run() {
            try { activity.startActivity(new Intent(Intent.ACTION_VIEW, uri)); }
            catch (Exception e) { diagnostics.log("WARN", "external.open_failed", "Could not open the Lichess page"); }
        } });
        return true;
    }

    @JavascriptInterface
    public void logEvent(String event, String detail) {
""",
    "safe Lichess browser bridge"
)

replace_once(
    "app/src/main/assets/js/native.js",
    """    openAuthUrl: function (url) { return call('openAuthUrl', [String(url || '')], false) === true; },
""",
    """    openAuthUrl: function (url) { return call('openAuthUrl', [String(url || '')], false) === true; },
    openExternalUrl: function (url) { return call('openExternalUrl', [String(url || '')], false) === true; },
""",
    "native external URL adapter"
)

# Original, device-saved learning path.
learn = [
  {"id":"board-coordinates","level":"New to Chess","title":"The Board and Coordinates","duration":"4 min","text":"A chessboard has eight files (a–h) and eight ranks (1–8). Every square has one coordinate, such as e4 or b7. White starts at the bottom with a light square on h1.","takeaways":["Files run from left to right as a, b, c, d, e, f, g, h.","Ranks run from White's side to Black's side, 1 through 8.","The board is correctly oriented when each player's right-hand corner is light."]},
  {"id":"piece-moves","level":"New to Chess","title":"How the Pieces Move","duration":"6 min","text":"Rooks move along ranks and files. Bishops move diagonally. Queens combine both. Knights jump in an L-shape. Kings move one square, and pawns move forward but capture diagonally.","takeaways":["A knight can jump over pieces.","Pawns promote when they reach the final rank.","Kings are never legally allowed to move into check."]},
  {"id":"check-checkmate","level":"New to Chess","title":"Check and Checkmate","duration":"5 min","text":"Check means the king is under attack. A player must answer check by moving the king, capturing the attacker, or blocking the attack. Checkmate means no legal answer exists.","takeaways":["You cannot ignore check.","Stalemate is a draw, not a win.","A king cannot be captured; the game ends at checkmate."]},
  {"id":"center","level":"Beginner","title":"Control the Center","duration":"5 min","text":"The central squares e4, d4, e5 and d5 influence movement across the board. A central pawn move can claim space and open lines for your pieces.","takeaways":["Fight for central squares early.","Central pieces often have more useful options.","Do not chase pawns while your pieces remain undeveloped."]},
  {"id":"development","level":"Beginner","title":"Develop Your Pieces","duration":"6 min","text":"Bring knights and bishops into the game, usually toward active squares. Avoid moving the same piece repeatedly in the opening unless there is a concrete reason.","takeaways":["Develop minor pieces before launching an attack.","Castle to improve king safety.","Connect your rooks by developing the back rank."]},
  {"id":"forks","level":"Intermediate","title":"Knight Forks","duration":"5 min","text":"A fork is one move that attacks two or more targets at once. Knights are especially good at forks because their attack pattern is difficult to block.","takeaways":["Look for checks that also attack a queen or rook.","Count the opponent's legal replies after a fork.","Before playing a fork, check whether your knight can be captured."]},
  {"id":"pins","level":"Intermediate","title":"Pins and Skewers","duration":"6 min","text":"A pin attacks a piece that cannot or should not move because a more valuable piece stands behind it. A skewer attacks a valuable piece first, then wins a less valuable target behind it.","takeaways":["Absolute pins involve the king.","Relative pins can still be tactically powerful.","Move the front target and recalculate the line."]},
  {"id":"endgame-kpk","level":"Advanced","title":"King and Pawn Endgames","duration":"7 min","text":"In king and pawn endgames, the king becomes an active piece. Opposition, the square rule and pawn promotion races often decide the result.","takeaways":["Activate your king.","Use opposition to gain access to key squares.","Calculate whether the king can catch a passed pawn."]},
  {"id":"rook-activity","level":"Advanced","title":"Active Rooks","duration":"6 min","text":"Rooks belong on open files and behind passed pawns. Activity often matters more than winning a pawn that leaves your rook passive.","takeaways":["Place rooks on open or semi-open files.","A rook behind a passed pawn can support its advance.","Coordinate rooks before trading into a pawn ending."]}
]
import json
learn_json = json.dumps(learn, ensure_ascii=False)

js = """
  /* ================= Next Gen content tabs ================= */
  const LEARN_LESSONS = __LEARN_JSON__;
  let puzzleSession = null, puzzleLoading = false, watchChannels = null, watchLoading = false;

  function renderPuzzleProgress() {
    const done = Number(settings.progress.puzzlesSolved || 0);
    if ($('puzzlesSolvedCount')) $('puzzlesSolvedCount').textContent = String(done);
    if ($('puzzleLessonsCount')) $('puzzleLessonsCount').textContent = String((settings.progress.completedLessons || []).length);
  }
  function puzzleStatus(text, kind) {
    const el = $('puzzleStatus');
    if (!el) return;
    el.textContent = text;
    el.className = 'notice' + (kind ? ' ' + kind : '');
  }
  function renderPuzzleBoard() {
    const ps = puzzleSession, host = $('puzzleBoard');
    if (!ps || !host) return;
    const legal = {}, caps = {};
    if (ps.selected) {
      ps.game.moves({ square: ps.selected, verbose: true }).forEach(m => {
        legal[m.to] = true; if (m.captured) caps[m.to] = true;
      });
    }
    Board.draw(host, ps.game, { selected: ps.selected, legal: legal, captures: caps,
      last: ps.lastMove || null, hint: ps.hintMove || null, coords: true });
    Board.arrow(host, ps.hintMove && ps.hintMove.from, ps.hintMove && ps.hintMove.to, false);
    $('btnPuzzleHint').disabled = ps.completed || !ps.solution.length;
    $('btnPuzzleReset').disabled = false;
  }
  async function loadDailyPuzzle() {
    if (puzzleLoading) return;
    puzzleLoading = true;
    $('btnDailyPuzzle').disabled = true;
    puzzleStatus('Connecting to the Lichess daily puzzle feed…');
    try {
      const data = await Lichess.dailyPuzzle();
      if (!data || !data.puzzle || !data.puzzle.fen || !Array.isArray(data.puzzle.solution) || !data.puzzle.solution.length)
        throw new Error('The daily puzzle response is incomplete.');
      const game = new Chess(data.puzzle.fen);
      const pz = data.puzzle;
      puzzleSession = { data: data, game: game, solution: pz.solution.slice(), index: 0,
        selected: null, hintMove: null, lastMove: pz.lastMove ? { from: pz.lastMove.slice(0,2), to: pz.lastMove.slice(2,4) } : null,
        completed: false, originalFen: pz.fen };
      $('puzzleRating').textContent = 'Rating ' + pz.rating;
      $('puzzleThemes').textContent = (pz.themes || []).map(t => t.replace(/-/g, ' ')).join(' · ') + ' · ' + Number(pz.plays || 0).toLocaleString() + ' plays';
      puzzleStatus('Find the best move for ' + (game.turn() === 'w' ? 'White' : 'Black') + '.');
      renderPuzzleBoard();
    } catch (e) {
      puzzleStatus(e.message || 'Could not load the daily puzzle. Check your connection and retry.', 'bad');
    } finally {
      puzzleLoading = false;
      $('btnDailyPuzzle').disabled = false;
      $('btnDailyPuzzle').textContent = puzzleSession ? 'Reload Daily Puzzle' : 'Try Again';
    }
  }
  function applyPuzzleUci(ps, uci) {
    if (!/^[a-h][1-8][a-h][1-8][qrbn]?$/.test(uci)) throw new Error('The puzzle feed contained an invalid move.');
    const m = ps.game.move({ from: uci.slice(0,2), to: uci.slice(2,4), promotion: uci.length > 4 ? uci[4] : undefined });
    if (!m) throw new Error('The published puzzle line is not legal in this position.');
    ps.lastMove = { from: uci.slice(0,2), to: uci.slice(2,4) };
  }
  function puzzleBoardTap(event) {
    const ps = puzzleSession;
    const square = event.target && event.target.closest ? event.target.closest('.sq[data-sq]') : null;
    if (!ps || ps.completed || !square) return;
    const sq = square.getAttribute('data-sq'), piece = ps.game.get(sq), turn = ps.game.turn();
    if (!ps.selected) {
      if (piece && piece.color === turn) { ps.selected = sq; ps.hintMove = null; renderPuzzleBoard(); }
      return;
    }
    if (piece && piece.color === turn && sq !== ps.selected) { ps.selected = sq; renderPuzzleBoard(); return; }
    const expected = ps.solution[ps.index], from = ps.selected;
    if (!expected || expected.slice(0,2) !== from || expected.slice(2,4) !== sq) {
      puzzleStatus('Not quite. Check the forcing moves and try again.', 'warn');
      ps.selected = null; renderPuzzleBoard(); return;
    }
    try {
      applyPuzzleUci(ps, expected);
      ps.index++;
      // The opponent's published reply is automatic; the player chooses the next side-to-move solution.
      if (ps.index < ps.solution.length) {
        const reply = ps.solution[ps.index];
        applyPuzzleUci(ps, reply);
        ps.index++;
      }
      ps.selected = null; ps.hintMove = null;
      if (ps.index >= ps.solution.length) {
        ps.completed = true;
        settings.progress.puzzlesSolved = Number(settings.progress.puzzlesSolved || 0) + 1;
        saveSettings(); renderPuzzleProgress();
        puzzleStatus('Puzzle solved. Great work — your progress has been saved on this device.', 'ok');
      } else puzzleStatus('Correct. Find the next move.');
      renderPuzzleBoard();
    } catch (e) { puzzleStatus(e.message || 'The puzzle line could not be applied.', 'bad'); }
  }
  function hintDailyPuzzle() {
    const ps = puzzleSession;
    if (!ps || ps.completed || !ps.solution[ps.index]) return;
    const uci = ps.solution[ps.index];
    ps.hintMove = { from: uci.slice(0,2), to: uci.slice(2,4) };
    ps.selected = null;
    puzzleStatus('Hint: look at the piece on ' + ps.hintMove.from + '. The arrow shows a candidate destination.', 'warn');
    renderPuzzleBoard();
  }
  function resetDailyPuzzle() {
    const ps = puzzleSession;
    if (!ps) return;
    ps.game = new Chess(ps.originalFen); ps.index = 0; ps.selected = null; ps.hintMove = null; ps.completed = false;
    ps.lastMove = ps.data.puzzle.lastMove ? { from: ps.data.puzzle.lastMove.slice(0,2), to: ps.data.puzzle.lastMove.slice(2,4) } : null;
    puzzleStatus('Puzzle reset. Find the best move for ' + (ps.game.turn() === 'w' ? 'White' : 'Black') + '.');
    renderPuzzleBoard();
  }

  const LESSON_LEVELS = ['New to Chess','Beginner','Intermediate','Advanced'];
  function renderLearn() {
    const complete = settings.progress.completedLessons || [], host = $('learnPaths');
    if (!host) return;
    $('learnProgressText').textContent = complete.length + ' of ' + LEARN_LESSONS.length + ' lessons completed';
    $('learnProgressBar').style.width = (100 * complete.length / LEARN_LESSONS.length) + '%';
    host.innerHTML = LESSON_LEVELS.map(level => {
      const lessons = LEARN_LESSONS.filter(l => l.level === level);
      return '<div class=\"learn-level\"><div class=\"content-head\"><h3>' + esc(level) + '</h3><span class=\"muted tiny\">' + lessons.filter(l => complete.indexOf(l.id) >= 0).length + '/' + lessons.length + ' complete</span></div>' +
        lessons.map(l => '<button class=\"learn-lesson\" type=\"button\" data-lesson=\"' + l.id + '\"><span class=\"lesson-index\">' + (complete.indexOf(l.id) >= 0 ? '✓' : '♟') + '</span><span class=\"lesson-copy\"><b>' + esc(l.title) + '</b><small>' + esc(l.duration) + ' · ' + esc(l.level) + '</small></span><span class=\"lesson-chevron\">›</span></button>').join('') + '</div>';
    }).join('');
  }
  function openLearnLesson(id) {
    const l = LEARN_LESSONS.find(x => x.id === id);
    if (!l) return;
    const done = (settings.progress.completedLessons || []).indexOf(l.id) >= 0;
    openModal('<div class=\"lesson-modal\"><span class=\"eyebrow\">' + esc(l.level) + ' · ' + esc(l.duration) + '</span><h3>' + esc(l.title) + '</h3><p>' + esc(l.text) + '</p><h4>Key Ideas</h4><ul>' + l.takeaways.map(x => '<li>' + esc(x) + '</li>').join('') + '</ul><div class=\"controls\"><button class=\"btn primary\" id=\"btnLessonComplete\" type=\"button\">' + (done ? 'Completed' : 'Mark Complete') + '</button><button class=\"btn\" id=\"btnLessonClose\" type=\"button\">Close</button></div></div>');
    $('btnLessonClose').onclick = closeModal;
    $('btnLessonComplete').onclick = () => {
      settings.progress.completedLessons = settings.progress.completedLessons || [];
      if (settings.progress.completedLessons.indexOf(l.id) < 0) settings.progress.completedLessons.push(l.id);
      saveSettings(); renderLearn(); renderPuzzleProgress(); closeModal(); toast('Lesson progress saved');
    };
  }

  async function loadWatchChannels() {
    if (watchLoading) return;
    watchLoading = true;
    $('watchStatus').textContent = 'Updating live Lichess TV channels…';
    try {
      watchChannels = await Lichess.tvChannels();
      renderWatch();
    } catch (e) {
      $('watchStatus').textContent = e.message || 'Live channels are temporarily unavailable.';
    } finally { watchLoading = false; }
  }
  function renderWatch() {
    const host = $('watchChannels');
    if (!host) return;
    if (!watchChannels) { if (!watchLoading) loadWatchChannels(); return; }
    const keys = ['best','bullet','blitz','rapid','classical','computer','bot','ultraBullet','chess960'];
    const items = keys.filter(k => watchChannels[k] && watchChannels[k].gameId);
    $('watchStatus').textContent = items.length + ' live public channels · supplied by Lichess';
    host.innerHTML = items.map(k => {
      const item = watchChannels[k], user = item.user || {};
      return '<div class=\"watch-channel\"><div><span class=\"eyebrow\">' + esc(k.replace(/([A-Z])/g,' $1')) + '</span><b>' + esc(user.name || user.id || 'Featured player') + '</b><small>' + Number(item.rating || 0).toLocaleString() + ' rating · ' + esc(item.color || 'playing') + '</small></div><button class=\"btn small\" type=\"button\" data-watch-channel=\"' + esc(k) + '\">Watch Live</button></div>';
    }).join('') || '<p class=\"muted tiny\">No featured games are available at the moment. Refresh to check again.</p>';
  }
  function renderMore() {
    const list = lsGet(K_GAMES, []), wins = list.filter(g => g.human && g.result === (g.human === 'w' ? '1-0' : '0-1')).length;
    $('moreGames').textContent = String(list.length);
    $('moreWins').textContent = String(wins);
    $('moreLessons').textContent = String((settings.progress.completedLessons || []).length);
    $('moreAccountState').textContent = Online.signedIn() ? 'Signed In' : 'Offline';
    $('moreProfileName').textContent = 'Local Player';
    $('moreProfileSub').textContent = Online.signedIn() ? 'Loading your synced player profile…' : 'Sign in from Play Online to sync your player profile.';
    if (Online.signedIn()) {
      Online.profile().then(p => {
        if (currentTab !== 'more') return;
        $('moreProfileName').textContent = p && (p.display_name || p.username) || 'Player Profile';
        $('moreProfileSub').textContent = p && p.username ? '@' + p.username : 'Your profile is ready.';
      }).catch(() => { if (currentTab === 'more') $('moreProfileSub').textContent = 'Profile could not be loaded. Refresh Online Play to retry.'; });
    }
  }
"""
js = js.replace("__LEARN_JSON__", learn_json)

replace_once(
    "app/src/main/assets/js/app.js",
    "  let availableAppUpdate = null;",
    js + "\n  let availableAppUpdate = null;",
    "content tab controllers"
)

# Bind only the new real controls; every button has a concrete handler.
replace_once(
    "app/src/main/assets/js/app.js",
    """    bindBoardInput();
    $('btnMenu').onclick = openMenu; $('btnAnalysis').onclick = () => openReview();
""",
    """    bindBoardInput();
    $('puzzleBoard').addEventListener('click', puzzleBoardTap);
    $('btnDailyPuzzle').onclick = loadDailyPuzzle;
    $('btnPuzzleHint').onclick = hintDailyPuzzle;
    $('btnPuzzleReset').onclick = resetDailyPuzzle;
    $('learnPaths').addEventListener('click', e => { const b = e.target.closest('[data-lesson]'); if (b) openLearnLesson(b.getAttribute('data-lesson')); });
    $('btnWatchRefresh').onclick = () => { watchChannels = null; loadWatchChannels(); };
    $('watchChannels').addEventListener('click', e => {
      const b = e.target.closest('[data-watch-channel]'); if (!b) return;
      const channel = b.getAttribute('data-watch-channel');
      if (!Native.openExternalUrl('https://lichess.org/tv/' + encodeURIComponent(channel))) toast('Could not open the Lichess TV page.');
    });
    $('moreOnline').onclick = () => { showTab('play'); showPlayScreen('online'); };
    $('moreCoach').onclick = () => showTab('coach');
    $('moreArchive').onclick = () => showTab('history');
    $('moreSettings').onclick = () => showTab('settings');
    $('btnMenu').onclick = openMenu; $('btnAnalysis').onclick = () => openReview();
""",
    "new page event handlers"
)

# 5-column tab bar plus responsive layouts for the new pages.
css = """
/* Next Gen main navigation and content modules */
.tabbar { grid-template-columns:repeat(5,minmax(0,1fr)); }
.tab { min-width:0; padding:5px 1px; }
.tab svg { width:23px; height:23px; }
.tab i { font-size:10px; white-space:nowrap; }
.content-hero { padding:20px 18px; margin:10px 0 14px; border-radius:16px; background:linear-gradient(135deg,#334a2a,#262f24); border:1px solid #ffffff12; }
.content-hero h1 { margin:4px 0 6px; }
.content-hero p { color:#d0d9c8; margin:0; font-size:13px; max-width:38ch; }
.learn-hero { background:linear-gradient(135deg,#38475e,#272f3c); }
.watch-hero { background:linear-gradient(135deg,#493b5b,#2f2938); }
.more-hero { background:linear-gradient(135deg,#4c4730,#302e25); }
.content-head { display:flex; align-items:center; justify-content:space-between; gap:10px; margin-bottom:8px; }
.content-head h3 { margin:0; }
.puzzle-board-wrap { width:min(100%,360px); margin:12px auto; }
#puzzleBoard { width:100%; max-width:360px; aspect-ratio:1; }
.puzzle-actions { display:grid; grid-template-columns:minmax(0,1.6fr) repeat(2,minmax(0,1fr)); gap:8px; }
.puzzle-actions .btn { min-width:0; padding:8px 7px; font-size:12px; }
.stat-strip { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:8px; text-align:center; margin:10px 0 2px; }
.stat-strip>div { background:var(--surface2); border-radius:10px; padding:10px 5px; min-width:0; }
.stat-strip b { display:block; font-size:20px; font-variant-numeric:tabular-nums; }
.stat-strip span { display:block; font-size:10px; color:var(--muted); }
.learn-progress { background:var(--surface); padding:12px; border-radius:12px; margin-bottom:12px; }
.learn-progress>div:first-child { display:flex; justify-content:space-between; gap:8px; flex-wrap:wrap; }
.progress-track { height:7px; background:var(--line); border-radius:99px; overflow:hidden; margin-top:9px; }
.progress-track>div { height:100%; width:0; background:var(--green); border-radius:99px; transition:width .2s; }
.learn-level { margin:16px 2px; }
.learn-lesson { width:100%; border:1px solid var(--line); border-radius:12px; background:var(--surface); color:var(--text); display:flex; gap:11px; align-items:center; text-align:left; padding:11px; margin:7px 0; min-width:0; }
.lesson-index { width:32px; height:32px; display:grid; place-items:center; border-radius:9px; flex:none; background:var(--surface2); color:var(--green); font-weight:900; }
.lesson-copy { flex:1; min-width:0; }
.lesson-copy b,.lesson-copy small { display:block; overflow-wrap:anywhere; }
.lesson-copy small { color:var(--muted); font-size:11px; margin-top:2px; }
.lesson-chevron { font-size:22px; color:var(--muted); }
.lesson-modal p { line-height:1.6; }
.lesson-modal ul { padding-left:20px; color:#d8d6d2; }
.lesson-modal li { margin:7px 0; }
.watch-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:9px; margin-top:10px; }
.watch-channel { min-width:0; display:flex; flex-direction:column; justify-content:space-between; gap:10px; background:var(--surface2); border-radius:11px; padding:11px; }
.watch-channel>div { min-width:0; }
.watch-channel b,.watch-channel small { display:block; overflow-wrap:anywhere; }
.watch-channel b { margin:4px 0 2px; }
.watch-channel small { color:var(--muted); font-size:11px; }
.watch-channel .btn { width:100%; min-width:0; }
#view-more .row-btn { margin:8px 0; }
#view-more .ri[data-ic] { flex:none; }
@media (max-width:380px) {
  .tab svg { width:21px; height:21px; }
  .tab i { font-size:9px; }
  .watch-grid { grid-template-columns:1fr; }
  .puzzle-actions { grid-template-columns:1fr 1fr; }
  .puzzle-actions #btnDailyPuzzle { grid-column:1/-1; }
}
"""
replace_once(
    "app/src/main/assets/css/app.css",
    "[hidden]{display:none !important}",
    "[hidden]{display:none !important}\n" + css,
    "responsive content tab styles"
)

print("Five-tab Next Gen navigation, daily puzzle trainer, learning path, Lichess TV and More hub applied.")
