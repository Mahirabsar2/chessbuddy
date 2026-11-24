#!/usr/bin/env python3
"""Connect ChessBuddy local state to the authenticated Supabase persistence tables."""
from pathlib import Path

def replace_once(path, old, new, label):
    p = Path(path)
    s = p.read_text(encoding="utf-8")
    if new in s:
        return
    count = s.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one anchor for {label}, found {count}")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")

replace_once("app/src/main/assets/js/updater.js",
    "asset(release, 'ChessBuddy-NextGen-1.0.0.apk')",
    "asset(release, 'ChessBuddy-NextGen-2.0.0.apk')", "stable APK filename")
replace_once("app/src/main/assets/js/updater.js",
    "asset(release, 'ChessBuddy-NextGen-1.0.0.apk.sha256')",
    "asset(release, 'ChessBuddy-NextGen-2.0.0.apk.sha256')", "stable checksum filename")

replace_once("app/src/main/assets/js/online.js",
    "function send(method, path, body, retried) {\n"
    "    var url = URL + '/rest/v1/' + path, h, started = Date.now(), safePath = String(path || '').split('?')[0];\n"
    "    try { h = headers(); } catch (e) { return Promise.reject(e); }\n"
    "    log('online.request', method + ' ' + safePath);",
    "function send(method, path, body, retried, extraHeaders) {\n"
    "    var url = URL + '/rest/v1/' + path, h, started = Date.now(), safePath = String(path || '').split('?')[0];\n"
    "    try { h = headers(); } catch (e) { return Promise.reject(e); }\n"
    "    if (extraHeaders) h += '\\n' + extraHeaders;\n"
    "    log('online.request', method + ' ' + safePath);", "authenticated REST extra headers")
replace_once("app/src/main/assets/js/online.js",
    "return auth('refresh', {}).then(function () { return send(method, path, body, true); });",
    "return auth('refresh', {}).then(function () { return send(method, path, body, true, extraHeaders); });",
    "REST retry retains upsert headers")
replace_once("app/src/main/assets/js/online.js",
    "    profile: function () {\n"
    "      if (!signedIn()) return Promise.reject(new Error('Sign in to load your player profile.'));\n"
    "      var id = api.user().id;\n"
    "      return query('chessbuddy_profiles', 'select=user_id,username,display_name&user_id=eq.' + encodeURIComponent(id) + '&limit=1').then(function (rows) { return rows && rows[0] || null; });\n"
    "    },\n"
    "    registerProfile:",
    "    profile: function () {\n"
    "      if (!signedIn()) return Promise.reject(new Error('Sign in to load your player profile.'));\n"
    "      var id = api.user().id;\n"
    "      return query('chessbuddy_profiles', 'select=user_id,username,display_name&user_id=eq.' + encodeURIComponent(id) + '&limit=1').then(function (rows) { return rows && rows[0] || null; });\n"
    "    },\n"
    "    loadUserState: function () {\n"
    "      if (!signedIn()) return Promise.reject(new Error('Sign in to load cloud progress.'));\n"
    "      var id = encodeURIComponent(api.user().id);\n"
    "      return query('chessbuddy_user_state', 'select=profile,settings,progress,updated_at&user_id=eq.' + id + '&limit=1').then(function (rows) { return rows && rows[0] || null; });\n"
    "    },\n"
    "    saveUserState: function (state) {\n"
    "      if (!signedIn()) return Promise.reject(new Error('Sign in to save cloud progress.'));\n"
    "      var row = { user_id: api.user().id, profile: state.profile || {}, settings: state.settings || {}, progress: state.progress || {} };\n"
    "      return send('POST', 'chessbuddy_user_state?on_conflict=user_id', row, false, 'Prefer: resolution=merge-duplicates,return=minimal');\n"
    "    },\n"
    "    loadSavedGames: function () {\n"
    "      if (!signedIn()) return Promise.reject(new Error('Sign in to load cloud games.'));\n"
    "      var id = encodeURIComponent(api.user().id);\n"
    "      return query('chessbuddy_saved_games', 'select=client_game_id,pgn,metadata,created_at,updated_at&user_id=eq.' + id + '&order=updated_at.desc&limit=100').then(function (rows) {\n"
    "        return (rows || []).map(function (row) {\n"
    "          var metadata = row.metadata && typeof row.metadata === 'object' ? row.metadata : {};\n"
    "          var game = Object.assign({}, metadata, { id: row.client_game_id, pgn: row.pgn || '' });\n"
    "          if (!game.date) game.date = row.created_at || row.updated_at || '';\n"
    "          return game;\n"
    "        });\n"
    "      });\n"
    "    },\n"
    "    saveSavedGames: function (games) {\n"
    "      if (!signedIn()) return Promise.reject(new Error('Sign in to save cloud games.'));\n"
    "      var id = api.user().id;\n"
    "      var rows = (Array.isArray(games) ? games : []).filter(function (g) { return g && g.id && g.pgn; }).map(function (g) {\n"
    "        var metadata = Object.assign({}, g);\n"
    "        delete metadata.id; delete metadata.pgn;\n"
    "        return { user_id: id, client_game_id: String(g.id).slice(0, 128), pgn: String(g.pgn), metadata: metadata };\n"
    "      });\n"
    "      var batches = [];\n"
    "      for (var i = 0; i < rows.length; i += 20) batches.push(rows.slice(i, i + 20));\n"
    "      return batches.reduce(function (chain, batch) {\n"
    "        return chain.then(function () { return send('POST', 'chessbuddy_saved_games?on_conflict=user_id%2Cclient_game_id', batch, false, 'Prefer: resolution=merge-duplicates,return=minimal'); });\n"
    "      }, Promise.resolve()).then(function () { return true; });\n"
    "    },\n"
    "    registerProfile:",
    "Supabase cloud state and game archive API")

