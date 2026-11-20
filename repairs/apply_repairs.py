from pathlib import Path

def edit(path, replacements):
    p = Path(path)
    s = p.read_text()
    for old, new in replacements:
        if old not in s:
            raise SystemExit("Expected source fragment not found in " + path + ": " + old[:90].replace("\n", "\\n"))
        s = s.replace(old, new, 1)
    p.write_text(s)

# Root cause of the Supabase 401: native HTTP silently dropped JWTs longer than 512 chars.
edit("app/src/main/java/com/chessbuddy/HttpTransport.java", [
("""            String name = line.substring(0, i).trim(), value = line.substring(i + 1).trim();
            if (name.matches("[A-Za-z0-9-]{1,64}") && value.length() <= 512 && value.indexOf('\\r') < 0 && value.indexOf('\\n') < 0) c.setRequestProperty(name, value);
""",
"""            String name = line.substring(0, i).trim(), value = line.substring(i + 1).trim();
            // Supabase JWTs commonly exceed 512 characters. The old cap silently discarded
            // Authorization, so /auth/v1/user and authenticated REST/RPC calls arrived unauthenticated.
            int maxValueLength = "authorization".equalsIgnoreCase(name) ? 16384 : 512;
            if (name.matches("[A-Za-z0-9-]{1,64}") && value.length() <= maxValueLength && value.indexOf('\\r') < 0 && value.indexOf('\\n') < 0) c.setRequestProperty(name, value);
"""),
("    private static void applyExtraHeaders(HttpURLConnection c, String extra) {",
 "    static void applyExtraHeaders(HttpURLConnection c, String extra) {")
])

# Java regression test: preserve long Authorization while keeping ordinary header caps.
edit("tests/java/PolicyTest.java", [
("package com.chessbuddy;\n",
"""package com.chessbuddy;
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
"""),
("""public class PolicyTest {
    static int fails = 0;
""",
"""public class PolicyTest {
    static final class HeaderCapture extends HttpURLConnection {
        final Map<String, String> headers = new HashMap<String, String>();
        HeaderCapture() throws Exception { super(new URL("https://example.test/")); }
        @Override public void disconnect() { }
        @Override public boolean usingProxy() { return false; }
        @Override public void connect() throws IOException { }
        @Override public void setRequestProperty(String key, String value) { headers.put(key.toLowerCase(java.util.Locale.US), value); }
    }
    static int fails = 0;
"""),
("""        eq("null blocked", ok(null), false);
""",
"""        eq("null blocked", ok(null), false);
        HeaderCapture captured = new HeaderCapture();
        String longBearer = "Bearer " + new String(new char[1400]).replace('\\0', 'x');
        HttpTransport.applyExtraHeaders(captured, "apikey: sb_publishable_test\\nAuthorization: " + longBearer);
        eq("long Supabase Bearer JWT is retained", captured.headers.get("authorization"), longBearer);
        eq("publishable key is retained", captured.headers.get("apikey"), "sb_publishable_test");
""")
])

# Delay presence until the profile exists; presence rows reference chessbuddy_profiles.
edit("app/src/main/assets/js/app.js", [
("""  const sfPlayer = b => ({ kind: 'sf', botId: b.id, name: b.name, elo: b.elo, ratingLabel: b.ratingLabel, level: b.level || 0, boost: b.boost || 0, vis: b.vis || 0, adaptive: !!b.adaptive, flag: b.flag || '', av: Avatars.forBot ? Avatars.forBot(b) : b.av, cat: b.cat, engine: b.engine || 'stockfish', modelId: b.modelId || '' });
""",
"""  const sfPlayer = b => ({ kind: 'sf', botId: b.id, name: b.name, elo: b.elo, ratingLabel: b.ratingLabel, level: b.level || 0, boost: b.boost || 0, vis: b.vis || 0, adaptive: !!b.adaptive, flag: b.flag || '', av: Avatars.forBot ? Avatars.forBot(b) : b.av, cat: b.cat, engine: b.engine || 'stockfish', modelId: b.modelId || '', isTribute: !!b.isTribute });
"""),
("""  async function openOnlinePage() {
    clearInterval(onlineHubTimer);
    if (!Online.available) { setOnlinePanels('auth'); onlineMessage('Online play is available in the Android app only.', 'warn'); return; }
    if (Online.signedIn()) { await Online.setPresence('online').catch(noop); await refreshOnlineHub(false); onlineHubTimer = setInterval(() => { if (playScreen === 'online' && Online.signedIn()) refreshOnlineHub(false); }, 6500); startOnlineHeartbeat(); return; }
    setOnlinePanels('auth'); onlineMessage('');
    try {
      await Online.restore();
      await Online.setPresence('online');
      await refreshOnlineHub(false);
      onlineHubTimer = setInterval(() => { if (playScreen === 'online' && Online.signedIn()) refreshOnlineHub(false); }, 6500);
      startOnlineHeartbeat();
    } catch (e) {
      setOnlinePanels('auth');
      if (e.message && e.message.indexOf('No saved session') < 0) onlineMessage('Sign in to continue. ' + e.message, 'warn');
    }
  }
""",
"""  async function openOnlinePage() {
    clearInterval(onlineHubTimer);
    if (!Online.available) { setOnlinePanels('auth'); onlineMessage('Online play is available in the Android app only.', 'warn'); return; }
    setOnlinePanels('auth'); onlineMessage('');
    try {
      if (!Online.signedIn()) await Online.restore();
      // A new account has no profile row yet. Presence has a foreign key to that profile.
      await refreshOnlineHub(false);
      if (onlineProfile) await Online.setPresence('online');
      onlineHubTimer = setInterval(() => { if (playScreen === 'online' && Online.signedIn()) refreshOnlineHub(false); }, 6500);
      if (onlineProfile) startOnlineHeartbeat();
    } catch (e) {
      setOnlinePanels('auth');
      if (e.message && e.message.indexOf('No saved session') < 0) onlineMessage('Sign in to continue. ' + e.message, 'warn');
    }
  }
"""),
("""      await Online.setPresence('online');
      await refreshOnlineHub(false);
      if (!onlineHubTimer) onlineHubTimer = setInterval(() => { if (playScreen === 'online' && Online.signedIn()) refreshOnlineHub(false); }, 6500);
      startOnlineHeartbeat();
      if (create) onlineMessage('Account created. Finish your player profile below.', 'ok');
""",
"""      // Do not create presence until the authenticated user has registered a profile row.
      await refreshOnlineHub(false);
      if (onlineProfile) {
        await Online.setPresence('online');
        if (!onlineHubTimer) onlineHubTimer = setInterval(() => { if (playScreen === 'online' && Online.signedIn()) refreshOnlineHub(false); }, 6500);
        startOnlineHeartbeat();
      }
      if (create) onlineMessage(onlineProfile ? 'Account created. Your player profile is ready.' : 'Account created. Choose a username and display name to finish setting up your profile.', 'ok');
"""),
("""      (maia ? '<div class="notice info">Maia predicts human-like moves. Its official model is downloaded once on this device when you start the game; no AI API key is needed.</div>' : '') +
""",
"""      (maia ? '<div class="notice info">Maia predicts human-like moves. Its official model is downloaded once on this device when you start the game; no AI API key is needed.</div>' : '') +
      (p.isTribute ? '<div class="notice info">ChessBuddy tribute profile. This bot uses Stockfish at an approximate practice rating; it is not an official account, verified likeness, or simulation of this player.</div>' : '') +
""")
])

