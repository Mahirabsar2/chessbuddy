# ChessBuddy v0.4.0 — project status (2026-11-03)

## Latest verified build
- Source: `ChessBuddy-v0.4.0-source.zip` (188,010 bytes), present in repository root.
- Build commit: `26625d6d80f521db15b21e749a6cca5881fd1cf9`.
- GitHub Actions run #12: **SUCCESS** — https://github.com/Mahirabsar2/chessbuddy/actions/runs/41648945256
- Artifact: `ChessBuddy-build-12` (79,901,351 bytes). It includes the arm64 APK, the exact source ZIP used by the build, verification/provenance files and `SHA256SUMS.txt`.
- Artifact expires 2026-11-17 13:58:42 UTC. Download before expiry.
- APK: `com.chessbuddy`, versionCode `1012`, versionName `0.4.0`, arm64-v8a, 79,716,447 bytes.

## Product requirements and source capabilities
- Fresh Android chess app built around real Stockfish, not random/fake engine moves.
- Play, Coach, Archive/History and Settings areas with a Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI modes.
- Tap selection and drag/drop, legal-move validation, captures, promotion, undo, board flip, hints and evaluation display.
- OpenAI-compatible/GPT and Anthropic/Claude model/provider settings. README documents Android Keystore-encrypted API-key storage.
- Every release must include the exact matching source ZIP beside the APK, plus verification/provenance and checksums.

## v0.4.0 changes
- Separated capture rings and legal-move dots from piece artwork to avoid overlay collisions.
- Resized evaluation bar and score labels for narrow screens.
- Added drag ghost and move-arrival animation alongside drag/drop.
- Added seven Stockfish style presets inspired by Capablanca, Tal, Polgar, Fischer, Nakamura, Kasparov and Carlsen. They are not official Chess.com bots.
- Removed the committed sideload keystore from the source package.
- Set app versionName to 0.4.0.

## Verified by GitHub Actions run #12
- `node tests/run-all.js`: **55/55 logic tests passed** across six suites: coach 9/9, engine 14/14, perft 5/5 positions, prompts 13/13, review 3/3, strength/models 11/11.
- Stockfish sf_19 compiled for Android arm64 with NDK 27.2.12479018. Source commit: `edb0d9db6731067ec50ce619ff372b463bc4dd5d`. Embedded binary SHA-256: `0470a60d55495faaa56fa4a47a938569abdbeb80cd6b4c12dcc4efc139a11bd6`.
- Gradle release build: **BUILD SUCCESSFUL**.
- APK verification passed: non-empty APK, ZIP integrity, packaged web assets, ARM aarch64 Stockfish binary, package/version/ABI/INTERNET permission, extractNativeLibs and APK signature.
- Workflow copied the same `ChessBuddy-v0.4.0-source.zip` used for the build into the artifact and generated `SHA256SUMS.txt`.
- CI now masks the generated ephemeral signing password; run #12 logs show it masked. Documentation-only pushes are excluded from Android builds.

## Not yet verified / blockers
- Playwright/browser UI tests were not run.
- No physical Android installation or device interaction test has been performed.
- Real OpenAI/Claude network calls and on-device API-key/Keystore behaviour have not been tested. Provider request formatting has logic-test coverage only.
- APK uses a newly generated ephemeral personal sideload key. It is not a Play Store signing key and cannot sign future updates with the same identity. Configure a persistent user-owned signing key before distributing update builds.
- The CI build is verified, but device validation is still outstanding.

## Exact next steps
1. Download `ChessBuddy-build-12` before its 2026-11-17 expiry; keep the APK and matching source ZIP together.
2. Install the arm64 APK on Android and run Settings → Run engine self-test.
3. Test tap/drag selection, legal and illegal drops, captures, castling, en passant, promotion, undo, evaluation layout, human-vs-AI, AI-vs-AI, Coach and Archive.
4. Test Claude and OpenAI-compatible providers with valid keys entered in the app; verify success and error handling on-device.
5. Run the separate browser UI suite and record its actual result.
6. Before the next update build, configure a persistent user-owned signing key in GitHub Actions secrets and update the workflow to reuse it securely.
7. For every later release, build from a versioned source ZIP and package that exact ZIP with the APK and SHA-256 manifest. Do not call a build device-validated until the device checks pass.
