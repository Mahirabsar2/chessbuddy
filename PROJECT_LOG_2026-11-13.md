# ChessBuddy daily progress log — 2026-11-13

## Requirements
- Fresh Android chess app powered by native Stockfish.
- Play, Coach, History/Archive and Settings tabs; polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Correct piece selection and legal move handling: captures, castling, en passant, promotion and undo.
- GPT/OpenAI and Claude API-key settings with secure native storage.
- Every APK must ship with the exact source ZIP used to build it, plus provenance and SHA-256 checksums.

## Repository review
- Repository `Mahirabsar2/chessbuddy`; `main` HEAD `b08d9b5962cb89aec129de984f4ae0afda94d316` (2026-11-12 13:47 UTC).
- Compared with build #15 commit `80ec03208d3646c5e5ebb266a4fd7f3101bdfc90`: 12 commits ahead, 0 behind; all changes are documentation/log/status files. No app source or workflow changes.
- Branches are `main` and `master`; no GitHub Releases. `master` contains only project documentation and root Gradle configuration.
- `main` contains `ChessBuddy-v0.3.0-source.zip` (187,655 bytes) and `ChessBuddy-v0.4.0-source.zip` (226,940 bytes; blob SHA `aeb1fbe6e9d41e1c5c095742061439f109f8e5c8`). The v0.4.0 ZIP is present again despite the earlier deletion.
- Actual ChessBuddy 4.0 source ZIP and expanded app source directory are absent. The v0.4.0 archive is only the old test baseline.
- CI still downloads, validates and packages the fixed v0.4.0 ZIP, hardcodes `versionName '0.4.0'`, and runs only `node tests/run-all.js`.

## Files, builds and tests
- No app source, APK or new source ZIP was produced today; no new build or tests were run.
- Latest verified Actions run: #15 / ID `42623107658`, **SUCCESS for v0.4.0 test build only**. All 18 job steps succeeded.
- Verified logic tests: **70/70 passed** — coach 9, coaches/clock 6, engine 14, perft 5 positions, prompts 13, review/openings 10, strength/models 13.
- Stockfish sf_19 compiled for arm64 with NDK 27.2.12479018; Gradle release build and APK verification succeeded.
- APK: `com.chessbuddy`, versionCode 1015, versionName `0.4.0`, 79,749,986 bytes; SHA-256 `7d42dc7bf1ef51599ec99c6406d8a868c21f71e739e2433cbe9da3d5c75ec214`.
- Artifact `ChessBuddy-build-15`, ID `13677721762`, contains the APK, matching v0.4.0 ZIP, build info, verification, Stockfish provenance and SHA-256 manifest. It is not expired; expiry 2026-11-23 13:12:42 UTC.
- Playwright UI, Java policy, physical-device, live-provider and on-device API-key persistence tests remain unverified.

## Blockers
- Actual 4.0 source and matching ZIP are missing; current CI can only build v0.4.0.
- The v0.4.0 ZIP contains `app/sideload.keystore` with a documented default password `android`; treat it as exposed and exclude it from future archives.
- CI generates a new ephemeral signing key each run, preventing consistent update-install continuity.
- `SecretStore` can fall back to app-private plaintext storage if Keystore encryption fails.
- UI interaction and physical-device behavior have not been verified, so piece-selection fixes cannot be signed off from the logic suite alone.

## Exact next steps
1. Upload Claude's actual 4.0 source and exact matching versioned ZIP to a clearly identified branch/commit.
2. Inspect the archive and internal Gradle version; verify it is genuinely new 4.0 source and contains no exposed keystore.
3. Review the implementation against every requirement; fix and test piece selection and legal move behavior.
4. Update CI to build and package that exact ZIP, pin its checksum, and run logic, Playwright UI and Java policy suites.
5. Remove the plaintext fallback and configure persistent private signing via GitHub Secrets.
6. Run Stockfish NDK, Gradle/APK, signature and UI checks; inspect the artifact for the exact matching ZIP, provenance and checksums.
7. Install on Android and verify both play modes, board interactions, live OpenAI/Claude requests and API-key save/reload.