# Add 88 actual chess-player names as clearly labelled Stockfish tribute profiles.
players = [
('ian_nepomniachtchi','Ian Nepomniachtchi',2767),('alireza_firouzja','Alireza Firouzja',2804),('levon_aronian','Levon Aronian',2729),('wesley_so','Wesley So',2751),('maxime_vachier_lagrave','Maxime Vachier-Lagrave',2732),('shakhriyar_mamedyarov','Shakhriyar Mamedyarov',2725),('teimour_radjabov','Teimour Radjabov',2700),('sergey_karjakin','Sergey Karjakin',2747),('alexander_grischuk','Alexander Grischuk',2724),('peter_svidler','Peter Svidler',2690),('anish_giri','Anish Giri',2740),('jan_krzysztof_duda','Jan-Krzysztof Duda',2726),('richard_rapport','Richard Rapport',2719),('praggnanandhaa','R. Praggnanandhaa',2743),('arjun_erigaisi','Arjun Erigaisi',2771),('nihal_sarin','Nihal Sarin',2681),('vidit_gujrathi','Vidit Gujrathi',2715),('pentala_harikrishna','Pentala Harikrishna',2693),('parham_maghsoodloo','Parham Maghsoodloo',2719),('amin_tabatabaei','Amin Tabatabaei',2695),('nodirbek_abdusattorov','Nodirbek Abdusattorov',2766),('javokhir_sindarov','Javokhir Sindarov',2692),('daniil_dubov','Daniil Dubov',2705),('vladislav_artemiev','Vladislav Artemiev',2700),('andrey_esipenko','Andrey Esipenko',2683),('alexey_sarana','Alexey Sarana',2680),('sam_shankland','Sam Shankland',2692),('ray_robson','Ray Robson',2662),('jeffery_xiong','Jeffery Xiong',2650),('awonder_liang','Awonder Liang',2612),('sam_sevian','Sam Sevian',2660),('hans_niemann','Hans Moke Niemann',2660),('daniel_naroditsky','Daniel Naroditsky',2620),('michael_adams','Michael Adams',2690),('nigel_short','Nigel Short',2650),('john_nunn','John Nunn',2600),('jonathan_speelman','Jonathan Speelman',2530),('matthew_sadler','Matthew Sadler',2640),('ivan_sokolov','Ivan Sokolov',2600),('alexei_shirov','Alexei Shirov',2690),('vasyl_ivanchuk','Vasyl Ivanchuk',2690),('sergey_tiviakov','Sergei Tiviakov',2600),('boris_gelfand','Boris Gelfand',2660),('peter_leko','Peter Leko',2670),('alexander_morozevich','Alexander Morozevich',2650),('evgeny_tomashevsky','Evgeny Tomashevsky',2630),('rustam_kasimdzhanov','Rustam Kasimdzhanov',2650),('leinier_dominguez','Leinier Dominguez',2700),('koneru_humpy','Koneru Humpy',2580),('anna_muzychuk','Anna Muzychuk',2520),('mariya_muzychuk','Mariya Muzychuk',2500),('kateryna_lagno','Kateryna Lagno',2540),('alexandra_kosteniuk','Alexandra Kosteniuk',2500),('tan_zhongyi','Tan Zhongyi',2500),('lei_tingjie','Lei Tingjie',2540),('ju_wenjun','Ju Wenjun',2560),('zhu_jiner','Zhu Jiner',2520),('bibisara_assaubayeva','Bibisara Assaubayeva',2500),('aleksandra_goryachkina','Aleksandra Goryachkina',2550),('harika_dronavalli','Harika Dronavalli',2500),('nana_dzagnidze','Nana Dzagnidze',2500),('elisabeth_paethz','Elisabeth Paehtz',2450),('pia_cramling','Pia Cramling',2450),('nona_gaprindashvili','Nona Gaprindashvili',2400),('maia_chiburdanidze','Maia Chiburdanidze',2450),('susan_polgar','Susan Polgar',2450),('tania_sachdev','Tania Sachdev',2400),('anna_cramling','Anna Cramling',2300),('mikhail_chigorin','Mikhail Chigorin',2600),('johannes_zukertort','Johannes Zukertort',2550),('joseph_blackburne','Joseph Henry Blackburne',2550),('henry_bird','Henry Bird',2450),('harry_pillsbury','Harry Nelson Pillsbury',2650),('frank_marshall','Frank Marshall',2600),('dawid_janowski','Dawid Janowski',2550),('carl_schlechter','Carl Schlechter',2550),('rudolf_spielmann','Rudolf Spielmann',2550),('richard_reti','Richard Réti',2550),('savelly_tartakower','Savielly Tartakower',2550),('gyula_breyer','Gyula Breyer',2450),('efim_bogoljubow','Efim Bogoljubow',2600),('salomon_flohr','Salo Flohr',2600),('samuel_reshevsky','Samuel Reshevsky',2650),('miguel_najdorf','Miguel Najdorf',2650),('geza_maroczy','Géza Maróczy',2550),('svetozar_gligoric','Svetozar Gligorić',2600),('wolfgang_uhlmann','Wolfgang Uhlmann',2550),('isaac_boleslavsky','Isaac Boleslavsky',2550)]
if len(players) < 80 or len({x[0] for x in players}) != len(players) or len({x[1].lower() for x in players}) != len(players):
    raise SystemExit("Real-player roster failed uniqueness/count checks")
roster = """  /* Real chess players. These are Stockfish practice bots with approximate difficulty labels,
   * not simulations, official accounts, endorsements, or verified likenesses. */
  var REAL_PLAYERS = [
""" + ",\n".join("    { id: %r, name: %r, elo: %d }" % x for x in players) + """
  ].map(function (p) {
    var b = bot('cp_' + p.id, p.name, p.elo, 'Chess Personalities', 'ChessBuddy tribute profile. Stockfish practice opponent at an approximate difficulty rating; not an official account or a simulation of this player.', genSpec('cp_' + p.id));
    b.isTribute = true;
    return b;
  });
"""
edit("app/src/main/assets/js/strength.js", [
("  var MAIA = [\n", roster + "  var MAIA = [\n"),
("BOTS = BOTS.concat(GM, LEGENDS, CHARACTERS, GENERATED, VIS, MAIA);",
 "BOTS = BOTS.concat(GM, LEGENDS, CHARACTERS, GENERATED, VIS, REAL_PLAYERS, MAIA);"),
("'Personalities', 'Characters', 'Visualization', 'Maia'];",
 "'Personalities', 'Characters', 'Visualization', 'Chess Personalities', 'Maia'];")
])

