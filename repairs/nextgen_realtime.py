#!/usr/bin/env python3
"""Add authenticated Supabase Realtime game subscriptions with REST polling fallback."""
from pathlib import Path

def replace_once(path, old, new, label):
    p = Path(path)
    source = p.read_text(encoding="utf-8")
    if new in source:
        return
    if old not in source:
        raise SystemExit("Realtime patch could not find " + label + " in " + path)
    p.write_text(source.replace(old, new, 1), encoding="utf-8")

online_realtime = r'''
  var realtimeTokenRefreshers = [];
  function refreshRealtimeTokens() {
    realtimeTokenRefreshers.slice().forEach(function (refresh) {
      try { refresh(); } catch (_) { log('realtime.token_refresh_failed', 'Could not refresh the live game channel token'); }
    });
  }
  function subscribeGame(gameId, onChange) {
    var id = String(gameId || '').trim();
    if (!/^[0-9a-f-]{16,64}$/i.test(id)) throw new Error('Invalid online game id.');
    if (typeof onChange !== 'function') throw new Error('A game update callback is required.');
    if (!root.WebSocket) {
      log('realtime.unavailable', 'WebSocket is not available; REST polling remains active');
      return function () {};
    }
    var stopped = false, socket = null, heartbeat = 0, reconnectTimer = 0;
    var retries = 0, ref = 0, joinRef = null, subscriptionIds = [];
    var topic = 'realtime:chessbuddy-game:' + id;
    function clearSocketTimers() {
      if (heartbeat) { clearInterval(heartbeat); heartbeat = 0; }
      if (reconnectTimer) { clearTimeout(reconnectTimer); reconnectTimer = 0; }
    }
    function sendFrame(target, frame) {
      if (!target || target.readyState !== 1) return false;
      try { target.send(JSON.stringify(frame)); return true; } catch (_) { return false; }
    }
    function sendAccessToken() {
      if (!socket || !joinRef || stopped) return;
      sendFrame(socket, {
        topic: topic, event: 'access_token',
        payload: { access_token: session && session.accessToken || '' },
        ref: String(++ref), join_ref: joinRef
      });
    }
    realtimeTokenRefreshers.push(sendAccessToken);
    function reconnect() {
      if (stopped || reconnectTimer) return;
      retries = Math.min(retries + 1, 5);
      var delay = Math.min(15000, 750 * Math.pow(2, retries - 1));
      log('realtime.reconnect_scheduled', 'Retrying game subscription in ' + delay + 'ms');
      reconnectTimer = setTimeout(function () { reconnectTimer = 0; connect(); }, delay);
    }
    function connect() {
      if (stopped || !signedIn()) return;
      var ws;
      try {
        var endpoint = URL.replace(/^https:/i, 'wss:') + '/realtime/v1/websocket?apikey=' +
          encodeURIComponent(KEY) + '&vsn=1.0.0';
        ws = new root.WebSocket(endpoint);
        socket = ws;
      } catch (e) {
        log('realtime.connect_failed', 'Could not create the game update socket');
        reconnect();
        return;
      }
      ws.onopen = function () {
        if (stopped || socket !== ws) { try { ws.close(); } catch (_) {} return; }
        retries = 0;
        joinRef = String(++ref);
        subscriptionIds = [];
        var filter = 'id=eq.' + id;
        var joined = sendFrame(ws, {
          topic: topic,
          event: 'phx_join',
          payload: {
            config: {
              broadcast: { ack: false, self: false },
              presence: { enabled: false, key: '' },
              postgres_changes: [{ event: '*', schema: 'public', table: 'chessbuddy_games', filter: filter }],
              private: false
            },
            access_token: session.accessToken
          },
          ref: joinRef,
          join_ref: joinRef
        });
        if (!joined) { try { ws.close(); } catch (_) {} return; }
        heartbeat = setInterval(function () {
          if (socket === ws && ws.readyState === 1)
            sendFrame(ws, { topic: 'phoenix', event: 'heartbeat', payload: {}, ref: String(++ref) });
        }, 25000);
        log('realtime.join_sent', 'Authenticated game channel join requested');
      };
      ws.onmessage = function (event) {
        if (stopped || socket !== ws) return;
        var frame = parse(event && event.data);
        if (!frame) return;
        if (frame.event === 'phx_reply' && frame.ref === joinRef) {
          if (!frame.payload || frame.payload.status !== 'ok') {
            log('realtime.join_rejected', 'Server rejected the game subscription; REST polling remains active');
            try { ws.close(1011, 'Realtime subscription rejected'); } catch (_) { reconnect(); }
            return;
          }
          var response = frame.payload.response || {};
          var subscriptions = response.postgres_changes || [];
          subscriptionIds = subscriptions.map(function (item) { return Number(item.id); }).filter(function (value) { return Number.isFinite(value); });
          if (!subscriptionIds.length) {
            log('realtime.join_missing_id', 'Server accepted the channel but returned no Postgres subscription id');
            try { ws.close(1011, 'Missing subscription id'); } catch (_) { reconnect(); }
            return;
          }
          log('realtime.subscribed', 'Server confirmed the game row subscription');
          return;
        }
        if (frame.event === 'system' && frame.payload && frame.payload.status === 'error') {
          log('realtime.system_error', 'Supabase Realtime reported a channel error');
          try { ws.close(1011, 'Realtime system error'); } catch (_) { reconnect(); }
          return;
        }
        if (frame.event !== 'postgres_changes') return;
        var payload = frame.payload || {};
        var incomingIds = Array.isArray(payload.ids) ? payload.ids.map(Number) : [];
        if (!subscriptionIds.length || !incomingIds.some(function (value) { return subscriptionIds.indexOf(value) >= 0; })) {
          log('realtime.subscription_mismatch', 'Incoming change did not match the active join subscription id');
          try { ws.close(1011, 'Realtime subscription id mismatch'); } catch (_) { reconnect(); }
          return;
        }
        var change = payload.data || {};
        if ((change.schema && change.schema !== 'public') || (change.table && change.table !== 'chessbuddy_games')) return;
        var record = change.record || {}, oldRecord = change.old_record || {};
        var recordId = record.id || oldRecord.id;
        if (!recordId || String(recordId) !== id) return;
        try {
          onChange({
            eventType: change.type || 'UPDATE',
            record: record,
            oldRecord: oldRecord,
            commitTimestamp: change.commit_timestamp || null
          });
        } catch (_) { log('realtime.callback_failed', 'The game update handler raised an error'); }
      };
      ws.onerror = function () {
        if (socket === ws && !stopped) { try { ws.close(); } catch (_) { reconnect(); } }
      };
      ws.onclose = function () {
        if (socket !== ws) return;
        clearSocketTimers();
        socket = null; joinRef = null; subscriptionIds = [];
        if (!stopped) reconnect();
      };
    }
    connect();
    return function unsubscribeGame() {
      if (stopped) return;
      stopped = true;
      clearSocketTimers();
      var current = socket;
      if (current && joinRef) {
        sendFrame(current, { topic: topic, event: 'phx_leave', payload: {}, ref: String(++ref), join_ref: joinRef });
      }
      socket = null; joinRef = null; subscriptionIds = [];
      var refreshIndex = realtimeTokenRefreshers.indexOf(sendAccessToken);
      if (refreshIndex >= 0) realtimeTokenRefreshers.splice(refreshIndex, 1);
      if (current) {
        current.onclose = null; current.onerror = null; current.onmessage = null; current.onopen = null;
        try { current.close(1000, 'ChessBuddy game view closed'); } catch (_) {}
      }
      log('realtime.unsubscribed', 'Game update subscription closed');
    };
  }
'''
replace_once(
    "app/src/main/assets/js/online.js",
    "  function signedIn() { return !!(session && session.accessToken && session.user && session.user.id); }\n",
    "  function signedIn() { return !!(session && session.accessToken && session.user && session.user.id); }\n" + online_realtime + "\n",
    "online session helper"
)
replace_once(
    "app/src/main/assets/js/online.js",
    "      if (data && (data.access_token || data.data || data.session || data.result)) acceptSession(data);\n",
    "      if (data && (data.access_token || data.data || data.session || data.result)) acceptSession(data);\n      if (operation === 'refresh' && signedIn()) refreshRealtimeTokens();\n",
    "propagate refreshed Auth token to Realtime"
)
replace_once(
    "app/src/main/assets/js/online.js",
    "    clearMemorySession: function () { session = null; }\n",
    "    subscribeGame: subscribeGame,\n    clearMemorySession: function () { session = null; }\n",
    "Online public API"
)

