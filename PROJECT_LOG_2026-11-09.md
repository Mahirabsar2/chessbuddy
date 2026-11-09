# ChessBuddy daily progress log — 2026-11-09

## Current requirements
- Fresh Android chess app powered by native Stockfish.
- Clear Play, Coach, History/Archive and Settings tabs; polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Reliable piece selection and legal move handling, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI and Claude API-key settings, with secure native storage.
- Every release artifact must contain the exact source ZIP used to build its APK, plus provenance and SHA-256 checksums.

## Current repository and source
- Repository: `Mahirabsar2/chessbuddy`; branch: `main`.
- Latest head reviewed: `80ec03208d3646c5e5ebb266a4fd7f3101bdfc90`.
- Available source ZIPs: `ChessBuddy-v0.3.0-source.zip` (187,655 bytes) and `ChessBuddy-v0.4.0-source.zip` (226,940 bytes).
- No ChessBuddy 4.0 source ZIP or expanded 4.0 app source is present. The v0.4.0 ZIP's Git blob SHA remains `aeb1fbe6e9d41e1c5c095742061439f109f8e5c8`; its internal Gradle version is 0.4.0.
- The v0.4.0 ZIP was deleted in commit `1287325`, then reappeared unchanged in the later `80ec032` tree.
- CI still hardcodes v0.4.0 and does not run the separate Playwright UI suite or Java policy tests.

## Files and versions produced
- Latest verified artifact: `ChessBuddy-build-15` (artifact ID `13677721762`).
- APK: `ChessBuddy-v0.4.0-build15-arm64.apk`, package `com.chessbuddy`, versionCode 1015, versionName 0.4.0, 79,749,986 bytes.
- APK SHA-256: `7d42dc7bf1ef51599ec99c6406d8a868c21f71e739e2433cbe9da3d5c75ec214`.
- Matching source: `ChessBuddy-v0.4.0-build15-source.zip` (226,940 bytes).
- Artifact also contains `BUILD_INFO.txt`, `VERIFIED_CHECKS.txt`, `STOCKFISH_PROVENANCE.txt` and `SHA256SUMS.txt`.
- Artifact expires 2026-11-23 13:12:42 UTC.
- This is still a **v0.4.0 test build**, not the actual ChessBuddy 4.0 release.

## Tests and build results
- GitHub Actions run #15 / ID `42623107658`: **SUCCESS** for commit `80ec032`.
- Logic tests: **70/70 passed** (coach 9, coaches/clock 6, engine 14, perft 5, prompts 13, review/openings 10, strength/models 13).
- Stockfish sf_19 built for arm64 using NDK 27.2.12479018. Source commit: `edb0d9db6731067ec50ce619ff372b463bc4dd5d`.
- Gradle release build succeeded; APK ZIP integrity, packaged assets, native Stockfish binary and APK signature all verified.
- Artifact contents were downloaded and inspected; the APK and exact v0.4.0 source ZIP are both present.
- Not run/verified: Playwright UI suite, Java policy suite, physical Android device tests, live API calls, API-key persistence on a device.

## Review findings and blockers
- The uploaded commit named “4.0 release / hi” did not add a new source archive. The old v0.4.0 archive remains byte-identical by Git blob SHA.
- The workflow still downloads, validates and packages v0.4.0.
- The source archive includes `app/sideload.keystore`; the Gradle file documents its default password as `android`. Treat this key as exposed and remove it from future source packages.
- CI creates a new ephemeral signing key each run. Builds therefore cannot update-install over one another. Configure a persistent private key in GitHub Secrets.
- API-key storage uses Android Keystore AES-GCM when available but falls back to app-private plaintext when unavailable; device behavior has not been tested.

## Exact next steps
1. Upload Claude's actual 4.0 source and exact matching ZIP; verify internal version metadata and new content.
2. Review the 4.0 source against every product requirement and correct selection/move-legality bugs.
3. Update CI to build/package the exact 4.0 ZIP and run logic, Playwright UI and Java policy tests.
4. Remove the committed sideload keystore; configure persistent signing securely via GitHub Secrets.
5. Run and record the native Stockfish build, Gradle APK build, APK/signature checks and full test suites.
6. Inspect the artifact for the APK, exact matching source ZIP, provenance and checksums.
7. Install on Android and verify both play modes, board interactions, real provider calls and API-key save/reload.
