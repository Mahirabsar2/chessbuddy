#!/usr/bin/env python3
"""Full mobile product pass: profile, local practice ratings, stats, settings navigation,
responsive bot roster, real lobby icons, and safe Maia-to-Stockfish recovery."""
from pathlib import Path

def replace_once(path, old, new, label):
    p = Path(path)
    source = p.read_text(encoding="utf-8")
    if new in source:
        return
    if old not in source:
        raise SystemExit("Mobile experience patch could not find " + label + " in " + path)
    p.write_text(source.replace(old, new, 1), encoding="utf-8")

def replace_section(path, start, end, new, label):
    p = Path(path)
    source = p.read_text(encoding="utf-8")
    if new in source:
        return
    a = source.find(start)
    b = source.find(end, a + len(start)) if a >= 0 else -1
    if a < 0 or b < 0:
        raise SystemExit("Mobile experience patch could not find section " + label)
    p.write_text(source[:a] + new + source[b + len(end):], encoding="utf-8")

# 1) A persistent, one-tap profile shortcut in the mobile header.
replace_once(
    "app/src/main/assets/index.html",
    '    <div class="brand" id="hdrBrand"><div class="logo"><svg viewBox="0 0 45 45" aria-hidden="true"><use href="#wN"/></svg></div><b id="hdrTitle">ChessBuddy</b></div>\n    <button id="enginePill"',
    '''    <div class="brand" id="hdrBrand"><div class="logo"><svg viewBox="0 0 45 45" aria-hidden="true"><use href="#wN"/></svg></div><b id="hdrTitle">ChessBuddy</b></div>
    <button id="profileQuickBtn" class="profile-quick" type="button" aria-label="Open your player profile" hidden>
      <span class="profile-quick-avatar" id="profileQuickAvatar">C</span>
      <span class="profile-quick-copy"><b id="profileQuickName">Player</b><small id="profileQuickRating">Unrated</small></span>
    </button>
    <button id="enginePill"''',
    "top profile shortcut"
)

# 2) Replace the thin More page with a real mobile dashboard. Keep the original
# control IDs where the existing controllers already expect them.
more = r'''    <!-- ================= MORE ================= -->
    <section id="view-more" class="view" aria-label="More">
      <div class="content-hero more-hero">
        <span class="eyebrow">YOUR CHESSBUDDY</span>
        <h1>More</h1>
        <p>Your profile, ratings, performance, community and app controls.</p>
      </div>
      <button class="more-profile-card" id="moreProfile" type="button">
        <span class="profile-avatar" id="moreProfileAvatar">C</span>
        <span class="more-profile-copy">
          <span class="eyebrow">PLAYER PROFILE</span>
          <b id="moreProfileName">Local Player</b>
          <small id="moreProfileSub">Local practice profile · Not synced</small>
        </span>
        <span class="more-profile-rating"><b id="moreRapidRating">1200</b><small>Rapid</small></span>
        <span class="more-profile-chevron" data-ic="chev"></span>
      </button>
      <div class="more-stat-strip">
        <div><b id="moreGames">0</b><span>Games</span></div>
        <div><b id="moreWins">0</b><span>Wins</span></div>
        <div><b id="moreLessons">0</b><span>Lessons</span></div>
      </div>
      <div class="more-section-title"><h2>Player</h2><span class="muted tiny" id="moreAccountState">Offline</span></div>
      <div class="more-action-grid">
        <button class="more-action" id="moreStats" type="button"><span class="more-action-icon" data-ic="chart"></span><b>Stats &amp; Ratings</b><small>Rating history and performance</small></button>
        <button class="more-action" id="moreOnline" type="button"><span class="more-action-icon" data-ic="users"></span><b>Friends &amp; Online</b><small>Challenges and player list</small></button>
        <button class="more-action" id="moreArchive" type="button"><span class="more-action-icon" data-ic="tHist"></span><b>Game Archive</b><small>Replay, import and export</small></button>
        <button class="more-action" id="moreCoach" type="button"><span class="more-action-icon" data-ic="spark"></span><b>Coach &amp; Analysis</b><small>Review games and positions</small></button>
      </div>
      <div class="more-section-title"><h2>Study</h2></div>
      <div class="more-action-grid">
        <button class="more-action" id="morePuzzles" type="button"><span class="more-action-icon" data-ic="tPuzzle"></span><b>Puzzles</b><small>Daily, Rush and Survival</small></button>
        <button class="more-action" id="moreOpenings" type="button"><span class="more-action-icon" data-ic="book"></span><b>Opening &amp; Gambit Lab</b><small>Repertoire and coach practice</small></button>
        <button class="more-action" id="moreEndgames" type="button"><span class="more-action-icon" data-ic="crown"></span><b>Endgame Lab</b><small>Positions and tablebases</small></button>
        <button class="more-action" id="moreCharacters" type="button"><span class="more-action-icon" data-ic="user"></span><b>Character Studio</b><small>Meet the original ChessBuddy cast</small></button>
      </div>
      <div class="more-section-title"><h2>App</h2></div>
      <div class="card more-settings-card">
        <button class="row-btn" id="moreSettings" type="button"><span class="ri" data-ic="tSet"></span><span class="rt"><b>Settings</b><small>Board, gameplay, engine, coach, data and privacy</small></span><span class="rc" data-ic="chev"></span></button>
        <button class="row-btn" id="moreAbout" type="button"><span class="ri" data-ic="info"></span><span class="rt"><b>About ChessBuddy</b><small>Version, credits and release information</small></span><span class="rc" data-ic="chev"></span></button>
      </div>
    </section>'''
replace_section(
    "app/src/main/assets/index.html",
    '    <!-- ================= MORE ================= -->',
    '    </section>',
    more,
    "More dashboard"
)