replace_once("app/src/main/assets/js/app.js",
    "  let settings = buildSettings(lsGet(K_SET, null) || lsGet(K_SET_BAK, null));\n"
    "  const saveSettings = () => {\n"
    "    settings.schema = SCHEMA;\n"
    "    try { const prev = localStorage.getItem(K_SET); if (prev) localStorage.setItem(K_SET_BAK, prev); } catch (e) { /* ignore */ }\n"
    "    return lsSet(K_SET, settings);\n"
    "  };",
    "  let settings = buildSettings(lsGet(K_SET, null) || lsGet(K_SET_BAK, null));\n"
    "  let cloudStateReady = false, cloudSettingsTimer = 0, cloudGamesTimer = 0, cloudSyncBusy = false;\n"
    "  function currentCloudState() { return { profile: settings.profile || {}, settings: settings, progress: settings.progress || {} }; }\n"
    "  function scheduleCloudSettingsSync() {\n"
    "    if (!cloudStateReady || !Online.signedIn()) return;\n"
    "    clearTimeout(cloudSettingsTimer);\n"
    "    cloudSettingsTimer = setTimeout(async function () {\n"
    "      if (!cloudStateReady || !Online.signedIn()) return;\n"
    "      try { await Online.saveUserState(currentCloudState()); Native.logEvent('cloud.state_saved', 'Profile, settings and progress synced'); }\n"
    "      catch (e) { Native.logEvent('cloud.state_save_failed', 'Cloud state sync failed: ' + String(e && e.message || 'request error').slice(0, 160)); }\n"
    "    }, 800);\n"
    "  }\n"
    "  function scheduleCloudGamesSync() {\n"
    "    if (!cloudStateReady || !Online.signedIn()) return;\n"
    "    clearTimeout(cloudGamesTimer);\n"
    "    cloudGamesTimer = setTimeout(async function () {\n"
    "      if (!cloudStateReady || !Online.signedIn() || cloudSyncBusy) return;\n"
    "      cloudSyncBusy = true;\n"
    "      try { await Online.saveSavedGames(lsGet(K_GAMES, [])); Native.logEvent('cloud.games_saved', 'Local game archive synced'); }\n"
    "      catch (e) { Native.logEvent('cloud.games_save_failed', 'Game archive sync failed: ' + String(e && e.message || 'request error').slice(0, 160)); }\n"
    "      finally { cloudSyncBusy = false; }\n"
    "    }, 900);\n"
    "  }\n"
    "  async function hydrateCloudState() {\n"
    "    if (!Online.signedIn()) return false;\n"
    "    cloudStateReady = false;\n"
    "    try {\n"
    "      var cloud = await Online.loadUserState();\n"
    "      if (cloud) {\n"
    "        var saved = cloud.settings && typeof cloud.settings === 'object' ? cloud.settings : {};\n"
    "        settings = buildSettings(Object.assign({}, saved, {\n"
    "          profile: cloud.profile && typeof cloud.profile === 'object' ? cloud.profile : saved.profile,\n"
    "          progress: cloud.progress && typeof cloud.progress === 'object' ? cloud.progress : saved.progress\n"
    "        }));\n"
    "        lsSet(K_SET, settings);\n"
    "      } else { await Online.saveUserState(currentCloudState()); }\n"
    "      var cloudGames = await Online.loadSavedGames();\n"
    "      var localGames = lsGet(K_GAMES, []);\n"
    "      var progress = settings.progress || (settings.progress = {});\n"
    "      var deleted = new Set(Array.isArray(progress.cloudDeletedGameIds) ? progress.cloudDeletedGameIds.map(String) : []);\n"
    "      var clearedAt = Number(progress.cloudGamesClearedAt || 0);\n"
    "      cloudGames = (cloudGames || []).filter(function (g) { return !deleted.has(String(g.id)) && (!clearedAt || !g.date || new Date(g.date).getTime() > clearedAt); });\n"
    "      var known = new Set(cloudGames.map(function (g) { return String(g.id); }));\n"
    "      var merged = cloudGames.slice();\n"
    "      localGames.forEach(function (g) { if (g && g.id && g.pgn && !deleted.has(String(g.id)) && !known.has(String(g.id))) merged.push(g); });\n"
    "      merged.sort(function (a, b) { return new Date(b.date || 0).getTime() - new Date(a.date || 0).getTime(); });\n"
    "      lsSet(K_GAMES, merged.slice(0, 100));\n"
    "      cloudStateReady = true;\n"
    "      applyTheme(); Sound.setEnabled(settings.ui.sound); render();\n"
    "      scheduleCloudSettingsSync(); scheduleCloudGamesSync();\n"
    "      Native.logEvent('cloud.hydration_complete', 'Cloud profile, app settings, progress and saved games loaded');\n"
    "      return true;\n"
    "    } catch (e) {\n"
    "      cloudStateReady = false;\n"
    "      Native.logEvent('cloud.hydration_failed', 'Cloud restore failed; local data remains available: ' + String(e && e.message || 'request error').slice(0, 180));\n"
    "      return false;\n"
    "    }\n"
    "  }\n"
    "  const saveSettings = () => {\n"
    "    settings.schema = SCHEMA;\n"
    "    try { const prev = localStorage.getItem(K_SET); if (prev) localStorage.setItem(K_SET_BAK, prev); } catch (e) { /* ignore */ }\n"
    "    const saved = lsSet(K_SET, settings);\n"
    "    if (saved) scheduleCloudSettingsSync();\n"
    "    return saved;\n"
    "  };", "cloud-first local settings persistence")

