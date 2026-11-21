const assert = require('assert');
const fs = require('fs');

const app = fs.readFileSync('app/src/main/assets/js/app.js', 'utf8');
const match = app.match(/const RUSH_PUZZLE_PACK = \[([\s\S]*?)\n  \];/);
assert(match, 'Puzzle Rush pack exists');
const entries = Array.from(match[1].matchAll(/\{\s*id:'([^']+)',\s*fen:'([^']+)',\s*solution:\['([a-h][1-8][a-h][1-8])'\]/g),
  m => ({ id: m[1], fen: m[2], move: m[3] }));
assert.strictEqual(entries.length, 8, 'all eight curated puzzle positions are present');

function squareOf(uci, offset) {
  const file = uci.charCodeAt(offset) - 97;
  const rank = Number(uci[offset + 1]);
  return [8 - rank, file];
}
function parseBoard(fen) {
  const rows = fen.split(' ')[0].split('/');
  assert.strictEqual(rows.length, 8, 'FEN has eight ranks');
  return rows.map(row => {
    const out = [];
    for (const ch of row) {
      if (/^[1-8]$/.test(ch)) {
        for (let i = 0; i < Number(ch); i++) out.push('.');
      } else out.push(ch);
    }
    assert.strictEqual(out.length, 8, 'FEN rank has eight files');
    return out;
  });
}
function findPiece(board, piece) {
  for (let r = 0; r < 8; r++) for (let c = 0; c < 8; c++)
    if (board[r][c] === piece) return [r, c];
  return null;
}
function clearPath(board, from, to) {
  const dr = Math.sign(to[0] - from[0]), dc = Math.sign(to[1] - from[1]);
  let r = from[0] + dr, c = from[1] + dc;
  while (r !== to[0] || c !== to[1]) {
    if (board[r][c] !== '.') return false;
    r += dr; c += dc;
  }
  return true;
}
function whiteAttacks(board, target) {
  const king = findPiece(board, 'K');
  if (king && Math.max(Math.abs(king[0]-target[0]), Math.abs(king[1]-target[1])) <= 1) return true;
  const queen = findPiece(board, 'Q');
  if (!queen) return false;
  const dr = Math.abs(queen[0]-target[0]), dc = Math.abs(queen[1]-target[1]);
  if (!(dr === 0 || dc === 0 || dr === dc)) return false;
  return clearPath(board, queen, target);
}
function hasBlackKingEscape(board, king) {
  for (let dr = -1; dr <= 1; dr++) for (let dc = -1; dc <= 1; dc++) {
    if (dr === 0 && dc === 0) continue;
    const target = [king[0]+dr, king[1]+dc];
    if (target[0] < 0 || target[0] > 7 || target[1] < 0 || target[1] > 7) continue;
    const occupant = board[target[0]][target[1]];
    if (occupant !== '.' && occupant !== 'Q' && occupant !== 'K') continue;
    const copy = board.map(row => row.slice());
    copy[king[0]][king[1]] = '.';
    copy[target[0]][target[1]] = 'k';
    if (!whiteAttacks(copy, target)) return true;
  }
  return false;
}
for (const p of entries) {
  const board = parseBoard(p.fen);
  const from = squareOf(p.move, 0), to = squareOf(p.move, 2);
  assert.strictEqual(board[from[0]][from[1]], 'Q', p.id + ': move starts on the white queen');
  assert.strictEqual(board[to[0]][to[1]], '.', p.id + ': destination is empty');
  const dr = Math.abs(to[0]-from[0]), dc = Math.abs(to[1]-from[1]);
  assert(dr === 0 || dc === 0 || dr === dc, p.id + ': queen move follows a legal line');
  assert(clearPath(board, from, to), p.id + ': queen path is clear');
  const beforeKing = findPiece(board, 'k');
  assert(beforeKing, p.id + ': black king exists');
  assert(!whiteAttacks(board, beforeKing), p.id + ': side to move is not already giving check');
  board[from[0]][from[1]] = '.';
  board[to[0]][to[1]] = 'Q';
  const king = findPiece(board, 'k');
  assert(whiteAttacks(board, king), p.id + ': solution gives check');
  assert(!hasBlackKingEscape(board, king), p.id + ': solution is checkmate');
}
console.log('OK Puzzle Rush: 8 FENs, legal queen moves and verified mate-in-one solutions');
