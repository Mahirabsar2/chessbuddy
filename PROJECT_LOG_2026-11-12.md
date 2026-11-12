# ChessBuddy daily progress log — 2026-11-12

## Requirements
- Build a fresh Android chess app powered by native Stockfish.
- Provide Play, Coach, History/Archive and Settings tabs with a polished Chess.com-inspired board and pieces.
- Support human-vs-AI and AI-vs-AI.
- Fix piece selection and enforce legal moves, including captures, castling, en passant, promotion and undo.
- Include GPT/OpenAI and Claude API-key settings with secure native storage.
- Ship every APK with the exact source ZIP used to build it, plus provenance and SHA-256 checksums.

## Repository review
- Repository: `Mahirabsar2/chessbuddy`; reviewed `main` HEAD `1635c71670fe2e821f5829aa38bee41fe8c6da91` (2026-11-11 13:05 UTC).
- Compared with build #15 commit `80ec03208d3646c5e5ebb266a4fd7f3101bdfc90`: 9 commits ahead, 0 behind. The comparison shows documentation-only changes (5 documentation/status files); no app source or workflow changes.
- Branches: `main` and `master`. The inspected `master` tree has no app source, source ZIP or workflow.
- `main` still contains `ChessBuddy-v0.3.0-source.zip` (187,655 bytes) and `ChessBuddy-v0.4.0-source.zip` (226,940 bytes). The actual ChessBuddy 4.0 ZIP and expanded app source tree are missing.
- CI still downloads, validates and packages the fixed v0.4.0 ZIP and checks `versionName '0.4.0'`.

## Files, builds and tests
- No app source, APK or source archive was produced today; no tests or build were run today.
- Latest verified build remains Actions run #15 / ID `42623107658`, commit `80ec032`: **SUCCESS for the v0.4.0 test build only**, not actual 4.0.
- Historical run #15 results: logic tests **70/70 passed**; Stockfish sf_19 compiled for Android arm64 with NDK 27.2.12479018; Gradle release APK build and APK verification succeeded.
- APK: `com.chessbuddy`, versionCode 1015, versionName `0.4.0`, 79,749,986 bytes; SHA-256 `7d42dc7bf1ef51599ec99c6406d8a868c21f71e739e2433cbe9da3d5c75ec214`.
- Artifact `ChessBuddy-build-15`, ID `13677721762`, remains available (not expired at review) and includes the APK, matching v0.4.0 ZIP, build information, verification, Stockfish provenance and SHA-256 manifest. Expiry: 2026-11-23 13:12:42 UTC.
- The workflow runs `node tests/run-all.js`; Playwright UI and Java policy suites are not wired into CI. Physical-device, live-provider and on-device API-key persistence checks remain unverified.

## Blockers
- Actual 4.0 source and matching ZIP are absent; the workflow can only build v0.4.0.
- The v0.4.0 archive was previously inspected and found to contain `app/sideload.keystore` with documented default password `android`; treat it as exposed and exclude it from future source packages.
- CI uses a fresh ephemeral signing key per run, so APKs do not support normal update-install continuity.
- `SecretStore` has a plaintext fallback if Keystore encryption fails; runtime behavior has not been device-verified.

## Exact next steps
1. Upload Claude's actual 4.0 source and its exact versioned ZIP to a clearly identified branch/commit; confirm the archive contents and internal version metadata.
2. Review the 4.0 code against every requirement; fix and test piece selection and legal move handling.
3. Update CI to build and package that exact ZIP, then run logic, Playwright UI and Java policy suites.
4. Remove the exposed keystore from future source packages, remove the plaintext fallback, and configure persistent private signing through GitHub Secrets.
5. Run Stockfish NDK, Gradle/APK, signature, logic and UI checks; inspect the artifact to verify the exact APK/source pairing, provenance and checksums.
6. Install on Android and verify board interactions, both play modes, live OpenAI/Claude requests and API-key save/reload.
