#!/usr/bin/env python3
"""ChessBuddy 2.0.0 expansion: achievements, solo bot cups and PGN collections."""
from pathlib import Path


def replace_once(path, old, new, label):
    target = Path(path)
    source = target.read_text(encoding="utf-8")
    if new in source:
        return
    if old not in source:
        raise SystemExit("2.0.0 expansion could not find " + label + " in " + path)
    target.write_text(source.replace(old, new, 1), encoding="utf-8")


# Dedicated destinations are routed through the existing five-tab navigation.
new_views = r'''    <section id="view-achievements" class="view" aria-label="Achievements">
      <div class="content-hero achievement-hero">
        <span class="eyebrow">YOUR CHESS JOURNEY</span>
        <h1>Achievements</h1>
        <p>Milestones earned through real ChessBuddy games, puzzles, lessons and opening practice.</p>
      </div>
      <div class="achievement-level-card">
        <div class="achievement-level-top"><div><span class="eyebrow">CHESSBUDDY XP</span><b id="achievementXp">0 XP</b></div><span class="achievement-level-pill" id="achievementLevel">LEVEL 1</span></div>
        <div class="achievement-progress-track"><span id="achievementProgressBar"></span></div>
        <small id="achievementProgressText">0 XP toward the next level</small>
      </div>
      <div class="achievement-summary-grid">
        <div><b id="achievementUnlocked">0</b><span>Unlocked</span></div>
        <div><b id="achievementAvailable">0</b><span>Available</span></div>
        <div><b id="achievementTotal">0</b><span>Total XP</span></div>
      </div>
      <div class="content-head"><h2>Milestones</h2><span class="muted tiny">Earned automatically</span></div>
      <div id="achievementGrid" class="achievement-grid"></div>
      <div class="notice info">Achievements and XP are stored on this device. They are progress rewards, not official Chess.com trophies, FIDE titles or online ratings.</div>
    </section>

    <section id="view-tournaments" class="view" aria-label="Practice tournaments">
      <div class="content-hero tournament-hero">
        <span class="eyebrow">COMPETITIVE PRACTICE</span>
        <h1>Events &amp; Cups</h1>
        <p>Run a structured solo event against the ChessBuddy bot roster and track every result.</p>
      </div>
      <div class="card tournament-create-card">
        <div class="content-head"><div><span class="eyebrow">CREATE AN EVENT</span><h3>Solo Bot Cup</h3></div><span class="chip">OFFLINE</span></div>
        <p class="muted tiny">Choose a cup length. ChessBuddy selects a set of opponents near your current practice rating. Each round is a normal standard-chess bot game.</p>
        <div class="field"><label for="botCupName">Event name</label><input id="botCupName" maxlength="32" value="ChessBuddy Practice Cup" placeholder="Name your event"></div>
        <div class="field"><label for="botCupRounds">Rounds</label><select id="botCupRounds"><option value="3">3-round cup</option><option value="5" selected>5-round cup</option><option value="7">7-round cup</option></select></div>
        <button class="btn primary" id="btnCreateBotCup" type="button">CREATE PRACTICE CUP</button>
      </div>
      <div class="content-head"><h2>Current event</h2><span class="muted tiny">Your score and round</span></div>
      <div id="botCupCurrent"><p class="muted tiny">No active event. Create a cup to begin.</p></div>
      <div class="content-head"><h2>Event history</h2></div>
      <div id="botCupHistory"><p class="muted tiny">Finished cups will appear here.</p></div>
      <div class="notice info">These are local solo events against bundled bots. They are not live-player tournaments, rated events, or official Chess.com events.</div>
    </section>

    <section id="view-collections" class="view" aria-label="Game collections">
      <div class="content-hero collection-hero">
        <span class="eyebrow">YOUR CHESS LIBRARY</span>
        <h1>Collections</h1>
        <p>Keep important games together, save favourites and copy PGN for analysis or sharing.</p>
      </div>
      <div class="card collection-create-card">
        <div class="content-head"><h3>Create a collection</h3><span class="chip">LOCAL</span></div>
        <div class="field"><label for="collectionName">Collection name</label><input id="collectionName" maxlength="28" placeholder="e.g. Best wins, Opening study"></div>
        <button class="btn primary" id="btnCreateCollection" type="button">CREATE COLLECTION</button>
      </div>
      <div class="card">
        <div class="content-head"><h3>Save an archived game</h3><span class="muted tiny" id="collectionArchiveCount">0 games</span></div>
        <div class="field"><label for="collectionGameSelect">Game</label><select id="collectionGameSelect"></select></div>
        <div class="field"><label for="collectionTargetSelect">Add to</label><select id="collectionTargetSelect"></select></div>
        <button class="btn" id="btnAddCollectionGame" type="button">ADD GAME</button>
      </div>
      <div class="content-head"><h2>Your collections</h2><span class="muted tiny">Saved on this device</span></div>
      <div id="collectionList"></div>
      <div id="collectionGames"></div>
    </section>

    <!-- ================= MORE ================= -->'''