# 3) Dedicated Profile and Stats pages, both reachable from More and the top avatar.
profile_stats = r'''    <section id="view-profile" class="view" aria-label="Player profile">
      <div class="profile-hero-card">
        <div class="profile-hero-main">
          <span class="profile-avatar profile-avatar-large" id="profileAvatar">C</span>
          <div class="profile-hero-copy"><span class="eyebrow">PLAYER PROFILE</span><h1 id="profileDisplayName">Local Player</h1><p id="profileHandle">Local practice account</p></div>
          <button class="icon-btn profile-edit-icon" id="btnEditProfile" type="button" aria-label="Edit profile" title="Edit profile"><span data-ic="edit"></span></button>
        </div>
        <p class="profile-bio" id="profileBio">Your chess journey starts here.</p>
        <div class="profile-online-line"><span class="profile-status-dot" id="profileStatusDot"></span><span id="profileOnlineState">Local profile · Not synced</span><button class="text-btn" id="btnProfileOnline" type="button">Online account</button></div>
      </div>
      <div class="profile-section-head"><h2>Practice ratings</h2><span class="chip">LOCAL</span></div>
      <div class="profile-rating-grid" id="profileRatingGrid"></div>
      <div class="profile-section-head"><h2>Overview</h2><button class="text-btn" id="btnProfileStats" type="button">Full stats</button></div>
      <div class="profile-overview-grid">
        <div><b id="profileGames">0</b><span>Games</span></div>
        <div><b id="profileWins">0</b><span>Wins</span></div>
        <div><b id="profileWinRate">—</b><span>Win rate</span></div>
        <div><b id="profilePuzzleCount">0</b><span>Puzzles solved</span></div>
      </div>
      <div class="card">
        <div class="content-head"><h3>Recent games</h3><button class="text-btn" id="btnProfileArchive" type="button">View archive</button></div>
        <div id="profileRecentGames"><p class="muted tiny">Completed games will appear here.</p></div>
      </div>
      <div class="notice info profile-rating-note">Practice ratings are calculated locally from completed timed games against ChessBuddy bots. They are not Chess.com, FIDE, or official online ratings. Friend challenges are currently unrated.</div>
    </section>

    <section id="view-stats" class="view" aria-label="Player statistics">
      <div class="content-hero stats-hero">
        <span class="eyebrow">YOUR PERFORMANCE</span><h1>Stats &amp; Ratings</h1>
        <p>Track your local practice rating, results and improvement over time.</p>
      </div>
      <div class="stats-filter-row"><span class="muted tiny">TIME CONTROL</span><select id="statsTimeControl" aria-label="Choose a time control"><option value="all">All controls</option><option value="bullet">Bullet</option><option value="blitz">Blitz</option><option value="rapid">Rapid</option><option value="classical">Classical</option></select></div>
      <div class="stats-rating-hero">
        <div><span class="eyebrow" id="statsRatingLabel">RAPID PRACTICE RATING</span><b id="statsCurrentRating">1200</b><small id="statsRatingSub">Provisional · 0 rated games</small></div>
        <div class="stats-rating-change" id="statsRatingChange">—</div>
      </div>
      <div class="card">
        <div class="content-head"><h3>Rating history</h3><span class="muted tiny">Recent games</span></div>
        <div id="statsRatingGraph" class="stats-rating-graph"></div>
        <div class="stats-graph-legend"><span>Previous</span><b id="statsPeakRating">Peak 1200</b><span>Current</span></div>
      </div>
      <div class="profile-overview-grid">
        <div><b id="statsGames">0</b><span>Rated games</span></div>
        <div><b id="statsWins">0</b><span>Wins</span></div>
        <div><b id="statsDraws">0</b><span>Draws</span></div>
        <div><b id="statsLosses">0</b><span>Losses</span></div>
      </div>
      <div class="card"><h3>All time controls</h3><div id="statsRatingBreakdown" class="stats-rating-breakdown"></div></div>
      <div class="card"><h3>Training</h3><div class="stats-training-grid">
        <div><b id="statsPuzzles">0</b><span>Puzzles solved</span></div>
        <div><b id="statsPuzzleStreak">0</b><span>Daily streak</span></div>
        <div><b id="statsRushBest">0</b><span>Best Puzzle Rush</span></div>
        <div><b id="statsLessons">0</b><span>Lessons completed</span></div>
      </div></div>
      <div class="notice info profile-rating-note">Ratings are local practice estimates. Only standard timed games against ChessBuddy bots count; untimed games, online friend challenges and custom variants do not change them.</div>
    </section>
'''
# Insert immediately before the closing main tag after More.
p = Path("app/src/main/assets/index.html")
html_source = p.read_text(encoding="utf-8")
if 'id="view-profile"' not in html_source:
    marker = '  </main>\n\n  <nav class="tabbar"'
    if marker not in html_source:
        raise SystemExit("Mobile experience patch could not find main close for Profile and Stats")
    html_source = html_source.replace(marker, profile_stats + marker, 1)
    p.write_text(html_source, encoding="utf-8")

# Add quick category navigation to the existing Settings page and name its sections.
replace_once(
    "app/src/main/assets/index.html",
    '    <section id="view-settings" class="view" aria-label="Settings">\n      <div class="card" id="cardModels">',
    '''    <section id="view-settings" class="view" aria-label="Settings">
      <div class="content-hero settings-hero"><span class="eyebrow">MAKE IT YOURS</span><h1>Settings</h1><p>Customize your board, gameplay, engine, coach, notifications and app data.</p></div>
      <div class="settings-shortcuts" id="settingsShortcuts">
        <button type="button" data-settings-target="cardBoard"><span data-ic="board"></span><b>Board &amp; pieces</b></button>
        <button type="button" data-settings-target="cardEngine"><span data-ic="engine"></span><b>Engine</b></button>
        <button type="button" data-settings-target="cardModels"><span data-ic="robot"></span><b>AI &amp; coach</b></button>
        <button type="button" data-settings-target="cardData"><span data-ic="database"></span><b>Data &amp; backup</b></button>
        <button type="button" data-settings-target="cardPrivacy"><span data-ic="shield"></span><b>Privacy</b></button>
        <button type="button" data-settings-target="cardAbout"><span data-ic="info"></span><b>About</b></button>
      </div>
      <div class="card" id="cardModels">''',
    "Settings shortcuts"
)
replace_once("app/src/main/assets/index.html", '<div class="card"><h3>Game &amp; board</h3>', '<div class="card" id="cardBoard"><h3>Board &amp; pieces</h3>', "Settings board card")
replace_once("app/src/main/assets/index.html", '<div class="card"><h3>Data</h3>', '<div class="card" id="cardData"><h3>Data &amp; backup</h3>', "Settings data card")
replace_once("app/src/main/assets/index.html", '<div class="card"><h3>Diagnostics &amp; privacy</h3>', '<div class="card" id="cardPrivacy"><h3>Diagnostics &amp; privacy</h3>', "Settings privacy card")
replace_once("app/src/main/assets/index.html", '<div class="card"><h3>About</h3>', '<div class="card" id="cardAbout"><h3>About</h3>', "Settings about card")

# 4) Add a local profile object to settings; existing saved settings are merged,
# so this introduces defaults without resetting user preferences.
replace_once(
    "app/src/main/assets/js/app.js",
    "      custom: { elo: 1500 },\n      ava: { w: 'sf:atlas', b: 'sf:marlow' },\n      models: Models.defaultModels(), progress: {}, adaptive: {}",
    "      custom: { elo: 1500 },\n      profile: { displayName: '', bio: '' },\n      ava: { w: 'sf:atlas', b: 'sf:marlow' },\n      models: Models.defaultModels(), progress: {}, adaptive: {}",
    "profile settings defaults"
)

