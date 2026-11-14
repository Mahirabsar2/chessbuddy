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
- Repository has `main` and `master` branches, no visible ChessBuddy 4.0 source archive. v0.4.0 ZIP remains the latest available app-source baseline; expanded source directory is absent from repository root.
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

## 2026-11-08 — repository review
- Reviewed `main` at final head `e2781fb09a4539753d4b52f6122705afee85d6de` (2026-11-08 13:56 UTC). Compared with test-build commit `26625d6d80f521db15b21e749a6cca5881fd1cf9`: 21 commits ahead, 0 behind; all 10 changed paths are documentation/build-instruction files. No app-source or workflow changes.
- Confirmed only branches `main` and `master`; no pull requests or GitHub releases. `master` contains project-level Gradle/configuration and documentation only, with no app source or source ZIP.
- `main` contains only the v0.4.0 test-source ZIP (188,010 bytes) and v0.3.0 ZIP (187,655 bytes) as app-source archives. The expanded app source is absent. No 4.0 branch, source files, matching ZIP or release is visible.
- Confirmed `.github/workflows/android-build.yml` still downloads and packages v0.4.0, checks `versionName '0.4.0'`, runs only `node tests/run-all.js`, and does not run Playwright UI tests.
- Latest Actions run remains #12 / ID `41648945256`: **SUCCESS** for the v0.4.0 test build. All job steps succeeded; historical evidence is 55/55 logic tests, Stockfish sf_19 arm64 compilation, Gradle release APK build, APK/signature verification and artifact upload. Artifact `ChessBuddy-build-12` (ID `13237225252`) remains available until 2026-11-17 13:58:42 UTC.
- No tests or builds were run in this review; no new app source, APK or source ZIP was produced. No Android device, Playwright UI, live-provider or on-device key-persistence test is verified.
- Next: obtain Claude's actual 4.0 source and exact matching ZIP, inspect it against all requirements, pin that ZIP/version in CI, run logic/UI/native/build checks, verify APK + exact ZIP + provenance/checksums, then device-test and configure persistent signing.

## 2026-11-09 — repository review and CI build #15
- Reviewed latest `main` head `80ec03208d3646c5e5ebb266a4fd7f3101bdfc90` (2026-11-09 13:10 UTC; commit message: “4.0 release / hi”).
- The commit does **not** contain a new ChessBuddy 4.0 source archive. The root still contains only `ChessBuddy-v0.3.0-source.zip` (187,655 bytes) and `ChessBuddy-v0.4.0-source.zip` (226,940 bytes). The v0.4.0 ZIP has the same Git blob SHA `aeb1fbe6e9d41e1c5c095742061439f109f8e5c8` as before; its contents still declare `versionName '0.4.0'`. No expanded app-source directory or 4.0 ZIP is present.
- The v0.4.0 ZIP was removed in commit `1287325`, but the later `80ec032` tree contains that exact same ZIP blob again. It is currently present on `main`.
- GitHub Actions run #15 / ID `42623107658`, commit `80ec032`: **SUCCESS**. The workflow downloaded and built the v0.4.0 archive, not 4.0.
- Verified logic tests: **70/70 passed** — coach 9, coaches/clock 6, engine 14, perft 5, prompts 13, review/openings 10, strength/models 13. `tests/run-all.js` runs only the logic suite; the separate Playwright UI suite and Java policy tests were not run by this workflow.
- Stockfish sf_19 compiled for arm64 with NDK 27.2.12479018; source commit `edb0d9db6731067ec50ce619ff372b463bc4dd5d`; binary SHA-256 `0470a60d55495faaa56fa4a47a938569abdbeb80cd6b4c12dcc4efc139a11bd6`.
- Gradle release build and APK verification succeeded. APK: `com.chessbuddy`, versionCode 1015, versionName 0.4.0, 79,749,986 bytes; SHA-256 `7d42dc7bf1ef51599ec99c6406d8a868c21f71e739e2433cbe9da3d5c75ec214`.
- Artifact `ChessBuddy-build-15`, ID `13677721762`, was uploaded successfully and inspected. It contains `ChessBuddy-v0.4.0-build15-arm64.apk`, the same v0.4.0 source ZIP used by CI, `BUILD_INFO.txt`, `VERIFIED_CHECKS.txt`, `STOCKFISH_PROVENANCE.txt` and `SHA256SUMS.txt`. Artifact expires 2026-11-23 13:12:42 UTC. This verifies the APK/source pairing for the **v0.4.0 test build only**.
- Source review confirms four app tabs, Stockfish integration, human-vs-AI and AI-vs-AI flows, move legality checks and Claude/OpenAI-compatible model configuration. API keys are encrypted with Android Keystore AES-GCM when available, but `SecretStore` falls back to app-private plaintext storage if Keystore encryption fails. No physical-device or live-provider test was run.
- Security/release finding: the source ZIP includes `app/sideload.keystore`, and `app/build.gradle` documents its default password as `android`. Treat this committed signing key as exposed; remove it from future source archives and use a private signing key stored in GitHub Secrets. The current workflow generates a fresh ephemeral key per run, so separate CI APKs cannot be installed as in-place updates over one another.
- No actual 4.0 source, APK or matching 4.0 release archive was produced. No Playwright UI, Java policy, Android device, live API-provider or on-device API-key persistence tests were verified.
- Exact next steps:
  1. Add Claude's actual 4.0 source and its exact versioned ZIP to `main` or a clearly identified release branch; verify the ZIP's internal Gradle version is 4.0 and its contents are new.
  2. Review the new source against all required features and fix any piece-selection or legal-move defects.
  3. Update CI to build and package that exact 4.0 ZIP; add the Playwright UI and Java policy suites to CI.
  4. Remove the committed sideload keystore from future source archives and configure one persistent private signing key through GitHub Secrets.
  5. Run logic, UI, Java policy, Stockfish NDK and Gradle/APK verification; record only observed results.
  6. Inspect the final artifact to confirm the APK, exact source ZIP, provenance and SHA-256 manifest are all present.
  7. Install on a physical Android device and verify board interactions, human-vs-AI, AI-vs-AI, real provider requests and API-key save/reload.
