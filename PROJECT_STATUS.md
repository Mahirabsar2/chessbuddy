# ChessBuddy v0.4.0 — project status (2026-11-03)

## Current build
- Source: `ChessBuddy-v0.4.0-source.zip` (188,010 bytes), present in the repository root.
- Repository commit used by CI: `32b42da7580b0cf8dc03df3dbdf850b3101596c8`.
- GitHub Actions run #7: **SUCCESS** — https://github.com/Mahirabsar2/chessbuddy/actions/runs/41595023404
- Artifact: `ChessBuddy-build-7` (79,901,351 bytes), containing the arm64 APK, the exact v0.4.0 source ZIP copied into the release package, verification/provenance files, and SHA-256 manifest.
- Artifact expiry: 2026-11-17 07:16:57 UTC. Download before it expires.
- APK: package `com.chessbuddy`, versionCode `1007`, versionName `0.4.0`, 79,716,455 bytes, arm64-v8a.

## Product requirements and source capabilities
- Fresh Android chess app built around real Stockfish, not random/fake engine moves.
- Play, Coach, Archive/History and Settings areas with a Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI modes.
- Tap selection and drag/drop, legal-move validation, captures, promotion, undo, board flip, hints and evaluation display.
- OpenAI-compatible/GPT and Anthropic/Claude model/provider settings. README documents Android Keystore-encrypted API-key storage.
- Every release artifact must include the exact matching source ZIP beside the APK, plus verification/provenance and checksums.

## v0.4.0 changes
- Separated capture rings and legal-move dots from piece artwork to avoid overlay collisions.
- Resized evaluation bar and score labels for narrow screens.
- Added drag ghost and move-arrival animation alongside drag/drop.
- Added seven Stockfish style presets inspired by Capablanca, Tal, Polgar, Fischer, Nakamura, Kasparov and Carlsen. They are not official Chess.com bots.
- Removed the committed sideload keystore from the source package.
- Set app versionName to 0.4.0.

## Verified by GitHub Actions on 2026-11-03
- `node tests/run-all.js`: **55/55 logic tests passed** across six suites: coach 9/9, engine 14/14, perft 5/5 positions, prompts 13/13, review 3/3, strength/models 11/11.
- Stockfish sf_19 compiled successfully for Android arm64 using NDK 27.2.12479018. Source commit: `edb0d9db6731067ec50ce619ff372b463bc4dd5d`. The embedded ARM aarch64 ELF includes the NNUE network.
- Gradle release build: **BUILD SUCCESSFUL**, 41 actionable tasks.
- APK verification passed: non-empty APK, ZIP integrity, web assets, arm64 Stockfish binary, package/version/ABI/INTERNET permission, extractNativeLibs, and APK signature verification.
- Release packaging and artifact upload both completed successfully. Workflow copies the same `ChessBuddy-v0.4.0-source.zip` used for the build into the artifact and creates `SHA256SUMS.txt`.

## Not yet verified / blockers
- Playwright/browser UI tests were not run in this workflow.
- No physical Android installation or device interaction test has been performed.
- Real OpenAI/Claude network calls and on-device API-key/Keystore behaviour have not been tested. Provider request formatting has logic-test coverage only.
- The APK uses a newly generated ephemeral personal sideload key. It is not a Play Store signing key and cannot sign future updates with the same identity. Configure a persistent user-owned signing key before distributing update builds.
- The successful CI build is ready for sideload testing, but device validation is still outstanding.

## Exact next steps
1. Download `ChessBuddy-build-7` before its 2026-11-17 expiry; keep the APK and matching source ZIP together.
2. Install the arm64 APK on an Android device and run Settings → Run engine self-test.
3. Test tap/drag selection, legal and illegal drops, captures, castling, en passant, promotion, undo, evaluation layout, human-vs-AI, AI-vs-AI, Coach and Archive.
4. Test Claude and OpenAI-compatible providers with valid keys entered in the app; verify success and error handling on-device.
5. Run the separate browser UI suite and record its actual result.
6. Before the next update build, configure a persistent signing key in GitHub Actions secrets and update the workflow to reuse it securely.
7. For every later release, build from a versioned source ZIP and package that exact ZIP with the APK and SHA-256 manifest. Do not call a build device-validated until the device checks pass.
