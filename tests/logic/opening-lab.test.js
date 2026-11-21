const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const appPath = 'app/src/main/assets/js/app.js';
const htmlPath = 'app/src/main/assets/index.html';
const app = fs.readFileSync(appPath, 'utf8');
const lichess = fs.readFileSync('app/src/main/assets/js/lichess.js', 'utf8');
const html = fs.readFileSync(htmlPath, 'utf8');

assert(html.includes('id="openingLab"'), 'Opening Lab panel is mounted');
assert(html.includes('id="openingBoard"'), 'Opening Lab board exists');
assert(html.includes('id="openingCourseSelect"'), 'Opening Lab course selector exists');
assert(html.includes('id="btnOpeningNext"') && html.includes('id="btnOpeningBack"'), 'Opening Lab navigation controls exist');

const match = app.match(/const OPENING_COURSES = (\[[\s\S]*?\n  \]);/);
assert(match, 'Opening Lab course data exists');
const courses = vm.runInNewContext(match[1]);
assert(courses.length >= 8, 'at least eight opening courses are available');
assert.strictEqual(new Set(courses.map(c => c.id)).size, courses.length, 'course IDs are unique');

const Chess = require('../helpers/load-chessjs')().Chess;
assert(Chess, 'the bundled chess rules engine is available to validate repertoire courses');

for (const course of courses) {
  assert(course.name && course.eco && course.focus, course.id + ': descriptive course metadata exists');
  assert(Array.isArray(course.moves) && course.moves.length >= 8, course.id + ': course has a useful main line');
  const game = new Chess();
  for (let i = 0; i < course.moves.length; i++) {
    const [uci, explanation] = course.moves[i];
    assert(/^[a-h][1-8][a-h][1-8][qrbn]?$/.test(uci), course.id + ': UCI notation is valid at step ' + (i + 1));
    assert(explanation && explanation.length >= 8, course.id + ': every move has an explanation');
    const move = game.move({ from:uci.slice(0,2), to:uci.slice(2,4), promotion:uci.length > 4 ? uci[4] : undefined });
    assert(move, course.id + ': illegal move at step ' + (i + 1) + ' (' + uci + ')');
  }
}
assert(app.includes('function buildOpeningStudy(course)'), 'Opening Lab validates every course before display');
assert(app.includes('settings.progress.completedOpenings'), 'opening completions are saved');

assert(html.includes('id="endgameLab"'), 'Endgame Lab panel is mounted');
assert(html.includes('id="endgamePreset"') && html.includes('id="endgameFen"'), 'Endgame Lab preset selector and custom FEN input exist');
assert(html.includes('id="btnLookupEndgame"') && html.includes('id="btnPlayEndgameBest"'), 'Endgame Lab tablebase and best-move controls exist');
assert(app.includes('function lookupEndgameTablebase()'), 'Endgame Lab tablebase controller exists');
assert(app.includes('function loadEndgamePosition(fen)'), 'Endgame Lab FEN validator exists');
assert(app.includes('function playBestEndgameMove()'), 'Endgame Lab best-move playback exists');
assert(lichess.includes('tablebase: tablebase'), 'Lichess tablebase adapter is exposed');
const endgameMatch = app.match(/const ENDGAME_PRESETS = (\[[\s\S]*?\n  \]);/);
assert(endgameMatch, 'Endgame Lab presets are bundled');
const endgamePresets = vm.runInNewContext(endgameMatch[1]);
assert.strictEqual(endgamePresets.length, 4, 'four preset endgames are available');
for (const preset of endgamePresets) {
  const game = new Chess(preset.fen);
  const pieces = preset.fen.split(' ')[0].replace(/[1-8/]/g, '').length;
  assert(pieces <= 7, preset.id + ': tablebase piece limit is respected');
  assert(game.fen(), preset.id + ': FEN can be parsed by the bundled chess rules');
  assert(game.moves().length > 0, preset.id + ': sample position has a legal continuation');
}
console.log('OK Study Labs: ' + courses.length + ' opening courses, ' + courses.reduce((n,c) => n+c.moves.length,0) + ' legal half-moves, and ' + endgamePresets.length + ' valid tablebase endgames');
