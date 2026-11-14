# ChessBuddy project status — reviewed 2026-11-14

## Release distinction
- **Actual ChessBuddy 4.0 and 5.0 source are not present in the inspected repository branches.**
- Latest verified APK is v0.4.0 / Actions build #15, a **test build only**. It is not the real 4.0 or 5.0 release.

## Required product scope
- Fresh Android chess app powered by native Stockfish.
- Play, Coach, History/Archive and Settings tabs with a polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Correct piece selection and legal moves, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI and Claude API-key settings with secure native storage.
- Every APK release must ship with the exact source ZIP used to build it, plus provenance and SHA-256 checksums.

## Repository state
- Repository: `Mahirabsar2/chessbuddy`; review baseline on `main`: `be49bd6515c877a0843256bf5c5eedf1792a35a0` (2026-11-13 13:30:54 UTC). Subsequent commits from this review update progress documentation only.
- Compared with build #15 commit `80ec03208d3646c5e5ebb266a4fd7f3101bdfc90`: 15 commits ahead, 0 behind; compared paths are documentation/log/status only.
- Branches: `main`, `master`, `chessbuddy-4.0-claude`, `chessbuddy-5.0-prototype`.
- Both named feature branches point to the same commit `618e48c86ec05721bac4a51d135c8e0af678b777`. That commit adds only `ChessBuddy-v0.4.0-source (1).zip`, whose Git blob SHA is identical to the existing v0.4.0 ZIP (`aeb1fbe6e9d41e1c5c095742061439f109f8e5c8`). Neither branch contains new 4.0/5.0 app source.
- `main` archives: `ChessBuddy-v0.3.0-source.zip` (187,655 bytes) and `ChessBuddy-v0.4.0-source.zip` (226,940 bytes). No actual 4.0/5.0 ZIP or expanded Android app source tree is present in the inspected branch trees.
- No GitHub Releases are published.
- CI workflow `.github/workflows/android-build.yml` is unchanged (blob SHA `b25cdcb13f16cc96c43c8fd3d1c8ede659f98c05`): it downloads, validates and packages the fixed v0.4.0 ZIP, checks `versionName '0.4.0'`, and runs only `node tests/run-all.js`. Playwright UI and Java policy suites are not wired into CI.

## Latest verified test build — not 4.0/5.0
- Actions run #15 / ID `42623107658`, commit `80ec03208d3646c5e5ebb266a4fd7f3101bdfc90`: **SUCCESS**. No newer Actions run was listed in the review.
- Rechecked job metadata and logs: all 18 reported steps succeeded. Logic tests **70/70 passed**: coach 9, coaches/clock 6, engine 14, perft 5 positions, prompts 13, review/openings 10, strength/models 13.
- Stockfish sf_19 compiled for arm64 with NDK 27.2.12479018; source commit `edb0d9db6731067ec50ce619ff372b463bc4dd5d`; binary SHA-256 `0470a60d55495faaa56fa4a47a938569abdbeb80cd6b4c12dcc4efc139a11bd6`.
- Gradle release build and APK verification succeeded.
- APK: package `com.chessbuddy`, versionCode 1015, versionName `0.4.0`, 79,749,986 bytes; SHA-256 `7d42dc7bf1ef51599ec99c6406d8a868c21f71e739e2433cbe9da3d5c75ec214`.
- Artifact `ChessBuddy-build-15`, ID `13677721762`, includes the APK, exact v0.4.0 source ZIP, build info, verification, Stockfish provenance and SHA-256 manifest. It expires 2026-11-23 13:12:42 UTC.
- No app source, APK, source ZIP, build or test was produced on 2026-11-14. No newer Actions run was found.

## Security and verification gaps
- The v0.4.0 source archive contains `app/sideload.keystore`; `app/build.gradle` documents default password `android`. Treat the key as exposed and exclude it from future source packages.
- CI creates a fresh ephemeral signing key per run, preventing consistent update-install continuity.
- `SecretStore` can fall back to app-private plaintext storage if Keystore encryption fails.
- Not verified: Playwright UI, Java policy, physical Android behavior, live provider requests, on-device API-key persistence or persistent signing/update installs.

## Exact next steps
1. Upload the genuine current Claude source and exact versioned source ZIP to a clearly identified branch/commit; do not rename or duplicate the v0.4.0 archive.
2. Inspect archive contents, internal Gradle version and SHA-256; confirm the source is genuinely the intended 4.0/5.0 version and contains no keystore.
3. Audit tabs/board/pieces, human-vs-AI, AI-vs-AI, piece selection, full legal-move handling and OpenAI/Claude settings; fix gaps and remove plaintext fallback.
4. Update CI to build/package that exact ZIP, pin and verify its checksum/version, and run logic, Playwright UI and Java policy suites.
5. Remove the exposed keystore from source packages and configure persistent private signing through GitHub Secrets.
6. Run Stockfish NDK, Gradle/APK, signature, logic and UI checks; inspect the artifact to verify the exact APK/source pair, provenance and checksums.
7. Install on Android and verify board interactions, both play modes, real OpenAI/Claude requests and API-key save/reload.
