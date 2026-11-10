# ChessBuddy project status — reviewed 2026-11-10

## Release distinction
- **The actual ChessBuddy 4.0 release is not available in the inspected repository.**
- The latest verified APK is v0.4.0 / build #15, a **test build only**. It is not the real 4.0 release.
- Actual 4.0 source ZIP and expanded source tree are missing from the latest inspected `main` tree.

## Required product scope
- Fresh Android chess app powered by native Stockfish.
- Play, Coach, History/Archive and Settings tabs; polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Correct piece selection and legal move handling, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI and Claude API-key settings with secure native storage.
- Every release ships the exact source ZIP used to build its APK, plus provenance and SHA-256 checksums.

## Repository state
- Repository: `Mahirabsar2/chessbuddy`; branch: `main`.
- Reviewed head: `7d42836c4888d2994edf8ef006387ea79e1bced5`. Its 3 commits after build #15 changed documentation only; no app source or workflow changed.
- Current root archives: `ChessBuddy-v0.3.0-source.zip` (187,655 bytes) and `ChessBuddy-v0.4.0-source.zip` (226,940 bytes; blob SHA `aeb1fbe6e9d41e1c5c095742061439f109f8e5c8`).
- The v0.4.0 ZIP was deleted in commit `1287325`, but reappeared unchanged in commit `80ec032`; it is currently present. Run #14 failed with HTTP 404 while it was absent.
- CI still downloads, validates and packages v0.4.0. It runs `node tests/run-all.js` only; Playwright UI and Java policy tests are not wired into the workflow.

## Latest verified test build (not 4.0)
- Actions run #15 / ID `42623107658`, commit `80ec03208d3646c5e5ebb266a4fd7f3101bdfc90`: **SUCCESS**.
- All 18 job steps succeeded; logic tests **70/70 passed**.
- Stockfish sf_19 compiled for arm64 with NDK 27.2.12479018; Gradle release build and APK verification succeeded.
- APK: `com.chessbuddy`, versionCode 1015, versionName `0.4.0`, 79,749,986 bytes; SHA-256 `7d42dc7bf1ef51599ec99c6406d8a868c21f71e739e2433cbe9da3d5c75ec214`.
- Artifact `ChessBuddy-build-15`, ID `13677721762`, contains the APK, exact v0.4.0 ZIP, build info, verification record, Stockfish provenance and SHA-256 manifest. Expires 2026-11-23 13:12:42 UTC.
- No tests/builds were run during the 2026-11-10 review.

## Security and verification gaps
- The source archive contains `app/sideload.keystore`; `app/build.gradle` documents its default password as `android`. Treat it as exposed and remove it from future source packages.
- CI creates a new ephemeral signing key per run, so builds cannot update-install over one another.
- `SecretStore` can fall back to app-private plaintext storage if Keystore encryption fails.
- Not verified: Playwright UI, Java policy, physical Android behavior, live provider requests, on-device API-key persistence and persistent signing/update installs.

## Exact next steps
1. Upload Claude's actual 4.0 source and exact matching ZIP; verify internal version metadata and new contents.
2. Review the 4.0 source against all requirements and fix selection/legal-move defects.
3. Update CI to build/package that exact ZIP and run logic, Playwright UI and Java policy suites.
4. Remove the exposed keystore from future source packages and configure persistent private signing through GitHub Secrets.
5. Run and record Stockfish NDK, Gradle/APK, signature, logic and UI checks; inspect the final artifact for the exact matching ZIP, provenance and checksums.
6. Install on Android and verify board interactions, both play modes, live OpenAI/Claude calls and API-key save/reload.
