# ChessBuddy project status — reviewed 2026-11-18

## Required product scope
- Fresh Android chess app powered by native Stockfish.
- Play, Coach, Archive/History and Settings tabs; polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Reliable piece selection and legal moves, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI and Claude API-key settings with secure Android Keystore storage.
- Every release includes the exact source ZIP used for its APK, build provenance and SHA-256 checksums.

## Current repository state
- Repository: `Mahirabsar2/chessbuddy`.
- `main` HEAD: `a8741119c5279b3250f4cbff17f8768abc3b7e39` (2026-11-18 11:51:08 UTC).
- Latest main commit adds `ChessBuddy-2.0.0-Part1-Stockfish.zip` (Git blob `a19fd393abf12a604b5d0b18413d538182015c95`). The GitHub file fetch returned an empty binary payload; archive contents, size and internal version are not verified. No complete 2.0.0 source ZIP or matching APK is verified.
- Latest inspectable complete candidate is on `Mahirabsar2-patch-7`, HEAD `05afe3caac9bcf3cdf98bea6ddd330039af4aa6c`: `ChessBuddy-v1.0.0-rc1-lc0-patch5-rustfix-source-1.zip` (319,941 bytes, 205 entries; Git blob `a8a6531092423451136cec244903b8d5aecb6cd1`). It contains the Android app tree, tests, Rust core, Stockfish/Lc0 build scripts and Supabase functions. The internal Gradle version has not been independently read; the workflow prints but does not assert the expected version.
- The patch-7 workflow includes Node logic tests, Maia static integration checks, shell syntax validation, Stockfish/Lc0/Rust builds, Gradle/APK verification and packaging of the same source archive with provenance/checksums. It omits Playwright UI, Java policy and Deno suites, uses ephemeral signing, and has no verified successful Actions result in this review.
- Main CI remains hardcoded to v0.4.0, including its source fetch and version assertion; it does not build the latest Part1 upload or patch-7 candidate.
- The 5.0 final-dev branch uses a v0.5.0 base plus overlays. Run #43911525393 failed at Playwright/Chromium installation on `ubuntu26.04-x64`; Node logic and Java policy/bridge compile tests passed, while UI, Deno, native builds, APK and artifact steps were skipped.

## Latest verified build — development only
- v0.5.0 development build #37 / run ID `44071209046`, branch `Mahirabsar2-patch-3`: SUCCESS.
- Logic tests: 96/96 passed. Stockfish sf_19 arm64 compilation, Gradle release build, APK verification and artifact upload passed.
- APK: package `com.chessbuddy`, versionCode 1037, versionName 0.5.0, 79,778,392 bytes.
- Artifact `ChessBuddy-build-37`, ID `14322817023`, contains the APK, exact diagnostics source ZIP used for the build, build info, verification, Stockfish provenance and SHA256 manifest. Expires 2026-12-01 11:09:33 UTC.
- This is a v0.5.0 development/account-auth-diagnostics build, not a verified 1.0.0, 2.0.0, 4.0 or 5.0 release.
- No new build or tests were verified on 2026-11-18.

## Blockers and verification gaps
- 2.0.0 Part1 payload is not inspectable and no complete source/APK pair is verified.
- Patch-7 1.0.0-rc1 candidate has no verified build result and lacks an exact version assertion.
- Patch-7 workflow omits UI, Java policy and Deno tests; signing is ephemeral.
- 5.0 UI workflow is blocked by Playwright/Chromium incompatibility on the current runner.
- Main CI is stale and builds v0.4.0.
- No physical-device, full board interaction, both play modes on-device, live provider, API-key persistence or stable update-signing test is verified.

## Exact next steps
1. Obtain/assemble the complete 2.0.0 source archive and inspect its version, source tree and security-sensitive files.
2. Select one immutable source ZIP and make CI assert its exact version and SHA-256.
3. Build the APK from that exact source and package the identical ZIP beside it with provenance and SHA256SUMS.
4. Pin a Playwright-compatible runner (for example, Ubuntu 24.04) and run logic, Java, UI, Deno, Stockfish, Lc0/Rust, Gradle and APK checks.
5. Configure persistent private signing through GitHub Secrets; never include signing keys in source.
6. Device-test tabs, board/piece selection, all special legal moves, both play modes, OpenAI/Claude requests and API-key save/reload.
7. Verify the final APK/source pair, provenance, checksums and signing identity before release.