# 5) Local practice Elo: only standard timed bot games count. Online challenges,
# human-vs-human, variants and untimed games remain explicitly unrated.
rating_logic = r'''
  const PRACTICE_RATING_BUCKETS = [
    { id:'bullet', label:'Bullet', time:'1 min' },
    { id:'blitz', label:'Blitz', time:'3–5 min' },
    { id:'rapid', label:'Rapid', time:'10–15 min' },
    { id:'classical', label:'Classical', time:'30 min' }
  ];
  function practiceBucketForTimeControl() {
    const tc = Clock.byId(settings.play.tc);
    if (!tc || !tc.base) return null;
    if (tc.base <= 60) return 'bullet';
    if (tc.base <= 300) return 'blitz';
    if (tc.base <= 900) return 'rapid';
    return 'classical';
  }
  function practiceRating(bucket) {
    const values = settings.progress.practiceRatings || {};
    return Math.round(Number(values[bucket] || 1200));
  }
  function updatePracticeRating() {
    const side = humanSide();
    if (!side || ctx.online || modeOf() !== 'hva' || activeGameVariant !== 'standard' ||
        !over || game.history().length < 8 || resultCode() === '*') return null;
    const opponent = playerOf(side === 'w' ? 'b' : 'w');
    if (!opponent || opponent.kind !== 'sf' || (opponent.botId && String(opponent.botId).indexOf('coach_') === 0)) return null;
    const bucket = practiceBucketForTimeControl();
    if (!bucket) return null;
    const progress = settings.progress || (settings.progress = {});
    const ratings = progress.practiceRatings || (progress.practiceRatings = {});
    const counts = progress.practiceRatingGames || (progress.practiceRatingGames = {});
    const history = progress.practiceRatingHistory || (progress.practiceRatingHistory = []);
    const gameKey = String(ctx.startedAt || 0) + '|' + game.history().join(' ');
    if (history.some(item => item && item.gameKey === gameKey)) return null;
    const before = practiceRating(bucket), opponentRating = Math.max(300, Math.min(3500, Number(opponent.elo || (opponent.engine === 'lc0' ? 1100 : 1800))));
    const score = over.winner === side ? 1 : over.winner ? 0 : 0.5;
    const expected = 1 / (1 + Math.pow(10, (opponentRating - before) / 400));
    const games = Number(counts[bucket] || 0), k = games < 10 ? 40 : games < 30 ? 24 : 16;
    const delta = Math.round(k * (score - expected)), after = Math.max(100, Math.min(3500, before + delta));
    ratings[bucket] = after;
    counts[bucket] = games + 1;
    const peaks = progress.practiceRatingPeaks || (progress.practiceRatingPeaks = {});
    peaks[bucket] = Math.max(Number(peaks[bucket] || 1200), after);
    const entry = {
      at:new Date().toISOString(), gameKey:gameKey, bucket:bucket, before:before, after:after, delta:after-before,
      opponent:String(opponent.name || 'ChessBuddy bot').slice(0,48), opponentRating:opponentRating,
      result:score === 1 ? 'win' : score === 0 ? 'loss' : 'draw', timeControl:settings.play.tc
    };
    history.push(entry);
    if (history.length > 120) history.splice(0, history.length - 120);
    saveSettings();
    return entry;
  }
  function localCompletedGames() {
    return lsGet(K_GAMES, []).filter(g => g && g.done && g.human && ['1-0','0-1','1/2-1/2'].includes(g.result));
  }
  function localGameResult(g) {
    if (!g || !g.human) return '';
    if (g.result === '1/2-1/2') return 'draw';
    return g.result === (g.human === 'w' ? '1-0' : '0-1') ? 'win' : 'loss';
  }
  function localProfileName() {
    const local = settings.profile && String(settings.profile.displayName || '').trim();
    return local || (onlineProfile && (onlineProfile.display_name || onlineProfile.username)) || 'Local Player';
  }
  function profileInitial(name) {
    const clean = String(name || 'C').trim();
    return (clean.charAt(0) || 'C').toUpperCase();
  }
  function practiceRatingTotalGames(bucket) {
    const values = settings.progress.practiceRatingGames || {};
    return Object.keys(values).reduce((n, key) => n + (bucket && key !== bucket ? 0 : Number(values[key] || 0)), 0);
  }
  function practiceRatingGraph(values) {
    const list = (Array.isArray(values) ? values : []).map(Number).filter(Number.isFinite).slice(-18);
    if (!list.length) list.push(1200, 1200);
    if (list.length === 1) list.unshift(1200);
    const lo = Math.min.apply(null, list) - 25, hi = Math.max.apply(null, list) + 25, span = Math.max(50, hi-lo);
    const points = list.map((value, i) => {
      const x = 6 + i * (288 / Math.max(1,list.length-1)), y = 66 - ((value-lo)/span)*54;
      return x.toFixed(1)+','+y.toFixed(1);
    }).join(' ');
    return '<svg viewBox="0 0 300 78" role="img" aria-label="Local practice rating history"><path d="M6 66H294" stroke="currentColor" opacity=".18" stroke-width="1"/><polyline points="' + points + '" fill="none" stroke="#9bc96a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>' +
      '<circle cx="' + points.split(' ').slice(-1)[0].split(',')[0] + '" cy="' + points.split(' ').slice(-1)[0].split(',')[1] + '" r="4" fill="#c7ed98"/></svg>';
  }
'''
replace_once(
    "app/src/main/assets/js/app.js",
    "  function recordGame() {",
    rating_logic + "\n  function recordGame() {",
    "local practice rating logic"
)
replace_once(
    "app/src/main/assets/js/app.js",
    "  function recordGame() {\n    const list = lsGet(K_GAMES, []);\n    game.setHeader('Result', resultCode());\n    list.unshift({ id: 'g' + Date.now(), date: new Date().toISOString(), players: ctx.players, human: humanSide(), mode: modeOf(),\n      white: labelOf('w'), black: labelOf('b'), result: resultCode(), resultText: over ? over.text : 'Unfinished game',\n      plies: game.history().length, pgn: game.pgn(), fen: game.fen(), variant:activeGameVariant, done: !!over });",
    "  function recordGame() {\n    const list = lsGet(K_GAMES, []);\n    game.setHeader('Result', resultCode());\n    const practiceRatingChange = updatePracticeRating();\n    list.unshift({ id: 'g' + Date.now(), date: new Date().toISOString(), players: ctx.players, human: humanSide(), mode: modeOf(),\n      white: labelOf('w'), black: labelOf('b'), result: resultCode(), resultText: over ? over.text : 'Unfinished game',\n      plies: game.history().length, pgn: game.pgn(), fen: game.fen(), variant:activeGameVariant, done: !!over, practiceRating:practiceRatingChange });",
    "record local practice rating in game archive"
)

