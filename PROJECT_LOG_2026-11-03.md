# ChessBuddy daily progress — 2026-11-03

## Current target
- Version: v0.4.0
- Source archive: `ChessBuddy-v0.4.0-source.zip` (188,010 bytes, present in repository root).
- Repository: `Mahirabsar2/chessbuddy`
- Build commit: `32b42da7580b0cf8dc03df3dbdf850b3101596c8`

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
- GitHub Actions run #7 / ID `41595023404`: **SUCCESS**.
- Run URL: https://github.com/Mahirabsar2/chessbuddy/actions/runs/41595023404
- `node tests/run-all.js`: **55/55 passed** across coach 9/9, engine 14/14, perft 5/5 positions, prompts 13/13, review 3/3 and strength/models 11/11.
- Stockfish sf_19 compiled successfully for ARM aarch64 using NDK 27.2.12479018; source commit `edb0d9db6731067ec50ce619ff372b463bc4dd5d`.
- Gradle release build succeeded (41 actionable tasks).
- APK verification passed: APK non-empty and ZIP-valid; UI assets packaged; ARM64 Stockfish ELF present; package `com.chessbuddy`, versionCode 1007, versionName 0.4.0; INTERNET permission, arm64-v8a ABI, extractNativeLibs and signature checks passed.
- APK size: 79,716,455 bytes.
- Artifact `ChessBuddy-build-7`: 79,901,351 bytes. It includes the APK, the exact source ZIP used by the workflow, verification/provenance records and `SHA256SUMS.txt`. Expires 2026-11-17 07:16:57 UTC.
- Artifact signing is an ephemeral personal sideload key, not a persistent Play Store/update key.

## Files and versions
- `ChessBuddy-v0.3.0-source.zip`: retained as previous source.
- `ChessBuddy-v0.4.0-source.zip`: current source package.
- `.github/workflows/android-build.yml`: updated to build v0.4.0 and package its exact source ZIP with the APK.
- `PROJECT_STATUS.md`, `PROJECT_LOG.md`, this daily log: updated with verified CI results and remaining work.
- Build artifact: `ChessBuddy-build-7` (download from the Actions run above).

## Blockers / not yet verified
- Browser UI tests were not run.
- No Android device install or interaction testing yet.
- Real OpenAI/Claude network calls and on-device Keystore behaviour remain untested; provider request formatting is covered by logic tests.
- The ephemeral signing key cannot be reused for future app updates. A persistent user-owned signing key must be configured before update releases.
- This is a successful CI build, not yet a device-validated release.

## Exact next steps
1. Download `ChessBuddy-build-7` before 2026-11-17 07:16:57 UTC; retain the APK and matching source ZIP together.
2. Install the arm64 APK on Android and run Settings → Run engine self-test.
3. Test tap/drag selection, legal and illegal drops, captures, castling, en passant, promotion, undo, evaluation layout, human-vs-AI, AI-vs-AI, Coach and Archive.
4. Test real Claude/OpenAI-compatible requests and key storage/error handling on-device.
5. Run the browser UI suite and record the result.
6. Configure a persistent signing key in GitHub Actions before the next update build.
7. Keep every future APK paired with the exact source ZIP used to build it and a SHA-256 manifest.
