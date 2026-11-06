# ChessBuddy — project status (reviewed 2026-11-06)

## Release distinction
- **v0.4.0 / build #12 is a test build only**, not the real ChessBuddy 4.0 release.
- The user reports that Claude is preparing the actual 4.0. No 4.0 source, ZIP, branch or PR is currently visible in this repository.
- Latest available source baseline here: `ChessBuddy-v0.4.0-source.zip` (188,010 bytes). The expanded `ChessBuddy/` source folder is not checked into the repository root.

## Required product scope
- Fresh Android chess app powered by real Stockfish.
- Play, Coach, Archive/History and Settings tabs; polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Reliable piece selection and legal move handling: tap/drag, captures, castling, en passant, promotion and undo.
- GPT/OpenAI and Claude provider/API-key settings. Keep keys in native Android Keystore-backed storage, not JavaScript.
- Every release must include the **exact source ZIP used for its APK**, beside the APK, with provenance and SHA-256 checksums.

## Repository state
- Repository: `Mahirabsar2/chessbuddy`, branch `main`.
- Latest app-source review baseline: `cc5002f0f9400fac454e501a39415f80e1d4b6f1` (2026-11-05); the subsequent 2026-11-06 commits update project logs/status only.
- Compared with build #12 commit, the 12 later commits modify documentation/log files only; no app-source or workflow changes.
- Branches found: `main`, `master`; no pull requests.
- Available archives: `ChessBuddy-v0.4.0-source.zip` (188,010 bytes) and `ChessBuddy-v0.3.0-source.zip` (187,655 bytes). No 4.0 archive is present.

## Last verified test build (not 4.0)
- GitHub Actions run #12, ID `41648945256`: **SUCCESS**.
- Actual CI log confirms `node tests/run-all.js`: **55/55 passed** (coach 9, engine 14, perft 5, prompts 13, review 3, strength/models 11).
- Stockfish sf_19 compiled for arm64 with NDK 27.2.12479018.
- Gradle `assembleRelease`, APK verification and signature verification succeeded.
- APK metadata: package `com.chessbuddy`, versionCode 1012, versionName 0.4.0, arm64-v8a, 79,716,447 bytes.
- Artifact `ChessBuddy-build-12`, ID `13237225252`, 79,901,351 bytes; includes APK, exact matching v0.4.0 source ZIP, provenance and SHA-256 manifest. Expires 2026-11-17 13:58:42 UTC.
- This is CI evidence for the test build only. It is not proof of 4.0 readiness or device validation.

## Blockers
- Actual Claude-produced 4.0 files are not yet available in the inspected repo.
- No physical Android testing, Playwright UI run, live OpenAI/Claude request, or on-device key save/reload test has been verified.
- Workflow still generates an ephemeral signing key; persistent signing-key support is not configured.
- No tests were run during the 2026-11-06 review.

## Exact next steps
1. Add Claude's actual 4.0 project files and versioned source ZIP to the repository.
2. Review the source and verify every product requirement above.
3. Pin the 4.0 source ZIP and version in the GitHub Actions workflow; do not build 4.0 from the v0.4.0 test archive.
4. Run and record logic tests, Playwright UI tests, Stockfish NDK build, Gradle build and APK verification.
5. Confirm the resulting artifact contains the APK and the exact matching 4.0 source ZIP plus provenance/checksums.
6. Install on Android and test board interactions, legal moves, human-vs-AI, AI-vs-AI, Stockfish, provider requests and API-key persistence.
7. Configure and verify persistent signing-key support before update distribution.
