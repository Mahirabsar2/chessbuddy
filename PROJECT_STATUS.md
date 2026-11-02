# ChessBuddy v0.3.0 — project status (2026-10-31)

## Blocked
- **No APK was built.** The environment this was written in has no network, no Gradle, no Android SDK/NDK, and no Stockfish source, so it cannot compile an APK or Stockfish.
  Single next action: run the GitHub workflow (`BUILD_ON_GITHUB.md`). The workflow builds Stockfish, the APK and the matching source ZIP, and records what it verified.

## Completed (written)
- Android app: WebView shell, Stockfish process bridge, Keystore-backed key storage, native HTTP with HTTPS-only policy, share/copy, edge-to-edge insets, back handling.
- Real Stockfish integration (official tag, NDK build script, UCI client, self-test screen).
- chess.com-style UI, bots 400–full strength, custom Elo, AI-model opponents, AI vs AI, coach, game review, archive/replay, FEN/PGN export and import.
- Professional prompts: board diagram, every move explained, tactical facts, Stockfish ground truth, legal-move list, PNG screenshot.
- CI workflow with APK verification and a source ZIP built from the exact commit.

## Previously verified (historical report, 2026-10-31)
- The previous author reported chess.js perft on five standard positions, 55 logic tests, 26 UI tests (mock bridge), Java compilation against stubs, and URL-policy JVM checks.
- Gradle/AGP build, NDK compile of Stockfish, APK itself, installation and behaviour on a real phone, real Stockfish strength calibration, real API calls, HttpTransport and EngineProcess at runtime, and on-device Keystore behaviour were not verified in that report.

## Independent review (2026-11-02)
- Latest reviewed repository commit before this log update: `cc77271ed32f4ef8488245f633b68d31e14e8e84`. The local v0.3.0 source archive matches the repository ZIP blob exactly.
- Re-run: 50/50 non-perft logic tests passed; perft depths 1–2 passed 10/10 checks across five positions; Java PolicyTest passed; 12/12 JavaScript files passed syntax checks; Android manifest XML, both shell scripts, and ZIP integrity passed.
- The complete `node tests/run-all.js` did not finish within 300 seconds while executing the deeper perft suite (depths 1–4). The workflow invokes the same runner, so this is a likely CI blocker. Depth 3–4 is not verified.
- Playwright UI tests were not run because Playwright is unavailable. Live API requests, Gradle/NDK build, APK signing verification, installation, and device tests were not run.
- No APK is present in the available workspace. The environment has Java 21 and Node 22, but no Gradle, Android SDK/NDK, sdkmanager, or adb. GitHub API access from this environment failed DNS resolution.
- The source contains a committed throwaway sideload keystore with the documented default password; it is not suitable for Play distribution or wider release.

## Next actions
1. Make the CI perft suite complete reliably (depth 1–2 in the fast suite; deeper checks optional or optimized).
2. Run GitHub Actions and inspect actual logs and artifact list.
3. Verify APK signature, embedded ARM64 Stockfish binary, matching source ZIP, and checksums.
4. Install on Android and test piece selection, legal moves, promotion, undo, human-vs-AI, AI-vs-AI, Stockfish self-test, and real Claude/OpenAI calls.
5. Replace the throwaway signing key before wider distribution.
