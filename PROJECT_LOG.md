# ChessBuddy project log

## 2026-10-28
- Reset project to a fresh Android project named ChessBuddy.
- Current UI includes Play, Coach, History, and Settings tabs.
- Bundled chess.js legal-move rules; basic opponent is not Stockfish.
- Added GitHub Actions workflow to build a debug APK in a hosted Android/Gradle environment and upload APK + exact matching source ZIP + checksums.
- Local APK build is still unavailable because this execution environment has no Android SDK/Gradle installation.
- Next: push this source ZIP to a GitHub repository and run the workflow; then integrate a verified Stockfish build and test on-device.

## 2026-10-31 — v0.3.0
- Rebuilt on the supplied scaffold: replaced the random-move prototype with a real Stockfish integration (NDK build in CI, UCI client, process bridge).
- chess.com-style UI (lobby, bot picker, game screen, Coach, Archive, Settings). AI models shown by real model names.
- AI-model opponents and coach with full position reports, move explanations and board screenshots; strict legal-move validation (fixes the "illegal move at game start" class of bug).
- Strength: Stockfish limiter >= 1320 Elo, handicap mode below.
- Previous sandbox report: 55 logic tests, 26 UI tests (mock bridge), Java compile against stubs, URL-policy JVM test. NOT verified in this review: Gradle/NDK build, APK, on-device behaviour.

## 2026-11-02 — independent review of v0.3.0
- Latest repository commit checked: `cc77271ed32f4ef8488245f633b68d31e14e8e84` (2026-10-31).
- The available `ChessBuddy-v0.3.0-source.zip` exactly matches the repository ZIP blob (Git blob SHA-1 `e541349898afd6fe388fcf61687f75d041da71da`); local SHA-256: `bbba5e65e07a5e61f433e7ba69cae85152e04efb20c1f49798d515060186999f`.
- Source includes Stockfish NDK/UCI integration, Play/Coach/Archive/Settings tabs, bot and AI-vs-AI modes, move legality handling, Claude and OpenAI-compatible provider settings, and native key storage.
- Re-run results: 50/50 non-perft logic tests passed (coach 9, engine 14, prompts 13, review 3, strength/models 11); perft depth 1–2 passed 10/10 checks across five positions; Java PolicyTest passed; 12/12 JavaScript files passed syntax checks; Android manifest XML, both shell scripts, and ZIP integrity passed.
- Full `node tests/run-all.js` did not complete within 300 seconds while running the deeper perft suite (depths 1–4). This is a likely CI test-step blocker because the workflow invokes the same runner. Deep perft remains incomplete, not a pass.
- Playwright UI tests were not run because the Playwright package is unavailable. No live API, Gradle/NDK build, APK installation, or device tests were run. No APK was found in the available workspace; current repository status also says no APK was built.
- Local environment has Java 21 and Node 22, but no Gradle, Android SDK/NDK, sdkmanager, or adb. GitHub API network access from this environment failed DNS resolution.
- Signing note: the source contains a committed throwaway sideload keystore with the documented default password; it is explicitly not suitable for Play distribution or wider release.

### Next steps
1. Split fast CI perft checks (depth 1–2) from the deeper optional suite, or optimize the full suite so `tests/run-all.js` reliably completes.
2. Run the GitHub Actions workflow and retain the run URL, logs, and artifact IDs.
3. Verify the resulting APK contains the ARM64 Stockfish binary, is signed, and is paired with the exact source ZIP and checksums.
4. Install on Android and test piece selection, legal moves, promotion, undo, human-vs-AI, AI-vs-AI, Stockfish self-test, and real Claude/OpenAI calls.
5. Replace the throwaway signing key before any wider distribution.
