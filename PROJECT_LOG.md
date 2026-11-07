# ChessBuddy project log

## 2026-10-28
- Reset project to a fresh Android project named ChessBuddy.
- Initial UI included Play, Coach, History and Settings tabs.
- Added chess.js legal-move rules and a GitHub Actions build workflow.
- The first prototype opponent was not Stockfish.

## 2026-10-31 — v0.3.0
- Rebuilt around a real Stockfish integration: Android NDK build, UCI client and native process bridge.
- Added the chess.com-inspired lobby, board, bot picker, Coach, Archive and Settings.
- Added Stockfish bot strengths, human-vs-AI, AI-vs-AI, model opponents, review and FEN/PGN archive features.
- Added Claude and OpenAI-compatible provider support, position-aware prompts and legal validation of model moves.
- Historical local tests were recorded, but the Android build and device behaviour were not verified at that time.

## 2026-11-02 — independent v0.3.0 review
- Re-ran available logic/perft, Java policy and JavaScript syntax checks; the fast checks passed.
- The deeper perft run timed out in the local review environment. Browser UI, live provider calls, Gradle/NDK build and physical-device tests were not run.
- The repository's v0.3.0 source archive was checked against its GitHub blob.

## 2026-11-03 — v0.4.0 test build CI verified
- Added `ChessBuddy-v0.4.0-source.zip` to the repository root (188,010 bytes).
- Updated the Android workflow to fetch v0.4.0, run the logic suite, compile Stockfish for arm64, assemble and verify the APK, and package the exact same source ZIP beside it.
- GitHub Actions run #12 / ID `41648945256`: **SUCCESS**.
- Logic tests: **55/55 passed** — coach 9, engine 14, perft 5 positions, prompts 13, review 3, strength/models 11.
- Stockfish sf_19 compiled for Android arm64 with NDK 27.2.12479018; source commit `edb0d9db6731067ec50ce619ff372b463bc4dd5d`; binary SHA-256 `0470a60d55495faaa56fa4a47a938569abdbeb80cd6b4c12dcc4efc139a11bd6`.
- Gradle release build and APK verification succeeded.
- APK metadata: `com.chessbuddy`, versionCode 1012, versionName 0.4.0, 79,716,447 bytes.
- Artifact `ChessBuddy-build-12` contains the APK, matching v0.4.0 source ZIP, verification/provenance records and SHA-256 manifest. It expires 2026-11-17 13:58:42 UTC.
- Signing is an ephemeral personal sideload key, not a persistent Play Store/update key.

## 2026-11-04 — repository review
- Confirmed the commits after build #12 changed documentation/status only; app source and workflow were unchanged.
- Confirmed v0.4.0 source ZIP is present in the repository root (188,010 bytes); expanded app source is not checked into the root.
- Re-queried run #12, its jobs and artifact. Overall conclusion **success**, all job steps completed, artifact ID `13237225252`, 79,901,351 bytes.
- Corrected build/signing instructions to match the actual workflow.
- Remaining gaps: browser UI tests, physical-device tests, real provider calls/Keystore runtime checks, and persistent signing-key support.

## 2026-11-05 — repository review
- Reviewed app-source baseline `9e9391fff4855c70be48b46ec06750ea7e0dbb40`. Commits after build #12 changed documentation/logs only; no app-source or workflow changes.
- Confirmed `ChessBuddy-v0.4.0-source.zip` remains present (188,010 bytes); expanded app source is not checked into the repository root.
- Inspected build #12 job metadata and actual job logs: 55/55 logic tests passed; Stockfish sf_19 arm64 build succeeded; Gradle release build succeeded; APK verification and artifact upload succeeded.
- No new app source, APK, source archive or tests were produced/run during the review.
- Remaining gaps: browser UI suite, physical-device tests, live provider/Keystore runtime checks, and persistent signing-key support.

## 2026-11-06 — release clarification and repository review
- User clarified that build #12 / v0.4.0 is a **test build**, while Claude is preparing the actual ChessBuddy 4.0.
- Reviewed latest `main` head `cc5002f0f9400fac454e501a39415f80e1d4b6f1`. Compared with build #12, 12 commits ahead; changed files are documentation/logs only. No app source or workflow changes.
- Repository has `main` and `master` branches, no pull requests, and no visible ChessBuddy 4.0 source archive. v0.4.0 ZIP remains the latest available app-source baseline; expanded source directory is absent from repository root.
- Re-verified run #12: success; actual logs confirm 55/55 logic tests, Stockfish sf_19 arm64 compilation, Gradle release build, APK/signature verification, and successful upload of artifact `ChessBuddy-build-12` (ID `13237225252`). Artifact includes the exact v0.4.0 ZIP copied by the workflow and expires 2026-11-17 13:58:42 UTC.
- No tests were run today; historical CI results above are not 4.0 test results. No new app code, APK or source ZIP was produced.
- Next: obtain Claude's actual 4.0 source, review it against requirements, update workflow to build the exact 4.0 archive, run tests and device validation, then package APK + matching source ZIP + provenance/checksums.


## 2026-11-07 — repository review
- Reviewed current `main` head `674123fbd09468f4c0096b6cd78ae1ba7c959a61`. Compared with build #12 commit `26625d6d80f521db15b21e749a6cca5881fd1cf9`: 16 commits ahead, with documentation/status changes only; no app-source or workflow changes.
- Confirmed only `main` and `master` branches, no pull requests, and no 4.0 source files/archive. `main` still contains v0.4.0 (188,010 bytes) and v0.3.0 (187,655 bytes) source ZIPs; expanded source is absent from the root. `master` has neither ZIP.
- Confirmed the Android workflow still hardcodes v0.4.0 and runs only `node tests/run-all.js`; it is not ready to build Claude's 4.0.
- Rechecked Actions run #12: success; historical evidence remains 55/55 logic tests, Stockfish sf_19 arm64 build, Gradle release build, APK/signature verification and matching-source artifact upload. Artifact ID `13237225252` remains available until 2026-11-17 13:58:42 UTC.
- No tests were run today; no new app source, APK or source ZIP was produced. No Android device, Playwright UI or live provider/Keystore runtime test is verified.
- Next: obtain Claude's actual 4.0 source and exact matching ZIP, review requirements, pin that ZIP in CI, run full logic/UI/native/build verification, package APK + matching ZIP + provenance/checksums, then device-test and configure persistent signing.
