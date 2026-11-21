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
  'btnGambitPractice','btnGambitDemo','btnGambitCoachMove','btnGambitUndo','btnGambitRestart']) {
  assert(html.includes('id="' + id + '"'), 'Gambit Coach control exists: ' + id);
}
assert(app.includes('function gambitCoachReplies()'), 'coach automatically plays the opposing book replies');
assert(app.includes('function gambitEngineReply()'), 'Stockfish can continue when the user leaves the prepared line');
assert(app.includes('settings.progress.gambitStars'), 'three-star course mastery is saved');
assert(app.includes('Openings.LINES'), 'the complete existing ChessBuddy opening book is selectable');
assert(html.includes('id="variantStartMode"'), 'start-mode selector exists');
assert(app.includes('function chess960Fen(seed)'), 'Chess960 back-rank generation exists');
assert(app.includes("activeGameVariant === 'threecheck'"), '3-Check win condition is enforced');
assert(app.includes("activeGameVariant === 'koth'"), 'King of the Hill win condition is enforced');
assert(app.includes("options.startFen ? new Chess(options.startFen) : new Chess()"), 'custom FEN positions start a game');
console.log('OK Opening & Gambit Coach: ' + gambits.length + ' gambits, ' + totalPlies + ' legal SAN plies, Alien Gambit, coach practice/demo, star mastery and game setup variants');
