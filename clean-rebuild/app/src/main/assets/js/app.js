(function () {
  'use strict';

  if (!window.ChessBundle || !window.ChessBundle.Chess) {
    document.body.innerHTML = '<main style="padding:24px;color:white">Chess rules failed to load. Reinstall the latest build.</main>';
    return;
  }

  const Chess = window.ChessBundle.Chess;
  const START_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
  const PUZZLE_FEN = '7k/8/5KQ1/8/8/8/8/8 w - - 0 1';
  const PIECES = {
    w: { k: '♔', q: '♕', r: '♖', b: '♗', n: '♘', p: '♙' },
    b: { k: '♚', q: '♛', r: '♜', b: '♝', n: '♞', p: '♟︎' }
  };
  const files = 'abcdefgh';
  const games = {
    play: new Chess(),
    puzzle: new Chess(PUZZLE_FEN),
    learn: new Chess(),
    analysis: new Chess()
  };
  const selected = { play: null, puzzle: null, learn: null, analysis: null };
  const flipped = { play: false, puzzle: false, learn: false, analysis: false };
  let activeView = 'home';
  let selectedTime = 10;
  let clocks = { w: 600, b: 600 };
  let clockSide = null;
  let lastClockTick = 0;
  let clockTimer = null;
  let pendingPromotion = null;
  let puzzleSolved = false;
  let lessonIndex = 0;
  let playRecorded = false;
  let toastTimer = null;
  const lessonMoves = [
    { from: 'e2', to: 'e4', title: 'Claim the center', copy: '1. e4 controls central squares and opens lines for your pieces.' },
    { from: 'e7', to: 'e5', title: 'Meet the challenge', copy: 'Black contests the center. Central space is a shared resource.' },
    { from: 'g1', to: 'f3', title: 'Develop with purpose', copy: 'The knight attacks e5 and moves toward the center.' },
    { from: 'b8', to: 'c6', title: 'Defend and develop', copy: 'Black develops a knight while protecting the e5 pawn.' },
    { from: 'f1', to: 'c4', title: 'The Italian bishop', copy: 'The bishop targets the f7 square and helps prepare castling.' }
  ];

  function getContext(view) {
    if (view === 'puzzles') return 'puzzle';
    if (view === 'learn') return 'learn';
    if (view === 'analysis') return 'analysis';
    return 'play';
  }

  function currentGame() {
    return games[getContext(activeView)];
  }

  function safeReadStats() {
    try {
      return JSON.parse(localStorage.getItem('cb.stats') || '{"games":0,"wins":0,"draws":0,"puzzles":0}');
    } catch (e) {
      return { games: 0, wins: 0, draws: 0, puzzles: 0 };
    }
  }

  function saveStats(stats) {
    try { localStorage.setItem('cb.stats', JSON.stringify(stats)); } catch (e) {}
    renderStats();
  }

  function renderStats() {
    const stats = safeReadStats();
    const set = function (id, value) {
      const node = document.getElementById(id);
      if (node) node.textContent = String(value);
    };
    set('home-games', stats.games);
    set('home-wins', stats.wins);
    set('home-puzzles', stats.puzzles);
    set('profile-games', stats.games);
    set('profile-wins', stats.wins);
    set('profile-draws', stats.draws);
    set('profile-puzzles', stats.puzzles);
  }

  function showToast(message) {
    const node = document.getElementById('toast');
    if (!node) return;
    node.textContent = message;
    node.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { node.classList.remove('show'); }, 2100);
  }

  function setView(view) {
    if (!document.getElementById('view-' + view)) view = 'home';
    activeView = view;
    document.querySelectorAll('.view').forEach(function (node) {
      node.classList.toggle('active', node.id === 'view-' + view);
    });
    document.querySelectorAll('[data-view]').forEach(function (node) {
      node.classList.toggle('active', node.getAttribute('data-view') === view);
    });
    selected[getContext(view)] = null;
    renderAll();
    if (view === 'profile') renderStats();
  }

  function formatTime(value) {
    const safe = Math.max(0, Math.ceil(value));
    const minutes = Math.floor(safe / 60);
    const seconds = safe % 60;
    return minutes + ':' + String(seconds).padStart(2, '0');
  }

  function stopClock() {
    if (clockTimer) clearInterval(clockTimer);
    clockTimer = null;
    clockSide = null;
    lastClockTick = 0;
  }

  function updateClockDisplay() {
    const white = document.getElementById('white-clock');
    const black = document.getElementById('black-clock');
    if (white) {
      white.textContent = selectedTime === 0 ? '—' : formatTime(clocks.w);
      white.classList.toggle('active-clock', clockSide === 'w');
    }
    if (black) {
      black.textContent = selectedTime === 0 ? '—' : formatTime(clocks.b);
      black.classList.toggle('active-clock', clockSide === 'b');
    }
  }

  function newGame(minutes) {
    if (typeof minutes === 'number') selectedTime = minutes;
    games.play = new Chess();
    playRecorded = false;
    selected.play = null;
    flipped.play = false;
    clocks = { w: selectedTime * 60, b: selectedTime * 60 };
    stopClock();
    document.getElementById('game-status').textContent = 'White to move';
    document.querySelectorAll('[data-time]').forEach(function (node) {
      node.classList.toggle('selected', Number(node.dataset.time) === selectedTime);
    });
    renderAll();
    setView('play');
  }

  function finishGame(message, result) {
    stopClock();
    const status = document.getElementById('game-status');
    if (status) status.textContent = message;
    if (result && !playRecorded) {
      const stats = safeReadStats();
      stats.games += 1;
      if (result === 'win') stats.wins += 1;
      if (result === 'draw') stats.draws += 1;
      playRecorded = true;
      saveStats(stats);
    }
    renderAll();
  }

  function tickClock() {
    if (!clockSide || selectedTime === 0) return;
    const now = Date.now();
    const elapsed = Math.floor((now - lastClockTick) / 1000);
    if (elapsed < 1) return;
    lastClockTick += elapsed * 1000;
    clocks[clockSide] -= elapsed;
    if (clocks[clockSide] <= 0) {
      clocks[clockSide] = 0;
      const loser = clockSide;
      const winner = loser === 'w' ? 'Black' : 'White';
      stopClock();
      finishGame(winner + ' wins on time.', 'win');
    }
    updateClockDisplay();
  }

  function startNextClock() {
    if (selectedTime === 0 || games.play.isGameOver()) return;
    clockSide = games.play.turn();
    lastClockTick = Date.now();
    if (!clockTimer) clockTimer = setInterval(tickClock, 250);
    updateClockDisplay();
  }

  function getStatus(game) {
    if (game.isCheckmate()) return 'Checkmate — ' + (game.turn() === 'w' ? 'Black' : 'White') + ' wins.';
    if (game.isStalemate()) return 'Draw — stalemate.';
    if (game.isThreefoldRepetition()) return 'Draw available — threefold repetition.';
    if (game.isInsufficientMaterial()) return 'Draw — insufficient material.';
    if (game.isDraw()) return 'Draw — game rules.';
    return (game.turn() === 'w' ? 'White' : 'Black') + ' to move' + (game.isCheck() ? ' · Check' : '');
  }

  function getLastMove(game) {
    const history = game.history({ verbose: true });
    return history.length ? history[history.length - 1] : null;
  }

  function squareClass(game, context, square, piece, lastMove, legalMoves) {
    const parts = ['square'];
    const rank = Number(square[1]);
    const fileIndex = files.indexOf(square[0]);
    parts.push((fileIndex + rank) % 2 === 1 ? 'dark' : 'light');
    if (selected[context] === square) parts.push('selected');
    if (lastMove && (lastMove.from === square || lastMove.to === square)) parts.push('last-move');
    const move = legalMoves.find(function (item) { return item.to === square; });
    if (move && localStorage.getItem('cb.legal') !== 'false') parts.push(move.captured ? 'capture' : 'legal');
    return parts.join(' ');
  }

  function renderBoard(context) {
    const ids = { play: 'board', puzzle: 'puzzle-board', learn: 'lesson-board', analysis: 'analysis-board' };
    const board = document.getElementById(ids[context]);
    if (!board) return;
    const game = games[context];
    const lastMove = getLastMove(game);
    const selectedSquare = selected[context];
    const legalMoves = selectedSquare ? game.moves({ square: selectedSquare, verbose: true }) : [];
    const rows = [];
    for (let row = 0; row < 8; row += 1) {
      for (let col = 0; col < 8; col += 1) {
        const file = flipped[context] ? 7 - col : col;
        const rank = flipped[context] ? row + 1 : 8 - row;
        const square = files[file] + String(rank);
        const piece = game.get(square);
        const glyph = piece ? PIECES[piece.color][piece.type] : '';
        const button = document.createElement('button');
        button.type = 'button';
        button.className = squareClass(game, context, square, piece, lastMove, legalMoves);
        button.dataset.square = square;
        button.setAttribute('aria-label', square + (piece ? ' ' + piece.color + ' ' + piece.type : ' empty'));
        const pieceNode = document.createElement('span');
        pieceNode.className = 'piece';
        pieceNode.textContent = glyph;
        button.appendChild(pieceNode);
        if (col === 0 && localStorage.getItem('cb.coords') !== 'false') {
          const coord = document.createElement('span');
          coord.className = 'coord';
          coord.textContent = String(rank);
          button.appendChild(coord);
        }
        if (row === 7 && localStorage.getItem('cb.coords') !== 'false') {
          const coord = document.createElement('span');
          coord.className = 'coord file-coord';
          coord.textContent = files[file];
          button.appendChild(coord);
        }
        rows.push(button);
      }
    }
    board.replaceChildren.apply(board, rows);
  }

  function renderMoves(game) {
    const node = document.getElementById('move-list');
    if (!node) return;
    const history = game.history();
    const pairs = [];
    for (let i = 0; i < history.length; i += 2) {
      const row = document.createElement('div');
      row.className = 'move-pair';
      const number = document.createElement('span');
      number.className = 'move-number';
      number.textContent = String(Math.floor(i / 2) + 1) + '.';
      const white = document.createElement('span');
      white.className = 'move-san' + (i === history.length - 1 ? ' latest' : '');
      white.textContent = history[i] || '';
      const black = document.createElement('span');
      black.className = 'move-san' + (i + 1 === history.length - 1 ? ' latest' : '');
      black.textContent = history[i + 1] || '';
      row.append(number, white, black);
      pairs.push(row);
    }
    if (!pairs.length) {
      const empty = document.createElement('span');
      empty.className = 'empty-state';
      empty.textContent = 'Moves will appear here.';
      node.replaceChildren(empty);
    } else {
      node.replaceChildren.apply(node, pairs);
      node.scrollTop = node.scrollHeight;
    }
    const count = document.getElementById('move-count');
    if (count) count.textContent = history.length + (history.length === 1 ? ' move' : ' moves');
  }

  function renderLesson() {
    const current = lessonMoves[Math.min(lessonIndex, lessonMoves.length - 1)];
    const title = document.getElementById('lesson-title');
    const copy = document.getElementById('lesson-copy');
    const progress = document.querySelector('#lesson-progress span');
    if (title) title.textContent = lessonIndex >= lessonMoves.length ? 'Opening complete' : current.title;
    if (copy) copy.textContent = lessonIndex >= lessonMoves.length ? 'You completed the opening line. Restart to practise it again.' : current.copy;
    if (progress) progress.style.width = Math.round((lessonIndex / lessonMoves.length) * 100) + '%';
  }

  function renderAll() {
    renderBoard('play');
    renderBoard('puzzle');
    renderBoard('learn');
    renderBoard('analysis');
    renderMoves(games.play);
    renderStats();
    updateClockDisplay();
    const status = document.getElementById('game-status');
    if (status && games.play.isGameOver()) status.textContent = getStatus(games.play);
    renderLesson();
  }

  function handleSquare(context, square) {
    const game = games[context];
    if ((context === 'play' && game.isGameOver()) || (context === 'puzzle' && puzzleSolved)) return;
    const chosen = selected[context];
    const piece = game.get(square);
    if (context === 'play' && !game.history().length && selectedTime > 0 && !clockSide && piece && piece.color === game.turn()) {
      clockSide = game.turn();
      lastClockTick = Date.now();
      if (!clockTimer) clockTimer = setInterval(tickClock, 250);
      updateClockDisplay();
    }
    if (chosen) {
      const candidate = game.moves({ square: chosen, verbose: true }).filter(function (move) { return move.to === square; });
      if (candidate.length) {
        if (candidate.some(function (move) { return !!move.promotion; })) {
          pendingPromotion = { context: context, from: chosen, to: square };
          document.getElementById('promotion-modal').classList.remove('hidden');
          return;
        }
        commitMove(context, chosen, square, 'q');
        return;
      }
    }
    if (piece && piece.color === game.turn()) {
      selected[context] = square;
    } else {
      selected[context] = null;
    }
    renderBoard(context);
  }

  function commitMove(context, from, to, promotion) {
    const game = games[context];
    if (context === 'learn') {
      const expected = lessonMoves[lessonIndex];
      if (!expected || expected.from !== from || expected.to !== to) {
        showToast('Follow the highlighted opening move.');
        return;
      }
    }
    let move;
    try { move = game.move({ from: from, to: to, promotion: promotion || 'q' }); } catch (e) { move = null; }
    if (!move) {
      selected[context] = null;
      renderBoard(context);
      showToast('That move is not legal.');
      return;
    }
    selected[context] = null;

    if (context === 'play') {
      if (!games.play.isGameOver()) startNextClock();
      if (games.play.isGameOver()) {
        const result = games.play.isDraw() ? 'draw' : 'win';
        finishGame(getStatus(games.play), result);
      } else {
        const status = document.getElementById('game-status');
        if (status) status.textContent = getStatus(games.play);
      }
    } else if (context === 'puzzle') {
      if (move.san === 'Qg7#') {
        puzzleSolved = true;
        const feedback = document.getElementById('puzzle-feedback');
        if (feedback) feedback.textContent = 'Solved — Qg7 is checkmate. Nice find.';
        const stats = safeReadStats();
        stats.puzzles += 1;
        saveStats(stats);
      } else {
        games.puzzle.undo();
        selected.puzzle = null;
        const feedback = document.getElementById('puzzle-feedback');
        if (feedback) feedback.textContent = 'Not the solution. Look for a forcing check and try again.';
      }
    } else if (context === 'learn') {
      lessonIndex += 1;
    }
    renderAll();
  }

  function resetPuzzle() {
    games.puzzle = new Chess(PUZZLE_FEN);
    selected.puzzle = null;
    flipped.puzzle = false;
    puzzleSolved = false;
    document.getElementById('puzzle-feedback').textContent = 'Your move, White.';
    renderBoard('puzzle');
  }

  function resetLesson() {
    games.learn = new Chess();
    lessonIndex = 0;
    selected.learn = null;
    flipped.learn = false;
    renderBoard('learn');
    renderLesson();
  }

  function copyText(text, message) {
    if (window.AndroidBridge && typeof window.AndroidBridge.copyText === 'function') {
      window.AndroidBridge.copyText(text);
      showToast(message || 'Copied.');
      return;
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { showToast(message || 'Copied.'); })
        .catch(function () { showToast('Copy is unavailable here.'); });
    } else {
      showToast('Copy is unavailable here.');
    }
  }

  function shareText(text) {
    if (window.AndroidBridge && typeof window.AndroidBridge.shareText === 'function') {
      window.AndroidBridge.shareText(text);
    } else {
      copyText(text, 'Game text copied.');
    }
  }

  function bindEvents() {
    document.querySelectorAll('[data-view]').forEach(function (node) {
      node.addEventListener('click', function () { setView(node.dataset.view); });
    });
    document.querySelectorAll('.chessboard').forEach(function (board) {
      board.addEventListener('click', function (event) {
        const square = event.target.closest('[data-square]');
        if (square) handleSquare(board.dataset.context, square.dataset.square);
      });
    });
    document.querySelectorAll('[data-time]').forEach(function (node) {
      node.addEventListener('click', function () {
        selectedTime = Number(node.dataset.time);
        document.querySelectorAll('[data-time]').forEach(function (option) {
          option.classList.toggle('selected', option === node);
        });
      });
    });
    document.querySelectorAll('[data-promotion]').forEach(function (node) {
      node.addEventListener('click', function () {
        if (!pendingPromotion) return;
        const pending = pendingPromotion;
        pendingPromotion = null;
        document.getElementById('promotion-modal').classList.add('hidden');
        commitMove(pending.context, pending.from, pending.to, node.dataset.promotion);
      });
    });
    document.querySelectorAll('[data-action]').forEach(function (node) {
      node.addEventListener('click', function () { runAction(node.dataset.action); });
    });
  }

  function runAction(action) {
    if (action === 'start-game') return newGame(selectedTime);
    if (action === 'new-game') return newGame();
    if (action === 'open-puzzle') { resetPuzzle(); return setView('puzzles'); }
    if (action === 'open-lesson') { resetLesson(); return setView('learn'); }
    if (action === 'undo') {
      games.play.undo(); stopClock(); selected.play = null;
      if (games.play.history().length && selectedTime > 0) startNextClock();
      document.getElementById('game-status').textContent = getStatus(games.play);
      return renderAll();
    }
    if (action === 'flip') { flipped.play = !flipped.play; return renderBoard('play'); }
    if (action === 'copy-fen') return copyText(games.play.fen(), 'FEN copied.');
    if (action === 'share-pgn') return shareText(games.play.pgn({ maxWidth: 80, newline: '\n' }));
    if (action === 'offer-draw') {
      if (games.play.history().length < 2) return showToast('Play a few moves first.');
      stopClock(); return finishGame('Draw agreed by both local players.', 'draw');
    }
    if (action === 'resign') {
      if (!games.play.history().length) return showToast('There is no game to resign.');
      stopClock();
      const winner = games.play.turn() === 'w' ? 'Black' : 'White';
      return finishGame(winner + ' wins by resignation.', 'win');
    }
    if (action === 'reset-puzzle') return resetPuzzle();
    if (action === 'flip-puzzle') { flipped.puzzle = !flipped.puzzle; return renderBoard('puzzle'); }
    if (action === 'lesson-reset') return resetLesson();
    if (action === 'lesson-back') {
      if (lessonIndex > 0) {
        games.learn.undo(); games.learn.undo(); lessonIndex = Math.max(0, lessonIndex - 2);
        renderBoard('learn'); renderLesson();
      }
      return;
    }
    if (action === 'lesson-next') return showToast('Play the highlighted move on the board.');
    if (action === 'analysis-undo') { games.analysis.undo(); return renderBoard('analysis'); }
    if (action === 'analysis-flip') { flipped.analysis = !flipped.analysis; return renderBoard('analysis'); }
    if (action === 'analysis-copy') return copyText(games.analysis.fen(), 'FEN copied.');
    if (action === 'analysis-reset') {
      games.analysis = new Chess(); document.getElementById('analysis-feedback').textContent = 'Standard starting position.';
      document.getElementById('fen-input').value = ''; return renderBoard('analysis');
    }
    if (action === 'load-fen') {
      const fen = document.getElementById('fen-input').value.trim();
      try {
        const candidate = new Chess();
        candidate.load(fen);
        games.analysis = candidate;
        document.getElementById('analysis-feedback').textContent = 'Position loaded. ' + getStatus(candidate);
        selected.analysis = null;
        renderBoard('analysis');
      } catch (e) {
        document.getElementById('analysis-feedback').textContent = 'Invalid FEN. Check the position and try again.';
      }
    }
    if (action === 'cancel-promotion') {
      pendingPromotion = null;
      document.getElementById('promotion-modal').classList.add('hidden');
    }
  }

  function loadSettings() {
    const theme = localStorage.getItem('cb.theme') || 'classic';
    document.documentElement.dataset.boardTheme = theme;
    const themeSelect = document.getElementById('board-theme');
    const coordinates = document.getElementById('coordinates-toggle');
    const legal = document.getElementById('legal-toggle');
    if (themeSelect) themeSelect.value = theme;
    if (coordinates) coordinates.checked = localStorage.getItem('cb.coords') !== 'false';
    if (legal) legal.checked = localStorage.getItem('cb.legal') !== 'false';
    if (coordinates) coordinates.addEventListener('change', function () {
      localStorage.setItem('cb.coords', String(coordinates.checked));
      renderAll();
    });
    if (legal) legal.addEventListener('change', function () {
      localStorage.setItem('cb.legal', String(legal.checked));
      renderAll();
    });
    if (themeSelect) themeSelect.addEventListener('change', function () {
      document.documentElement.dataset.boardTheme = themeSelect.value;
      localStorage.setItem('cb.theme', themeSelect.value);
    });
  }

  function boot() {
    bindEvents();
    loadSettings();
    document.getElementById('fen-input').value = '';
    renderAll();
    updateClockDisplay();
  }

  document.addEventListener('DOMContentLoaded', boot);
}());