# Portrait shading and detail improvements while keeping every avatar original SVG.
edit("app/src/main/assets/js/avatars.js", [
("""'<linearGradient id="' + uid + '-skin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="' + s.skin + '"/><stop offset=".72" stop-color="' + s.skin + '"/><stop offset="1" stop-color="#74472f" stop-opacity=".38"/></linearGradient>' +""",
"""'<linearGradient id="' + uid + '-skin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff0df" stop-opacity=".48"/><stop offset=".18" stop-color="' + s.skin + '"/><stop offset=".66" stop-color="' + s.skin + '"/><stop offset="1" stop-color="#55372d" stop-opacity=".62"/></linearGradient>' +
      '<radialGradient id="' + uid + '-cheek"><stop stop-color="#e78c7e" stop-opacity=".22"/><stop offset="1" stop-color="#e78c7e" stop-opacity="0"/></radialGradient>' +"""),
("""      p.push('<g clip-path="url(#' + uid + '-faceClip)"><ellipse cx="46" cy="79" rx="8" ry="4" fill="#e67c79" opacity=".16"/><ellipse cx="82" cy="79" rx="8" ry="4" fill="#e67c79" opacity=".16"/><path d="M34 91 Q64 112 94 91 L94 111 L34 111Z" fill="#6d4137" opacity=".06"/></g>');""",
"""      p.push('<g clip-path="url(#' + uid + '-faceClip)"><ellipse cx="45" cy="79" rx="15" ry="10" fill="url(#' + uid + '-cheek)"/><ellipse cx="83" cy="79" rx="15" ry="10" fill="url(#' + uid + '-cheek)"/><path d="M38 52 Q45 34 64 34 Q84 34 90 52" stroke="#fff" stroke-opacity=".13" stroke-width="5" fill="none"/><path d="M39 76 Q45 91 52 92 M89 76 Q83 91 76 92" stroke="#6d4137" stroke-opacity=".11" stroke-width="2" fill="none"/><path d="M34 91 Q64 112 94 91 L94 111 L34 111Z" fill="#6d4137" opacity=".07"/></g>');"""),
("""      p.push('<path d="M64 69 Q60 79 64 81 Q67 83 69 80" stroke="#8b5d48" stroke-opacity=".6" stroke-width="1.8" fill="none" stroke-linecap="round"/>');""",
"""      p.push('<path d="M64 68 Q59 79 63 82 Q66 84 69 80" stroke="#8b5d48" stroke-opacity=".58" stroke-width="1.8" fill="none" stroke-linecap="round"/><path d="M62 80 Q64 82 67 80" stroke="#fff0df" stroke-opacity=".36" stroke-width="1.3" fill="none" stroke-linecap="round"/><path d="M46 70 Q53 73 59 70 M69 70 Q76 73 82 70" stroke="#fff" stroke-opacity=".16" stroke-width="1.2" fill="none"/>');""")
])

# Roster + signup regression tests.
edit("tests/logic/strength-models.test.js", [
("test('Legends are deceased players only; living players are Top Players', () => {\n",
"""test('Chess Personalities roster contains at least 80 real-player tribute profiles, all explicitly non-simulations', () => {
  const players = S.BOTS.filter(b => b.cat === 'Chess Personalities');
  assert.ok(players.length >= 80, 'expected 80+ named player profiles, got ' + players.length);
  assert.ok(players.every(b => b.id.startsWith('cp_') && b.isTribute && b.elo >= 2200 && b.elo <= 2900));
  assert.strictEqual(new Set(players.map(b => b.name.toLowerCase())).size, players.length);
});
test('Legends are deceased players only; living players are Top Players', () => {
""")
])
edit("tests/logic/online-auth.test.js", [
("test('presence is blocked until a verified authenticated user session exists', async () => {\n",
"""test('email signup can complete without a session and does not create authenticated requests', async () => {
  const { api, calls } = setup();
  await api.signUp('new-player@example.com', 'a-long-password');
  assert.strictEqual(api.signedIn(), false, 'email confirmation may leave signup without a session');
  await assert.rejects(api.setPresence('online'), /session is missing/i);
  assert.strictEqual(calls.some(c => c.type === 'post'), false);
});

test('presence is blocked until a verified authenticated user session exists', async () => {
""")
])
edit("tests/ui/ui.test.js", [
("'Personalities', 'Visualization', 'Maia'",
 "'Personalities', 'Chess Personalities', 'Visualization', 'Maia'")
])

print("ChessBuddy repair overlay applied.")




# Online-play hardening: server move endpoint, authoritative clocks and polling.
def edit_online(path, replacements):
    from pathlib import Path
    p = Path(path)
    content = p.read_text(encoding="utf-8")
    for old, new in replacements:
        if old not in content:
            raise SystemExit("Online-play patch could not find expected source in " + path + ": " + old[:100].replace("\n", "\\n"))
        content = content.replace(old, new, 1)
    p.write_text(content, encoding="utf-8")

edit_online("app/src/main/assets/js/clock.js", [
("""  Clock.restore = function (s) {
    var c = new Clock(byId(s.id), s);
    c.running = s.running === 'w' || s.running === 'b' ? s.running : (c.moves >= 1 ? (c.moves % 2 === 1 ? 'b' : 'w') : 'w');
    return c;
  };""",
"""  Clock.restore = function (s) {
    var c = new Clock(byId(s.id), s);
    // Explicit null means an online game is waiting for White's opening move.
    if (s && Object.prototype.hasOwnProperty.call(s, 'running')) {
      c.running = s.running === 'w' || s.running === 'b' ? s.running : null;
    } else {
      c.running = c.moves >= 1 ? (c.moves % 2 === 1 ? 'b' : 'w') : 'w';
    }
    return c;
  };""")
])