replace_once(
    "app/src/main/assets/index.html",
    '    <!-- ================= MORE ================= -->',
    new_views,
    "More navigation marker"
)

# The More dashboard gets distinct, reachable destinations for the new areas.
replace_once(
    "app/src/main/assets/index.html",
    '      <div class="more-section-title"><h2>App</h2></div>',
    '''      <div class="more-section-title"><h2>Competitive &amp; Library</h2></div>
      <div class="more-action-grid">
        <button class="more-action" id="moreTournaments" type="button"><span class="more-action-icon" data-ic="trophy"></span><b>Events &amp; Cups</b><small>Solo bot cups and round results</small></button>
        <button class="more-action" id="moreAchievements" type="button"><span class="more-action-icon" data-ic="crown"></span><b>Achievements</b><small>XP, milestones and progress</small></button>
        <button class="more-action" id="moreCollections" type="button"><span class="more-action-icon" data-ic="book"></span><b>Game Collections</b><small>Save, organize and export PGNs</small></button>
      </div>
      <div class="more-section-title"><h2>App</h2></div>''',
    "More competitive and library cards"
)

# Add a profile shortcut to the achievements page.
replace_once(
    "app/src/main/assets/index.html",
    '      <div class="profile-section-head"><h2>Overview</h2><button class="text-btn" id="btnProfileStats" type="button">Full stats</button></div>',
    '''      <div class="profile-section-head"><h2>Overview</h2><button class="text-btn" id="btnProfileStats" type="button">Full stats</button></div>
      <div class="card profile-achievement-shortcut"><div class="content-head"><div><span class="eyebrow">PLAYER PROGRESS</span><h3>Achievements</h3><small class="muted" id="profileAchievementSummary">0 unlocked</small></div><button class="text-btn" id="btnProfileAchievements" type="button">VIEW ALL</button></div></div>''',
    "Profile achievement shortcut"
)