# 6) Replace More's old summary renderer and add real Profile/Stats renderers.
renderers = r'''
  function renderMore() {
    const list = localCompletedGames(), wins = list.filter(g => localGameResult(g) === 'win').length;
    const profileName = localProfileName();
    $('moreGames').textContent = String(list.length);
    $('moreWins').textContent = String(wins);
    $('moreLessons').textContent = String((settings.progress.completedLessons || []).length);
    $('moreAccountState').textContent = Online.signedIn() ? 'Signed in' : 'Local profile';
    $('moreProfileName').textContent = profileName;
    $('moreProfileSub').textContent = Online.signedIn() ? (onlineProfile && onlineProfile.username ? '@' + onlineProfile.username : 'Synced online profile') : 'Practice profile · Not synced';
    $('moreProfileAvatar').textContent = profileInitial(profileName);
    $('moreRapidRating').textContent = String(practiceRating('rapid'));
    if (Online.signedIn() && !onlineProfile) {
      Online.profile().then(p => {
        if (currentTab !== 'more' || !p) return;
        onlineProfile = p;
        $('moreProfileName').textContent = settings.profile.displayName || p.display_name || p.username || 'Player';
        $('moreProfileSub').textContent = p.username ? '@' + p.username + ' · Synced' : 'Synced online profile';
        $('moreAccountState').textContent = 'Signed in';
        $('moreProfileAvatar').textContent = profileInitial($('moreProfileName').textContent);
      }).catch(() => {});
    }
  }
  function renderProfile() {
    const name = localProfileName(), profile = settings.profile || {};
    const bio = String(profile.bio || '').trim();
    const list = localCompletedGames(), wins = list.filter(g => localGameResult(g) === 'win').length;
    const draws = list.filter(g => localGameResult(g) === 'draw').length;
    $('profileDisplayName').textContent = name;
    $('profileAvatar').textContent = profileInitial(name);
    $('profileHandle').textContent = Online.signedIn() && onlineProfile && onlineProfile.username ? '@' + onlineProfile.username : 'Local practice profile';
    $('profileBio').textContent = bio || 'Your chess journey starts here.';
    $('profileOnlineState').textContent = Online.signedIn() ? 'Signed in · online profile available' : 'Local profile · sign in to sync your account';
    $('profileStatusDot').classList.toggle('is-online', Online.signedIn());
    $('profileGames').textContent = String(list.length);
    $('profileWins').textContent = String(wins);
    $('profileWinRate').textContent = list.length ? Math.round(wins/list.length*100) + '%' : '—';
    $('profilePuzzleCount').textContent = String(Number(settings.progress.puzzlesSolved || 0));
    $('profileRatingGrid').innerHTML = PRACTICE_RATING_BUCKETS.map(bucket => {
      const games = practiceRatingTotalGames(bucket.id), peak = Number((settings.progress.practiceRatingPeaks || {})[bucket.id] || 1200);
      return '<div class="profile-rating-card"><span>' + bucket.label + '</span><b>' + practiceRating(bucket.id) + '</b><small>' + (games ? games + ' rated games' : 'Provisional') + ' · Peak ' + peak + '</small></div>';
    }).join('');
    const recent = list.slice(0,4);
    $('profileRecentGames').innerHTML = recent.length ? recent.map(g => {
      const outcome = localGameResult(g), tag = outcome === 'win' ? 'WIN' : outcome === 'draw' ? 'DRAW' : 'LOSS';
      const when = g.date ? new Date(g.date).toLocaleDateString() : '';
      const delta = g.practiceRating && typeof g.practiceRating.delta === 'number' ? ' · ' + (g.practiceRating.delta > 0 ? '+' : '') + g.practiceRating.delta : '';
      return '<div class="profile-recent-row"><span class="profile-result ' + outcome + '">' + tag + '</span><span><b>' + esc(g.white || 'White') + ' vs ' + esc(g.black || 'Black') + '</b><small>' + esc(when) + ' · ' + Number(g.plies || 0) + ' plies' + esc(delta) + '</small></span></div>';
    }).join('') : '<p class="muted tiny">No completed games yet. Play a timed bot game to start your practice record.</p>';
    if (Online.signedIn() && !onlineProfile) {
      Online.profile().then(p => {
        if (currentTab !== 'profile' || !p) return;
        onlineProfile = p;
        $('profileHandle').textContent = p.username ? '@' + p.username : 'Online profile';
        if (!profile.displayName) $('profileDisplayName').textContent = p.display_name || p.username || 'Player';
        $('profileOnlineState').textContent = p.username ? 'Signed in as @' + p.username : 'Signed in · online profile available';
      }).catch(() => {});
    }
  }
  function renderStats() {
    const selected = $('statsTimeControl').value || 'all';
    const buckets = selected === 'all' ? PRACTICE_RATING_BUCKETS : PRACTICE_RATING_BUCKETS.filter(x => x.id === selected);
    const ratings = settings.progress.practiceRatingHistory || [];
    const history = selected === 'all' ? ratings : ratings.filter(x => x.bucket === selected);
    const last = history.slice(-1)[0], currentBucket = selected === 'all' ? 'rapid' : selected;
    const games = selected === 'all' ? practiceRatingTotalGames(null) : practiceRatingTotalGames(selected);
    const all = localCompletedGames(), modeHistory = history;
    const wins = modeHistory.filter(x => x.result === 'win').length;
    const draws = modeHistory.filter(x => x.result === 'draw').length;
    const losses = modeHistory.filter(x => x.result === 'loss').length;
    const current = practiceRating(currentBucket);
    $('statsRatingLabel').textContent = (selected === 'all' ? 'RAPID PRACTICE RATING · DEFAULT' : selected.toUpperCase() + ' PRACTICE RATING');
    $('statsCurrentRating').textContent = String(current);
    $('statsRatingSub').textContent = (selected === 'all' ? practiceRatingTotalGames('rapid') : games) + ' rated games · local estimate';
    $('statsRatingChange').textContent = last ? (last.delta > 0 ? '+' : '') + last.delta + ' last game' : 'No change yet';
    const listValues = modeHistory.slice(-18).map(x => x.after);
    $('statsRatingGraph').innerHTML = practiceRatingGraph(listValues);
    const peak = selected === 'all' ? Math.max.apply(null, PRACTICE_RATING_BUCKETS.map(b => Number((settings.progress.practiceRatingPeaks || {})[b.id] || 1200))) :
      Number((settings.progress.practiceRatingPeaks || {})[selected] || 1200);
    $('statsPeakRating').textContent = 'Peak ' + peak;
    $('statsGames').textContent = String(games);
    $('statsWins').textContent = String(wins);
    $('statsDraws').textContent = String(draws);
    $('statsLosses').textContent = String(losses);
    $('statsRatingBreakdown').innerHTML = buckets.map(bucket => {
      const n = practiceRatingTotalGames(bucket.id);
      return '<div class="stats-rating-row"><span><b>' + bucket.label + '</b><small>' + bucket.time + ' · ' + n + ' games</small></span><strong>' + practiceRating(bucket.id) + '</strong><small>Peak ' + Number((settings.progress.practiceRatingPeaks || {})[bucket.id] || 1200) + '</small></div>';
    }).join('');
    $('statsPuzzles').textContent = String(Number(settings.progress.puzzlesSolved || 0));
    $('statsPuzzleStreak').textContent = String(Number(settings.progress.dailyPuzzleStreak || 0));
    $('statsRushBest').textContent = String(Math.max(Number(settings.progress.puzzleRushBest3 || 0), Number(settings.progress.puzzleRushBest5 || 0), Number(settings.progress.puzzleRushBestSurvival || 0)));
    $('statsLessons').textContent = String((settings.progress.completedLessons || []).length);
  }
  function editLocalProfile() {
    const profile = settings.profile || (settings.profile = { displayName:'', bio:'' });
    openModal('<div class="content-head"><div><span class="eyebrow">YOUR PLAYER CARD</span><h3>Edit profile</h3></div></div>' +
      '<div class="field"><label for="localProfileName">Display name</label><input id="localProfileName" maxlength="32" value="' + esc(profile.displayName || '') + '" placeholder="Your chess name"></div>' +
      '<div class="field"><label for="localProfileBio">Bio</label><textarea id="localProfileBio" rows="3" maxlength="140" placeholder="A little about your chess journey">' + esc(profile.bio || '') + '</textarea></div>' +
      '<p class="muted tiny">This local profile stays on this device. Sign in from Play Online to access your synced ChessBuddy account.</p>' +
      '<div class="controls"><button class="btn primary" id="btnSaveLocalProfile" type="button">Save profile</button><button class="btn" id="btnCancelLocalProfile" type="button">Cancel</button></div>');
    $('btnCancelLocalProfile').onclick = closeModal;
    $('btnSaveLocalProfile').onclick = () => {
      const displayName = $('localProfileName').value.trim(), bio = $('localProfileBio').value.trim();
      if (displayName.length > 32 || bio.length > 140) { toast('Display name and bio are too long.'); return; }
      settings.profile = { displayName:displayName, bio:bio };
      saveSettings(); closeModal(); renderProfile(); renderMore(); renderHeader(); toast('Profile saved on this device.');
    };
  }
  function updateProfileShortcut() {
    const button = $('profileQuickBtn');
    if (!button) return;
    const name = localProfileName();
    $('profileQuickName').textContent = name;
    $('profileQuickAvatar').textContent = profileInitial(name);
    $('profileQuickRating').textContent = 'Local rapid ' + practiceRating('rapid');
  }
'''
replace_once(
    "app/src/main/assets/js/app.js",
    "  function renderMore() {",
    renderers + "\n  function legacyRenderMoreRemoved() {",
    "replace More renderer with Profile and Stats"
)
# Delete the old renderMore body now renamed, leaving only the new one above.
replace_once(
    "app/src/main/assets/js/app.js",
    "  function legacyRenderMoreRemoved() {\n    const list = lsGet(K_GAMES, []), wins = list.filter(g => g.human && g.result === (g.human === 'w' ? '1-0' : '0-1')).length;",
    "  function legacyRenderMoreRemoved() {\n    return;\n    const list = lsGet(K_GAMES, []), wins = list.filter(g => g.human && g.result === (g.human === 'w' ? '1-0' : '0-1')).length;",
    "disable legacy More renderer"
)

