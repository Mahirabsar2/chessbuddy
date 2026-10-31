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

## Verified (actually run)
- chess.js move generation: perft on 5 standard positions (startpos, Kiwipete, positions 3–5).
- 55 logic tests in 6 files: UCI client against a scripted UCI peer (14), provider requests/responses/images (9), prompts + move parser incl. first-move regressions (13), review (3), strength + model naming (11), perft (5).
- 26 UI tests (all passing on this exact source) in headless Chromium over `file://` with a **test-only** mock Android bridge (first move as Black and as White, strength options reaching the engine, promotion, checkmate, undo/flip/hint, AI vs AI, engine crash/retry, missing engine, export, screenshots in requests, AI-model player incl. illegal-reply retry and failure card, key handling, review, resume, back button).
- All 7 Java classes compile against Android API stubs (Java 8 source level); URL-safety policy passes 17 JVM cases.

## Not verified
- Gradle/AGP build, NDK compile of Stockfish, the APK itself, installation and behaviour on a real phone, real Stockfish strength calibration, real API calls (no network was available), HttpTransport and EngineProcess at runtime, Keystore on devices.

## Incomplete / ideas
- Chess clocks and time controls; sound; drag-and-drop moves; x86_64 and 32-bit ARM builds; ARMv8 dot-product build for faster NPS.
