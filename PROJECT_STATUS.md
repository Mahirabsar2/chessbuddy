# ChessBuddy v0.4.0 — project status (reviewed 2026-11-05)

## Current requirements
- Fresh Android chess app powered by real Stockfish.
- Play, Coach, Archive/History and Settings tabs; polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Reliable tap/drag selection and legal move handling, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI-compatible and Anthropic/Claude provider/model settings. API keys should remain in native Android Keystore-backed storage, not JavaScript.
- Every release must include the **exact source ZIP used for its APK**, plus provenance and SHA-256 checksums.

## Source and repository state
- Repository: `Mahirabsar2/chessbuddy`, branch `main`.
- App-source baseline reviewed: `9e9391fff4855c70be48b46ec06750ea7e0dbb40`. The seven commits after build #12 changed documentation/logs only; no app source or workflow changes.
- Current app/source version: **v0.4.0**.
- `ChessBuddy-v0.4.0-source.zip`: present at repository root, **188,010 bytes**. Previous `v0.3.0` archive is retained.
- The expanded `ChessBuddy/` app source directory is not checked into the repository root; CI extracts the versioned ZIP. The archive is present, so the source is not missing, but direct file-level review requires extracting it.
- Workflow: `.github/workflows/android-build.yml`, still pinned to the v0.4.0 ZIP and versionName 0.4.0.

## Latest verified build
- GitHub Actions **run #12**, ID `41648945256`, build commit `26625d6d80f521db15b21e749a6cca5881fd1cf9`: **SUCCESS**; all job steps completed successfully.
- Actual job log confirms `node tests/run-all.js`: **55/55 passed** — coach 9/9, engine 14/14, perft 5/5, prompts 13/13, review 3/3, strength/models 11/11.
- Stockfish **sf_19** compiled for Android arm64 with NDK `27.2.12479018`; source commit `edb0d9db6731067ec50ce619ff372b463bc4dd5d`.
- Gradle `assembleRelease` succeeded and `scripts/verify_apk.sh` completed successfully.
- APK: package `com.chessbuddy`, versionCode `1012`, versionName `0.4.0`, arm64-v8a, **79,716,447 bytes**.
- Artifact `ChessBuddy-build-12`, ID `13237225252`, **79,901,351 bytes**. It contains the APK, exact matching source ZIP, provenance/verification records and `SHA256SUMS.txt`.
- Artifact expires **2026-11-17 13:58:42 UTC**. Keep the APK and matching source ZIP together.

## v0.4.0 changes recorded
- Capture rings/legal-move dots separated from piece artwork.
- Evaluation bar and score labels resized for narrow screens.
- Drag ghost and move-arrival animation added.
- Seven Stockfish style presets inspired by Capablanca, Tal, Polgar, Fischer, Nakamura, Kasparov and Carlsen; these are not official Chess.com bots.
- VersionName set to 0.4.0 and committed sideload keystore removed.

## Blockers / not yet verified
- No physical Android installation or interaction test.
- Browser UI suite `node tests/ui/ui.test.js` has not been run; current CI does not run it.
- Real Claude/OpenAI-compatible network calls and on-device API-key save/reload/error handling have not been tested.
- Workflow creates a fresh ephemeral sideload signing key per run. Persistent user-owned signing-key secrets are not wired in, so later APKs cannot be assumed to update-install over this build.
- Build #12 is CI-verified, **not device-validated**.

## Exact next steps
1. Download `ChessBuddy-build-12` before **2026-11-17 13:58:42 UTC**; retain its APK and exact matching source ZIP.
2. Install the arm64 APK on Android and run Settings → Run engine self-test.
3. Test tap/drag selection, legal/illegal drops, captures, castling, en passant, promotion, undo, evaluation layout, both game modes, Coach and Archive.
4. Run `node tests/ui/ui.test.js` with Playwright/Chromium installed; record the result and consider adding it to CI.
5. Test real Claude/OpenAI-compatible requests, Android Keystore key save/reload and error handling on-device.
6. Add and verify persistent signing-key support using protected GitHub Actions secrets before distributing update builds.
7. For every future release, update the pinned source ZIP and version check, then package that exact ZIP with the APK and SHA-256 manifest.