# 7) Navigation and settings integration.
replace_once(
    "app/src/main/assets/js/app.js",
    "  const TAB_TITLES = { puzzles: 'Puzzles', learn: 'Learn', watch: 'Watch', more: 'More', coach: 'Coach', history: 'Archive', settings: 'Settings' };",
    "  const TAB_TITLES = { puzzles: 'Puzzles', learn: 'Learn', watch: 'Watch', more: 'More', profile:'Profile', stats:'Stats & Ratings', coach: 'Coach', history: 'Archive', settings: 'Settings' };",
    "profile and stats page titles"
)
replace_once(
    "app/src/main/assets/js/app.js",
    "    const inPlay = currentTab === 'play', showBack = inPlay && playScreen !== 'lobby';\n    const back = $('hdrBack'); back.hidden = !showBack; if (showBack) back.innerHTML = ic('back');\n    $('hdrBrand').querySelector('.logo').style.display = (showBack || !inPlay) ? 'none' : '';",
    "    const inPlay = currentTab === 'play', secondaryView = ['profile','stats','settings','history','coach'].indexOf(currentTab) >= 0;\n    const showBack = (inPlay && playScreen !== 'lobby') || secondaryView;\n    const back = $('hdrBack'); back.hidden = !showBack; if (showBack) back.innerHTML = ic('back');\n    $('profileQuickBtn').hidden = !(inPlay && playScreen === 'lobby');\n    $('enginePill').hidden = inPlay && playScreen === 'lobby';\n    $('hdrBrand').querySelector('.logo').style.display = (showBack || !inPlay) ? 'none' : '';\n    updateProfileShortcut();",
    "header Profile shortcut visibility"
)
replace_once(
    "app/src/main/assets/js/app.js",
    "    const navTab = ['coach', 'history', 'settings'].indexOf(name) >= 0 ? 'more' : name;",
    "    const navTab = ['coach', 'history', 'settings', 'profile', 'stats'].indexOf(name) >= 0 ? 'more' : name;",
    "Profile and Stats keep More selected"
)
replace_once(
    "app/src/main/assets/js/app.js",
    "    if (name === 'more') renderMore();",
    "    if (name === 'more') renderMore();\n    if (name === 'profile') renderProfile();\n    if (name === 'stats') renderStats();",
    "Profile and Stats render on navigation"
)
replace_once(
    "app/src/main/assets/js/app.js",
    "  window.cbBack = function () {\n    if (!$('modal').hidden) { closeModal(); return true; }\n    if (!$('boardOverlay').hidden && playScreen === 'game' && currentTab === 'play') { hideOverlay(); return true; }\n    if (currentTab !== 'play') { showTab('play'); return true; }",
    "  window.cbBack = function () {\n    if (!$('modal').hidden) { closeModal(); return true; }\n    if (!$('boardOverlay').hidden && playScreen === 'game' && currentTab === 'play') { hideOverlay(); return true; }\n    if (['profile','stats','settings','history','coach'].indexOf(currentTab) >= 0) { showTab('more'); return true; }\n    if (currentTab !== 'play') { showTab('play'); return true; }",
    "Back from profile/stats/settings to More"
)
replace_once(
    "app/src/main/assets/js/app.js",
    "    $('hdrBack').onclick = () => window.cbBack();",
    "    $('hdrBack').onclick = () => window.cbBack();\n    $('profileQuickBtn').onclick = () => showTab('profile');",
    "Profile header click"
)

