# ChessBuddy project log

## 2026-10-28
- Reset project to a fresh Android project named ChessBuddy.
- Current UI includes Play, Coach, History, and Settings tabs.
- Bundled chess.js legal-move rules; basic opponent is not Stockfish.
- Added GitHub Actions workflow to build a debug APK in a hosted Android/Gradle environment and upload APK + exact matching source ZIP + checksums.
- Local APK build is still unavailable because this execution environment has no Android SDK/Gradle installation.
- Next: push this source ZIP to a GitHub repository and run the workflow; then integrate a verified Stockfish build and test on-device.

## 2026-10-31 — v0.3.0 (Claude)
- Rebuilt on the supplied scaffold: replaced the random-move prototype with a real Stockfish integration (NDK build in CI, UCI client, process bridge).
- chess.com-style UI (lobby, bot picker, game screen, Coach, Archive, Settings). AI models shown by real model names.
- AI-model opponents and coach with full position reports, move explanations and board screenshots; strict legal-move validation (fixes the "illegal move at game start" class of bug).
- Strength: Stockfish limiter >= 1320 Elo, handicap mode below.
- Verified in the sandbox: 55 logic tests, 26 UI tests (mock bridge), Java compile against stubs, URL-policy JVM test. NOT verified: Gradle/NDK build, APK, on-device behaviour (sandbox has no network/SDK).