controller = r'''
  /* ================= ChessBuddy 2.0.0: Achievements ================= */
  const CB2_ACHIEVEMENTS = [
    { id:'first-game', title:'First Steps', detail:'Finish your first game against a ChessBuddy bot.', xp:25, metric:'games', target:1, icon:'tPlay' },
    { id:'first-win', title:'Opening Victory', detail:'Win your first completed bot game.', xp:35, metric:'wins', target:1, icon:'crown' },
    { id:'ten-games', title:'Getting Comfortable', detail:'Finish 10 bot games.', xp:50, metric:'games', target:10, icon:'chart' },
    { id:'fifty-games', title:'Regular at the Board', detail:'Finish 50 bot games.', xp:100, metric:'games', target:50, icon:'board' },
    { id:'hundred-games', title:'Century of Chess', detail:'Finish 100 bot games.', xp:200, metric:'games', target:100, icon:'trophy' },
    { id:'puzzle-five', title:'Tactical Spark', detail:'Solve 5 puzzles.', xp:30, metric:'puzzles', target:5, icon:'tPuzzle' },
    { id:'puzzle-twenty-five', title:'Pattern Hunter', detail:'Solve 25 puzzles.', xp:80, metric:'puzzles', target:25, icon:'tPuzzle' },
    { id:'rush-ten', title:'Rush Hour', detail:'Solve 10 puzzles in a single Puzzle Rush run.', xp:100, metric:'rush', target:10, icon:'spark' },
    { id:'daily-three', title:'Consistency', detail:'Build a 3-day daily puzzle streak.', xp:75, metric:'streak', target:3, icon:'calendar' },
    { id:'lesson-five', title:'Student of the Game', detail:'Complete 5 lessons.', xp:60, metric:'lessons', target:5, icon:'book' },
    { id:'opening-five', title:'Opening Explorer', detail:'Complete 5 Opening Lab courses.', xp:75, metric:'openings', target:5, icon:'book' },
    { id:'gambit-five', title:'Gambit Specialist', detail:'Complete 5 opening or gambit coach lines.', xp:90, metric:'gambits', target:5, icon:'spark' },
    { id:'cup-finish', title:'Cup Finisher', detail:'Complete a full Solo Bot Cup.', xp:100, metric:'cups', target:1, icon:'trophy' },
    { id:'cup-podium', title:'Podium Finish', detail:'Score at least 3 points in a completed 5- or 7-round cup.', xp:150, metric:'podiums', target:1, icon:'medal' }
  ];

  function cb2AchievementStats() {
    const p = settings.progress || {}, games = localCompletedGames();
    return {
      games:games.length,
      wins:games.filter(g => localGameResult(g) === 'win').length,
      puzzles:Number(p.puzzlesSolved || 0),
      rush:Math.max(Number(p.puzzleRushBest3 || 0), Number(p.puzzleRushBest5 || 0), Number(p.puzzleRushBestSurvival || 0)),
      streak:Number(p.dailyPuzzleBestStreak || p.dailyPuzzleStreak || 0),
      lessons:(p.completedLessons || []).length,
      openings:(p.completedOpenings || []).length,
      gambits:Number(p.gambitCompleted || 0),
      cups:(p.botCups || []).filter(e => e && e.completed).length,
      podiums:(p.botCups || []).filter(e => e && e.completed && (e.rounds === 5 || e.rounds === 7) && Number(e.score || 0) >= 3).length
    };
  }

  function cb2RefreshAchievementAwards(notify) {
    const p = settings.progress || (settings.progress = {});
    const awards = p.achievementAwards || (p.achievementAwards = {});
    const stats = cb2AchievementStats();
    let changed = false, newly = [];
    CB2_ACHIEVEMENTS.forEach(item => {
      if (stats[item.metric] >= item.target && !awards[item.id]) {
        awards[item.id] = { at:new Date().toISOString(), xp:item.xp };
        changed = true; newly.push(item.title);
      }
    });
    if (changed) saveSettings();
    if (notify && newly.length) toast('Achievement unlocked: ' + newly[0] + (newly.length > 1 ? ' +' + (newly.length - 1) + ' more' : ''));
    return awards;
  }

  function renderAchievements() {
    const awards = cb2RefreshAchievementAwards(false), stats = cb2AchievementStats();
    const unlocked = CB2_ACHIEVEMENTS.filter(a => !!awards[a.id]);
    const xp = unlocked.reduce((n,a) => n + a.xp, 0);
    const level = Math.floor(xp / 250) + 1, within = xp % 250;
    $('achievementXp').textContent = xp + ' XP';
    $('achievementLevel').textContent = 'LEVEL ' + level;
    $('achievementProgressBar').style.width = (within / 250 * 100) + '%';
    $('achievementProgressText').textContent = within + ' / 250 XP toward level ' + (level + 1);
    $('achievementUnlocked').textContent = String(unlocked.length);
    $('achievementAvailable').textContent = String(CB2_ACHIEVEMENTS.length - unlocked.length);
    $('achievementTotal').textContent = String(xp);
    $('achievementGrid').innerHTML = CB2_ACHIEVEMENTS.map(a => {
      const value = Math.min(a.target, Number(stats[a.metric] || 0)), done = !!awards[a.id];
      return '<article class="achievement-card ' + (done ? 'is-unlocked' : 'is-locked') + '">' +
        '<span class="achievement-icon" data-ic="' + a.icon + '"></span>' +
        '<div class="achievement-copy"><b>' + esc(a.title) + '</b><small>' + esc(a.detail) + '</small>' +
        '<span class="achievement-meter"><i style="width:' + (value / a.target * 100) + '%"></i></span>' +
        '<small>' + value + ' / ' + a.target + ' · ' + a.xp + ' XP' + (done ? ' · UNLOCKED' : '') + '</small></div></article>';
    }).join('');
    $('profileAchievementSummary').textContent = unlocked.length + ' / ' + CB2_ACHIEVEMENTS.length + ' unlocked · ' + xp + ' XP';
    if (typeof ic === 'function') $('achievementGrid').querySelectorAll('[data-ic]').forEach(el => { el.innerHTML = ic(el.getAttribute('data-ic')); });
  }

  /* ================= ChessBuddy 2.0.0: Solo Bot Cups ================= */
  let activeBotTournamentMatch = null;

  function cb2BotCups() {
    const p = settings.progress || (settings.progress = {});
    if (!Array.isArray(p.botCups)) p.botCups = [];
    return p.botCups;
  }

  function cb2CupOpponentList(rounds) {
    const roster = (Str.BOTS || []).filter(b => b && b.id && b.kind !== 'llm').slice();
    const target = practiceRating('rapid');
    roster.sort((a,b) => Math.abs(Number(a.elo || 1200) - target) - Math.abs(Number(b.elo || 1200) - target));
    return roster.slice(0, Math.max(rounds, 7));
  }

  function createBotCup() {
    const name = String($('botCupName').value || 'ChessBuddy Practice Cup').trim().slice(0,32) || 'ChessBuddy Practice Cup';
    const rounds = Math.max(3, Math.min(7, Number($('botCupRounds').value) || 5));
    const opponents = cb2CupOpponentList(rounds);
    if (opponents.length < rounds) { toast('Not enough playable bots are available for this cup.'); return; }
    const cup = {
      id:'cup-' + Date.now(),
      name:name,
      rounds:rounds,
      currentRound:0,
      score:0,
      opponentIds:opponents.slice(0,rounds).map(b => b.id),
      results:[],
      createdAt:new Date().toISOString(),
      completed:false
    };
    cb2BotCups().unshift(cup);
    saveSettings();
    renderTournaments();
    toast('Practice cup created. Start round 1 when ready.');
  }

  function cb2CupResult(gameEntry) {
    const match = activeBotTournamentMatch;
    if (!match || !gameEntry) return;
    const cup = cb2BotCups().find(e => e.id === match.cupId);
    if (!cup || cup.completed || cup.currentRound !== match.round) { activeBotTournamentMatch = null; return; }
    const human = gameEntry.human || 'w';
    const result = gameEntry.result === '1/2-1/2' ? 0.5 :
      gameEntry.result === (human === 'w' ? '1-0' : '0-1') ? 1 : 0;
    const bot = Str.botById(match.botId);
    cup.score = Number(cup.score || 0) + result;
    cup.results.push({
      round:match.round + 1,
      opponent:bot && bot.name ? String(bot.name) : 'ChessBuddy bot',
      outcome:result === 1 ? 'Win' : result === 0.5 ? 'Draw' : 'Loss',
      score:result,
      pgn:gameEntry.pgn || '',
      date:gameEntry.date || new Date().toISOString()
    });
    cup.currentRound++;
    cup.completed = cup.currentRound >= cup.rounds;
    cup.completedAt = cup.completed ? new Date().toISOString() : null;
    activeBotTournamentMatch = null;
    saveSettings();
    cb2RefreshAchievementAwards(true);
  }

  function startBotCupRound(cupId) {
    const cup = cb2BotCups().find(e => e.id === cupId);
    if (!cup || cup.completed || activeBotTournamentMatch) { toast('Choose an active cup with no round already running.'); return; }
    const bot = Str.botById(cup.opponentIds[cup.currentRound]);
    if (!bot) { toast('This cup opponent is no longer in the installed bot roster.'); return; }
    activeBotTournamentMatch = { cupId:cup.id, round:cup.currentRound, botId:bot.id };
    const opponent = botPlayer(bot), humanWhite = Math.random() >= 0.5;
    startGame(humanWhite ? { w:HUMAN, b:opponent } : { w:opponent, b:HUMAN }, { variant:'standard' });
  }

  function renderTournaments() {
    const cups = cb2BotCups(), active = cups.find(c => !c.completed);
    if (!active) $('botCupCurrent').innerHTML = '<p class="muted tiny">No active event. Create a cup to begin.</p>';
    else {
      const pct = active.currentRound / active.rounds * 100;
      const nextBot = Str.botById(active.opponentIds[active.currentRound]);
      $('botCupCurrent').innerHTML = '<article class="bot-cup-card"><div class="content-head"><div><span class="eyebrow">IN PROGRESS</span><h3>' + esc(active.name) + '</h3></div><span class="chip">' + active.score + ' / ' + active.rounds + '</span></div>' +
        '<div class="achievement-progress-track"><span style="width:' + pct + '%"></span></div><p class="muted tiny">Round ' + (active.currentRound + 1) + ' of ' + active.rounds + ' · ' + active.results.length + ' completed</p>' +
        (nextBot ? '<p>Next opponent: <b>' + esc(nextBot.name || 'ChessBuddy bot') + '</b> · ' + Number(nextBot.elo || 1200) + '</p>' : '') +
        (nextBot ? '<button class="btn primary" type="button" data-cup-start="' + esc(active.id) + '">PLAY ROUND ' + (active.currentRound + 1) + '</button>' : '<p class="muted tiny">The next opponent is unavailable.</p>') +
        '<div class="bot-cup-results">' + active.results.map(r => '<div><span>Round ' + r.round + '</span><b>' + esc(r.opponent) + '</b><strong class="' + r.outcome.toLowerCase() + '">' + r.outcome + '</strong></div>').join('') + '</div></article>';
    }
    const finished = cups.filter(c => c.completed);
    $('botCupHistory').innerHTML = finished.length ? finished.map(c =>
      '<article class="bot-cup-history"><b>' + esc(c.name) + '</b><span>' + c.score + ' / ' + c.rounds + ' points</span><small>' + new Date(c.completedAt || c.createdAt).toLocaleDateString() + ' · ' + c.results.length + ' rounds</small></article>'
    ).join('') : '<p class="muted tiny">Finished cups will appear here.</p>';
    $('botCupCurrent').querySelectorAll('[data-cup-start]').forEach(btn => {
      btn.addEventListener('click', () => startBotCupRound(btn.getAttribute('data-cup-start')));
    });
  }

  /* ================= ChessBuddy 2.0.0: PGN Collections ================= */
  function cb2Collections() {
    const p = settings.progress || (settings.progress = {});
    if (!Array.isArray(p.gameCollections)) p.gameCollections = [];
    if (!p.gameCollections.some(c => c && c.id === 'favorites')) p.gameCollections.unshift({ id:'favorites', name:'Favorites', gameIds:[] });
    p.gameCollections.forEach(c => { if (!Array.isArray(c.gameIds)) c.gameIds = []; });
    return p.gameCollections;
  }

  function cb2ArchiveGames() {
    return lsGet(K_GAMES, []).filter(g => g && g.id && g.pgn);
  }

  function renderCollections() {
    const collections = cb2Collections(), games = cb2ArchiveGames();
    $('collectionArchiveCount').textContent = games.length + ' archived games';
    $('collectionGameSelect').innerHTML = games.length ? games.slice(0,100).map(g =>
      '<option value="' + esc(g.id) + '">' + esc((g.white || 'White') + ' vs ' + (g.black || 'Black') + ' · ' + (g.date ? new Date(g.date).toLocaleDateString() : 'Archived game')) + '</option>'
    ).join('') : '<option value="">No archived PGN games yet</option>';
    $('collectionTargetSelect').innerHTML = collections.map(c => '<option value="' + esc(c.id) + '">' + esc(c.name) + '</option>').join('');
    $('collectionList').innerHTML = collections.map(c =>
      '<button class="collection-chip ' + (c.id === (settings.progress.selectedCollection || 'favorites') ? 'active' : '') + '" type="button" data-collection-open="' + esc(c.id) + '">' +
      '<b>' + esc(c.name) + '</b><small>' + c.gameIds.length + ' games</small></button>'
    ).join('');
    const selected = collections.find(c => c.id === (settings.progress.selectedCollection || 'favorites')) || collections[0];
    if (selected) settings.progress.selectedCollection = selected.id;
    const entries = selected ? selected.gameIds.map(id => games.find(g => g.id === id)).filter(Boolean) : [];
    $('collectionGames').innerHTML = selected ? '<div class="card collection-entry-card"><div class="content-head"><h3>' + esc(selected.name) + '</h3><span class="muted tiny">' + entries.length + ' saved</span></div>' +
      (entries.length ? entries.map(g => '<div class="collection-game-row"><span><b>' + esc(g.white || 'White') + ' vs ' + esc(g.black || 'Black') + '</b><small>' + esc(g.result || '*') + ' · ' + esc(g.date ? new Date(g.date).toLocaleDateString() : 'Saved game') + '</small></span><button class="btn small" type="button" data-pgn-copy="' + esc(g.id) + '">PGN</button><button class="btn small" type="button" data-collection-remove="' + esc(g.id) + '">REMOVE</button></div>').join('') : '<p class="muted tiny">This collection is empty. Add a game from your archive above.</p>') + '</div>' : '';
    $('collectionList').querySelectorAll('[data-collection-open]').forEach(btn => btn.addEventListener('click', () => {
      settings.progress.selectedCollection = btn.getAttribute('data-collection-open'); saveSettings(); renderCollections();
    }));
    $('collectionGames').querySelectorAll('[data-pgn-copy]').forEach(btn => btn.addEventListener('click', () => showCollectionPgn(btn.getAttribute('data-pgn-copy'))));
    $('collectionGames').querySelectorAll('[data-collection-remove]').forEach(btn => btn.addEventListener('click', () => removeCollectionGame(btn.getAttribute('data-collection-remove'))));
    $('btnAddCollectionGame').disabled = !games.length;
  }

  function createCollection() {
    const name = String($('collectionName').value || '').trim().slice(0,28);
    if (!name) { toast('Enter a collection name first.'); return; }
    const list = cb2Collections();
    if (list.some(c => c.name.toLowerCase() === name.toLowerCase())) { toast('A collection with that name already exists.'); return; }
    const item = { id:'col-' + Date.now(), name:name, gameIds:[] };
    list.push(item); settings.progress.selectedCollection = item.id;
    $('collectionName').value = ''; saveSettings(); renderCollections(); toast('Collection created.');
  }

  function addGameToCollection() {
    const gameId = $('collectionGameSelect').value, collectionId = $('collectionTargetSelect').value;
    const game = cb2ArchiveGames().find(g => g.id === gameId), collection = cb2Collections().find(c => c.id === collectionId);
    if (!game || !collection) { toast('Choose an archived game and a collection.'); return; }
    if (collection.gameIds.indexOf(game.id) >= 0) { toast('That game is already in this collection.'); return; }
    collection.gameIds.unshift(game.id);
    settings.progress.selectedCollection = collection.id;
    saveSettings(); renderCollections(); toast('Game added to ' + collection.name + '.');
  }

  function removeCollectionGame(gameId) {
    const collection = cb2Collections().find(c => c.id === settings.progress.selectedCollection);
    if (!collection) return;
    collection.gameIds = collection.gameIds.filter(id => id !== gameId);
    saveSettings(); renderCollections();
  }

  function showCollectionPgn(gameId) {
    const game = cb2ArchiveGames().find(g => g.id === gameId);
    if (!game) { toast('Archived PGN not found.'); return; }
    const pgn = String(game.pgn || '');
    openModal('<div class="content-head"><div><span class="eyebrow">GAME EXPORT</span><h3>PGN</h3></div></div>' +
      '<textarea id="collectionPgnText" rows="12" readonly spellcheck="false">' + esc(pgn) + '</textarea>' +
      '<p class="muted tiny">Copy this PGN to move the game into another chess tool.</p>' +
      '<div class="controls"><button class="btn primary" id="btnCopyCollectionPgn" type="button">COPY PGN</button><button class="btn" id="btnCloseCollectionPgn" type="button">CLOSE</button></div>');
    $('btnCloseCollectionPgn').onclick = closeModal;
    $('btnCopyCollectionPgn').onclick = () => {
      const text = $('collectionPgnText').value;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => toast('PGN copied.'), () => { $('collectionPgnText').focus(); $('collectionPgnText').select(); toast('Select and copy the PGN.'); });
      } else {
        $('collectionPgnText').focus(); $('collectionPgnText').select(); toast('Select and copy the PGN.');
      }
    };
  }
'''
replace_once(
    "app/src/main/assets/js/app.js",
    "  function renderMore() {",
    controller + "\n  function renderMore() {",
    "2.0.0 expansion controllers"
)