# Rebuild icons on the Play lobby; Play Online had an empty icon span in the existing UI.
replace_once(
    "app/src/main/assets/js/app.js",
    "    users: '<circle cx=\"9\" cy=\"8\" r=\"3\"/><path d=\"M3.5 19c.5-3.5 3-5 5.5-5s5 1.5 5.5 5\"/><circle cx=\"17\" cy=\"9\" r=\"2.4\"/><path d=\"M16 14.2c2.6-.3 4.6 1 5 4.3\"/>',",
    "    users: '<circle cx=\"9\" cy=\"8\" r=\"3\"/><path d=\"M3.5 19c.5-3.5 3-5 5.5-5s5 1.5 5.5 5\"/><circle cx=\"17\" cy=\"9\" r=\"2.4\"/><path d=\"M16 14.2c2.6-.3 4.6 1 5 4.3\"/>',\n    online: '<circle cx=\"12\" cy=\"12\" r=\"9\"/><path d=\"M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18\"/>',\n    userPlus: '<circle cx=\"9\" cy=\"8\" r=\"3\"/><path d=\"M3 20c.4-3.4 2.8-5 6-5 2.1 0 3.9.7 5 2M19 8v6M16 11h6\"/>',\n    chart: '<path d=\"M4 19V5M4 19h17M7 15l4-4 3 2 5-7\"/><circle cx=\"19\" cy=\"6\" r=\"1\"/>',\n    book: '<path d=\"M3 5.5c3.1-1.2 6.1-.9 9 1v13c-2.9-1.9-5.9-2.2-9-1zM21 5.5c-3.1-1.2-6.1-.9-9 1v13c2.9-1.9 5.9-2.2 9-1z\"/>',\n    user: '<circle cx=\"12\" cy=\"8\" r=\"3.5\"/><path d=\"M4 21c.5-4.3 3.2-6.5 8-6.5s7.5 2.2 8 6.5\"/>',\n    edit: '<path d=\"M12 20h9M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4z\"/>',\n    board: '<rect x=\"4\" y=\"4\" width=\"16\" height=\"16\" rx=\"2\"/><path d=\"M12 4v16M4 12h16M4 4l8 8 8-8M4 20l8-8 8 8\"/>',\n    engine: '<path d=\"M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1\"/><circle cx=\"12\" cy=\"12\" r=\"4\"/>',\n    database: '<ellipse cx=\"12\" cy=\"5\" rx=\"8\" ry=\"3\"/><path d=\"M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3\"/>',\n    shield: '<path d=\"M12 3 20 6v5c0 5-3.4 8-8 10-4.6-2-8-5-8-10V6z\"/><path d=\"m8.5 12 2.2 2.2 4.8-5\"/>',\n    info: '<circle cx=\"12\" cy=\"12\" r=\"9\"/><path d=\"M12 11v5M12 7h.01\"/>',",
    "professional lobby and settings icons"
)
replace_once(
    "app/src/main/assets/js/app.js",
    "    $('riBots').innerHTML = '<svg viewBox=\"0 0 45 45\"><use href=\"#wN\"/></svg>'; $('riModels').innerHTML = ic('robot'); $('riAvA').innerHTML = ic('versus'); $('riFriend').innerHTML = ic('users');",
    "    $('riBots').innerHTML = '<svg viewBox=\"0 0 45 45\"><use href=\"#wN\"/></svg>'; $('riModels').innerHTML = ic('robot'); $('riAvA').innerHTML = ic('versus'); $('riFriend').innerHTML = ic('userPlus'); $('riOnline').innerHTML = ic('online');",
    "Play Online and Friend icons"
)

# 8) Hook up the new cards and category shortcuts.
replace_once(
    "app/src/main/assets/js/app.js",
    "    $('moreOnline').onclick = () => { showTab('play'); showPlayScreen('online'); };\n    $('moreCoach').onclick = () => showTab('coach');\n    $('moreArchive').onclick = () => showTab('history');\n    $('moreSettings').onclick = () => showTab('settings');",
    """    $('moreProfile').onclick = () => showTab('profile');
    $('moreStats').onclick = () => showTab('stats');
    $('moreOnline').onclick = () => { showTab('play'); showPlayScreen('online'); };
    $('moreCoach').onclick = () => showTab('coach');
    $('moreArchive').onclick = () => showTab('history');
    $('moreSettings').onclick = () => showTab('settings');
    $('morePuzzles').onclick = () => showTab('puzzles');
    $('moreOpenings').onclick = () => { showTab('learn'); $('openingLab').scrollIntoView({ behavior:'smooth', block:'start' }); };
    $('moreEndgames').onclick = () => { showTab('learn'); $('endgameLab').scrollIntoView({ behavior:'smooth', block:'start' }); };
    $('moreCharacters').onclick = openCharacterStudio;
    $('moreAbout').onclick = () => { showTab('settings'); $('cardAbout').scrollIntoView({ behavior:'smooth', block:'start' }); };
    $('btnEditProfile').onclick = editLocalProfile;
    $('btnProfileStats').onclick = () => showTab('stats');
    $('btnProfileArchive').onclick = () => showTab('history');
    $('btnProfileOnline').onclick = () => { showTab('play'); showPlayScreen('online'); };
    $('statsTimeControl').onchange = renderStats;
    $('settingsShortcuts').addEventListener('click', e => {
      const b = e.target.closest('[data-settings-target]'); if (!b) return;
      const target = $(b.getAttribute('data-settings-target'));
      if (target) target.scrollIntoView({ behavior:'smooth', block:'start' });
    });""",
    "More, Profile, Stats and Settings navigation handlers"
)

