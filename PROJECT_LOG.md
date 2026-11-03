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
- Re-ran the available logic/perft, Java policy and JavaScript syntax checks; the fast checks passed.
- The deeper perft run timed out in the local review environment. Browser UI, live provider calls, Gradle/NDK build and physical-device tests were not run.
- The repository's v0.3.0 source archive was checked against its GitHub blob.

## 2026-11-03 — v0.4.0 CI build verified
- Added `ChessBuddy-v0.4.0-source.zip` to the repository root (188,010 bytes).
- Updated `.github/workflows/android-build.yml` to fetch v0.4.0, run the logic suite, compile Stockfish for arm64, assemble and verify the release APK, and package the exact same source ZIP with the APK.
- Commit: `32b42da7580b0cf8dc03df3dbdf850b3101596c8`.
- GitHub Actions run #7 / ID `41595023404`: **SUCCESS**. Run: https://github.com/Mahirabsar2/chessbuddy/actions/runs/41595023404
- CI logic tests: **55/55 passed** — coach 9, engine 14, perft 5 positions, prompts 13, review 3, strength/models 11.
- Stockfish sf_19 compiled for Android arm64 with NDK 27.2.12479018; source commit `edb0d9db6731067ec50ce619ff372b463bc4dd5d`.
- Gradle release build succeeded (41 actionable tasks). APK verification passed for ZIP integrity, packaged web assets, ARM aarch64 Stockfish, package/version/ABI/permissions, extractNativeLibs and signature.
- Artifact `ChessBuddy-build-7` uploaded successfully (79,901,351 bytes). It contains the arm64 APK, the matching v0.4.0 source ZIP, verification/provenance records and SHA-256 manifest. It expires 2026-11-17 07:16:57 UTC.
- APK metadata: `com.chessbuddy`, versionCode 1007, versionName 0.4.0, 79,716,455 bytes.
- Signing uses an ephemeral personal sideload key. This build is not Play Store signed and cannot serve as the signing identity for future updates.

### Remaining verification
- Browser UI suite not run.
- No physical-device installation or interaction tests yet.
- Real OpenAI/Claude requests and on-device Keystore behaviour not tested; only provider request logic tests passed.
- The CI build is verified, but the app is not yet device-validated.

### Exact next steps
1. Download the build-7 artifact before expiry and retain the APK with its matching source ZIP.
2. Install on Android; run the Stockfish self-test.
3. Test tap/drag selection, legal/illegal moves, captures, castling, en passant, promotion, undo, evaluation layout, both game modes, Coach and Archive.
4. Test real Claude and OpenAI-compatible requests and on-device key storage/error handling.
5. Run the separate browser UI tests and record results.
6. Configure a persistent user-owned signing key in GitHub Actions before building update releases.
7. Keep packaging the exact source ZIP used for each build beside its APK, with provenance and SHA-256 checksums.