-
## 2026-11-14 — repository and feature-branch review
- Reviewed `main` HEAD `be49bd6515c877a0843256bf5c5eedf1792a35a0` (2026-11-13 13:30:54 UTC). Compared with build #15 commit `80ec03208d3646c5e5ebb266a4fd7f3101bdfc90`: 15 commits ahead, 0 behind; the changed paths are documentation/log/status only. No app-source or workflow changes.
- Branches now include `main`, `master`, `chessbuddy-4.0-claude` and `chessbuddy-5.0-prototype`. Both named feature branches point to the same commit `618e48c86ec05721bac4a51d135c8e0af678b777`, which adds only `ChessBuddy-v0.4.0-source (1).zip`. Its blob SHA matches the old v0.4.0 ZIP exactly; it is not new 4.0 or 5.0 app source.
- `main` still contains only v0.3.0 and v0.4.0 app-source ZIPs; no actual 4.0/5.0 ZIP or expanded Android app source tree is present in the inspected branches. No GitHub Releases are published.
- CI workflow remains unchanged and hardcodes v0.4.0; it runs only `node tests/run-all.js`, not Playwright UI or Java policy tests.
- No app source, APK or source ZIP was produced on 2026-11-14; no build or test was run today.
- Rechecked Actions run #15 / ID `42623107658`: **SUCCESS for the v0.4.0 test build only**. Job metadata and logs confirm all 18 reported steps succeeded, 70/70 logic tests passed, Stockfish sf_19 arm64 compiled, Gradle release build and APK verification succeeded. Artifact `ChessBuddy-build-15` (ID `13677721762`) remains available until 2026-11-23 13:12:42 UTC and contains the matching v0.4.0 ZIP and APK plus provenance/verification/checksum files.
- Blockers: actual 4.0/5.0 source missing; stale CI; exposed sideload keystore in old source archive; ephemeral signing; plaintext fallback in `SecretStore`; UI/device/provider/key-persistence behavior unverified.
- Next: upload the genuine current source and exact versioned ZIP; inspect version, archive hash and keystore contents; audit and fix UI/selection/legal moves/both play modes/provider settings; update CI to build that exact archive and run logic/UI/Java suites; configure persistent private signing and remove plaintext fallback; verify APK + exact ZIP + provenance/checksums; device-test all required flows.
