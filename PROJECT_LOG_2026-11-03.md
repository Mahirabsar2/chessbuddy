# ChessBuddy daily progress — 2026-11-03

## Current target
- Version: v0.4.0
- Source archive: `ChessBuddy-v0.4.0-source.zip` (188,010 bytes, present in repository root).
- Repository: `Mahirabsar2/chessbuddy`
- Latest workflow commit: `26625d6d80f521db15b21e749a6cca5881fd1cf9`

## Requirements retained
- Fresh Android chess app using real Stockfish.
- Play, Coach, Archive/History and Settings tabs; Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Reliable tap/drag selection and legal move validation, captures, promotion and undo.
- OpenAI-compatible/GPT and Anthropic/Claude provider/API-key settings; README documents Android Keystore-encrypted key storage.
- Every release must ship the exact matching source ZIP alongside its APK, with verification/provenance and SHA-256 checksums.

## v0.4.0 source work
- Fixed capture-target styling collision and separated capture rings/legal-move dots from piece artwork.
- Adjusted evaluation bar and score-label sizing for narrow screens.
- Added drag ghost and move-arrival animation.
- Added seven Stockfish style presets inspired by Capablanca, Tal, Polgar, Fischer, Nakamura, Kasparov and Carlsen; these are not official Chess.com bots.
- Removed the committed sideload keystore and set versionName to 0.4.0.

## Build and tests verified
- Latest GitHub Actions run #12 / ID `41648945256`: **SUCCESS**.
- Run URL: https://github.com/Mahirabsar2/chessbuddy/actions/runs/41648945256
- `node tests/run-all.js`: **55/55 passed** across coach 9/9, engine 14/14, perft 5/5 positions, prompts 13/13, review 3/3 and strength/models 11/11.
- Stockfish sf_19 compiled for ARM aarch64 using NDK 27.2.12479018; source commit `edb0d9db6731067ec50ce619ff372b463bc4dd5d`; binary SHA-256 `0470a60d55495faaa56fa4a47a938569abdbeb80cd6b4c12dcc4efc139a11bd6`.
- Gradle release build succeeded.
- APK verification passed: APK non-empty and ZIP-valid; UI assets packaged; ARM64 Stockfish ELF present; package `com.chessbuddy`, versionCode 1012, versionName 0.4.0; INTERNET permission, arm64-v8a ABI, extractNativeLibs and signature checks passed.
- APK size: 79,716,447 bytes.
- Artifact `ChessBuddy-build-12`: 79,901,351 bytes. It includes the APK, the exact source ZIP used by the workflow, verification/provenance records and `SHA256SUMS.txt`. Expires 2026-11-17 13:58:42 UTC.
- Workflow now skips documentation-only pushes and masks its generated ephemeral signing password. Build #12 logs confirm masking.

## Files and versions
- `ChessBuddy-v0.3.0-source.zip`: retained as previous source.
- `ChessBuddy-v0.4.0-source.zip`: current source package.
- `.github/workflows/android-build.yml`: builds v0.4.0, runs tests, compiles Stockfish, verifies APK and packages the matching source ZIP.
- `PROJECT_STATUS.md`, `PROJECT_LOG.md`, this daily log: current build results and next steps.
- Build artifact: `ChessBuddy-build-12` (download from the Actions run above).

## Blockers / not yet verified
- Browser UI tests were not run.
- No Android device install or interaction testing yet.
- Real OpenAI/Claude network calls and on-device Keystore behaviour remain untested; provider request formatting is covered by logic tests only.
- The ephemeral signing key cannot be reused for future app updates. A persistent user-owned signing key must be configured before update releases.
- This is a successful CI build, not yet a device-validated release.

## Exact next steps
1. Download `ChessBuddy-build-12` before 2026-11-17 13:58:42 UTC; retain the APK and matching source ZIP together.
2. Install the arm64 APK on Android and run Settings → Run engine self-test.
3. Test tap/drag selection, legal and illegal drops, captures, castling, en passant, promotion, undo, evaluation layout, human-vs-AI, AI-vs-AI, Coach and Archive.
4. Test real Claude/OpenAI-compatible requests and key storage/error handling on-device.
5. Run the browser UI suite and record the result.
6. Configure a persistent signing key in GitHub Actions before the next update build.
7. Keep every future APK paired with the exact source ZIP used to build it and a SHA-256 manifest.
