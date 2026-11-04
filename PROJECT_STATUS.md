# ChessBuddy v0.4.0 — project status (reviewed 2026-11-04)

## Latest verified build
- Repository: `Mahirabsar2/chessbuddy`, branch `main`.
- Latest repository head: `d10e0a064b935b651507adae88432ea2a9a6b7e9`. Commits after the build changed documentation/logs only.
- Source: `ChessBuddy-v0.4.0-source.zip` (188,010 bytes), present in repository root. The previous v0.3.0 ZIP is retained. The expanded app source directory is not checked into the root; CI extracts the ZIP.
- Build commit: `26625d6d80f521db15b21e749a6cca5881fd1cf9`.
- GitHub Actions run #12: **SUCCESS** — https://github.com/Mahirabsar2/chessbuddy/actions/runs/41648945256
- Artifact: `ChessBuddy-build-12` (79,901,351 bytes; artifact ID `13237225252`). Contains arm64 APK, exact source ZIP used by CI, verification/provenance files and `SHA256SUMS.txt`.
- Artifact expires **2026-11-17 13:58:42 UTC**.
- APK: `com.chessbuddy`, versionCode `1012`, versionName `0.4.0`, arm64-v8a, 79,716,447 bytes.

## Product requirements and current source capabilities
- Fresh Android chess app built around real Stockfish, not simulated engine moves.
- Play, Coach, Archive/History and Settings areas with a Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI modes.
- Tap selection and drag/drop, legal-move validation, captures, promotion, undo, board flip, hints and evaluation display.
- OpenAI-compatible/GPT and Anthropic/Claude model/provider settings. README documents Android Keystore-encrypted API-key storage; runtime behaviour still needs device testing.
- Every release must include the exact matching source ZIP beside its APK, plus provenance and SHA-256 checksums.

## v0.4.0 changes
- Separated capture rings/legal-move dots from piece artwork to avoid overlay collisions.
- Resized evaluation bar and score labels for narrow screens.
- Added drag ghost and move-arrival animation.
- Added seven Stockfish style presets inspired by Capablanca, Tal, Polgar, Fischer, Nakamura, Kasparov and Carlsen; these are not official Chess.com bots.
- Removed the committed sideload keystore and set versionName to 0.4.0.

## Verified by GitHub Actions run #12
- `node tests/run-all.js`: **55/55 logic tests passed** — coach 9/9, engine 14/14, perft 5/5 positions, prompts 13/13, review 3/3, strength/models 11/11.
- Stockfish sf_19 compiled for Android arm64 with NDK 27.2.12479018. Source commit: `edb0d9db6731067ec50ce619ff372b463bc4dd5d`. Embedded binary SHA-256: `0470a60d55495faaa56fa4a47a938569abdbeb80cd6b4c12dcc4efc139a11bd6`.
- Gradle release build succeeded.
- APK verification passed: APK integrity, bundled web assets, ARM64 Stockfish binary, package/version/ABI/INTERNET permission, extractNativeLibs and signature.
- Workflow packaged the exact `ChessBuddy-v0.4.0-source.zip` used for the build and generated `SHA256SUMS.txt`.

## Not yet verified / blockers
- Browser UI tests (`node tests/ui/ui.test.js`) have not been run.
- No physical Android installation or device interaction test has been performed.
- Real Claude/OpenAI-compatible network calls and on-device Android Keystore key storage/error handling have not been tested. Provider request formatting has logic-test coverage only.
- Workflow currently generates a new ephemeral sideload key on every run. Persistent user-owned signing-key secrets are not yet supported by the workflow, so do not assume future APKs can update-install over this one.
- This is a successful CI build, not a device-validated release.

## Exact next steps
1. Download `ChessBuddy-build-12` before its 2026-11-17 expiry; keep the APK and matching source ZIP together.
2. Install the arm64 APK on Android and run Settings → Run engine self-test.
3. Test tap/drag selection, legal and illegal drops, captures, castling, en passant, promotion, undo, evaluation layout, human-vs-AI, AI-vs-AI, Coach and Archive.
4. Run the browser UI suite with Playwright/Chromium installed and record its actual result.
5. Test Claude and OpenAI-compatible providers with valid keys; verify key save/reload and error handling on-device.
6. Add persistent signing-key secret support and configure a user-owned key before update builds.
7. For every later release, build from a versioned source ZIP and package that exact ZIP with the APK and SHA-256 manifest. Do not call a build device-validated until device checks pass.
