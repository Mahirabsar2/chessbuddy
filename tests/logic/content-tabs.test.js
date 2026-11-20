const assert = require('assert');
const fs = require('fs');
const html = fs.readFileSync('app/src/main/assets/index.html', 'utf8');
const app = fs.readFileSync('app/src/main/assets/js/app.js', 'utf8');
const lichess = fs.readFileSync('app/src/main/assets/js/lichess.js', 'utf8');
const css = fs.readFileSync('app/src/main/assets/css/app.css', 'utf8');
const tabs = ['play', 'puzzles', 'learn', 'watch', 'more'];
for (const tab of tabs) {
  assert(html.includes('data-tab="' + tab + '"'), 'main navigation includes ' + tab);
  assert(html.includes('id="view-' + tab + '"'), 'view exists for ' + tab);
}
assert(app.includes('function loadDailyPuzzle()'), 'daily puzzle loader exists');
assert(app.includes('function puzzleBoardTap(event)'), 'daily puzzle board input exists');
assert(app.includes('function renderLearn()'), 'lesson curriculum renderer exists');
assert(app.includes('function renderWatch()'), 'live watch renderer exists');
assert(app.includes('function renderMore()'), 'More hub renderer exists');
assert(lichess.includes('/api/puzzle/daily'), 'daily puzzle calls the public Lichess endpoint');
assert(lichess.includes('/api/tv/channels'), 'Watch calls the public Lichess TV channel endpoint');
assert(css.includes('.tabbar { grid-template-columns:repeat(5'), 'five-tab bar has responsive five-column layout');
assert(css.includes('#puzzleBoard { width:100%'), 'puzzle board is contained by its card');
console.log('OK Next Gen tabs: five destinations, daily puzzle solver, lessons, live TV and More hub');
