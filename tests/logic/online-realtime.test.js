const assert = require('assert');
const fs = require('fs');
const vm = require('vm');

class FakeWebSocket {
  static instances = [];
  constructor(url) {
    this.url = url;
    this.readyState = 0;
    this.sent = [];
    FakeWebSocket.instances.push(this);
  }
  send(value) { this.sent.push(JSON.parse(value)); }
  open() { this.readyState = 1; if (this.onopen) this.onopen(); }
  emit(value) { if (this.onmessage) this.onmessage({ data: JSON.stringify(value) }); }
  close() { this.readyState = 3; if (this.onclose) this.onclose(); }
}
FakeWebSocket.OPEN = 1;

async function main() {
  const window = {
    WebSocket: FakeWebSocket,
    CBNative: {
      available: true,
      logEvent: function () {},
      supabaseAuth: function () {
        return { promise: Promise.resolve({ status: 200, body: JSON.stringify({
          access_token: 'test-access-token-long-enough-for-the-client',
          user: { id: 'user-123' }
        }) }) };
      }
    }
  };
  const context = {
    window,
    globalThis: window,
    Promise,
    URLSearchParams,
    setInterval: function () { return 1; },
    clearInterval: function () {},
    setTimeout: function () { return 2; },
    clearTimeout: function () {},
  };
  vm.runInNewContext(fs.readFileSync('app/src/main/assets/js/online.js', 'utf8'), context);
  const online = window.CBOnline;
  await online.restore();
  const updates = [];
  const stop = online.subscribeGame('01234567-89ab-cdef-0123-456789abcdef', change => updates.push(change));
  assert.strictEqual(FakeWebSocket.instances.length, 1, 'creates one WebSocket');
  const socket = FakeWebSocket.instances[0];
  assert(socket.url.startsWith('wss://npicptuurxuqxepxzumi.supabase.co/realtime/v1/websocket?apikey='));
  socket.open();
  const join = socket.sent.find(frame => frame.event === 'phx_join');
  assert(join, 'joins a Supabase Realtime channel');
  assert.strictEqual(join.payload.access_token, 'test-access-token-long-enough-for-the-client');
  assert.deepStrictEqual(join.payload.config.postgres_changes[0], {
    event: '*', schema: 'public', table: 'chessbuddy_games',
    filter: 'id=eq.01234567-89ab-cdef-0123-456789abcdef'
  });
  socket.emit({
    topic: join.topic, event: 'phx_reply', ref: join.ref, join_ref: join.join_ref,
    payload: { status:'ok', response:{ postgres_changes:[{ id:77, event:'*', schema:'public', table:'chessbuddy_games' }] } }
  });
  await online.restore();
  assert(socket.sent.some(frame => frame.event === 'access_token'), 'auth refresh propagates the new access token to the live channel');
  socket.emit({
    topic: join.topic,
    event: 'postgres_changes',
    payload: { ids:[77], data: {
      schema:'public', table:'chessbuddy_games', type: 'UPDATE',
      record: { id: '01234567-89ab-cdef-0123-456789abcdef', current_fen: 'test-fen' },
      old_record: { current_fen: 'old-fen' }
    } }
  });
  assert.strictEqual(updates.length, 1, 'forwards a database update');
  assert.strictEqual(updates[0].record.current_fen, 'test-fen');
  stop();
  assert(socket.sent.some(frame => frame.event === 'phx_leave'), 'unsubscribe sends a channel leave frame');
  assert.strictEqual(socket.readyState, 3, 'unsubscribe closes the socket');
  assert.throws(() => online.subscribeGame('bad-id', function () {}), /Invalid online game id/);
  console.log('OK online realtime: authenticated join ack, subscription ID filter, token refresh, update callback and leave');
}
main().catch(error => { console.error(error); process.exitCode = 1; });
