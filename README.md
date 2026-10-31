# ChessBuddy

A modern Android chess app with a chess.com-style interface, a **real Stockfish** engine, and AI models
(Claude and any OpenAI-compatible service) that can coach you or play against you.

**Status: source ready, APK is built by GitHub Actions.** See `PROJECT_STATUS.md` for exactly what is verified.

## Features
- **Play**: lobby, Stockfish bots (Elo 400 – full strength) grouped Beginner / Intermediate / Advanced / Master, a custom-Elo slider, AI-model opponents, AI vs AI (bot or model on each side), pass-and-play.
- **Board**: legal-move validation (chess.js, perft-verified), selected-square / legal-move / capture / check / last-move highlights, promotion picker, undo, flip, hint, move strip, captured pieces, evaluation bar, three board colour themes.
- **Export**: FEN and PGN (with headers) – copy or share. Load a FEN or PGN from the Archive tab.
- **Coach**: Stockfish analysis (3 lines), a full-game review (every move classified Best … Blunder, accuracy %), and a chat with your chosen AI model.
- **AI models by name**: models appear as *Claude Sonnet 5.5*, *Claude Haiku 5.5*, … everywhere (never "API A / API B"). Add any model in Settings → AI models.
- **Archive**: finished and abandoned games, replay with ◀ ▶, share PGN.

## What the AI models receive
Every coach question and every AI-model move gets a complete, machine-generated description of the position:
text board, FEN, every piece, **every move played explained** ("1. e4 — White pawn e2→e4", captures, castling, checks…),
computed tactical facts (pieces under attack / undefended, checks, pawn structure, castling status, material), the full list of legal moves,
Stockfish lines (ground truth), and a **PNG screenshot of the board** (vision models). Models that reject images are detected and sent text only.
AI-model opponents must answer `MOVE: <san>`; replies are parsed leniently (SAN, UCI, castling variants, prose) but **always validated against the legal-move list**;
an illegal reply is sent back with the reason (3 tries). If it still fails you choose: try again, let Stockfish move, or resign for it.

## Stockfish
Not simulated. The GitHub workflow compiles the **official Stockfish source** (pinned tag, see `scripts/build_stockfish_android.sh`) with the Android NDK
(`make net && make build ARCH=armv8 COMP=ndk`, as documented on the Stockfish wiki), embeds the NNUE network, and ships it as `libstockfish.so`.
The app runs it as a child process and speaks UCI (`app/.../EngineProcess.java`, `assets/js/engine.js`). If the engine cannot start, the app says so; it never plays fake moves.
Settings → *Run engine self-test* runs a real depth-12 search on your phone and shows the engine name, nodes/s and best move.

### Strength
- Elo ≥ 1320: Stockfish's own limiter (`UCI_LimitStrength` + `UCI_Elo`).
- Elo < 1320 (and engines without the limiter): Stockfish searches with a small node budget and the move is picked from its MultiPV lines with Elo-dependent randomness (`assets/js/strength.js`).
- "Stockfish" bot = full strength. Elo values are approximate.

## Security & privacy
- API keys live in Android Keystore-encrypted storage (`SecretStore.java`) and are added to requests **natively**; JavaScript never sees them.
- One key per provider account, shared by all its models. Redirects are never followed (the key cannot leak). Plain `http://` is allowed only for local servers (`HostPolicy.java`).
- The WebView only loads bundled assets, with a strict Content-Security-Policy; the native bridge is exposed to nothing else.
- Nothing is sent anywhere until you ask the coach or play an AI-model opponent.

## Build
See `BUILD_ON_GITHUB.md`. Short version: put this folder in a GitHub repository, open **Actions → Build ChessBuddy APK → Run workflow**, download the APK from the run (or the Releases page).

## Layout
```
app/src/main/java/com/chessbuddy   MainActivity, NativeBridge, EngineProcess, HttpTransport, HostPolicy, SecretStore, Json
app/src/main/assets                index.html, css/app.css, js/*.js (UI, UCI client, prompts, strength, review, board, snapshot)
scripts/                           build_stockfish_android.sh, verify_apk.sh
.github/workflows/android-build.yml
tests/                             logic tests (node), UI tests (Playwright + test-only mock bridge), Java stub compile + JVM checks
```

## Tests (not part of the APK)
`node tests/run-all.js` – rules (perft), UCI client, provider requests, prompts + move parser, review, strength.
`node tests/ui/ui.test.js` – UI flows in headless Chromium with a **test-only** mock of the Android bridge (needs Playwright).

## Licence
ChessBuddy bundles Stockfish (GPL-3.0-or-later), so a distributed APK must be offered with its source under the GPL. See `NOTICE.md`.
