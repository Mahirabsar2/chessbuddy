# ChessBuddy daily progress log — 2026-11-15

## Required scope
- Fresh Android chess app powered by native Stockfish.
- Play, Coach, History/Archive and Settings tabs; polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Reliable piece selection and legal moves: captures, castling, en passant, promotion and undo.
- GPT/OpenAI and Claude API-key settings with secure Android Keystore storage.
- Every release must include the exact source ZIP used for its APK, with provenance and SHA-256 checksums.

## Repository review
- Repository: Mahirabsar2/chessbuddy. Reviewed main HEAD e9b63cfb0ec94b0cffc171e53bfc710eb37efda4 (2026-11-14 13:06:38 UTC).
- Compared with build #15 commit 80ec03208d3646c5e5ebb266a4fd7f3101bdfc90: 18 commits ahead, 0 behind; all changed paths are project logs/status documentation. No app-source or workflow changes since build #15.
- Branches: main, master, chessbuddy-4.0-claude and chessbuddy-5.0-prototype. Both named feature branches still point to 618e48c86ec05721bac4a51d135c8e0af678b777. Their extra v0.4.0-source (1).zip has the same Git blob SHA as the existing v0.4.0 ZIP; neither branch contains new 4.0/5.0 app source.
- main contains only v0.3.0 (187,655 bytes) and v0.4.0 (226,940 bytes) source archives, plus project-level Gradle files/docs. No expanded Android app source tree or genuine 4.0/5.0 source ZIP is present.
- Workflow .github/workflows/android-build.yml remains unchanged (blob SHA b25cdcb13f16cc96c43c8fd3d1c8ede659f98c05). It hardcodes v0.4.0 and runs only node tests/run-all.js.

## Files, builds and tests
- Produced today: PROJECT_LOG_2026-11-15.md; updated PROJECT_LOG.md and PROJECT_STATUS.md. No app source, APK or source archive produced.
- No new Actions run or build/test execution today. Latest Actions run remains #15 / ID 42623107658, commit 80ec03208d3646c5e5ebb266a4fd7f3101bdfc90.
- Rechecked run #15 job metadata and logs: all 18 reported steps succeeded. Logic suite passed 70/70: coach 9, coaches/clock 6, engine 14, perft 5, prompts 13, review/openings 10, strength/models 13.
- Stockfish sf_19 compiled for arm64 using NDK 27.2.12479018; Gradle release APK build and APK verification succeeded.
- APK metadata: com.chessbuddy, versionCode 1015, versionName 0.4.0, 79,749,986 bytes; SHA-256 7d42dc7bf1ef51599ec99c6406d8a868c21f71e739e2433cbe9da3d5c75ec214.
- Artifact ChessBuddy-build-15 (ID 13677721762) contains that APK and the exact v0.4.0 source ZIP used by CI, plus build info, verification, Stockfish provenance and SHA-256 manifest. It remains available and is scheduled to expire 2026-11-23 13:12:42 UTC. This is a v0.4.0 test build, not the real 4.0 release.

## Blockers and verification gaps
- Genuine 4.0/5.0 source and matching archive are missing from all inspected branches.
- CI still builds only v0.4.0; Playwright UI and Java policy suites are not wired into it.
- The old v0.4.0 archive contains app/sideload.keystore; app/build.gradle documents default password android. Treat it as exposed and do not reuse or redistribute it.
- CI creates a fresh ephemeral signing key per run, so APKs do not share a stable update-signing identity.
- SecretStore may fall back to app-private plaintext storage if Keystore encryption fails.
- Physical-device behavior, UI interactions, both play modes, live OpenAI/Claude requests and on-device key save/reload remain unverified.

## Exact next steps
1. Upload the genuine current Claude source and its exact versioned ZIP to a clearly identified branch/commit; do not rename or duplicate v0.4.0.
2. Inspect archive contents, internal Gradle version, SHA-256 and signing files; confirm it is genuinely the intended release source and contains no keystore.
3. Audit tabs/board/pieces, human-vs-AI, AI-vs-AI, selection, complete legal-move handling and OpenAI/Claude settings; fix gaps and remove plaintext fallback.
4. Update CI to build and package that exact ZIP, verify its version/hash, and run logic, Playwright UI and Java policy suites.
5. Remove the exposed keystore from release source and configure a persistent private signing key through GitHub Secrets.
6. Run Stockfish NDK, Gradle/APK, signature, logic and UI checks; inspect the artifact to verify the exact APK/source pair, provenance and checksums.
7. Install on Android and test board interaction, both play modes, provider calls and API-key save/reload.
