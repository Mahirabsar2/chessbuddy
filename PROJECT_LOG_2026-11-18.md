# ChessBuddy daily progress log — 2026-11-18

## Required scope
- Fresh Android chess app using native Stockfish.
- Play, Coach, Archive/History and Settings tabs; polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Reliable piece selection and legal moves: captures, castling, en passant, promotion and undo.
- GPT/OpenAI and Claude API-key settings with secure Android Keystore storage.
- Every release must contain the exact source ZIP used for its APK, plus provenance and SHA-256 checksums.

## Repository and source review
- Repository: `Mahirabsar2/chessbuddy`.
- `main` HEAD: `a8741119c5279b3250f4cbff17f8768abc3b7e39` (2026-11-18 11:51:08 UTC). The newest commit adds `ChessBuddy-2.0.0-Part1-Stockfish.zip` (Git blob `a19fd393abf12a604b5d0b18413d538182015c95`). GitHub's file fetch returned an empty binary payload, so its contents, size and internal version could not be inspected. Only Part1 is evidenced; no complete 2.0.0 source ZIP or matching APK is verified.
- Latest inspectable complete source candidate: branch `Mahirabsar2-patch-7`, HEAD `05afe3caac9bcf3cdf98bea6ddd330039af4aa6c` (2026-11-17 16:36:47 UTC). It contains `ChessBuddy-v1.0.0-rc1-lc0-patch5-rustfix-source-1.zip`, Git blob `a8a6531092423451136cec244903b8d5aecb6cd1`, 319,941 bytes and 205 ZIP entries.
- The patch-7 archive contains a full Android app tree, tests, Rust JNI core, Stockfish/Lc0 build scripts, Maia-related assets/docs and Supabase online-move functions. Filename suggests 1.0.0-rc1, but the internal Gradle version was not independently read. Its workflow only prints the versionName; it does not assert an expected value.
- ZIP directory-name scan found no obvious keystore, JKS/P12, .env or credential-named files. This is not a full source-text secret audit.
- Patch-7 workflow runs Node logic tests, Maia integration/static checks and shell syntax validation; builds Stockfish, Lc0/Maia and Rust; then Gradle-builds/verifies the APK and packages the source ZIP with provenance and SHA256SUMS. It does not run the Playwright UI, Java policy or Deno suites. It creates an ephemeral signing key. No successful patch-7 Actions run was verified in this review.
- `main` CI remains stale: `.github/workflows/android-build.yml` downloads/checks/builds v0.4.0 and creates an ephemeral signing key. It does not build the newly uploaded 2.0.0 Part1 archive or the patch-7 candidate.
- The 5.0 final-dev branch still builds from a v0.5.0 base plus overlays. Its latest reviewed workflow run #43911525393 failed while installing Playwright/Chromium on `ubuntu26.04-x64`. Node logic tests and Java policy/bridge compile tests passed; UI, Deno, Stockfish, APK and packaging steps were skipped.

## Verified builds and tests
- No new build or test result was verified on 2026-11-18; no APK was produced by this review.
- Latest verified successful build remains v0.5.0 development build #37 / run ID `44071209046` on `Mahirabsar2-patch-3`.
- Build #37: 96/96 logic tests passed; Stockfish sf_19 compiled for arm64; Gradle APK build and APK/ZIP/signature verification passed. APK: `com.chessbuddy`, versionCode 1037, versionName 0.5.0, 79,778,392 bytes.
- Artifact `ChessBuddy-build-37`, ID `14322817023`, contains the APK, the exact v0.5.0 diagnostics ZIP used by that workflow, build info, verification, Stockfish provenance and SHA256 manifest. It expires 2026-12-01 11:09:33 UTC. This is a development build, not a 1.0.0, 2.0.0, 4.0 or 5.0 release.

## Blockers and verification gaps
- The new 2.0.0 Part1 archive is not inspectable through the current file fetch, and a complete 2.0.0 source archive/APK pair is not verified.
- Patch-7 1.0.0-rc1 candidate has no verified build result; internal version assertion is missing.
- Patch-7 CI omits UI, Java policy and Deno tests; signing remains ephemeral.
- 5.0 UI pipeline is blocked by the Playwright/Chromium runner incompatibility.
- Main CI still builds v0.4.0, not the latest source.
- Physical Android behavior, piece-selection UX, full legal-move cases, both play modes on-device, live OpenAI/Claude requests and API-key save/reload remain unverified.

## Exact next steps
1. Provide the complete 2.0.0 source archive (or all parts plus a verifiable assembly/checksum); inspect it and confirm its internal version and source tree.
2. Choose one immutable source ZIP and branch for the intended build; make CI assert the exact version and SHA-256 rather than merely printing versionName.
3. Ensure the APK is built from that archive and the exact same archive is packaged beside it with build provenance and SHA256SUMS.
4. Pin a Playwright-compatible runner (for example, Ubuntu 24.04) and run logic, Java policy, UI, Deno, Stockfish, Lc0/Rust, Gradle and APK verification.
5. Use a persistent private release key through GitHub Secrets; keep all signing material out of source archives.
6. Install on Android and test tabs/board/piece selection, captures/castling/en passant/promotion/undo, human-vs-AI, AI-vs-AI, provider calls and API-key save/reload.
7. Inspect the final artifact and verify the APK/source pair, provenance, checksums and signing identity before calling it a release.