# Route names and screen titles.
replace_once(
    "app/src/main/assets/js/app.js",
    "const TAB_TITLES = { puzzles: 'Puzzles', learn: 'Learn', watch: 'Watch', more: 'More', profile:'Profile', stats:'Stats & Ratings', coach: 'Coach', history: 'Archive', settings: 'Settings' };",
    "const TAB_TITLES = { puzzles: 'Puzzles', learn: 'Learn', watch: 'Watch', more: 'More', profile:'Profile', stats:'Stats & Ratings', achievements:'Achievements', tournaments:'Events & Cups', collections:'Collections', coach: 'Coach', history: 'Archive', settings: 'Settings' };",
    "2.0.0 page titles"
)
replace_once(
    "app/src/main/assets/js/app.js",
    "['coach', 'history', 'settings', 'profile', 'stats'].indexOf(name) >= 0 ? 'more' : name",
    "['coach', 'history', 'settings', 'profile', 'stats', 'achievements', 'tournaments', 'collections'].indexOf(name) >= 0 ? 'more' : name",
    "2.0.0 destinations use More nav"
)
replace_once(
    "app/src/main/assets/js/app.js",
    "['profile','stats','settings','history','coach'].indexOf(currentTab) >= 0",
    "['profile','stats','settings','history','coach','achievements','tournaments','collections'].indexOf(currentTab) >= 0",
    "2.0.0 header back visibility"
)
replace_once(
    "app/src/main/assets/js/app.js",
    "  window.cbBack = function () {\\n    if (!$(\'modal\').hidden) { closeModal(); return true; }\\n    if (!$(\'boardOverlay\').hidden && playScreen === \'game\' && currentTab === \'play\') { hideOverlay(); return true; }\\n    if ([\'profile\',\'stats\',\'settings\',\'history\',\'coach\'].indexOf(currentTab) >= 0) { showTab(\'more\'); return true; }",
    "  window.cbBack = function () {\\n    if (!$(\'modal\').hidden) { closeModal(); return true; }\\n    if (!$(\'boardOverlay\').hidden && playScreen === \'game\' && currentTab === \'play\') { hideOverlay(); return true; }\\n    if ([\'profile\',\'stats\',\'settings\',\'history\',\'coach\',\'achievements\',\'tournaments\',\'collections\'].indexOf(currentTab) >= 0) { showTab(\'more\'); return true; }",
    "2.0.0 back navigation"
)