edit_online("app/src/main/assets/js/app.js", [
("""    try {
      await Online.applyMove({ id: online.id, fen: game.fen(), pgn: game.pgn(), whiteMs: c.w, blackMs: c.b,
        finished: !!over, result: over ? resultCode() : null, winner: over && over.winner ? (over.winner === online.myColor ? Online.user().id : online.opponentId) : null });
      online.saving = false; online.lastUpdated = new Date().toISOString(); saveCurrent(); renderControls(); renderStatus();
    } catch (e) { online.saving = false; online.syncError = true; renderControls(); setStatus('Move not synced. Reopen the game from the online list to reload the server position. ' + e.message, 'bad'); throw e; }
""",
"""    try {
      const saved = await Online.applyMove({ id: online.id, fen: game.fen(), pgn: game.pgn(), whiteMs: c.w, blackMs: c.b,
        finished: !!over, result: over ? resultCode() : null, winner: over && over.winner ? (over.winner === online.myColor ? Online.user().id : online.opponentId) : null });
      const serverGame = saved && saved.game;
      if (serverGame && ctx.clock) {
        ctx.clock = Clock.restore({ id: serverGame.time_control || online.timeControl,
          w: Number(serverGame.white_ms) || 0, b: Number(serverGame.black_ms) || 0,
          moves: game.history().length, running: game.history().length ? serverGame.turn_color : null });
        if (ctx.clock.running && serverGame.updated_at) {
          const elapsed = Math.max(0, Date.now() - new Date(serverGame.updated_at).getTime());
          ctx.clock.t[ctx.clock.running] = Math.max(0, ctx.clock.t[ctx.clock.running] - elapsed);
          ctx.clock.last = performance.now();
        }
      }
      online.saving = false; online.lastUpdated = serverGame && serverGame.updated_at || new Date().toISOString();
      saveCurrent(); renderControls(); renderClocks(); renderStatus();
    } catch (e) { online.saving = false; online.syncError = true; renderControls(); setStatus('Move not synced. Reopen the game from the online list to reload the server position. ' + e.message, 'bad'); throw e; }
"""),
("""  async function pollOnlineGame() {
    if (!ctx.online || ctx.online.polling || ctx.online.saving) return;
    ctx.online.polling = true;
    try {
      const row = await Online.game(ctx.online.id); if (!row) return;
      if (row.pgn && row.pgn !== game.pgn()) {
""",
"""  async function pollOnlineGame() {
    if (!ctx.online || ctx.online.polling || ctx.online.saving) return;
    ctx.online.polling = true;
    try {
      const row = await Online.game(ctx.online.id); if (!row) return;
      const previousUpdatedAt = ctx.online.lastUpdated;
      if (row.pgn && row.pgn !== game.pgn()) {
"""),
("""        over = computeOver(); sel = null; legalMap = {}; capMap = {}; viewPly = null; saveCurrent(); render();
      } else if (ctx.clock && row.updated_at && row.updated_at !== ctx.online.lastUpdated) {
        ctx.clock = Clock.restore({ id: row.time_control, w: Number(row.white_ms) || 0, b: Number(row.black_ms) || 0, moves: game.history().length, running: game.history().length ? row.turn_color : null });
        if (ctx.clock && ctx.clock.running) { const e = Math.max(0, Date.now() - new Date(row.updated_at).getTime()); ctx.clock.t[ctx.clock.running] = Math.max(0, ctx.clock.t[ctx.clock.running] - e); ctx.clock.last = performance.now(); }
        ctx.online.lastUpdated = row.updated_at; renderClocks();
      }
""",
"""        over = computeOver(); sel = null; legalMap = {}; capMap = {}; viewPly = null; saveCurrent(); render();
        ctx.online.lastUpdated = row.updated_at || ctx.online.lastUpdated;
      } else if (ctx.clock && row.updated_at && row.updated_at !== previousUpdatedAt) {
        ctx.clock = Clock.restore({ id: row.time_control, w: Number(row.white_ms) || 0, b: Number(row.black_ms) || 0, moves: game.history().length, running: game.history().length ? row.turn_color : null });
        if (ctx.clock && ctx.clock.running) { const e = Math.max(0, Date.now() - new Date(row.updated_at).getTime()); ctx.clock.t[ctx.clock.running] = Math.max(0, ctx.clock.t[ctx.clock.running] - e); ctx.clock.last = performance.now(); }
        ctx.online.lastUpdated = row.updated_at; renderClocks();
      } else if (row.updated_at) {
        ctx.online.lastUpdated = row.updated_at;
      }
""")
])

edit_online("supabase/functions/_shared/online-validation.mjs", [
("    const elapsed = Math.max(0, nowMs - updatedAt);",
 "    // White's opening move starts Black's clock; challenge waiting time is uncharged.\n    const elapsed = game.pgn ? Math.max(0, nowMs - updatedAt) : 0;")
])

edit_online("supabase/operations/validated_online_moves.sql", [
("-- DRAFT ONLY — do not apply until the apply-online-move Edge Function is deployed and tested.\n-- The app must stop calling cb_apply_move directly before this is enabled.",
 "-- Apply alongside the apply-online-move Edge Function. The Android app calls the\n-- Edge Function; direct client writes to cb_apply_move are disabled."),
("    v_elapsed_ms := greatest(0, floor(extract(epoch from (v_now - g.updated_at)) * 1000)::bigint);",
 "    -- Do not charge White for time spent waiting for the opening move.\n    v_elapsed_ms := case when coalesce(g.pgn, '') = '' then 0\n      else greatest(0, floor(extract(epoch from (v_now - g.updated_at)) * 1000)::bigint) end;"),
("if p_next_turn_color is distinct from case when g.turn_color = 'w' then 'b' else 'w' end then",
 "if p_next_turn_color is distinct from (case when g.turn_color = 'w' then 'b' else 'w' end) then"),
("if p_next_turn_user is distinct from case when g.turn_color = 'w' then g.black_user_id else g.white_user_id end then",
 "if p_next_turn_user is distinct from (case when g.turn_color = 'w' then g.black_user_id else g.white_user_id end) then")
])

edit_online("tests/logic/coaches-clock.test.js", [
("test('clock: an expired side cannot receive increment or hand the clock to the opponent', () => {",
"""test('online clock: an explicit null stays stopped until White makes the first move', () => {
  const c = C.restore({ id: '3+2', w: 180000, b: 180000, moves: 0, running: null });
  assert.strictEqual(c.running, null);
  assert.strictEqual(c.t.w, 180000);
  c.onMove('w', 5000);
  assert.strictEqual(c.t.w, 182000);
  assert.strictEqual(c.running, 'b');
  assert.strictEqual(c.moves, 1);
});
test('clock: an expired side cannot receive increment or hand the clock to the opponent', () => {""")
])

edit_online("tests/logic/online-validation.test.js", [
("""  const expired = game(); expired.updated_at = new Date(now - 181000).toISOString();
  assert.strictEqual(validateOnlineMove(Chess, expired, payload('e4'), 'white-user', now).status, 409);
""",
"""  const expired = game();
  const first = new Chess(); first.move('e4');
  expired.current_fen = first.fen(); expired.pgn = first.pgn();
  expired.turn_user_id = 'black-user'; expired.turn_color = 'b';
  expired.white_ms = 182000; expired.updated_at = new Date(now - 181000).toISOString();
  const second = new Chess(); second.move('e4'); second.move('e5');
  const afterOpening = { game_id: expired.id, p_next_fen: second.fen(), p_pgn: second.pgn(), p_white_ms: 182000, p_black_ms: 0 };
  assert.strictEqual(validateOnlineMove(Chess, expired, afterOpening, 'black-user', now).status, 409);
"""),
("done('online move validation');",
"""test('does not charge White while a new challenge waits for the opening move', async () => {
  const { validateOnlineMove } = await validation;
  const waiting = game(); waiting.updated_at = new Date(now - 240000).toISOString();
  const r = validateOnlineMove(Chess, waiting, payload('e4'), 'white-user', now);
  assert.strictEqual(r.ok, true);
  assert.strictEqual(r.update.white_ms, 182000);
  assert.strictEqual(r.update.black_ms, 180000);
});

test('charges the active side after the opening move and applies increment', async () => {
  const { validateOnlineMove } = await validation;
  const g = game(); const first = new Chess(); first.move('e4');
  g.current_fen = first.fen(); g.pgn = first.pgn();
  g.turn_user_id = 'black-user'; g.turn_color = 'b';
  g.white_ms = 182000; g.updated_at = new Date(now - 5000).toISOString();
  const second = new Chess(); second.move('e4'); second.move('e5');
  const p = { game_id: g.id, p_next_fen: second.fen(), p_pgn: second.pgn(), p_white_ms: 182000, p_black_ms: 177000 };
  const r = validateOnlineMove(Chess, g, p, 'black-user', now);
  assert.strictEqual(r.ok, true);
  assert.strictEqual(r.update.black_ms, 177000);
  assert.strictEqual(r.update.white_ms, 182000);
});

done('online move validation');""")
])