replace_once("app/src/main/assets/js/app.js",
    "      if (!Online.signedIn()) await Online.restore();\n"
    "      // A new account has no profile row yet. Presence has a foreign key to that profile.\n"
    "      await refreshOnlineHub(false);",
    "      if (!Online.signedIn()) await Online.restore();\n"
    "      await hydrateCloudState();\n"
    "      // A new account has no profile row yet. Presence has a foreign key to that profile.\n"
    "      await refreshOnlineHub(false);", "startup cloud hydration")
replace_once("app/src/main/assets/js/app.js",
    "      // Do not create presence until the authenticated user has registered a profile row.\n"
    "      await refreshOnlineHub(false);",
    "      await hydrateCloudState();\n"
    "      // Do not create presence until the authenticated user has registered a profile row.\n"
    "      await refreshOnlineHub(false);", "email sign-in cloud hydration")
replace_once("app/src/main/assets/js/app.js",
    "      onlineMessage('Sign-in complete. Restoring your ChessBuddy account…', 'ok');\n"
    "      try {\n"
    "        await refreshOnlineHub(true);",
    "      onlineMessage('Sign-in complete. Restoring your ChessBuddy account…', 'ok');\n"
    "      try {\n"
    "        await hydrateCloudState();\n"
    "        await refreshOnlineHub(true);", "OAuth callback cloud hydration")