# Page-specific render hooks are placed beside the existing Profile and Stats hooks.
replace_once(
    "app/src/main/assets/js/app.js",
    "    if (name === 'stats') renderStats();",
    "    if (name === 'stats') renderStats();\n    if (name === 'achievements') renderAchievements();\n    if (name === 'tournaments') renderTournaments();\n    if (name === 'collections') renderCollections();",
    "2.0.0 render hooks"
)

# Add navigation handlers inside the existing event-wiring block.
replace_once(
    "app/src/main/assets/js/app.js",
    "    $('moreAbout').onclick = () => { showTab('settings'); $('cardAbout').scrollIntoView({ behavior:'smooth', block:'start' }); };",
    """    $('moreAbout').onclick = () => { showTab('settings'); $('cardAbout').scrollIntoView({ behavior:'smooth', block:'start' }); };
    $('moreAchievements').onclick = () => showTab('achievements');
    $('moreTournaments').onclick = () => showTab('tournaments');
    $('moreCollections').onclick = () => showTab('collections');
    $('btnProfileAchievements').onclick = () => showTab('achievements');
    $('btnCreateBotCup').onclick = createBotCup;
    $('btnCreateCollection').onclick = createCollection;
    $('btnAddCollectionGame').onclick = addGameToCollection;""",
    "2.0.0 page navigation and buttons"
)

