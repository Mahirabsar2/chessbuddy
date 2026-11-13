# ChessBuddy project status — reviewed 2026-11-13

## Release distinction
- **Actual ChessBuddy 4.0 is not present in the inspected repository.** Its source ZIP and expanded app source tree are missing.
- Latest verified APK is v0.4.0 / Actions build #15, a **test build only**. It is not the real 4.0 release.

## Required product scope
- Fresh Android chess app powered by native Stockfish.
- Play, Coach, History/Archive and Settings tabs with a polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Correct piece selection and legal moves, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI and Claude API-key settings with secure native storage.
- Every APK ships with the exact source ZIP used to build it, plus provenance and SHA-256 checksums.

## Repository state
- Repository: `Mahirabsar2/chessbuddy`; branch: `main`.
- Current HEAD: `b08d9b5962cb89aec129de984f4ae0afda94d316` (2026-11-12 13:47 UTC).
- Compared with build #15 commit `80ec03208d3646c5e5ebb266a4fd7f3101bdfc90`: 12 commits ahead, 0 behind. The changed files are documentation/log/status files only; no app-source or workflow changes.
- Branches: `main` and `master`; no GitHub Releases. The inspected `master` tree contains project documentation and root Gradle configuration only.
- `main` archives: `ChessBuddy-v0.3.0-source.zip` (187,655 bytes) and `ChessBuddy-v0.4.0-source.zip` (226,940 bytes; blob SHA `aeb1fbe6e9d41e1c5c095742061439f109f8e5c8`). The v0.4.0 ZIP has reappeared after the earlier deletion.
- No actual 4.0 ZIP or expanded app source directory is present.
- CI still downloads, validates and packages the fixed v0.4.0 ZIP, checks `versionName '0.4.0'`, and runs only `node tests/run-all.js`. Playwright UI and Java policy suites are not wired into CI.

## Latest verified test build — not 4.0
- Actions run #15 / ID `42623107658`, commit `80ec03208d3646c5e5ebb266a4fd7f3101bdfc90`: **SUCCESS**. No newer Actions run is listed.
- All 18 job steps succeeded. Logic tests **70/70 passed**: coach 9, coaches/clock 6, engine 14, perft 5 positions, prompts 13, review/openings 10, strength/models 13.
- Stockfish sf_19 compiled for arm64 with NDK 27.2.12479018; source commit `edb0d9db6731067ec50ce619ff372b463bc4dd5d`; binary SHA-256 `0470a60d55495faaa56fa4a47a938569abdbeb80cd6b4c12dcc4efc139a11bd6`.
- Gradle release build and APK verification succeeded.
- APK: package `com.chessbuddy`, versionCode 1015, versionName `0.4.0`, 79,749,986 bytes; SHA-256 `7d42dc7bf1ef51599ec99c6406d8a868c21f71e739e2433cbe9da3d5c75ec214`.
- Artifact `ChessBuddy-build-15`, ID `13677721762`, includes the APK, exact v0.4.0 source ZIP, `BUILD_INFO.txt`, `VERIFIED_CHECKS.txt`, `STOCKFISH_PROVENANCE.txt` and `SHA256SUMS.txt`. It remains available until 2026-11-23 13:12:42 UTC.
- No app source, APK, source ZIP, build or test was produced during the 2026-11-13 review.

## Security and verification gaps
- The v0.4.0 source archive contains `app/sideload.keystore`; `app/build.gradle` documents default password `android`. Treat this key as exposed and remove it from future source packages.
- CI creates a fresh ephemeral signing key per run, so separate APKs cannot be update-installed over one another using a consistent signing identity.
- `SecretStore` can fall back to app-private plaintext storage if Keystore encryption fails.
- Not verified: Playwright UI, Java policy, physical Android behavior, live provider requests, on-device API-key persistence or persistent signing/update installs.

## Exact next steps
1. Upload Claude's actual 4.0 source and exact matching ZIP to a clearly identified branch/commit.
2. Inspect the ZIP and internal version metadata; confirm it is genuinely new 4.0 source and contains no exposed keystore.
3. Review the implementation against all requirements; fix and test piece-selection and legal-move defects.
4. Update CI to build/package that exact ZIP, pin its checksum, and run logic, Playwright UI and Java policy suites.
5. Remove the exposed keystore from future archives, remove the plaintext fallback, and configure persistent private signing through GitHub Secrets.
6. Run Stockfish NDK, Gradle/APK, signature, logic and UI checks; inspect the final artifact for the exact APK/source pairing, provenance and checksums.
7. Install on Android and verify board interactions, human-vs-AI, AI-vs-AI, real OpenAI/Claude requests and API-key save/reload.