# 9) Engine fallback: when Maia/Lc0 exits on Android, try the matching Stockfish
# practice strength for this move instead of freezing the whole game.
replace_once(
    "app/src/main/assets/js/app.js",
    "    const job = (p.kind === 'llm' ? llmMove(side, p, myToken) : stockfishMove(side, p, myToken)).catch(err => { if (myToken === token) aiError(err, side, p); });",
    "    const job = (p.kind === 'llm' ? llmMove(side, p, myToken) : stockfishMove(side, p, myToken)).catch(err => {\n      if (myToken !== token) return;\n      if (p.kind === 'sf' && p.engine === 'lc0' && Native.available) { recoverMaiaWithStockfish(side, p, myToken, err); return; }\n      aiError(err, side, p);\n    });",
    "Maia automatic recovery dispatch"
)
replace_once(
    "app/src/main/assets/js/app.js",
    "  function aiError(e, side, p) {",
    """  async function recoverMaiaWithStockfish(side, maiaPlayer, myToken, originalError) {
    setStatus('Maia could not start on this device. Switching to a Stockfish practice move at a similar target strength…', 'warn');
    toast('Maia failed to start. Stockfish is making this move instead.');
    try {
      const fallback = Object.assign({}, maiaPlayer, {
        engine:'stockfish', modelId:'', name:(maiaPlayer.name || 'Maia') + ' · practice fallback'
      });
      await stockfishMove(side, fallback, myToken);
    } catch (fallbackError) {
      if (myToken === token) {
        aiError(fallbackError, side, fallback);
        setStatus('Maia failed to start (' + (originalError && originalError.message || 'engine error') +
          ') and the Stockfish fallback also failed: ' + (fallbackError && fallbackError.message || 'unknown error'), 'bad');
      }
    }
  }

  function aiError(e, side, p) {""",
    "Maia-to-Stockfish fallback implementation"
)