app = Path("app/src/main/assets/js/app.js")
source = app.read_text(encoding="utf-8")
old_state = "  let onlineProfile = null, onlineRoster = [], onlineRefreshing = false, onlinePollTimer = 0, onlineHubTimer = 0, onlinePresenceTimer = 0;"
new_state = "  let onlineProfile = null, onlineRoster = [], onlineRefreshing = false, onlinePollTimer = 0, onlineHubTimer = 0, onlinePresenceTimer = 0, onlineRealtimeStop = null;"
if old_state in source:
    source = source.replace(old_state, new_state, 1)
elif new_state not in source:
    raise SystemExit("Realtime patch could not find online timer state")
if "function startOnlineGameRealtime()" not in source:
    marker = "  async function pollOnlineGame() {"
    realtime_app = r'''  function stopOnlineGameRealtime() {
    if (onlineRealtimeStop) { try { onlineRealtimeStop(); } catch (_) {} onlineRealtimeStop = null; }
  }
  function startOnlineGameRealtime() {
    stopOnlineGameRealtime();
    if (!ctx.online || !Online.subscribeGame || !Online.signedIn()) return;
    try {
      onlineRealtimeStop = Online.subscribeGame(ctx.online.id, function () {
        if (!ctx.online || appPaused || over || !Online.signedIn()) return;
        pollOnlineGame().catch(noop);
      });
    } catch (e) {
      Native.logEvent('realtime.subscribe_failed', 'Realtime unavailable; REST polling remains active');
    }
  }

'''
    if marker not in source: raise SystemExit("Realtime patch could not find poll function")
    source = source.replace(marker, realtime_app + marker, 1)