edit_online("supabase/functions/_shared/online-validation.test.ts", [
("""Deno.test("rejects stale state and expired clocks", () => {
  const g = game(); g.updated_at = new Date(now - 181000).toISOString();
  const expired = validateOnlineMove(Chess, g, payloadFor("e4"), "white-user", now);
  if (expired.ok || expired.status !== 409) throw new Error("expired clock was accepted");
  g.updated_at = new Date(now).toISOString(); g.current_fen = "invalid";
  const stale = validateOnlineMove(Chess, g, payloadFor("e4"), "white-user", now);
  if (stale.ok || stale.status !== 409) throw new Error("stale state was accepted");
});
""",
"""Deno.test("does not charge White while a new challenge waits for the opening move", () => {
  const g = game(); g.updated_at = new Date(now - 240000).toISOString();
  const r = validateOnlineMove(Chess, g, payloadFor("e4"), "white-user", now);
  if (!r.ok || r.update.white_ms !== 182000 || r.update.black_ms !== 180000) throw new Error("opening clock was charged before White moved");
});

Deno.test("charges the active side after the opening move and applies increment", () => {
  const g = game(); const first = new Chess(); first.move("e4");
  g.current_fen = first.fen(); g.pgn = first.pgn(); g.turn_user_id = "black-user"; g.turn_color = "b";
  g.white_ms = 182000; g.updated_at = new Date(now - 5000).toISOString();
  const second = new Chess(); second.move("e4"); second.move("e5");
  const payload = { game_id: g.id, p_next_fen: second.fen(), p_pgn: second.pgn(), p_white_ms: 182000, p_black_ms: 177000 };
  const r = validateOnlineMove(Chess, g, payload, "black-user", now);
  if (!r.ok || r.update.black_ms !== 177000 || r.update.white_ms !== 182000) throw new Error("active side clock/increment was incorrect");
});

Deno.test("rejects stale state and expired clocks after White has started the game", () => {
  const g = game(); const first = new Chess(); first.move("e4");
  g.current_fen = first.fen(); g.pgn = first.pgn(); g.turn_user_id = "black-user"; g.turn_color = "b";
  g.white_ms = 182000; g.updated_at = new Date(now - 181000).toISOString();
  const second = new Chess(); second.move("e4"); second.move("e5");
  const payload = { game_id: g.id, p_next_fen: second.fen(), p_pgn: second.pgn(), p_white_ms: 182000, p_black_ms: 0 };
  const expired = validateOnlineMove(Chess, g, payload, "black-user", now);
  if (expired.ok || expired.status !== 409) throw new Error("expired clock was accepted");
  g.updated_at = new Date(now).toISOString(); g.current_fen = "invalid";
  const stale = validateOnlineMove(Chess, g, payload, "black-user", now);
  if (stale.ok || stale.status !== 409) throw new Error("stale state was accepted");
});
""")
])

# Preserve the deployed database operations and applied trigger permission fix in migration source.
from pathlib import Path as _Path
_migrations = _Path("supabase/migrations")
_migrations.mkdir(parents=True, exist_ok=True)
(_migrations / "20261119125000_online_move_server_rpc_and_opening_clock.sql").write_text(
    _Path("supabase/operations/validated_online_moves.sql").read_text(encoding="utf-8"), encoding="utf-8")
(_migrations / "20261119132059_secure_chessbuddy_signup_trigger_rpc.sql").write_text(
    "revoke all on function public.handle_new_chessbuddy_user() from public, anon, authenticated;\n", encoding="utf-8")

edit_online("docs/ONLINE_PLAY_STATUS.md", [
("## Online move validation: pending deployment", "## Online move validation: deployed; device verification pending"),
("**Both are source only and have not been deployed to the live Supabase project.** Online moves are not yet production-ready or anti-cheat-certified. Deploy/review the SQL and Edge Function together, then perform two-account/two-device tests before enabling public multiplayer use.",
 "**The apply-online-move Edge Function and cb_apply_validated_move database RPC are deployed to the live Supabase project.** The endpoint requires a signed-in user, verifies each legal move on the server, and commits through a service-role-only transaction. Opening-clock timing is aligned. A full two-account/two-device playthrough is still required before calling online play production-ready or anti-cheat-certified.")
])

print("Online-play fixes applied.")



# ChessBuddy 3.0.0: Maia network switching and complete official Maia-1 ladder.
edit("app/src/main/assets/js/engine.js", [
("""    var key = provider === 'lc0' ? 'lc0|' : 'stockfish|';
    this.modelId = modelId;
    if (this.providerKey === key) { if (this.t && typeof this.t.setProvider === 'function') this.t.setProvider(provider, modelId); return this.ensureReady(); }
    this.provider = provider; this.providerKey = key;""",
"""    // Every Maia network is a distinct Lc0 configuration. Reusing the old process
    // after changing the selected weights silently keeps the previous network loaded.
    var key = provider === 'lc0' ? 'lc0|' + modelId : 'stockfish|';
    this.modelId = modelId;
    if (this.providerKey === key) { if (this.t && typeof this.t.setProvider === 'function') this.t.setProvider(provider, modelId); return this.ensureReady(); }
    this.provider = provider; this.providerKey = key;""")
])

