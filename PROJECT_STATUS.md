# ChessBuddy — project status (reviewed 2026-11-08)

## Release distinction
- **v0.4.0 / build #12 is a test build only**, not the real ChessBuddy 4.0 release.
- The user reports that Claude is preparing the actual 4.0. This is user-reported; no 4.0 source, ZIP, branch or PR is visible in the inspected repository.
- Latest available app-source baseline remains `ChessBuddy-v0.4.0-source.zip` (188,010 bytes). The expanded `ChessBuddy/` source folder is not checked into the repository root.

## Required product scope
- Fresh Android chess app powered by real Stockfish.
- Play, Coach, Archive/History and Settings tabs; polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Reliable piece selection and legal move handling: tap/drag, captures, castling, en passant, promotion and undo.
- GPT/OpenAI and Claude provider/API-key settings. Keep keys in native Android Keystore-backed storage, not JavaScript.
- Every release must include the **exact source ZIP used for its APK**, beside the APK, with provenance and SHA-256 checksums.

## Repository state
- Repository: `Mahirabsar2/chessbuddy`; default branch: `main`.
- Latest reviewed non-documentation `main` head: `e2781fb09a4539753d4b52f6122705afee85d6de` (2026-11-08 13:56 UTC); subsequent commits in this review update documentation/logs only.
- At the reviewed code head, `main` was 21 commits ahead and 0 behind build #12 commit `26625d6d80f521db15b21e749a6cca5881fd1cf9`. All 10 paths changed since that build were documentation/build-instruction files; the later commits made during this review also update documentation only. No app-source or workflow changes.
- Only branches found: `main` (`e2781fb09a4539753d4b52f6122705afee85d6de`) and `master` (`a7203fa75eead88e4bd9a3acfbebf9d5994e8148`); no pull requests or GitHub releases found. The `master` tree contains project-level Gradle/configuration and documentation only, with no app source or source ZIP.
- `main` contains `ChessBuddy-v0.4.0-source.zip` (188,010 bytes) and `ChessBuddy-v0.3.0-source.zip` (187,655 bytes). The expanded source directory is absent from the repository root. `master` contains neither source ZIP.
- No 4.0 source files or archive were found.
- `.github/workflows/android-build.yml` still downloads `ChessBuddy-v0.4.0-source.zip`, checks versionName 0.4.0, runs `node tests/run-all.js`, and packages that same v0.4.0 ZIP. It is not a 4.0 build workflow.

## Last verified test build (not 4.0)
- GitHub Actions run #12, ID `41648945256`, commit `26625d6d80f521db15b21e749a6cca5881fd1cf9`: **SUCCESS**.
- Historical job logs confirm logic tests **55/55 passed** (coach 9, engine 14, perft 5, prompts 13, review 3, strength/models 11).
- Stockfish sf_19 compiled for Android arm64 with NDK 27.2.12479018.
- Gradle `assembleRelease`, APK verification and signature verification succeeded.
- APK metadata: package `com.chessbuddy`, versionCode 1012, versionName 0.4.0, arm64-v8a, 79,716,447 bytes.
- Artifact `ChessBuddy-build-12`, ID `13237225252`, 79,901,351 bytes, remains available until 2026-11-17 13:58:42 UTC. It contains the APK, exact matching v0.4.0 source ZIP, provenance and SHA-256 manifest.
- This is CI evidence for the test build only. It does not verify ChessBuddy 4.0 or on-device behaviour.

## 2026-11-07 review activity
- Compared build #12 with current `main`: 16 documentation-only commits ahead; app source and workflow unchanged.
- Confirmed only `main` and `master` branches, no pull requests, and no visible 4.0 source.
- No app code, APK, source ZIP or tests were produced/run during that review.

## 2026-11-08 review activity
- Final repository head after the daily-log commits: `e2781fb09a4539753d4b52f6122705afee85d6de`. Compared with build #12, `main` is 21 commits ahead and 0 behind; all 10 changed paths are documentation/build-instruction files only.
- Reconfirmed branches `main` and `master`; no pull requests or GitHub releases. The `master` tree has no app source or source ZIP.
- Reconfirmed v0.4.0 (188,010 bytes) and v0.3.0 (187,655 bytes) are the only app-source ZIPs on `main`; expanded app source and all 4.0 files remain absent.
- Rechecked the workflow: it still fetches and packages v0.4.0, checks versionName 0.4.0, runs only `node tests/run-all.js`, and does not run Playwright.
- Latest Actions run remains #12 / ID `41648945256`, successful for the v0.4.0 test build. Its artifact `ChessBuddy-build-12` (ID `13237225252`) is not expired and expires 2026-11-17 13:58:42 UTC.
- No build or tests were run in this review; no app source, APK or source ZIP was produced. No Android device, UI, live-provider or on-device key-persistence tests are verified.

## Blockers
- Claude's actual 4.0 source is not yet available in the inspected repository.
- The workflow remains pinned to v0.4.0 and does not run the Playwright UI suite.
- No physical Android testing, live provider requests, or on-device API-key save/reload tests have been verified.
- Workflow signing uses an ephemeral sideload key; persistent signing-key support is not configured.

## Exact next steps
1. Obtain Claude's actual 4.0 source and matching versioned source ZIP; add them to a clearly identified branch or PR.
2. Review the 4.0 source against all required product features and fix selection/move-legality issues.
3. Update the workflow to pin and validate the exact 4.0 ZIP; do not build 4.0 from the v0.4.0 test archive.
4. Run logic tests, Playwright UI tests, Stockfish NDK build, Gradle build and APK/signature verification; record only verified results.
5. Package the APK with the exact source ZIP used for that build, provenance and SHA-256 checksums; inspect artifact contents.
6. Install on Android and test engine startup, board interactions, both play modes, provider calls and API-key persistence.
7. Configure and verify persistent signing-key support before distributing update builds.
