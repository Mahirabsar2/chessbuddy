# ChessBuddy project status — reviewed 2026-11-15

## Release distinction
- Actual ChessBuddy 4.0/5.0 source is not present in any inspected repository branch.
- Latest verified APK is v0.4.0 / Actions build #15. It is a test build only, not the real 4.0 release.

## Required product scope
- Fresh Android chess app powered by native Stockfish.
- Play, Coach, History/Archive and Settings tabs; polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Correct piece selection and legal moves, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI and Claude API-key settings with secure Android Keystore storage.
- Every release must include the exact source ZIP used for the APK, plus provenance and SHA-256 checksums.

## Repository state
- Repository: Mahirabsar2/chessbuddy. Current main HEAD: e9b63cfb0ec94b0cffc171e53bfc710eb37efda4 (2026-11-14 13:06:38 UTC).
- Compared with build #15 commit 80ec03208d3646c5e5ebb266a4fd7f3101bdfc90: 18 commits ahead, 0 behind; changes are documentation/log/status only.
- Branches: main, master, chessbuddy-4.0-claude, chessbuddy-5.0-prototype. Both named feature branches point to 618e48c86ec05721bac4a51d135c8e0af678b777 and contain only a duplicate v0.4.0 ZIP, not new app source.
- main contains v0.3.0 source ZIP (187,655 bytes) and v0.4.0 source ZIP (226,940 bytes). No expanded Android app source tree or genuine 4.0/5.0 archive is present.
- CI workflow .github/workflows/android-build.yml is unchanged and hardcodes v0.4.0. It runs node tests/run-all.js only; Playwright UI and Java policy suites are not wired into CI.
- No GitHub Release or newer Actions run was found.

## Latest verified test build — not 4.0
- Actions run #15 / ID 42623107658, commit 80ec03208d3646c5e5ebb266a4fd7f3101bdfc90: SUCCESS.
- Verified job metadata/logs: all 18 reported steps succeeded; logic tests 70/70 passed (coach 9, coaches/clock 6, engine 14, perft 5, prompts 13, review/openings 10, strength/models 13).
- Stockfish sf_19 compiled for arm64 with NDK 27.2.12479018; Gradle release build and APK verification succeeded.
- APK: package com.chessbuddy, versionCode 1015, versionName 0.4.0, 79,749,986 bytes; SHA-256 7d42dc7bf1ef51599ec99c6406d8a868c21f71e739e2433cbe9da3d5c75ec214.
- Artifact ChessBuddy-build-15, ID 13677721762, contains the APK, exact v0.4.0 source ZIP used by CI, build info, verification, Stockfish provenance and SHA-256 manifest. It expires 2026-11-23 13:12:42 UTC.
- No build or tests were run on 2026-11-15; no new app source, APK or source archive was produced.

## Blockers and verification gaps
- Genuine 4.0/5.0 source is missing; current feature branches only duplicate v0.4.0.
- Old v0.4.0 source archive contains app/sideload.keystore; app/build.gradle documents default password android. Treat it as exposed and exclude it from future source packages.
- CI generates a new ephemeral signing key each run, preventing consistent update installs.
- SecretStore may fall back to app-private plaintext storage if Keystore encryption fails.
- Not verified: Playwright UI, Java policy, physical Android behavior, both play modes on-device, live OpenAI/Claude requests, API-key save/reload or persistent signing/update installs.

## Exact next steps
1. Upload the genuine current Claude source and its exact versioned ZIP to a clearly identified branch/commit; do not rename or duplicate v0.4.0.
2. Inspect archive contents, internal version, SHA-256 and signing files; confirm the source is genuinely the intended release and contains no keystore.
3. Audit/fix tabs, board/pieces, human-vs-AI, AI-vs-AI, piece selection, full legal-move handling and provider settings; remove plaintext fallback.
4. Update CI to build/package that exact ZIP, verify its hash/version, and run logic, Playwright UI and Java policy suites.
5. Remove exposed signing material from source packages and configure persistent private signing through GitHub Secrets.
6. Run Stockfish NDK, Gradle/APK, signature, logic and UI checks; verify the artifact contains the exact APK/source pair, provenance and checksums.
7. Install on Android and verify board interactions, both play modes, real provider calls and API-key save/reload.
