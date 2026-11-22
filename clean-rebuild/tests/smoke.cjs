const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');

const root = path.resolve(__dirname, '..');
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');
const html = read('app/src/main/assets/index.html');
const js = read('app/src/main/assets/js/app.js');
const manifest = read('app/src/main/AndroidManifest.xml');
const gradle = read('app/build.gradle');

for (const view of ['home', 'play', 'puzzles', 'learn', 'analysis', 'profile', 'settings']) {
  assert.ok(html.includes('id="view-' + view + '"'), 'missing view: ' + view);
}
for (const action of ['undo', 'flip', 'copy-fen', 'share-pgn', 'load-fen', 'reset-puzzle']) {
  assert.ok(html.includes('data-action="' + action + '"'), 'missing action: ' + action);
}
for (const rule of ['game.moves(', 'game.move(', 'isCheckmate()', 'isStalemate()', 'isDraw()', 'game.load(fen)']) {
  assert.ok(js.includes(rule), 'missing chess rule call: ' + rule);
}
assert.ok(html.includes('js/chess-bundle.js'), 'chess rules bundle is not loaded');
assert.ok(manifest.includes('com.chessbuddy') || gradle.includes("applicationId 'com.chessbuddy'"));
assert.ok(gradle.includes("versionName '0.1.0'"));
assert.ok(!html.includes('chess.com'), 'do not ship remote Chess.com branding in this clean app');
console.log('ChessBuddy clean rebuild smoke checks passed.');