edit("app/src/main/java/com/chessbuddy/NativeBridge.java", [
("""            String key = "lc0".equals(selected) ? "lc0|" : "stockfish|";""",
"""            // Restart Lc0 when the selected weights change; otherwise it keeps the previous network in memory.
            String key = "lc0".equals(selected) ? "lc0|" + selectedModel : "stockfish|";"""),
("""                if (!("maia-1100".equals(selectedModel) || "maia-1500".equals(selectedModel) || "maia-1900".equals(selectedModel))) {""",
"""                if (!selectedModel.matches("maia-(1100|1200|1300|1400|1500|1600|1700|1800|1900)")) {"""),
("""        final String id, file, url, sha256;
        final long bytes;
        MaiaModelEntry(String id, String file, String url, String sha256, long bytes) {
            this.id = id; this.file = file; this.url = url; this.sha256 = sha256; this.bytes = bytes;
        }""",
"""        final String id, file, url, sha256, gitBlobSha1;
        final long bytes;
        MaiaModelEntry(String id, String file, String url, String sha256, String gitBlobSha1, long bytes) {
            this.id = id; this.file = file; this.url = url; this.sha256 = sha256; this.gitBlobSha1 = gitBlobSha1; this.bytes = bytes;
        }"""),
("""        if (!("maia-1100".equals(modelId) || "maia-1500".equals(modelId) || "maia-1900".equals(modelId))) return null;""",
"""        if (modelId == null || !modelId.matches("maia-(1100|1200|1300|1400|1500|1600|1700|1800|1900)")) return null;"""),
("""                    jsonString(item, "sha256").toLowerCase(java.util.Locale.US), jsonLong(item, "bytes"));""",
"""                    jsonString(item, "sha256").toLowerCase(java.util.Locale.US),
                    jsonString(item, "gitBlobSha1").toLowerCase(java.util.Locale.US), jsonLong(item, "bytes"));"""),
("""    private File maiaModelFile(String modelId, MaiaModelEntry entry) throws Exception {""",
"""    // Some official Maia release assets do not publish SHA-256 checksums. For those,
    // verify the exact upstream Git blob object hash pinned in the model manifest.
    private static String gitBlobSha1(File file) throws Exception {
        MessageDigest digest = MessageDigest.getInstance("SHA-1");
        digest.update(("blob " + file.length() + "\\\\0").getBytes("UTF-8"));
        InputStream in = new java.io.FileInputStream(file);
        byte[] buf = new byte[65536];
        try { int n; while ((n = in.read(buf)) != -1) digest.update(buf, 0, n); } finally { in.close(); }
        StringBuilder hex = new StringBuilder();
        for (byte b : digest.digest()) hex.append(String.format(java.util.Locale.US, "%02x", b & 0xff));
        return hex.toString();
    }
    private static boolean hasModelIntegrity(MaiaModelEntry entry) {
        return entry.sha256.matches("[0-9a-f]{64}") || entry.gitBlobSha1.matches("[0-9a-f]{40}");
    }

    private File maiaModelFile(String modelId, MaiaModelEntry entry) throws Exception {"""),
("""        if (!fileName.matches("maia-(1100|1500|1900)\\\\.pb\\\\.gz")) throw new IllegalArgumentException("Invalid model filename");""",
"""        if (!fileName.matches("maia-(1100|1200|1300|1400|1500|1600|1700|1800|1900)\\\\.pb\\\\.gz")) throw new IllegalArgumentException("Invalid model filename");"""),
("""            if (!file.isFile() || expectedBytes < 1024 || file.length() != expectedBytes || !expectedHash.matches("[0-9a-f]{64}")) return false;
            return expectedHash.equals(sha256(file));""",
"""            if (!file.isFile() || expectedBytes < 1024 || file.length() != expectedBytes || !hasModelIntegrity(entry)) return false;
            if (expectedHash.matches("[0-9a-f]{64}")) return expectedHash.equals(sha256(file));
            return entry.gitBlobSha1.equals(gitBlobSha1(file));"""),
("""            if (entry == null || !entry.sha256.matches("[0-9a-f]{64}") || entry.bytes < 1024) return "";""",
"""            if (entry == null || !hasModelIntegrity(entry) || entry.bytes < 1024) return "";"""),
("""            final String expectedHash = entry.sha256;
            final long expectedBytes = entry.bytes;
            if (!url.equals("https://github.com/CSSLab/maia-chess/releases/download/v1.0/" + target.getName())
                    || !expectedHash.matches("[0-9a-f]{64}") || expectedBytes < 1024 || expectedBytes > 100L * 1024L * 1024L) {""",
"""            final String expectedHash = entry.sha256;
            final String expectedGitBlobSha1 = entry.gitBlobSha1;
            final long expectedBytes = entry.bytes;
            if (!url.equals("https://github.com/CSSLab/maia-chess/releases/download/v1.0/" + target.getName())
                    || !hasModelIntegrity(entry) || expectedBytes < 1024 || expectedBytes > 100L * 1024L * 1024L) {"""),
("""                        MessageDigest digest = MessageDigest.getInstance("SHA-256");
                        InputStream in = conn.getInputStream(); FileOutputStream out = new FileOutputStream(temp);""",
"""                        boolean useGitBlobHash = !expectedHash.matches("[0-9a-f]{64}");
                        MessageDigest digest = MessageDigest.getInstance(useGitBlobHash ? "SHA-1" : "SHA-256");
                        if (useGitBlobHash) digest.update(("blob " + expectedBytes + "\\\\0").getBytes("UTF-8"));
                        InputStream in = conn.getInputStream(); FileOutputStream out = new FileOutputStream(temp);"""),
("""                        if (count != expectedBytes || !expectedHash.equals(actual.toString())) throw new IllegalStateException("Model checksum verification failed");""",
"""                        String expectedDigest = useGitBlobHash ? expectedGitBlobSha1 : expectedHash;
                        if (count != expectedBytes || !expectedDigest.equals(actual.toString())) throw new IllegalStateException("Model checksum verification failed");""")
])

import json
from pathlib import Path as _Path
manifest_path = _Path("app/src/main/assets/models/maia-models.json")
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
extra_models = [
    (1200, 1249692, "64706a23a3e105d1a0e02e63e6ee9bee40bfdfe8"),
    (1300, 1244431, "97181c6cc59de5a2d0c2d6a0fe1eb440cf76d7f2"),
    (1400, 1328977, "4c2c9cccd28b362d40b35697dcd4062f12ed97c3"),
    (1600, 1313870, "a5fcec728608025a35d5c06c1db3559fc2b39562"),
    (1700, 1313415, "ab4208a76eaf4ddca63df71664a2c38cd46c350e"),
    (1800, 1289431, "431bb24159a55bf32fe46e724353d3556b8b3862")
]
existing_ids = {m["id"] for m in manifest["models"]}
for rating, size, blob_sha in extra_models:
    model_id = "maia-" + str(rating)
    if model_id not in existing_ids:
        manifest["models"].append({
            "id": model_id, "rating": rating, "file": model_id + ".pb.gz",
            "url": "https://github.com/CSSLab/maia-chess/releases/download/v1.0/" + model_id + ".pb.gz",
            "sha256": "", "gitBlobSha1": blob_sha, "bytes": size
        })
manifest["models"].sort(key=lambda m: m["rating"])
manifest_path.write_text(json.dumps(manifest, indent=2) + "\\n", encoding="utf-8")

