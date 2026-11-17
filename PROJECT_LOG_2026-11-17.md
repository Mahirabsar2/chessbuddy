# ChessBuddy daily progress log — 2026-11-17

## Required scope
- Fresh Android chess app powered by native Stockfish.
- Play, Coach, Archive/History and Settings tabs; polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Reliable piece selection and legal moves, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI and Claude API-key settings with secure Android Keystore storage.
- Every release must include the exact source ZIP used for its APK, plus provenance and SHA-256 checksums.

## Repository and source review
- Repository: Mahirabsar2/chessbuddy. main HEAD: f571084c8dfa053ebd5cd9b36fda6e72e6cb848a (2026-11-17 06:10:35 UTC).
- main now contains ChessBuddy-v0.5.0-source.zip (239,144 bytes) and ChessBuddy-0.5.0-auth-deeplink-dev-v2.zip, in addition to v0.3.0/v0.4.0 archives. There is still no expanded Android source tree at the repository root.
- Important mismatch: main's .github/workflows/android-build.yml still downloads v0.4.0, checks versionName 0.4.0, and builds that archive. The successful v0.5.0 builds below ran on development branches, not main.
- Latest patch branch: Mahirabsar2-patch-3 at 24c90e71f5ebf3d9373dc5543976e7eae6bd8352. It contains ChessBuddy-0.5.0-account-auth-diagnostics.zip (278,950 bytes; Git blob 28c4f12edb6363c9d4567fa590d2d4cc0c90c7e9) and the v0.5.0 base source ZIP.
- Patch-3 workflow explicitly extracts the diagnostics ZIP, checks versionName 0.5.0, builds from that extracted tree, and copies that same input ZIP beside the APK. Logged source ZIP SHA-256: 2c2937ade80691f0b1db80ca9477ba7849daf99426f1d2f945b2f607a77406c9.
- The 5.0 final-dev branch still assembles changes by applying overlay parts to the v0.5.0 base ZIP; no complete standalone v5.0 source ZIP was found.

## Builds, files and tests
- Latest successful v0.5.0 development build: GitHub Actions run #37 / ID 44071209046 on Mahirabsar2-patch-3 — SUCCESS. Job steps confirm test execution, Stockfish build, APK build/verification, APK + matching input source ZIP packaging and artifact upload all succeeded.
- Logic tests: 96/96 passed — coach 9, coaches/clock 7, engine 16, lichess 2, online server validation 7, online 13, perft 5, prompts 13, review/openings 10, strength/models 14.
- Stockfish sf_19 compiled for Android arm64 with NDK 27.2.12479018; binary SHA-256 0470a60d55495faaa56fa4a47a938569abdbeb80cd6b4c12dcc4efc139a11bd6.
- APK verification passed: package com.chessbuddy, versionCode 1037, versionName 0.5.0, size 79,778,392 bytes; ZIP integrity, embedded arm64 Stockfish and APK signature checks passed.
- Artifact ChessBuddy-build-37 (ID 14322817023; 80,046,593 bytes) uploaded successfully. Workflow packages the exact diagnostics ZIP used for the build alongside the APK, plus BUILD_INFO, verification, Stockfish provenance and SHA256SUMS.
- Patch-1 and patch-2 Actions runs #35 (ID 44056553118) and #36 (ID 44064647343) also completed successfully.
- The 5.0 final-dev run #43911525393 failed at “Install Playwright and Chromium”: Playwright reports Chromium is unsupported on ubuntu26.04-x64. Node logic tests and Java policy/bridge compile tests passed; UI, Deno validation, Stockfish build, APK build and packaging were skipped.
- No physical Android device test or live OpenAI/Claude API/key-persistence test is verified. Patch-3 CI did not run Playwright UI or Java policy tests.

## Blockers and verification gaps
- main CI is stale and still builds v0.4.0, despite the v0.5.0 source and successful v0.5.0 development artifacts.
- No complete v4.0/v5.0 release source ZIP or verified 5.0 APK/source pair is present.
- 5.0 UI CI is blocked by the Playwright/Chromium runner compatibility failure.
- Latest v0.5.0 build is a development/account-auth-diagnostics build, not a final release.
- Patch-3 source archive contents have not yet been independently inspected for embedded signing material; inspect before distributing it.
- CI uses an ephemeral signing key, so builds do not share a stable update-signing identity.
- Board selection and move interactions, both modes on-device, real provider calls, API-key save/reload and persistent update installs remain unverified.

## Exact next steps
1. Make the intended v0.5.0 source/workflow explicit on main; remove the hard-coded v0.4.0 fetch/version check and ensure the selected archive is pinned by SHA-256.
2. Inspect the full diagnostics/base ZIP contents and verify the internal version, source completeness and absence of keystores/secrets before distribution.
3. Fix the 5.0 Playwright runner by pinning a supported Ubuntu image or compatible browser version; rerun UI tests, Deno validation, logic and Java suites.
4. Produce a complete standalone v5.0 source ZIP from the final patched source tree, then build the APK from that same tree and package that exact ZIP beside it.
5. Replace ephemeral release signing with a private persistent signing key supplied through GitHub Secrets; keep signing material out of source archives.
6. Install on Android and test tabs/board/piece selection, legal moves, human-vs-AI, AI-vs-AI, OpenAI/Claude requests and API-key save/reload.
7. Inspect the final artifact and verify APK + exact matching source ZIP + provenance + SHA-256 manifest before calling it a release.