replace_once("app/src/main/assets/js/app.js",
    "      await Online.signOut();\n"
    "      onlineProfile = null; onlineRoster = [];",
    "      await Online.signOut();\n"
    "      cloudStateReady = false;\n"
    "      clearTimeout(cloudSettingsTimer); clearTimeout(cloudGamesTimer);\n"
    "      onlineProfile = null; onlineRoster = [];", "sign-out cloud sync gate")
replace_once("app/src/main/assets/js/app.js",
    "    lsSet(K_GAMES, list.slice(0, 100));\n"
    "    ctx.saved = true;",
    "    lsSet(K_GAMES, list.slice(0, 100));\n"
    "    scheduleCloudGamesSync();\n"
    "    ctx.saved = true;", "finished game cloud archive sync")
replace_once("app/src/main/assets/js/app.js",
    "else if (a === 'del' && await confirmDialog('Delete this game from the archive?', 'Delete', true)) { list.splice(i, 1); lsSet(K_GAMES, list); renderHistory(); }",
    "else if (a === 'del' && await confirmDialog('Delete this game from the archive?', 'Delete', true)) { list.splice(i, 1); lsSet(K_GAMES, list); settings.progress.cloudDeletedGameIds = Array.from(new Set([...(settings.progress.cloudDeletedGameIds || []), String(rec.id)])); saveSettings(); scheduleCloudGamesSync(); renderHistory(); }",
    "single archived-game tombstone")
replace_once("app/src/main/assets/js/app.js",
    "if (await confirmDialog('Delete all saved games?', 'Delete all', true)) { lsDel(K_GAMES); renderHistory(); toast('Archive cleared'); }",
    "if (await confirmDialog('Delete all saved games?', 'Delete all', true)) { lsDel(K_GAMES); settings.progress.cloudGamesClearedAt = Date.now(); saveSettings(); renderHistory(); toast('Archive cleared'); }",
    "archive clear cloud tombstone")
replace_once("app/src/main/assets/js/app.js",
    "      '<p class=\"muted tiny\">This local profile stays on this device. Sign in from Play Online to access your synced ChessBuddy account.</p>' +",
    "      '<p class=\"muted tiny\">' + (Online.signedIn() ? 'Your profile syncs to your ChessBuddy account and is restored on your other signed-in devices.' : 'Guest profile is stored on this device. Sign in to sync it across your devices.') + '</p>' +",
    "profile copy explains cloud sync")
replace_once("app/src/main/assets/js/app.js",
    "      saveSettings(); closeModal(); renderProfile(); renderMore(); renderHeader(); toast('Profile saved on this device.');",
    "      saveSettings(); closeModal(); renderProfile(); renderMore(); renderHeader(); toast(Online.signedIn() ? 'Profile saved. Syncing to your ChessBuddy account…' : 'Profile saved on this device.');",
    "profile save confirmation")

replace_once("app/src/main/assets/js/strength.js",
    "  BOTS = BOTS.concat(GM, LEGENDS, CHARACTERS, GENERATED, VIS, REAL_PLAYERS, MEDIA_CAST, MAIA);",
    "  var CREATOR_CHALLENGES = [\n"
    "    bot('creator_mrbeast', 'MrBeast Challenge', 1400, 'Creators', 'Unofficial fan-made ChessBuddy challenge preset inspired by high-energy creator content. Stockfish practice opponent; not affiliated with or a simulation of the creator.', genSpec('creator_mrbeast')),\n"
    "    bot('creator_gothamchess', 'GothamChess Challenge', 1850, 'Creators', 'Unofficial fan-made ChessBuddy chess-commentary challenge preset. Stockfish practice opponent; not affiliated with or a simulation of the creator.', genSpec('creator_gothamchess')),\n"
    "    bot('creator_witty_alien', 'Witty Alien Challenge', 1550, 'Creators', 'Unofficial fan-made ChessBuddy challenge preset. Stockfish practice opponent with original art; not affiliated with or a simulation of the creator.', genSpec('creator_witty_alien'))\n"
    "  ];\n"
    "  CREATOR_CHALLENGES.forEach(function (b) { b.unofficial = true; b.practiceOnly = true; });\n"
    "  BOTS = BOTS.concat(GM, LEGENDS, CHARACTERS, GENERATED, VIS, REAL_PLAYERS, MEDIA_CAST, CREATOR_CHALLENGES, MAIA);",
    "creator practice challenge profiles")

print("Cloud persistence, updater filename, archive tombstones and unofficial creator presets applied.")