edit("app/src/main/assets/js/strength.js", [
("""  var MAIA = [
    bot('maia1100', 'Maia 1100', 1100, 'Maia', 'Human-move prediction trained around 1100 Elo. Plays natural moves and makes human-like choices.', genSpec('maia1100')),
    bot('maia1500', 'Maia 1500', 1500, 'Maia', 'Human-move prediction trained around 1500 Elo. A steady club-level opponent.', genSpec('maia1500')),
    bot('maia1900', 'Maia 1900', 1900, 'Maia', 'Human-move prediction trained around 1900 Elo. More accurate, still human-like.', genSpec('maia1900'))
  ];""",
"""  var MAIA = [1100,1200,1300,1400,1500,1600,1700,1800,1900].map(function (rating) {
    var id = 'maia' + rating;
    return bot(id, 'Maia ' + rating, rating, 'Maia',
      'Official Maia-1 human-move prediction network trained around ' + rating + ' Elo.', genSpec(id));
  });""")
])

edit("tests/logic/engine.test.js", [
("test('provider switching reuses one Lc0 process when only the Maia network changes', async () => {",
 "test('provider switching restarts Lc0 when the Maia network changes', async () => {"),
("assert.strictEqual(t.startCalls, afterFirst, 'changing the Maia model must not restart the Lc0 process');",
 "assert.ok(t.startCalls > afterFirst, 'changing the Maia model must restart Lc0 so the new weights are loaded');")
])

edit("tests/logic/strength-models.test.js", [
("test('Maia roster exposes the official 1100/1500/1900 models and one-node policyhead plans', () => {",
 "test('Maia roster exposes all nine official 1100-1900 models and one-node policyhead plans', () => {"),
("assert.deepStrictEqual(maia.map(b => b.modelId), ['maia-1100', 'maia-1500', 'maia-1900']);",
 "assert.deepStrictEqual(maia.map(b => b.modelId), ['maia-1100','maia-1200','maia-1300','maia-1400','maia-1500','maia-1600','maia-1700','maia-1800','maia-1900']);")
])

edit("app/build.gradle", [("versionName '2.0.0'", "versionName '3.0.0'")])


edit("tests/logic/rebuild-smoke.test.js", [
("assert(/versionName '2\\.0\\.0'/.test(gradle), 'Android versionName must be 2.0.0');",
 "assert(/versionName '3\\.0\\.0'/.test(gradle), 'Android versionName must be 3.0.0');")
])


# Startup authentication gate and persistent account restoration.
edit_online("app/src/main/assets/js/app.js", [
("""    if (name === 'bots') renderBots();
    if (name === 'online') openOnlinePage();
    if (name === 'lobby') renderLobbyResume();
    renderHeader(); renderEngineUi(); window.scrollTo(0, 0);
""",
"""    if (name === 'bots') renderBots();
    let pageTask = Promise.resolve();
    if (name === 'online') pageTask = openOnlinePage();
    if (name === 'lobby') renderLobbyResume();
    renderHeader(); renderEngineUi(); window.scrollTo(0, 0);
    return pageTask;
"""),
("""  let onlineAccountMode = 'signin';
  function setOnlineAccountMode(mode) {
""",
"""  let onlineAccountMode = 'signup';
  function unlockAuthenticatedApp() {
    if (!Online.signedIn()) return false;
    document.body.classList.remove('auth-required');
    showTab('play');
    showPlayScreen('lobby');
    Native.logEvent('auth.app_unlocked', 'Encrypted saved session validated; app unlocked');
    return true;
  }
  function setOnlineAccountMode(mode) {
"""),
("""      if (onlineProfile) {
        await Online.setPresence('online');
        if (!onlineHubTimer) onlineHubTimer = setInterval(() => { if (playScreen === 'online' && Online.signedIn()) refreshOnlineHub(false); }, 6500);
        startOnlineHeartbeat();
      }
      if (create) onlineMessage(onlineProfile ? 'Account created. Your player profile is ready.' : 'Account created. Finish your player profile below.', 'ok');
""",
"""      if (onlineProfile) {
        await Online.setPresence('online');
        if (!onlineHubTimer) onlineHubTimer = setInterval(() => { if (playScreen === 'online' && Online.signedIn()) refreshOnlineHub(false); }, 6500);
        startOnlineHeartbeat();
      }
      if (document.body.classList.contains('auth-required')) unlockAuthenticatedApp();
      if (create) onlineMessage(onlineProfile ? 'Account created. Your player profile is ready.' : 'Account created. Finish your player profile from Play Online.', 'ok');
"""),
("""  async function onlineSignOut() {
    try { await Online.signOut(); onlineProfile = null; onlineRoster = []; clearInterval(onlinePollTimer); clearInterval(onlineHubTimer); clearInterval(onlinePresenceTimer); onlinePresenceTimer = 0; setOnlinePanels('auth'); onlineMessage('Signed out.', 'ok'); }
    catch (e) { onlineMessage(e.message, 'bad'); }
  }
""",
"""  async function onlineSignOut() {
    try {
      await Online.signOut();
      onlineProfile = null; onlineRoster = [];
      clearInterval(onlinePollTimer); clearInterval(onlineHubTimer); clearInterval(onlinePresenceTimer); onlinePresenceTimer = 0;
      document.body.classList.add('auth-required');
      showTab('play');
      setOnlineAccountMode('signin');
      setOnlinePanels('auth');
      showPlayScreen('online');
    } catch (e) { onlineMessage(e.message, 'bad'); }
  }
"""),
("""      onlineMessage('Sign-in complete. Loading your ChessBuddy account…', 'ok');
      try {
        await Online.setPresence('online');
        await refreshOnlineHub(true);
        if (!onlineHubTimer) onlineHubTimer = setInterval(() => { if (playScreen === 'online' && Online.signedIn()) refreshOnlineHub(false); }, 6500);
        startOnlineHeartbeat();
      } catch (e) { onlineMessage(e.message || 'Your account signed in, but online presence could not be updated.', 'bad'); }
""",
"""      onlineMessage('Sign-in complete. Restoring your ChessBuddy account…', 'ok');
      try {
        await refreshOnlineHub(true);
        if (onlineProfile) await Online.setPresence('online');
        if (!onlineHubTimer) onlineHubTimer = setInterval(() => { if (playScreen === 'online' && Online.signedIn()) refreshOnlineHub(false); }, 6500);
        if (onlineProfile) startOnlineHeartbeat();
        if (document.body.classList.contains('auth-required')) unlockAuthenticatedApp();
      } catch (e) { onlineMessage(e.message || 'Your account signed in, but its profile could not be loaded.', 'bad'); }
"""),
("""    $('onlineGuest').onclick = () => { Native.logEvent('auth.continue_offline', 'User chose offline play without signing in'); showPlayScreen('lobby'); };
""", ""),
("""  function boot() {
    applyTheme(); buildStaticUi(); bindEvents(); bindExtras(); Sound.setEnabled(settings.ui.sound); setInterval(clockTick, 100);
    if (!restoreCurrent()) { setHeaders(); saveCurrent(); }
    render(); showTab('play');
    // Always boot into the local lobby. Network/auth screens are opened only after an explicit user action.
    showPlayScreen('lobby');
    Native.logEvent('app.ui_boot_complete', 'ChessBuddy interface initialized; local lobby opened');
    refreshDiagnosticsUi();
    const splash = $('startupSplash');
    if (splash) { requestAnimationFrame(() => { setTimeout(() => { splash.classList.add('done'); setTimeout(() => splash.remove(), 500); }, 420); }); }
    startEngine().then(() => renderEngineUi());
  }
""",
"""  async function boot() {
    applyTheme(); buildStaticUi(); bindEvents(); bindExtras(); Sound.setEnabled(settings.ui.sound); setInterval(clockTick, 100);
    if (!restoreCurrent()) { setHeaders(); saveCurrent(); }
    render(); showTab('play');
    document.body.classList.add('auth-required');
    setOnlineAccountMode('signup');
    Native.logEvent('app.auth_gate_started', 'Waiting for saved session restore or account creation');
    const splash = $('startupSplash');
    try {
      await showPlayScreen('online');
      if (Online.signedIn()) unlockAuthenticatedApp();
      else setOnlinePanels('auth');
    } catch (e) {
      setOnlinePanels('auth');
      onlineMessage('Could not restore your saved session. Sign in to continue. ' + (e.message || ''), 'warn');
    }
    Native.logEvent('app.ui_boot_complete', Online.signedIn() ? 'Saved account session restored' : 'Account screen shown; no valid saved session');
    refreshDiagnosticsUi();
    if (splash) { requestAnimationFrame(() => { setTimeout(() => { splash.classList.add('done'); setTimeout(() => splash.remove(), 500); }, 220); }); }
    startEngine().then(() => renderEngineUi()).catch(e => Native.logEvent('engine.startup_failed', 'Engine initialization failed: ' + (e && e.name || 'Error')));
  }
""")
]);

