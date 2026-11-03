# ChessBuddy daily progress — 2026-11-03

## Target release
- Source package: ChessBuddy v0.4.0
- Local archive: `ChessBuddy-v0.4.0-source.zip`
- Repository: `Mahirabsar2/chessbuddy`
- Base repository commit reviewed: `28e7e8ec7a7aa2ddd9cbf89bb1b7bd7744be2ae5`

## Requirements retained
- Fresh Android chess app using real Stockfish.
- Play, Coach, Archive and Settings tabs; polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Correct tap selection, drag-and-drop, legal move validation, captures, promotion and undo.
- GPT/OpenAI-compatible and Claude settings; API keys stored in Android Keystore.
- Every release must include the exact matching source ZIP beside the APK, plus verification details and checksums.

## v0.4.0 source changes
- Fixed capture-target styling collision that distorted board-square overlays.
- Separated capture rings and legal-move dots from piece artwork.
- Adjusted evaluation bar and score-label sizing for narrow screens.
- Added touch/mouse drag-and-drop, floating drag ghost and move-arrival animation.
- Added seven Stockfish style presets named for Capablanca, Tal, Polgar, Fischer, Nakamura, Kasparov and Carlsen. These are inspired presets, not official Chess.com bots or reproductions.
- Removed committed sideload keystore; CI uses configured signing secrets or an ephemeral personal-build key.
- Set app versionName to 0.4.0.
- CI perft suite uses depth 1–2 because the previous deeper suite timed out.

## Tests run against the recovered local v0.4.0 archive
- `node tests/run-all.js`: PASS, 55 tests across six suites; perft 5/5 standard positions.
- Java policy test: PASS (from the archive's test script on the prior local verification record; not rerun in this GitHub operation).
- JavaScript syntax checks: recorded as PASS in the archive's status file; not rerun in this GitHub operation.
- UI browser tests: NOT RUN.
- Android Gradle/NDK build, APK verification, live provider calls and physical-device tests: NOT RUN.

## GitHub operation
- Confirmed the target repository is `Mahirabsar2/chessbuddy`, default branch `main`.
- Reviewed current README, PROJECT_STATUS, PROJECT_LOG and Android Actions workflow.
- The current repository workflow still downloads the v0.3.0 source archive. It must be changed to consume v0.4.0 before a v0.4.0 APK build can be considered.
- The connected GitHub actions available in this session support text-file and Git-object writes, but do not expose a binary file upload action for the 188 KB ZIP. Therefore the v0.4.0 source archive and app code have NOT been pushed in this operation.
- No GitHub Actions run was triggered, because the existing workflow would build v0.3.0, not v0.4.0.

## Exact next steps
1. Upload `ChessBuddy-v0.4.0-source.zip` to the repository root (or push its extracted source tree).
2. Update `.github/workflows/android-build.yml` so it builds v0.4.0, runs the 55-test suite, compiles Stockfish for arm64, builds and verifies the APK, and packages the exact same source ZIP.
3. Run the workflow and inspect its actual logs and artifacts.
4. Verify APK signature, embedded arm64 Stockfish binary, source-commit identity and SHA-256 checksums.
5. Install on Android and test drag/tap selection, captures, legal/illegal drops, promotion, undo, evaluation layout, both game modes, bot presets, and real OpenAI/Claude requests.
6. Only call v0.4.0 a release after those checks pass.