# 10) Make the bot roster readable and stop the fixed dock obscuring the lower cards.
css = r'''
/* ChessBuddy mobile product refresh */
.profile-quick {
  display:flex; align-items:center; gap:8px; flex:none; min-width:0; max-width:42vw;
  border:1px solid var(--line); border-radius:999px; padding:4px 10px 4px 4px;
  background:var(--surface); color:var(--text); cursor:pointer;
}
.profile-quick[hidden] { display:none!important; }
.profile-quick-avatar,.profile-avatar {
  display:grid; place-items:center; flex:none; border-radius:50%;
  color:#20241d; background:linear-gradient(145deg,#cce4a8,#82b45d);
  font-weight:900; letter-spacing:-.4px;
}
.profile-quick-avatar { width:32px; height:32px; font-size:14px; }
.profile-quick-copy { display:flex; flex-direction:column; text-align:left; min-width:0; line-height:1.12; }
.profile-quick-copy b { font-size:11px; max-width:100px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.profile-quick-copy small { color:var(--muted); font-size:9px; margin-top:3px; }
.more-profile-card {
  display:flex; align-items:center; gap:12px; width:100%; min-width:0; text-align:left;
  padding:14px; margin:0 0 10px; border-radius:16px; border:1px solid #ffffff12;
  background:linear-gradient(115deg,#333d30,#2a2e28); color:var(--text); cursor:pointer;
}
.profile-avatar { width:54px; height:54px; font-size:22px; }
.more-profile-copy { display:flex; flex-direction:column; flex:1; min-width:0; gap:3px; }
.more-profile-copy b { font-size:16px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.more-profile-copy small { color:var(--muted); font-size:11px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.more-profile-rating { display:flex; flex-direction:column; text-align:right; flex:none; }
.more-profile-rating b { font-size:20px; font-variant-numeric:tabular-nums; }
.more-profile-rating small { color:var(--muted); font-size:10px; }
.more-profile-chevron svg { width:18px; height:18px; color:var(--muted); }
.more-stat-strip,.profile-overview-grid {
  display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:8px; margin:8px 0 18px;
}
.more-stat-strip>div,.profile-overview-grid>div {
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:3px;
  background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:11px 5px; min-width:0;
}
.more-stat-strip b,.profile-overview-grid b { font-size:20px; font-variant-numeric:tabular-nums; }
.profile-overview-grid { grid-template-columns:repeat(4,minmax(0,1fr)); }
.more-stat-strip span,.profile-overview-grid span { font-size:10px; color:var(--muted); text-align:center; }
.more-section-title,.profile-section-head { display:flex; align-items:center; justify-content:space-between; gap:10px; margin:18px 2px 9px; }
.more-section-title h2,.profile-section-head h2 { margin:0; font-size:16px; letter-spacing:-.2px; }
.more-action-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:9px; margin-bottom:12px; }
.more-action {
  display:flex; flex-direction:column; align-items:flex-start; gap:6px; min-height:112px;
  min-width:0; padding:13px; border-radius:14px; text-align:left;
  background:var(--surface); color:var(--text); border:1px solid var(--line); cursor:pointer;
}
.more-action:active { background:var(--surface2); transform:scale(.99); }
.more-action-icon { display:grid; place-items:center; width:34px; height:34px; border-radius:10px; background:var(--surface2); color:#b9db98; }
.more-action-icon svg { width:21px; height:21px; }
.more-action>b { font-size:13px; line-height:1.2; }
.more-action>small { color:var(--muted); font-size:10.5px; line-height:1.3; }
.more-settings-card { padding:5px 13px; }
.more-settings-card .row-btn { padding-left:0; padding-right:0; }
.profile-hero-card {
  padding:16px; margin:10px 0 14px; border-radius:18px; border:1px solid #ffffff12;
  background:linear-gradient(135deg,#34442e,#282c26);
}
.profile-hero-main { display:flex; align-items:center; gap:12px; min-width:0; }
.profile-avatar-large { width:68px; height:68px; font-size:28px; }
.profile-hero-copy { flex:1; min-width:0; }
.profile-hero-copy h1 { font-size:23px; margin:4px 0 2px; overflow-wrap:anywhere; }
.profile-hero-copy p { color:#c6cbbf; font-size:12px; margin:0; overflow-wrap:anywhere; }
.profile-edit-icon { flex:none; background:#ffffff10; border:1px solid #ffffff18; border-radius:11px; }
.profile-edit-icon svg { width:20px; height:20px; }
.profile-bio { margin:14px 0 10px; color:#e1e6da; font-size:13px; line-height:1.45; }
.profile-online-line { display:flex; align-items:center; gap:7px; min-width:0; padding-top:10px; border-top:1px solid #ffffff16; font-size:11px; color:#c5c8bd; }
.profile-online-line span:last-of-type { min-width:0; flex:1; }
.profile-status-dot { width:7px; height:7px; border-radius:50%; background:#94948d; flex:none; }
.profile-status-dot.is-online { background:#8bc35f; box-shadow:0 0 0 3px #8bc35f24; }
.text-btn { padding:5px 2px; border:0; color:#b4d68e; background:transparent; font-size:11px; font-weight:800; cursor:pointer; white-space:nowrap; }
.profile-rating-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:9px; }
.profile-rating-card { display:flex; flex-direction:column; gap:5px; padding:13px; border-radius:13px; background:var(--surface); border:1px solid var(--line); min-width:0; }
.profile-rating-card>span { color:var(--muted); font-size:11px; font-weight:750; }
.profile-rating-card>b { font-size:25px; font-variant-numeric:tabular-nums; letter-spacing:-.6px; }
.profile-rating-card>small { color:var(--muted); font-size:10px; line-height:1.3; }
.profile-recent-row { display:flex; align-items:center; gap:10px; padding:10px 0; border-bottom:1px solid var(--line); min-width:0; }
.profile-recent-row:last-child { border:0; }
.profile-recent-row>span:last-child { min-width:0; flex:1; display:flex; flex-direction:column; gap:3px; }
.profile-recent-row b { font-size:12px; overflow-wrap:anywhere; }
.profile-recent-row small { color:var(--muted); font-size:10px; }
.profile-result { min-width:46px; padding:5px 6px; border-radius:7px; text-align:center; font-size:10px; font-weight:900; background:var(--surface2); }
.profile-result.win { color:#a8d779; }.profile-result.loss { color:#ef9c8e; }.profile-result.draw { color:#c4c3bc; }
.profile-rating-note { font-size:11px; line-height:1.45; margin:12px 0; }
.stats-hero { background:linear-gradient(135deg,#334a2a,#282e27); }
.stats-filter-row { display:flex; align-items:center; justify-content:space-between; gap:10px; margin:12px 0; }
.stats-filter-row select { width:auto; min-width:128px; max-width:52%; }
.stats-rating-hero { display:flex; align-items:center; justify-content:space-between; gap:12px; padding:17px; border-radius:16px; background:linear-gradient(120deg,#34432e,#292e27); border:1px solid #ffffff12; }
.stats-rating-hero>div:first-child { display:flex; flex-direction:column; gap:4px; min-width:0; }
.stats-rating-hero b { font-size:36px; letter-spacing:-1px; font-variant-numeric:tabular-nums; }
.stats-rating-hero small { color:var(--muted); font-size:10px; }
.stats-rating-change { flex:none; padding:7px 9px; border-radius:9px; background:#ffffff0b; color:#b9d99b; font-size:11px; font-weight:800; }
.stats-rating-graph { width:100%; height:92px; display:flex; align-items:center; }
.stats-rating-graph svg { width:100%; height:100%; overflow:visible; }
.stats-graph-legend { display:flex; justify-content:space-between; color:var(--muted); font-size:10px; }
.stats-rating-breakdown { display:grid; gap:0; }
.stats-rating-row { display:grid; grid-template-columns:1fr auto auto; gap:10px; align-items:center; padding:11px 0; border-bottom:1px solid var(--line); }
.stats-rating-row:last-child { border:0; }
.stats-rating-row>span { display:flex; flex-direction:column; gap:3px; min-width:0; }
.stats-rating-row b,.stats-rating-row strong { font-size:13px; }
.stats-rating-row small { color:var(--muted); font-size:10px; }
.stats-training-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; }
.stats-training-grid>div { display:flex; flex-direction:column; gap:3px; padding:12px; border-radius:10px; background:var(--surface2); }
.stats-training-grid b { font-size:20px; }
.stats-training-grid span { font-size:10px; color:var(--muted); }
.settings-hero { background:linear-gradient(135deg,#39404c,#292c32); }
.settings-shortcuts { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:7px; margin:12px 0 18px; }
.settings-shortcuts button { display:flex; flex-direction:column; align-items:flex-start; justify-content:center; gap:7px; min-width:0; min-height:73px; padding:10px; border-radius:12px; border:1px solid var(--line); background:var(--surface); color:var(--text); text-align:left; cursor:pointer; }
.settings-shortcuts button svg { width:19px; height:19px; color:#b9d995; }
.settings-shortcuts button b { font-size:10px; line-height:1.2; }
#cardBoard,#cardEngine,#cardModels,#cardData,#cardPrivacy,#cardAbout { scroll-margin-top:14px; }
#botsList { padding-bottom:290px; }
.bgrid { grid-template-columns:repeat(auto-fit,minmax(96px,1fr)); gap:10px; }
.btile { aspect-ratio:.88; min-width:0; }
.btile .avatar { width:100%; height:auto; aspect-ratio:1; flex:none; }
.btile-meta { min-height:42px; padding:5px 3px; gap:2px; }
.btile-meta b { font-size:11px; }
.btile-meta small { font-size:9px; }
.botdock {
  bottom:calc(62px + env(safe-area-inset-bottom,0px));
  padding:10px 14px 9px; border-top:1px solid var(--line);
  border-radius:15px 15px 0 0; background:rgba(38,37,34,.985);
  box-shadow:0 -8px 26px #0004;
}
.botdock .dockrow { gap:8px; }
.botdock .dockrow select { min-height:46px; border-radius:11px; }
.botdock .seg.colors { display:flex; gap:5px; padding:4px; border-radius:12px; background:var(--surface2); }
.botdock .seg.colors button { width:44px; min-height:42px; border-radius:9px; }
.botdock #btnBotPlay { min-height:48px; font-size:18px; border-radius:12px; }
#lobby .row-btn { gap:12px; }
#lobby .ri { width:48px; height:48px; border-radius:14px; }
#lobby .ri svg { width:25px; height:25px; }
#engineBanner { align-items:flex-start; }
#engineBannerText { flex:1 1 auto; min-width:0; line-height:1.4; overflow-wrap:anywhere; }
#engineBanner #btnRetryEngine { flex:0 0 auto; width:auto; min-width:78px; white-space:nowrap; overflow-wrap:normal; padding:8px 12px; margin-left:auto; }
@media(max-width:420px) {
  .bgrid { grid-template-columns:repeat(3,minmax(0,1fr)); gap:9px; }
  .btile { aspect-ratio:.88; }
  .botdock .dockrow select { min-width:0; }
  .profile-quick { max-width:43vw; }
}
@media(max-width:345px) {
  .bgrid { grid-template-columns:repeat(2,minmax(0,1fr)); }
  .profile-quick-copy b { max-width:72px; }
  .more-action-grid { gap:7px; }
  .more-action { padding:10px; }
  .settings-shortcuts { grid-template-columns:repeat(2,minmax(0,1fr)); }
}
@media(prefers-reduced-motion:reduce) {
  .more-action:active { transform:none; }
}
'''
css_path = Path("app/src/main/assets/css/app.css")
css_source = css_path.read_text(encoding="utf-8")
if "/* ChessBuddy mobile product refresh */" not in css_source:
    css_path.write_text(css_source + "\n" + css + "\n", encoding="utf-8")

print("Mobile experience applied: clickable Profile and Stats, local timed practice ratings, Settings category shortcuts, responsive bot roster, fixed play dock spacing, Play Online icon and Maia fallback.")
