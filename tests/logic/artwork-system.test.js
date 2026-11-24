const assert = require('assert');
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '../..');
const pieces = require(path.join(root, 'app/src/main/assets/js/pieces.js'));

assert.strictEqual(pieces.version, 'atelier-1');
for (const color of ['w', 'b']) for (const type of 'pnbrqk') {
  const svg = pieces.standalone(color, type, 96);
  assert(svg.startsWith('<svg') && svg.includes('<path'), color + type + ' SVG geometry');
}
const sprite = pieces.sprite();
for (const id of ['wP','wN','wB','wR','wQ','wK','bP','bN','bB','bR','bQ','bK','cb-mark']) {
  assert(sprite.includes('id="' + id + '"'), 'symbol exists: ' + id);
}
assert(!sprite.includes('cburnett'), 'third-party piece set replaced');
const html = fs.readFileSync(path.join(root, 'app/src/main/assets/index.html'), 'utf8');
for (const theme of ['green','brown','blue','rose','midnight','parchment']) {
  assert(html.includes('data-v="' + theme + '"'), 'theme control exists: ' + theme);
}
assert(html.includes('href="#cb-mark"'), 'brand mark used in app shell');
const css = fs.readFileSync(path.join(root, 'app/src/main/assets/css/app.css'), 'utf8');
for (const theme of ['green','brown','blue','rose','midnight','parchment']) {
  assert(css.includes('body[data-theme=' + theme + ']'), 'board palette exists: ' + theme);
}
const icon = fs.readFileSync(path.join(root, 'app/src/main/res/drawable/ic_launcher_foreground.xml'), 'utf8');
assert(icon.includes('#F3E6C7') && icon.includes('#D9B76D'), 'launcher icon uses Atelier palette');
assert(fs.existsSync(path.join(root, 'app/src/main/assets/artwork/brand-mark.svg')), 'editable brand source exists');
console.log('OK artwork-system: 12 original pieces, brand, launcher icon and six board palettes');
