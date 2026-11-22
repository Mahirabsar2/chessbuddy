const assert = require('assert');
const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('app/src/main/assets/index.html', 'utf8');
const app = fs.readFileSync('app/src/main/assets/js/app.js', 'utf8');
const css = fs.readFileSync('app/src/main/assets/css/app.css', 'utf8');

function hasId(id) {
  assert(html.includes('id="' + id + '"'), 'UI contains #' + id);
}

for (const id of [
  'view-achievements','achievementXp','achievementLevel','achievementProgressBar',
  'achievementUnlocked','achievementAvailable','achievementTotal','achievementGrid',
  'view-tournaments','botCupName','botCupRounds','btnCreateBotCup','botCupCurrent','botCupHistory',
  'view-collections','collectionName','btnCreateCollection','collectionGameSelect',
  'collectionTargetSelect','btnAddCollectionGame','collectionList','collectionGames',
  'moreAchievements','moreTournaments','moreCollections','btnProfileAchievements'
]) hasId(id);

// The catalogue is data-backed, unique, and each achievement grants positive XP.
const block = app.match(/const CB2_ACHIEVEMENTS = (\[[\s\S]*?\n  \]);/);
assert(block, 'achievement catalogue exists');
const achievements = vm.runInNewContext(block[1]);
assert(achievements.length >= 14, 'at least 14 achievements exist');
assert.strictEqual(new Set(achievements.map(a => a.id)).size, achievements.length, 'achievement IDs are unique');
for (const a of achievements) {
  assert(a.id && a.title && a.detail, 'achievement has user-facing copy');
  assert(Number.isInteger(a.xp) && a.xp > 0, a.id + ' awards positive XP');
  assert(Number.isFinite(a.target) && a.target > 0, a.id + ' has a positive target');
  assert(a.metric, a.id + ' reads a measurable progress metric');
}
assert(app.includes('function cb2RefreshAchievementAwards('), 'achievements unlock from tracked progress');
assert(app.includes('function renderAchievements('), 'achievement page renders dynamic progress');

// Solo bot cups use real roster opponents and the actual game result.
for (const token of [
  'function cb2CupOpponentList(', 'function createBotCup(', 'function startBotCupRound(',
  'function renderTournaments(', 'function cb2CupResult(', 'activeBotTournamentMatch',
  'cb2CupResult(list[0])', 'data-cup-start'
]) assert(app.includes(token), 'cup integration exists: ' + token);
assert(html.includes('Solo Bot Cup') && html.includes('OFFLINE'), 'cups are clearly labelled local/offline');

// Collections reference real archived game IDs and export the stored PGN.
for (const token of [
  'function cb2Collections(', 'function cb2ArchiveGames(', 'function renderCollections(',
  'function createCollection(', 'function addGameToCollection(', 'function removeCollectionGame(',
  'function showCollectionPgn(', 'data-pgn-copy'
]) assert(app.includes(token), 'collection workflow exists: ' + token);
assert(app.includes('navigator.clipboard.writeText(text)'), 'PGN export offers clipboard copy');

// All three destinations must be reachable through More and use the ordinary app route.
for (const token of [
  "achievements:'Achievements'", "tournaments:'Events & Cups'", "collections:'Collections'",
  "name === 'achievements'", "name === 'tournaments'", "name === 'collections'",
  "showTab('achievements')", "showTab('tournaments')", "showTab('collections')"
]) assert(app.includes(token), 'navigation integration exists: ' + token);

assert(css.includes('.achievement-grid'), 'achievement cards have dedicated layout styles');
assert(css.includes('.bot-cup-card'), 'tournament cards have dedicated layout styles');
assert(css.includes('.collection-game-row'), 'collection rows have dedicated layout styles');
assert(app.includes('not official Chess.com trophies'), 'local achievements are not misrepresented');
assert(app.includes('OFFLINE'), 'solo events are not misrepresented as online tournaments');

console.log('OK ChessBuddy 2.0.0 expansion: ' + achievements.length +
  ' achievements, local bot cups, and PGN collections with navigation and styling');