# launchOnlineGame creates ctx.online before setting the fallback poll timer.
poll_start = "    if (onlinePollTimer) clearInterval(onlinePollTimer);\n    onlinePollTimer = setInterval(() => { if (ctx.online && !appPaused && !over) pollOnlineGame().catch(noop); }, 2200);"
poll_new = "    startOnlineGameRealtime();\n    if (onlinePollTimer) clearInterval(onlinePollTimer);\n    // Realtime is primary; slower REST polling recovers cleanly from socket/network failures.\n    onlinePollTimer = setInterval(() => { if (ctx.online && !appPaused && !over) pollOnlineGame().catch(noop); }, 5500);"
if poll_start in source:
    source = source.replace(poll_start, poll_new, 1)
elif poll_new not in source:
    raise SystemExit("Realtime patch could not find game polling setup")

# Clean up channel resources when signing out or suspending the app.
source = source.replace(
    "try { await Online.signOut(); onlineProfile = null; onlineRoster = []; clearInterval(onlinePollTimer);",
    "try { stopOnlineGameRealtime(); await Online.signOut(); onlineProfile = null; onlineRoster = []; clearInterval(onlinePollTimer);",
    1
)
source = source.replace(
    "window.cbOnPause = function () { appPaused = true; if (Online.signedIn())",
    "window.cbOnPause = function () { appPaused = true; stopOnlineGameRealtime(); if (Online.signedIn())",
    1
)
source = source.replace(
    "window.cbOnResume = function () { appPaused = false; if (Online.signedIn()) Online.setPresence('online').catch(noop); if (ctx.online) pollOnlineGame().catch(noop);",
    "window.cbOnResume = function () { appPaused = false; if (Online.signedIn()) Online.setPresence('online').catch(noop); if (ctx.online && !over) { startOnlineGameRealtime(); pollOnlineGame().catch(noop); }",
    1
)
app.write_text(source, encoding="utf-8")
print("Authenticated Supabase Realtime game subscription added; REST polling retained as fallback.")
