# ChessBuddy project log

## 2026-10-28
- Reset project to a fresh Android project named ChessBuddy.
- Initial UI included Play, Coach, History and Settings tabs.
- Added chess.js legal-move rules and a GitHub Actions build workflow.
- The first prototype opponent was not Stockfish.

## 2026-10-31 — v0.3.0
- Rebuilt around a real Stockfish integration: Android NDK build, UCI client and native process bridge.
- Added the chess.com-inspired lobby, board, bot picker, Coach, Archive and Settings.
- Added Stockfish bot strengths, human-vs-AI, AI-vs-AI, model opponents, review and FEN/PGN archive features.
- Added Claude and OpenAI-compatible provider support, position-aware prompts and legal validation of model moves.
- Historical local tests were recorded, but the Android build and device behaviour were not verified at that time.

## 2026-11-02 — independent v0.3.0 review
- Re-ran available logic/perft, Java policy and JavaScript syntax checks; the fast checks passed.
- The deeper perft run timed out in the local review environment. Browser UI, live provider calls, Gradle/NDK build and physical-device tests were not run.
- The repository's v0.3.0 source archive was checked against its GitHub blob.

## 2026-11-03 — v0.4.0 CI build verified
- Added `ChessBuddy-v0.4.0-source.zip` to the repository root (188,010 bytes).
- Updated the Android workflow to fetch v0.4.0, run the logic suite, compile Stockfish for arm64, assemble and verify the APK, and package the exact same source ZIP beside it.
- GitHub Actions run #12 / ID `41648945256`: **SUCCESS**.
- Logic tests: **55/55 passed** — coach 9, engine 14, perft 5 positions, prompts 13, review 3, strength/models 11.
- Stockfish sf_19 compiled for Android arm64 with NDK 27.2.12479018; source commit `edb0d9db6731067ec50ce619ff372b463bc4dd5d`; binary SHA-256 `0470a60d55495faaa56fa4a47a938569abdbeb80cd6b4c12dcc4efc139a11bd6`.
- Gradle release build and APK verification succeeded.
- APK metadata: `com.chessbuddy`, versionCode 1012, versionName 0.4.0, 79,716,447 bytes.
- Artifact `ChessBuddy-build-12` contains the APK, matching v0.4.0 source ZIP, verification/provenance records and SHA-256 manifest. It expires 2026-11-17 13:58:42 UTC.
- Signing is an ephemeral personal sideload key, not a persistent Play Store/update key.

## 2026-11-04 — repository review and daily status
- Confirmed `main` head `d10e0a064b935b651507adae88432ea2a9a6b7e9`. The three commits after the build commit only modify logs/status; app source and workflow are unchanged since build #12.
- Confirmed v0.4.0 source ZIP is present in the repository root (188,010 bytes); v0.3.0 archive is retained. There is no expanded source directory at repository root; CI extracts the ZIP.
- Re-queried run #12 and its jobs: overall conclusion **success** and every job step completed successfully. Re-queried artifact ID `13237225252`, 79,901,351 bytes, not expired at review time, expiry 2026-11-17 13:58:42 UTC.
- Confirmed the same 55/55 logic-test result and APK/Stockfish verification recorded above.
- Corrected `BUILD_ON_GITHUB.md`: it previously described a reusable signing key and Releases download path that do not match the current workflow.
- Remaining gaps: browser UI tests, physical-device tests, real provider calls/Keystore runtime checks, and persistent signing-key support.

## Current requirements
- Fresh Android chess app powered by real Stockfish.
- Play, Coach, Archive/History and Settings tabs; polished Chess.com-inspired board/pieces.
- Human-vs-AI and AI-vs-AI.
- Reliable tap/drag selection and legal move validation, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI-compatible and Anthropic/Claude provider/model settings with native Android Keystore-backed API-key storage.
- Every release must ship the exact matching source ZIP alongside its APK, plus provenance and SHA-256 checksums.

## Exact next steps
1. Download build #12 before its 2026-11-17 13:58:42 UTC expiry; keep the APK and matching source ZIP together.
2. Install the arm64 APK on Android and run Settings → Run engine self-test.
3. Test tap/drag selection, legal/illegal moves, captures, castling, en passant, promotion, undo, evaluation layout, both game modes, Coach and Archive.
4. Run `node tests/ui/ui.test.js` with Playwright/Chromium installed and record the result.
5. Test real Claude/OpenAI-compatible requests, key persistence and error handling on-device.
6. Add persistent user-owned signing-key secret support to the workflow before building update releases.
7. Build each future version from a versioned source ZIP and package that exact ZIP with the APK and SHA-256 manifest.


## 2026-11-05 — repository review and daily status
- Reviewed app-source baseline `9e9391fff4855c70be48b46ec06750ea7e0dbb40`. Compare against build #12 commit `26625d6d80f521db15b21e749a6cca5881fd1cf9` shows seven later commits, all documentation/log changes; no app source or workflow changes.
- Confirmed `ChessBuddy-v0.4.0-source.zip` remains present in the repository root (188,010 bytes); expanded app source is not checked into the root and CI extracts the ZIP.
- Inspected build #12 job metadata and actual job logs: 55/55 logic tests passed; Stockfish sf_19 arm64 build succeeded; Gradle release build succeeded; APK verification and artifact upload succeeded.
- Confirmed artifact `ChessBuddy-build-12` (ID `13237225252`, 79,901,351 bytes) remains available and expires 2026-11-17 13:58:42 UTC.
- Updated `PROJECT_LOG_2026-11-05.md`, `PROJECT_STATUS.md`, and README build instructions. No new app source, APK, source archive or tests were produced/run today.
- Remaining gaps: browser UI suite, physical-device tests, live provider/Keystore runtime checks, and persistent signing-key support.
