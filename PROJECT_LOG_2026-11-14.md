# ChessBuddy daily progress log — 2026-11-14

## Required scope
- Fresh Android chess app powered by native Stockfish.
- Play, Coach, History/Archive and Settings tabs; polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Correct piece selection and legal moves, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI and Claude API-key settings with secure native storage.
- Every APK release must include the exact source ZIP used to build it, plus provenance and SHA-256 checksums.

## Repository review
- Repository: `Mahirabsar2/chessbuddy`; `main` HEAD `be49bd6515c877a0843256bf5c5eedf1792a35a0` (2026-11-13 13:30:54 UTC).
- `main` is 15 commits ahead of build #15 commit `80ec03208d3646c5e5ebb266a4fd7f3101bdfc90`; the compared paths are documentation/log/status only. No app-source or workflow changes.
- Branches: `main`, `master`, `chessbuddy-4.0-claude`, `chessbuddy-5.0-prototype`.
- Important branch finding: both named feature branches point to the same commit `618e48c86ec05721bac4a51d135c8e0af678b777`. Compared with `main`, that commit adds only `ChessBuddy-v0.4.0-source (1).zip`; its Git blob SHA is identical to the existing v0.4.0 archive (`aeb1fbe6e9d41e1c5c095742061439f109f8e5c8`). These branches do not contain new 4.0 or 5.0 app source.
- `main` contains `ChessBuddy-v0.3.0-source.zip` (187,655 bytes) and `ChessBuddy-v0.4.0-source.zip` (226,940 bytes). No actual 4.0/5.0 source ZIP or expanded Android app source tree is present in the inspected branch trees.
- No GitHub Releases are published.
- CI workflow `.github/workflows/android-build.yml` is unchanged (blob SHA `b25cdcb13f16cc96c43c8fd3d1c8ede659f98c05`): it hardcodes the v0.4.0 ZIP and versionName, and runs only `node tests/run-all.js`. Playwright UI and Java policy suites are not wired into CI.

## Files, builds and tests
- This review produced no app source, APK or source archive. No build or test was run on 2026-11-14.
- Latest verified run remains GitHub Actions #15 / ID `42623107658`, commit `80ec03208d3646c5e5ebb266a4fd7f3101bdfc90`: **SUCCESS for the v0.4.0 test build only**, not actual 4.0/5.0.
- Rechecked run #15 job metadata and logs: all 18 reported steps succeeded; logic tests **70/70 passed** (coach 9, coaches/clock 6, engine 14, perft 5 positions, prompts 13, review/openings 10, strength/models 13); Stockfish sf_19 arm64 compiled with NDK 27.2.12479018; Gradle release build and APK verification succeeded.
- APK: `com.chessbuddy`, versionCode 1015, versionName `0.4.0`, 79,749,986 bytes; SHA-256 `7d42dc7bf1ef51599ec99c6406d8a868c21f71e739e2433cbe9da3d5c75ec214`.
- Artifact `ChessBuddy-build-15`, ID `13677721762`, is still available and expires 2026-11-23 13:12:42 UTC. It contains the v0.4.0 APK and the exact v0.4.0 source ZIP used by that workflow, plus build/provenance/verification/checksum files.
- No newer Actions run exists in the inspected recent run list. UI, Java policy, physical-device, live-provider and on-device API-key persistence tests remain unverified.

## Blockers
- Actual 4.0/5.0 app source and matching archive are missing; the similarly named branches only duplicate the old v0.4.0 ZIP.
- CI still builds v0.4.0 and omits UI/Java policy tests.
- The v0.4.0 archive contains an exposed `app/sideload.keystore`; `app/build.gradle` documents default password `android`. Do not reuse or redistribute this key.
- CI generates a new ephemeral signing key on each run, preventing consistent update installs.
- `SecretStore` can fall back to app-private plaintext storage if Keystore encryption fails.
- Device behavior, both play modes, UI interactions, real OpenAI/Claude requests and secure key persistence are not verified.

## Exact next steps
1. Upload the actual current Claude source and its exact versioned source ZIP to a clearly identified branch/commit; do not upload another copy of v0.4.0 under a new name.
2. Inspect the ZIP contents, Gradle version metadata and SHA-256; confirm it is genuinely the intended 4.0/5.0 source and contains no keystore.
3. Audit tabs/board/pieces, human-vs-AI, AI-vs-AI, piece selection, full legal-move handling and OpenAI/Claude settings; fix gaps and use Android Keystore without plaintext fallback.
4. Update CI to build and package that exact ZIP, verify its checksum and version, and run logic, Playwright UI and Java policy suites.
5. Configure a persistent private signing key through GitHub Secrets; remove the exposed keystore from source packages.
6. Run Stockfish NDK, Gradle/APK, signature, logic and UI checks; inspect the artifact to confirm the APK and matching ZIP are the exact same source version with provenance and checksums.
7. Install on Android and verify board interaction, both play modes, provider calls and API-key save/reload.