edit_online("app/src/main/assets/index.html", [
("""          <p class="muted auth-copy" id="onlineAuthSubheading">Sign in to play friends, keep your games and sync your progress.</p>
""",
"""          <p class="muted auth-copy" id="onlineAuthSubheading">Create an account to play, save your progress and sync your games.</p>
"""),
("""          <button class="auth-guest" id="onlineGuest" type="button">Continue offline without an account</button>
          <p class="auth-legal muted">Your session is protected by Android secure storage. An account is only needed for online friend play and synced profile features.</p>
""",
"""          <button class="auth-guest" id="onlineGuest" type="button" hidden>Continue offline without an account</button>
          <p class="auth-legal muted">Stay signed in on this device. ChessBuddy stores your refresh session encrypted with Android Keystore until you sign out.</p>
""")
]);

edit_online("app/src/main/assets/css/app.css", [
("""@media(prefers-reduced-motion:reduce){#lobby .row-btn{transition:none}}
""",
"""@media(prefers-reduced-motion:reduce){#lobby .row-btn{transition:none}}

/* Mandatory first-run account gate; hidden automatically after secure session restore. */
body.auth-required{background:radial-gradient(ellipse at 50% 12%,#35452d 0,#262522 48%,#1d1c1a 100%)}
body.auth-required #app{min-height:100dvh;max-width:620px;padding:0 16px 28px;display:flex;flex-direction:column}
body.auth-required #topbar,body.auth-required .tabbar{display:none!important}
body.auth-required main{display:flex;flex:1;align-items:center;padding:24px 0 calc(24px + env(safe-area-inset-bottom,0px))}
body.auth-required #view-play{display:block!important;width:100%;margin:auto}
body.auth-required #view-play> :not(#onlinePage){display:none!important}
body.auth-required #onlinePage{display:block!important;width:100%;max-width:520px;margin:0 auto;padding:0}
body.auth-required #onlinePage>.hero{display:none!important}
body.auth-required #onlineMessage{margin:0 0 12px}
body.auth-required .auth-card{margin:0;padding:24px 20px;border-radius:22px;background:linear-gradient(155deg,#343a30,#282724 66%);border:1px solid #c8e2ab22;box-shadow:0 24px 70px #0007}
body.auth-required .auth-mark{width:46px;height:46px;border-radius:14px}
body.auth-required .auth-mark svg{width:35px;height:35px}
body.auth-required .auth-brand{font-size:11px;letter-spacing:1.5px;margin-bottom:22px}
body.auth-required .auth-card h2{font-size:29px;letter-spacing:-.8px}
body.auth-required .auth-copy{font-size:14px;margin-bottom:22px}
body.auth-required .auth-legal{font-size:11px;color:#aaa69e}
body.auth-required #onlineGuest{display:none!important}
body.auth-required #onlineAuthCard[hidden],body.auth-required #onlineResetCard[hidden],body.auth-required #onlineProfileCard[hidden],body.auth-required #onlineHubCard[hidden]{display:none!important}
""")
]);

edit_online("app/src/main/java/com/chessbuddy/SecretStore.java", [
("""        return v.startsWith("e:") ? decrypt(v.substring(2)) : null;
""",
"""        if (!v.startsWith("e:")) { prefs.edit().remove(id).commit(); return null; }
        String plain = decrypt(v.substring(2));
        if (plain == null) prefs.edit().remove(id).commit();
        return plain;
""")
]);

edit_online("tests/logic/online-auth.test.js", [
("""test('a 401 refreshes once and retries with the new access token; permission errors are not retried', async () => {
""",
"""test('saved session is restored through native refresh when the app starts again', async () => {
  const { api, calls } = setup();
  assert.strictEqual(api.signedIn(), false);
  await api.restore();
  assert.strictEqual(api.signedIn(), true);
  assert.strictEqual(api.user().id, 'user-1');
  assert.strictEqual(calls.filter(c => c.type === 'auth' && c.op === 'refresh').length, 1);
});

test('a 401 refreshes once and retries with the new access token; permission errors are not retried', async () => {
""")
]);

edit_online("tests/logic/rebuild-smoke.test.js", [
("""assert(/showPlayScreen\\('lobby'\\)/.test(app), 'startup must land on the local lobby, not block on account/network screens');""",
"""assert(/document\\.body\\.classList\\.add\\('auth-required'\\)/.test(app) && /await showPlayScreen\\('online'\\)/.test(app), 'startup must show the account gate and await saved-session restoration');
assert(/function unlockAuthenticatedApp\\(\\)/.test(app) && /document\\.body\\.classList\\.remove\\('auth-required'\\)/.test(app), 'the app shell must unlock only after authentication');
assert(/let onlineAccountMode = 'signup'/.test(app), 'fresh installs must show signup by default');
assert(/body\\.auth-required #topbar/.test(css) && /body\\.auth-required \\.tabbar/.test(css), 'auth gate must hide app navigation');
assert(/Stay signed in on this device/.test(html), 'login UI must explain encrypted persistent sessions');""")
]);

print("Startup auth gate and persistent-login repair overlay applied.");
