const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const { Chess } = require('chess.js');

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
for (const rule of ['game.moves(', 'game.move(', 'isCheckmate()', 'isStalemate()', 'isDraw()', 'candidate.load(fen)']) {
  assert.ok(js.includes(rule), 'missing chess rule call: ' + rule);
}
assert.ok(html.includes('js/chess-bundle.js'), 'chess rules bundle is not loaded');
assert.ok(html.includes('data-view="settings"'), 'settings route must be reachable');
assert.ok(html.includes('data-view="analysis"'), 'analysis route must be reachable from game UI');
assert.ok(manifest.includes('android:name=".MainActivity"'));
assert.ok(gradle.includes("applicationId 'com.chessbuddy'"));
assert.ok(gradle.includes("versionName '0.1.0'"));
assert.ok(!html.toLowerCase().includes('chess.com'), 'clean rebuild must not reference Chess.com web assets');

const opening = new Chess();
for (const move of [
  { from: 'e2', to: 'e4' },
  { from: 'e7', to: 'e5' },
  { from: 'g1', to: 'f3' },
  { from: 'b8', to: 'c6' },
  { from: 'f1', to: 'c4' }
]) assert.ok(opening.move(move), 'opening line contains an illegal move');
assert.equal(opening.history().join(' '), 'e4 e5 Nf3 Nc6 Bc4');

const castle = new Chess('r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1');
assert.equal(castle.move({ from: 'e1', to: 'g1' }).san, 'O-O');

const enPassant = new Chess('8/8/8/3pP3/8/8/8/4K2k w - d6 0 1');
assert.equal(enPassant.move({ from: 'e5', to: 'd6' }).flags.includes('e'), true);

const promotion = new Chess('7k/P7/8/8/8/8/8/7K w - - 0 1');
assert.equal(promotion.move({ from: 'a7', to: 'a8', promotion: 'q' }).promotion, 'q');

const puzzle = new Chess('7k/8/5KQ1/8/8/8/8/8 w - - 0 1');
assert.equal(puzzle.move({ from: 'g6', to: 'g7' }).san, 'Qg7#');
assert.equal(puzzle.isCheckmate(), true);

assert.throws(() => new Chess().move({ from: 'e2', to: 'e5' }), 'illegal moves must be rejected');
console.log('ChessBuddy clean rebuild smoke and chess-rules tests passed.');
