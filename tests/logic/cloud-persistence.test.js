const assert = require('assert');
const { test, done } = require('../helpers/mini-test');
console.log('cloud persistence (Supabase user state + PGN archive)');

function setup() {
  const calls = [];
  const state = {
    profile: { displayName: 'Cloud Player', bio: 'Saved in cloud' },
    settings: { ui: { theme: 'blue' }, play: { tc: '3+2' } },
    progress: { puzzlesSolved: 27 }
  };
  const savedRows = [{
    client_game_id: 'g-cloud-1',
    pgn: '[Event "Cloud"]\n1. e4 e5 *',
    metadata: { date: '2026-11-24T10:00:00.000Z', white: 'Cloud Player', black: 'Marlow', result: '*' },
    created_at: '2026-11-24T10:00:00.000Z',
    updated_at: '2026-11-24T10:00:00.000Z'
  }];
  global.CBNative = {
    available: true,
    supabaseAuth: (op, payload) => {
      calls.push({ type: 'auth', op, payload });
      return { promise: Promise.resolve({ status: 200, body: JSON.stringify({ access_token: 'cloud-test-access-token-123456', user: { id: 'cloud-user-1' }, refresh_token: '[stored natively]' }) }) };
    },
    httpGet: (url, headers) => {
      calls.push({ type: 'get', url, headers });
      const body = url.includes('/chessbuddy_user_state?') ? [state]
        : url.includes('/chessbuddy_saved_games?') ? savedRows : [];
      return { promise: Promise.resolve({ status: 200, body: JSON.stringify(body) }) };
    },
    http: req => {
      calls.push({ type: 'post', req });
      return { promise: Promise.resolve({ status: 201, body: '' }) };
    }
  };
  delete require.cache[require.resolve('../../app/src/main/assets/js/online.js')];
  require('../../app/src/main/assets/js/online.js');
  return { api: global.CBOnline, calls };
}

test('loads only the signed-in account state and saved PGN games', async () => {
  const { api, calls } = setup();
  await api.signIn('player@example.com', 'password123');
  const state = await api.loadUserState();
  assert.strictEqual(state.profile.displayName, 'Cloud Player');
  assert.strictEqual(state.progress.puzzlesSolved, 27);
  const games = await api.loadSavedGames();
  assert.strictEqual(games.length, 1);
  assert.strictEqual(games[0].id, 'g-cloud-1');
  assert.ok(games[0].pgn.includes('1. e4 e5'));
  assert.ok(calls.some(c => c.type === 'get' && c.url.includes('user_id=eq.cloud-user-1')));
});

test('upserts profile/settings/progress with the authenticated user id', async () => {
  const { api, calls } = setup();
  await api.signIn('player@example.com', 'password123');
  await api.saveUserState({
    profile: { displayName: 'Mahir', bio: 'Chess' },
    settings: { ui: { theme: 'green' } },
    progress: { puzzlesSolved: 9 }
  });
  const post = calls.find(c => c.type === 'post').req;
  assert.ok(post.url.includes('/rest/v1/chessbuddy_user_state?on_conflict=user_id'));
  assert.ok(post.extraHeaders.includes('Prefer: resolution=merge-duplicates,return=minimal'));
  const row = JSON.parse(post.body);
  assert.strictEqual(row.user_id, 'cloud-user-1');
  assert.strictEqual(row.profile.displayName, 'Mahir');
  assert.strictEqual(row.progress.puzzlesSolved, 9);
});

test('upserts saved PGNs in batches with stable per-user client game IDs', async () => {
  const { api, calls } = setup();
  await api.signIn('player@example.com', 'password123');
  await api.saveSavedGames([
    { id: 'g-100', pgn: '1. d4 d5 *', date: '2026-11-24T11:00:00.000Z', white: 'Player', result: '*' },
    { id: 'g-101', pgn: '1. e4 c5 *', date: '2026-11-24T12:00:00.000Z', black: 'Marlow', result: '*' }
  ]);
  const post = calls.find(c => c.type === 'post').req;
  assert.ok(post.url.includes('/rest/v1/chessbuddy_saved_games?on_conflict=user_id%2Cclient_game_id'));
  assert.ok(post.extraHeaders.includes('resolution=merge-duplicates'));
  const rows = JSON.parse(post.body);
  assert.strictEqual(rows.length, 2);
  assert.strictEqual(rows[0].user_id, 'cloud-user-1');
  assert.strictEqual(rows[0].client_game_id, 'g-100');
  assert.strictEqual(rows[0].pgn, '1. d4 d5 *');
  assert.strictEqual(rows[0].metadata.white, 'Player');
  assert.strictEqual(Object.prototype.hasOwnProperty.call(rows[0].metadata, 'pgn'), false);
});

test('updater checks the 2.0.0 APK and checksum names published by CI', () => {
  const fs = require('fs');
  const updater = fs.readFileSync('app/src/main/assets/js/updater.js', 'utf8');
  assert.ok(updater.includes("ChessBuddy-NextGen-2.0.0.apk"));
  assert.ok(updater.includes("ChessBuddy-NextGen-2.0.0.apk.sha256"));
  assert.ok(!updater.includes("ChessBuddy-NextGen-1.0.0.apk"));
});

test('creator challenge presets are original Stockfish practice profiles', () => {
  const strength = require('../../app/src/main/assets/js/strength.js');
  for (const id of ['creator_mrbeast', 'creator_gothamchess', 'creator_witty_alien']) {
    const bot = strength.botById(id);
    assert.ok(bot, id + ' exists');
    assert.strictEqual(bot.unofficial, true);
    assert.strictEqual(bot.practiceOnly, true);
    assert.ok(bot.blurb.includes('not affiliated'));
  }
  assert.ok(strength.botById('mittens'), 'Mittens remains in the roster');
});

done('cloud persistence');