# Attach actual tournament metadata to the archived game and score the round only after
# recordGame has saved the final result.
replace_once(
    "app/src/main/assets/js/app.js",
    "      plies: game.history().length, pgn: game.pgn(), fen: game.fen(), variant:activeGameVariant, done: !!over, practiceRating:practiceRatingChange });",
    """      plies: game.history().length, pgn: game.pgn(), fen: game.fen(), variant:activeGameVariant, done: !!over, practiceRating:practiceRatingChange,
      tournament:activeBotTournamentMatch ? { id:activeBotTournamentMatch.cupId, round:activeBotTournamentMatch.round + 1 } : null });
    if (list[0].tournament) cb2CupResult(list[0]);""",
    "record Solo Bot Cup game results"
)

css = r'''
/* ChessBuddy 2.0.0 expansion */
.achievement-hero,.tournament-hero,.collection-hero { margin-bottom:12px; }
.achievement-level-card {
  padding:16px; border-radius:16px; background:linear-gradient(130deg,#34442e,#252c24);
  border:1px solid #ffffff18; margin:8px 0 12px; color:#f3f4ed;
}
.achievement-level-top { display:flex; align-items:center; justify-content:space-between; gap:10px; }
.achievement-level-top>div { display:flex; flex-direction:column; gap:4px; }
.achievement-level-top b { font-size:27px; font-variant-numeric:tabular-nums; }
.achievement-level-pill { border-radius:99px; padding:6px 10px; background:#d5e9bb; color:#26351f; font-size:10px; font-weight:900; }
.achievement-progress-track { height:8px; background:#ffffff24; border-radius:20px; overflow:hidden; margin:13px 0 7px; }
.achievement-progress-track>span { display:block; height:100%; background:#b5d98c; border-radius:20px; }
.achievement-level-card>small { color:#d0d8c8; font-size:10px; }
.achievement-summary-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:8px; margin:10px 0 18px; }
.achievement-summary-grid>div { display:flex; flex-direction:column; align-items:center; gap:3px; padding:12px 4px; border-radius:12px; background:var(--surface); border:1px solid var(--line); }
.achievement-summary-grid b { font-size:22px; font-variant-numeric:tabular-nums; }
.achievement-summary-grid span { color:var(--muted); font-size:10px; }
.achievement-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:9px; margin:10px 0 16px; }
.achievement-card { display:flex; gap:10px; min-width:0; min-height:110px; padding:12px; border-radius:13px; border:1px solid var(--line); background:var(--surface); }
.achievement-card.is-locked { opacity:.68; }
.achievement-card.is-unlocked { border-color:#86a96980; background:linear-gradient(140deg,var(--surface),#819f5d18); }
.achievement-icon { display:grid; place-items:center; flex:none; width:35px; height:35px; border-radius:10px; background:var(--surface2); color:#b9d995; }
.achievement-icon svg { width:20px; height:20px; }
.achievement-copy { display:flex; flex-direction:column; gap:5px; min-width:0; flex:1; }
.achievement-copy>b { font-size:12px; line-height:1.25; }
.achievement-copy>small { color:var(--muted); font-size:9.5px; line-height:1.3; overflow-wrap:anywhere; }
.achievement-meter { height:5px; border-radius:9px; overflow:hidden; background:var(--surface2); }
.achievement-meter i { display:block; height:100%; border-radius:9px; background:#99bc72; }
.bot-cup-card,.bot-cup-history { padding:14px; margin:9px 0; border:1px solid var(--line); border-radius:14px; background:var(--surface); }
.bot-cup-card h3 { margin:3px 0; font-size:16px; }
.bot-cup-card>p { font-size:12px; }
.bot-cup-card .btn { width:100%; margin:5px 0; }
.bot-cup-results { margin-top:9px; border-top:1px solid var(--line); }
.bot-cup-results>div,.bot-cup-history { display:flex; align-items:center; justify-content:space-between; gap:8px; flex-wrap:wrap; }
.bot-cup-results>div { padding:8px 0; border-bottom:1px solid var(--line); font-size:11px; }
.bot-cup-results>div>span,.bot-cup-history>small { color:var(--muted); font-size:10px; }
.bot-cup-results strong { font-size:11px; }.bot-cup-results strong.win { color:#9bc879; }.bot-cup-results strong.loss { color:#d68b81; }.bot-cup-results strong.draw { color:var(--muted); }
.bot-cup-history { flex-direction:column; align-items:flex-start; }
.bot-cup-history span { color:#b9d995; font-size:12px; font-weight:800; }
.collection-chip { display:inline-flex; flex-direction:column; align-items:flex-start; gap:3px; border:1px solid var(--line); border-radius:10px; background:var(--surface); color:var(--text); padding:9px 12px; margin:0 6px 6px 0; cursor:pointer; }
.collection-chip.active { border-color:#95b96c; background:#92b96b1a; }
.collection-chip>b { font-size:12px; }.collection-chip>small { color:var(--muted); font-size:10px; }
.collection-entry-card { margin-top:10px; }
.collection-game-row { display:flex; align-items:center; gap:6px; padding:9px 0; border-top:1px solid var(--line); min-width:0; }
.collection-game-row>span { display:flex; flex-direction:column; gap:3px; flex:1; min-width:0; }
.collection-game-row b { font-size:11px; overflow-wrap:anywhere; }
.collection-game-row small { color:var(--muted); font-size:10px; }
.collection-game-row .btn { min-height:34px; padding:5px 8px; font-size:10px; }
.profile-achievement-shortcut { margin:10px 0; }
#collectionPgnText { width:100%; min-height:180px; font-family:monospace; font-size:11px; }
@media(max-width:360px) {
  .achievement-grid { grid-template-columns:1fr; }
  .collection-game-row { flex-wrap:wrap; }
  .collection-game-row>span { flex-basis:100%; }
}
'''
replace_once(
    "app/src/main/assets/css/app.css",
    "/* ChessBuddy mobile product refresh */",
    "/* ChessBuddy mobile product refresh */\n" + css,
    "2.0.0 expansion styles"
)

print("ChessBuddy 2.0.0 expansion applied: achievement XP, local bot cups, PGN collections.")
