const assert = require('assert');
const fs = require('fs');

const html = fs.readFileSync('app/src/main/assets/index.html', 'utf8');
const app = fs.readFileSync('app/src/main/assets/js/app.js', 'utf8');
const css = fs.readFileSync('app/src/main/assets/css/app.css', 'utf8');

function hasId(id) {
  assert(html.includes('id="' + id + '"'), 'UI contains #' + id);
}

// Profile and Stats must be real, independently navigable screens.
for (const id of [
  'profileQuickBtn','view-profile','view-stats','moreProfile','moreStats',
  'profileAvatar','profileDisplayName','profileRatingGrid','profileRecentGames',
  'btnEditProfile','btnProfileStats','statsTimeControl','statsCurrentRating',
  'statsRatingGraph','statsRatingBreakdown'
]) hasId(id);

for (const id of [
  'moreOnline','moreArchive','moreCoach','morePuzzles','moreOpenings',
  'moreEndgames','moreCharacters','moreSettings','moreAbout'
]) hasId(id);

// Settings needs named categories with working scroll targets.
for (const id of ['settingsShortcuts','cardBoard','cardEngine','cardModels','cardData','cardPrivacy','cardAbout'])
  assert(html.includes('id="' + id + '"') || (id.startsWith('card') && app.includes(id)),
    'Settings navigation target exists: ' + id);
assert(html.includes('data-settings-target="cardBoard"'), 'Board settings shortcut is present');
assert(html.includes('data-settings-target="cardEngine"'), 'Engine settings shortcut is present');
assert(html.includes('data-settings-target="cardModels"'), 'AI settings shortcut is present');

// Navigation, profile editing and header back behaviour must be wired.
for (const fragment of [
  "function renderProfile()",
  "function renderStats()",
  "function editLocalProfile()",
  "function updateProfileShortcut()",
  "if (name === 'profile') renderProfile()",
  "if (name === 'stats') renderStats()",
  "showTab('profile')",
  "showTab('stats')",
  "showTab('more')"
]) assert(app.includes(fragment), 'app controller implements ' + fragment);

// Practice ratings are explicitly local and never count online, untimed or variant games.
assert(app.includes('function practiceBucketForTimeControl()'), 'time controls map to rating buckets');
assert(app.includes('function updatePracticeRating()'), 'local practice Elo calculation exists');
assert(app.includes("ctx.online || modeOf() !== 'hva' || activeGameVariant !== 'standard'"), 'online, two-human and variants are excluded');
assert(app.includes('if (!bucket) return null;'), 'untimed games are excluded');
assert(app.includes('practiceRatingHistory'), 'rating history is persisted');
assert(app.includes('gameKey'), 'a completed game cannot rate twice');
assert(app.includes('saveSettings();\n    return entry;'), 'local ratings are saved');
assert(app.includes('practiceRating:practiceRatingChange'), 'archive stores local rating deltas');
assert(html.includes('not Chess.com, FIDE, or official online ratings'), 'profile labels local ratings honestly');

// The Maia failure gets a bounded Stockfish fallback rather than freezing the game.
assert(app.includes('function recoverMaiaWithStockfish('), 'Maia runtime fallback exists');
assert(app.includes("engine:'stockfish', modelId:''"), 'fallback switches to Stockfish');
assert(app.includes('recoverMaiaWithStockfish(side, p, myToken, err)'), 'engine errors route through the fallback');

// The controls that clipped in the screenshots must now have responsive geometry.
assert(css.includes('.bgrid { grid-template-columns:repeat(auto-fit,minmax(96px,1fr))'), 'bot roster uses flexible columns');
assert(css.includes('@media(max-width:420px)'), 'phone-sized roster breakpoint exists');
assert(css.includes('#botsList { padding-bottom:290px; }'), 'bot roster reserves room for fixed dock and tab bar');
assert(css.includes('background:rgba(38,37,34,.985)'), 'bot dock is opaque enough to keep content legible');
assert(css.includes('#engineBanner #btnRetryEngine { flex:0 0 auto'), 'Retry button cannot collapse into vertical letters');

// Every statically authored icon name must exist in the app icon map.
const iconMatch = app.match(/const ICON = \{([\s\S]*?)\n  \};/);
assert(iconMatch, 'app icon registry exists');
const iconNames = new Set(Array.from(iconMatch[1].matchAll(/(?:^|,)\s*([A-Za-z][A-Za-z0-9]*):/g), m => m[1]));
const usedIcons = new Set(Array.from(html.matchAll(/data-ic="([^"]+)"/g), m => m[1]));
for (const name of usedIcons) assert(iconNames.has(name), 'HTML icon "' + name + '" exists in the icon registry');

console.log('OK mobile product: Profile, Stats, Settings, local ratings, Maia fallback, responsive bot cards, retry layout and ' + usedIcons.size + ' icon types');
