# ChessBuddy project status — reviewed 2026-11-12

## Release distinction
- **Actual ChessBuddy 4.0 is not present in the inspected repository.**
- Latest verified APK is v0.4.0 / Actions build #15, a **test build only**. It is not the real 4.0 release.
- Actual 4.0 source ZIP and expanded app source tree are missing from both inspected branches.

## Required product scope
- Fresh Android chess app powered by native Stockfish.
- Play, Coach, History/Archive and Settings tabs; polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Correct piece selection and legal move handling, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI and Claude API-key settings with secure native storage.
- Every release ships the exact source ZIP used to build its APK, plus provenance and SHA-256 checksums.

## Repository state
- Repository: `Mahirabsar2/chessbuddy`; branch: `main`.
- Current HEAD: `1635c71670fe2e821f5829aa38bee41fe8c6da91` (2026-11-11 13:05 UTC).
- Compared with build #15 commit `80ec03208d3646c5e5ebb266a4fd7f3101bdfc90`: 9 commits ahead, 0 behind; comparison shows documentation-only changes across 5 files, with no app-source or workflow changes.
- Branches checked: `main` and `master`; the inspected `master` tree has no app source, ZIP or workflow.
- `main` archives: `ChessBuddy-v0.3.0-source.zip` (187,655 bytes) and `ChessBuddy-v0.4.0-source.zip` (226,940 bytes). No actual 4.0 ZIP or expanded app source tree is present.
- CI still downloads, validates and packages v0.4.0 and hardcodes `versionName '0.4.0'`. It runs only `node tests/run-all.js`; Playwright UI and Java policy suites are not part of CI.

## Latest verified test build (not 4.0)
- Actions run #15 / ID `42623107658`, commit `80ec03208d3646c5e5ebb266a4fd7f3101bdfc90`: **SUCCESS**.
- Historical run #15: logic tests **70/70 passed**; Stockfish sf_19 compiled for arm64 with NDK 27.2.12479018; Gradle release build and APK verification succeeded.
- APK: `com.chessbuddy`, versionCode 1015, versionName `0.4.0`, 79,749,986 bytes; SHA-256 `7d42dc7bf1ef51599ec99c6406d8a868c21f71e739e2433cbe9da3d5c75ec214`.
- Artifact `ChessBuddy-build-15`, ID `13677721762`, remains available and was not expired at this review. It contains the APK, exact v0.4.0 ZIP, build info, verification record, Stockfish provenance and SHA-256 manifest. Expires 2026-11-23 13:12:42 UTC.
- No build or test ran during the 2026-11-12 review; no new app source, APK or source ZIP was produced.

## Security and verification gaps
- The v0.4.0 source archive was previously inspected and found to contain `app/sideload.keystore`; `app/build.gradle` documents default password `android`. Treat this key as exposed and remove it from future source packages.
- CI generates a new ephemeral signing key per run, so APKs cannot be update-installed over earlier builds using a consistent signing identity.
- `SecretStore` can fall back to app-private plaintext storage if Keystore encryption fails.
- Not verified: Playwright UI, Java policy, physical Android behavior, live provider requests, on-device API-key persistence or persistent signing/update installs.

## Exact next steps
1. Upload Claude's actual 4.0 source and exact matching ZIP to a clearly identified branch/commit; verify its contents and internal version metadata.
2. Review the 4.0 source against all requirements and fix piece-selection/legal-move defects.
3. Update CI to build/package that exact ZIP and run logic, Playwright UI and Java policy suites.
4. Remove the exposed keystore from future source archives, remove the plaintext fallback, and configure persistent private signing through GitHub Secrets.
5. Run and record Stockfish NDK, Gradle/APK, signature, logic and UI checks; inspect the final artifact for the exact matching ZIP, provenance and checksums.
6. Install on Android and verify board interactions, both play modes, live OpenAI/Claude requests and API-key save/reload.
