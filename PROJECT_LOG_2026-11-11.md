# ChessBuddy daily progress log — 2026-11-11

## Requirements
- Fresh Android chess app powered by native Stockfish.
- Play, Coach, History/Archive and Settings tabs; polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Correct piece selection and legal move handling, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI and Claude API-key settings with secure native storage.
- Every release must include the exact source ZIP used for its APK, plus provenance and SHA-256 checksums.

## Repository and available versions
- Repository: `Mahirabsar2/chessbuddy`; review baseline: `main` HEAD `431786003f4317ecbd82f11496ad0f42f4946a21`.
- Six commits after build #15 are documentation-only; no app source or workflow changes.
- Branches checked: `main` and `master`. No GitHub Releases are published.
- `main` contains `ChessBuddy-v0.3.0-source.zip` (187,655 bytes) and `ChessBuddy-v0.4.0-source.zip` (226,940 bytes). The actual ChessBuddy 4.0 source ZIP and expanded app source tree are absent. `master` also has no app source/archive.
- The v0.4.0 ZIP is present again despite the earlier deletion commit; it is the old test archive, not the real 4.0 source.
- `.github/workflows/android-build.yml` still downloads, validates and packages the fixed v0.4.0 ZIP and checks `versionName '0.4.0'`.

## Latest verified files/build
- No new app source, APK or source archive was produced today.
- Latest verified Actions run remains #15 / ID `42623107658`, commit `80ec03208d3646c5e5ebb266a4fd7f3101bdfc90`: **SUCCESS for v0.4.0 test build only**.
- APK: `ChessBuddy-v0.4.0-build15-arm64.apk`; package `com.chessbuddy`; versionCode 1015; versionName `0.4.0`; 79,749,986 bytes.
- APK SHA-256: `7d42dc7bf1ef51599ec99c6406d8a868c21f71e739e2433cbe9da3d5c75ec214`.
- Artifact `ChessBuddy-build-15`, ID `13677721762`, contains the APK, matching v0.4.0 ZIP, build info, verification record, Stockfish provenance and SHA-256 manifest. It expires 2026-11-23 13:12:42 UTC.

## Tests and verification
- Run #15: all 18 job steps succeeded.
- Logic tests: **70/70 passed** — coach 9, coaches/clock 6, engine 14, perft 5, prompts 13, review/openings 10, strength/models 13.
- Stockfish sf_19 compiled for Android arm64 with NDK 27.2.12479018; Gradle release APK build and APK verification succeeded.
- Run #14 failed because the workflow's fixed v0.4.0 ZIP download returned HTTP 404 while that archive was deleted.
- No build or test was run during this 2026-11-11 review.
- Not verified: Playwright UI suite, Java policy tests, physical Android behavior, live OpenAI/Claude requests, on-device API-key persistence.

## Blockers
- Actual 4.0 source and matching ZIP are missing; CI can only build v0.4.0.
- CI runs only `node tests/run-all.js`; Playwright UI and Java policy suites are not wired into the workflow.
- The v0.4.0 source archive contains `app/sideload.keystore` with documented default password `android`; treat it as exposed and exclude it from future source packages.
- CI creates a fresh ephemeral signing key per run, preventing normal update-install continuity.
- `SecretStore` can fall back to app-private plaintext storage if Keystore encryption fails; runtime behavior is not device-verified.

## Exact next steps
1. Add Claude's actual ChessBuddy 4.0 source and its exact versioned ZIP to a clearly identified branch/commit; verify its contents and internal version metadata.
2. Review the 4.0 implementation against every requirement and fix any piece-selection or legal-move defects.
3. Update CI to build and package that exact ZIP, and run logic, Playwright UI and Java policy suites.
4. Remove the exposed sideload keystore from future source archives; configure persistent private signing through GitHub Secrets and remove the plaintext fallback.
5. Run Stockfish NDK, Gradle/APK, signature, logic and UI checks; inspect the artifact for the exact matching source ZIP, provenance and SHA-256 manifest.
6. Install on Android and verify board interactions, both play modes, live provider requests and API-key save/reload.
