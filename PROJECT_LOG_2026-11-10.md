# ChessBuddy daily progress log — 2026-11-10

## Requirements
- Fresh Android chess app powered by native Stockfish.
- Tabs for Play, Coach, History/Archive and Settings; polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Fix piece selection and legal move handling, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI and Claude API-key settings with secure native storage.
- Every release must include the exact source ZIP used for its APK, plus provenance and SHA-256 checksums.

## Repository and available versions
- Repository: `Mahirabsar2/chessbuddy`, branch `main`.
- Reviewed head: `7d42836c4888d2994edf8ef006387ea79e1bced5`; its 3 commits after build #15 are documentation-only.
- Available archives: `ChessBuddy-v0.3.0-source.zip` (187,655 bytes) and `ChessBuddy-v0.4.0-source.zip` (226,940 bytes; blob SHA `aeb1fbe6e9d41e1c5c095742061439f109f8e5c8`).
- Actual ChessBuddy 4.0 source ZIP and expanded source tree are **missing** from the inspected `main` tree.
- The v0.4.0 ZIP was deleted in commit `1287325`; run #14 then failed on the workflow's HTTP 404 download. Commit `80ec032` later reintroduced the exact same ZIP blob. It is currently present again and is not the actual 4.0 source.
- Workflow `.github/workflows/android-build.yml` still hardcodes v0.4.0, including its download, version check and packaged source ZIP.

## Latest verified files/build
- Latest verified build: GitHub Actions run #15, ID `42623107658`, commit `80ec032` — **SUCCESS for v0.4.0 only**.
- APK: `ChessBuddy-v0.4.0-build15-arm64.apk`; package `com.chessbuddy`; versionCode 1015; versionName `0.4.0`; 79,749,986 bytes.
- APK SHA-256: `7d42dc7bf1ef51599ec99c6406d8a868c21f71e739e2433cbe9da3d5c75ec214`.
- Artifact: `ChessBuddy-build-15`, ID `13677721762`; includes the APK, exact v0.4.0 source ZIP, `BUILD_INFO.txt`, `VERIFIED_CHECKS.txt`, `STOCKFISH_PROVENANCE.txt` and `SHA256SUMS.txt`. Expires 2026-11-23 13:12:42 UTC.
- No new source, APK or archive was produced today.

## Tests and verification
- Run #15: all 18 job steps succeeded.
- Logic tests: **70/70 passed** — coach 9, coaches/clock 6, engine 14, perft 5, prompts 13, review/openings 10, strength/models 13.
- Stockfish sf_19 compiled for arm64 with NDK 27.2.12479018.
- Gradle release APK build and APK verification succeeded.
- Run #14 failed because the source ZIP download returned HTTP 404 after its deletion.
- No tests/builds were run during this review.
- Not verified: Playwright UI tests, Java policy tests, physical Android device behavior, live provider requests, API-key persistence on-device.

## Blockers
- Actual 4.0 source and matching ZIP are missing; current CI can only build v0.4.0.
- Workflow runs only the logic suite; UI and Java policy suites are not included.
- Source ZIP contains `app/sideload.keystore` with documented default password `android`; treat it as exposed.
- CI generates an ephemeral signing key every run, preventing normal update-install continuity.
- `SecretStore` falls back to app-private plaintext if Keystore encryption fails; device behavior has not been tested.

## Exact next steps
1. Upload Claude's actual ChessBuddy 4.0 source and exact versioned ZIP; verify its internal version and new contents.
2. Review it against every product requirement and fix selection/move-legality bugs.
3. Update CI to build/package that exact ZIP and run logic, Playwright UI and Java policy suites.
4. Remove the exposed keystore from future source packages and configure persistent signing via GitHub Secrets.
5. Run Stockfish, Gradle/APK, signature, logic and UI checks; inspect the artifact for the exact matching source ZIP, provenance and checksums.
6. Install on Android and test both play modes, board interaction, live OpenAI/Claude requests and API-key save/reload.
