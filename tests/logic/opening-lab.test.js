const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const appPath = 'app/src/main/assets/js/app.js';
const htmlPath = 'app/src/main/assets/index.html';
const app = fs.readFileSync(appPath, 'utf8');
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

const jsDir = path.dirname(appPath);
const candidates = fs.readdirSync(jsDir).filter(name => /chess/i.test(name) && /\.js$/i.test(name));
let Chess = null;
for (const name of candidates) {
  const filename = path.join(jsDir, name);
  const moduleShim = { exports: {} };
  const sandbox = { module: moduleShim, exports: moduleShim.exports, console };
  sandbox.globalThis = sandbox;
  sandbox.window = sandbox;
  sandbox.self = sandbox;
  try {
    vm.runInNewContext(fs.readFileSync(filename, 'utf8'), sandbox, { filename });
    const exported = moduleShim.exports;
    const possible = exported.Chess || exported.default || exported || sandbox.Chess || sandbox.window.Chess;
    if (typeof possible === 'function') { Chess = possible; break; }
  } catch (_) { /* Try the next bundled chess implementation candidate. */ }
}
assert(Chess, 'the bundled rules engine is available to validate opening courses');

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
console.log('OK Opening Lab: ' + courses.length + ' courses, ' + courses.reduce((n,c) => n+c.moves.length,0) + ' legal half-moves validated by bundled chess rules');
