const assert = require('assert');
const fs = require('fs');
const vm = require('vm');
const Chess = require('../helpers/load-chessjs')().Chess;

const app = fs.readFileSync('app/src/main/assets/js/app.js', 'utf8');
const html = fs.readFileSync('app/src/main/assets/index.html', 'utf8');
const match = app.match(/const GAMBIT_COURSES = \[([\s\S]*?)\n  \];/);
assert(match, 'dedicated gambit catalogue exists');
const gambits = vm.runInNewContext('[' + match[1] + ']');
assert(gambits.length >= 30, 'at least thirty curated gambit courses are included');
assert.strictEqual(new Set(gambits.map(c => c.id)).size, gambits.length, 'gambit IDs are unique');
assert(gambits.some(c => c.id === 'alien-gambit'), 'Alien Gambit has a dedicated course');

const alienBranches = gambits.filter(c => c.id.indexOf('alien-gambit') === 0);
assert.strictEqual(alienBranches.length, 3, 'Alien Gambit main line and two key defensive branches are included');

const openingContext = { window:{} };
vm.runInNewContext(fs.readFileSync('app/src/main/assets/js/openings.js', 'utf8'), openingContext);
const openingBook = openingContext.window.CBOpenings.LINES;
assert(openingBook.length >= 100, 'the full built-in opening catalogue is available');
for (const [name, sanLine] of openingBook) {
  const board = new Chess();
  for (const san of sanLine.split(/\s+/)) {
    assert(board.move(san), name + ': opening book contains an illegal SAN move (' + san + ')');
  }
}

const chess960Block = app.match(/function chess960BackRank\(seed\) \{[\s\S]*?\n  \}\n  function chess960Fen\(seed\) \{[\s\S]*?\n  \}/);
assert(chess960Block, 'Chess960 start-position generator exists');
const chess960Sandbox = {};
vm.runInNewContext(chess960Block[0] + '\nthis.makeChess960Fen = chess960Fen;', chess960Sandbox);
assert.strictEqual(chess960Sandbox.makeChess960Fen(518).split('/')[7].split(' ')[0], 'RNBQKBNR', 'seed 518 maps to the orthodox starting layout');
const layouts = new Set();
for (let seed = 0; seed < 960; seed++) {
  const fen = chess960Sandbox.makeChess960Fen(seed);
  const backRank = fen.split('/')[7].split(' ')[0];
  assert.strictEqual(backRank.length, 8, 'seed ' + seed + ': eight back-rank pieces');
  const bishops = [];
  const rooks = [];
  let king = -1;
  for (let file = 0; file < 8; file++) {
    if (backRank[file] === 'B') bishops.push(file);
    if (backRank[file] === 'R') rooks.push(file);
    if (backRank[file] === 'K') king = file;
  }
  assert.strictEqual(bishops.length, 2, 'seed ' + seed + ': two bishops');
  assert.notStrictEqual(bishops[0] % 2, bishops[1] % 2, 'seed ' + seed + ': bishops on opposite colours');
  assert.strictEqual(rooks.length, 2, 'seed ' + seed + ': two rooks');
  assert(rooks[0] < king && king < rooks[1], 'seed ' + seed + ': king between rooks');
  assert.doesNotThrow(() => new Chess(fen), 'seed ' + seed + ': FEN is legal');
  layouts.add(backRank);
}
assert.strictEqual(layouts.size, 960, 'all 960 unique Chess960 starting layouts are generated');

let totalPlies = 0;
for (const course of gambits) {
  assert(course.name && course.idea && course.eco, course.id + ': descriptive course metadata exists');
  assert(['w','b'].includes(course.side), course.id + ': a recommended gambit side is defined');
  const game = new Chess();
  const moves = course.moves.trim().split(/\s+/);
  assert(moves.length >= 3, course.id + ': line contains multiple moves');
  for (let i = 0; i < moves.length; i++) {
    const move = game.move(moves[i]);
    assert(move, course.id + ': illegal SAN at ply ' + (i + 1) + ' (' + moves[i] + ')');
    totalPlies++;
  }
}
const alien = gambits.find(c => c.id === 'alien-gambit');
assert(alien.moves.startsWith('e4 c6 d4 d5 Nd2 dxe4 Nxe4 Nf6 Ng5 h6 Nxf7'), 'Alien Gambit follows the documented Caro-Kann move order');
assert(html.includes('id="gambitCoachLab"'), 'Gambit Coach panel is mounted');
for (const id of ['gambitSearch','gambitCourseSelect','gambitPracticeSide','gambitPracticeMode','gambitCoachBoard',
  'btnGambitPractice','btnGambitDemo','btnGambitAutoDemo','btnGambitStopDemo','btnGambitCoachMove','btnGambitUndo','btnGambitRestart']) {
  assert(html.includes('id="' + id + '"'), 'Gambit Coach control exists: ' + id);
}
assert(app.includes('function gambitCoachReplies()'), 'coach automatically plays the opposing book replies');
assert(app.includes('function startGambitAutoDemo()'), 'coach can automatically demonstrate a complete line');
assert(app.includes('function stopGambitAutoDemo(silent)'), 'automatic coach demonstration can be stopped safely');
assert(app.includes('function gambitEngineReply()'), 'Stockfish can continue when the user leaves the prepared line');
assert(app.includes('settings.progress.gambitStars'), 'three-star course mastery is saved');
assert(app.includes('Openings.LINES'), 'the complete existing ChessBuddy opening book is selectable');
assert(html.includes('id="variantStartMode"'), 'start-mode selector exists');
assert(app.includes('function chess960Fen(seed)'), 'Chess960 back-rank generation exists');
assert(app.includes("activeGameVariant === 'threecheck'"), '3-Check win condition is enforced');
assert(app.includes("activeGameVariant === 'koth'"), 'King of the Hill win condition is enforced');
assert(app.includes("options.startFen ? new Chess(options.startFen) : new Chess()"), 'custom FEN positions start a game');
console.log('OK Repertoire: ' + openingBook.length + ' openings + ' + gambits.length + ' gambits, ' + totalPlies + ' legal gambit plies, 960 Chess960 layouts and coach/variant controls');
