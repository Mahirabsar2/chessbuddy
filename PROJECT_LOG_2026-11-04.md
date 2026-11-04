# ChessBuddy daily progress — 2026-11-04

## Current state
- Repository: `Mahirabsar2/chessbuddy`, branch `main`.
- Latest repository head: `d10e0a064b935b651507adae88432ea2a9a6b7e9`. The three commits after the verified build changed only project logs/status, not app source.
- Current app/source version: **v0.4.0**.
- Latest source archive: `ChessBuddy-v0.4.0-source.zip`, **188,010 bytes**, present at the repository root. Previous `v0.3.0` archive is also retained.
- There is no expanded `ChessBuddy/` source directory at the repository root; the workflow extracts the v0.4.0 ZIP into its CI workspace. The archive itself is available.

## Requirements retained
- Fresh Android chess app powered by real Stockfish.
- Play, Coach, Archive/History and Settings tabs; polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Fix tap/drag piece selection and legal-move handling; support captures, castling, en passant, promotion and undo.
- GPT/OpenAI-compatible and Anthropic/Claude model/provider settings, with API keys handled natively through Android Keystore-backed storage.
- Every release must package the **exact source ZIP used for that APK** beside the APK, plus build provenance and SHA-256 checksums.

## Files and versions
- `ChessBuddy-v0.3.0-source.zip`: previous source archive.
- `ChessBuddy-v0.4.0-source.zip`: current source archive (188,010 bytes).
- `.github/workflows/android-build.yml`: pins the v0.4.0 archive, runs logic tests, compiles Stockfish arm64, builds/verifies the APK and packages the matching ZIP.
- `PROJECT_STATUS.md`, `PROJECT_LOG.md`, and this daily log: project status and history.
- `BUILD_ON_GITHUB.md`: corrected today to match the actual workflow and signing behaviour.

## Latest verified build
- GitHub Actions **run #12**, ID `41648945256`, build commit `26625d6d80f521db15b21e749a6cca5881fd1cf9`: **SUCCESS**. Every build job step completed successfully.
- Run: https://github.com/Mahirabsar2/chessbuddy/actions/runs/41648945256
- `node tests/run-all.js`: **55/55 passed** — coach 9, engine 14, perft 5 positions, prompts 13, review 3, strength/models 11.
- Stockfish sf_19 compiled for Android arm64 with NDK 27.2.12479018. Source commit: `edb0d9db6731067ec50ce619ff372b463bc4dd5d`; embedded binary SHA-256: `0470a60d55495faaa56fa4a47a938569abdbeb80cd6b4c12dcc4efc139a11bd6`.
- Gradle release APK build succeeded. APK verification passed for ZIP integrity, bundled UI assets, ARM64 Stockfish ELF, package/version/ABI/INTERNET permission, extractNativeLibs and signature.
- APK: `com.chessbuddy`, versionCode `1012`, versionName `0.4.0`, **79,716,447 bytes**.
- Artifact `ChessBuddy-build-12`, artifact ID `13237225252`, **79,901,351 bytes**. It contains the APK, the exact v0.4.0 source ZIP used by CI, verification/provenance records and `SHA256SUMS.txt`.
- Artifact expires **2026-11-17 13:58:42 UTC**. Download it before expiry.

## v0.4.0 changes recorded
- Capture rings/legal-move dots separated from piece artwork to avoid visual overlap.
- Evaluation bar and score labels resized for narrow screens.
- Drag ghost and move-arrival animation added.
- Seven Stockfish style presets inspired by Capablanca, Tal, Polgar, Fischer, Nakamura, Kasparov and Carlsen. These are not official Chess.com bots.
- App versionName set to 0.4.0; committed sideload keystore removed.

## Blockers / not yet verified
- No physical Android installation or device interaction test.
- Browser UI suite has not been run.
- Real Claude/OpenAI-compatible network calls and Android Keystore key storage/error handling have not been tested on-device; provider request formatting has logic-test coverage only.
- The workflow currently creates a **new ephemeral sideload signing key on every run**. Persistent user-owned signing-key secrets are not wired into the workflow yet, so later APKs cannot be assumed to update-install over this build.
- Build #12 is CI-verified, not device-validated.

## Exact next steps
1. Download `ChessBuddy-build-12` from the run link above before **2026-11-17 13:58:42 UTC**; keep its APK and matching source ZIP together.
2. Install the arm64 APK on an Android phone and run Settings → Run engine self-test.
3. Manually test tap/drag selection, legal and illegal drops, captures, castling, en passant, promotion, undo, evaluation layout, human-vs-AI, AI-vs-AI, Coach and Archive.
4. Run `node tests/ui/ui.test.js` in an environment with Playwright/Chromium installed and record the actual result.
5. Test real Claude and OpenAI-compatible requests, API-key save/reload, and error handling on-device.
6. Add support for persistent `CB_KEYSTORE_BASE64`, `CB_KEYSTORE_PASSWORD`, `CB_KEY_ALIAS` and `CB_KEY_PASSWORD` GitHub Actions secrets; configure a user-owned key before distributing update builds.
7. For each future release, update the workflow's pinned source ZIP and version check, then package that exact ZIP with the APK and a SHA-256 manifest. Never mark a build device-validated until device tests pass.
