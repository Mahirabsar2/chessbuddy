# ChessBuddy project status — reviewed 2026-11-09

## Release distinction
- **v0.4.0 / build #15 is a test build only. It is not the actual ChessBuddy 4.0 release.**
- The user says Claude is preparing the real 4.0. No actual 4.0 source archive or expanded source tree is present in the latest inspected `main` commit.
- Latest available app-source baseline remains `ChessBuddy-v0.4.0-source.zip` (226,940 bytes).

## Required product scope
- Fresh Android chess app powered by real native Stockfish.
- Play, Coach, History/Archive and Settings tabs; polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Correct piece selection and legal moves, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI and Claude API-key settings with secure native storage.
- Every release must ship the **exact source ZIP used for its APK**, alongside provenance and SHA-256 checksums.

## Repository state
- Repository: `Mahirabsar2/chessbuddy`; default branch: `main`.
- Latest reviewed head: `80ec03208d3646c5e5ebb266a4fd7f3101bdfc90` (2026-11-09 13:10 UTC; message “4.0 release / hi”).
- Root source archives: `ChessBuddy-v0.3.0-source.zip` (187,655 bytes) and `ChessBuddy-v0.4.0-source.zip` (226,940 bytes). The v0.4.0 ZIP retains Git blob SHA `aeb1fbe6e9d41e1c5c095742061439f109f8e5c8`; its internal `app/build.gradle` declares `versionName '0.4.0'`.
- No 4.0 ZIP, 4.0 source directory, 4.0 branch or release was found.
- The v0.4.0 ZIP was removed by commit `1287325`, but the subsequent `80ec032` tree reintroduced the same blob. It is currently present.
- The workflow `.github/workflows/android-build.yml` still downloads, validates and packages v0.4.0. It runs `node tests/run-all.js`, which executes only the logic suite; the separate Playwright UI suite and Java policy tests are not wired into this workflow.

## Latest verified CI test build (not 4.0)
- GitHub Actions run #15, ID `42623107658`, commit `80ec03208d3646c5e5ebb266a4fd7f3101bdfc90`: **SUCCESS**.
- Logic tests: **70/70 passed** — coach 9, coaches/clock 6, engine 14, perft 5, prompts 13, review/openings 10, strength/models 13.
- Stockfish sf_19 compiled for arm64 with NDK 27.2.12479018; source commit `edb0d9db6731067ec50ce619ff372b463bc4dd5d`; binary SHA-256 `0470a60d55495faaa56fa4a47a938569abdbeb80cd6b4c12dcc4efc139a11bd6`.
- Gradle release build, APK ZIP-integrity check, asset/native-binary checks and APK signature verification succeeded.
- APK: `com.chessbuddy`, versionCode 1015, versionName 0.4.0, arm64-v8a, 79,749,986 bytes; SHA-256 `7d42dc7bf1ef51599ec99c6406d8a868c21f71e739e2433cbe9da3d5c75ec214`.
- Artifact `ChessBuddy-build-15`, ID `13677721762`, 79,971,643 bytes, expires 2026-11-23 13:12:42 UTC. Its contents were inspected: APK, exact v0.4.0 source ZIP, `BUILD_INFO.txt`, `VERIFIED_CHECKS.txt`, `STOCKFISH_PROVENANCE.txt` and `SHA256SUMS.txt`.
- This proves a matching APK/source pair for the **v0.4.0 test build only**. It does not prove 4.0.

## Source review and security findings
- The current v0.4.0 source contains four tabs, Stockfish integration, human-vs-AI and AI-vs-AI flows, move validation, and Claude/OpenAI-compatible model configuration.
- `SecretStore` encrypts keys with Android Keystore AES-GCM when available, but falls back to app-private plaintext storage if encryption fails. Device behavior and persistence have not been tested.
- The source archive contains `app/sideload.keystore`; `app/build.gradle` documents its default password as `android`. Treat the committed signing key as exposed and remove it from future source archives.
- The current workflow creates a fresh ephemeral signing key for each CI run. Separate APK builds therefore cannot update-install over one another. Configure a persistent private signing key through GitHub Secrets.

## Unverified
- Actual ChessBuddy 4.0 source/build/tests.
- Playwright browser UI tests and Java policy tests.
- Physical Android installation and interaction tests.
- Live OpenAI/Claude provider calls and on-device API-key save/reload.
- Persistent signing-key/update-install behavior.

## Exact next steps
1. Add Claude's actual 4.0 source and exact matching versioned ZIP to `main` or a clearly identified release branch; verify internal version metadata and new contents.
2. Review 4.0 against all required features and fix piece-selection/legal-move defects.
3. Update CI to pin and build the exact 4.0 ZIP; add the Playwright UI and Java policy suites.
4. Remove the committed sideload keystore from future source packages and configure a persistent private signing key via GitHub Secrets.
5. Run logic, UI, Java policy, Stockfish NDK and Gradle/APK/signature verification; log only observed results.
6. Inspect the final artifact to confirm the APK, exact matching source ZIP, provenance and SHA-256 checksums are all present.
7. Install on Android and test board interactions, both play modes, live provider calls and API-key persistence.
