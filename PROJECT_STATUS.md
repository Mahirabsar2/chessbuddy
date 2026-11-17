# ChessBuddy project status — reviewed 2026-11-17

## Required product scope
- Fresh Android chess app powered by native Stockfish.
- Play, Coach, Archive/History and Settings tabs; polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Correct piece selection and legal moves, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI and Claude API-key settings with secure Android Keystore storage.
- Every release must include the exact source ZIP used for its APK, plus build provenance and SHA-256 checksums.

## Repository state
- Repository: Mahirabsar2/chessbuddy.
- main HEAD: `f571084c8dfa053ebd5cd9b36fda6e72e6cb848a` (2026-11-17 06:10:35 UTC).
- main contains `ChessBuddy-v0.5.0-source.zip` (239,144 bytes), `ChessBuddy-0.5.0-auth-deeplink-dev-v2.zip`, and older v0.3.0/v0.4.0 archives. No expanded Android app source tree is checked in at the repository root.
- **Main CI mismatch:** `.github/workflows/android-build.yml` still fetches `ChessBuddy-v0.4.0-source.zip`, asserts version 0.4.0, and builds v0.4.0. The v0.5.0 development build workflow is on separate branches.
- Branch `Mahirabsar2-patch-3` HEAD: `24c90e71f5ebf3d9373dc5543976e7eae6bd8352`. It contains `ChessBuddy-0.5.0-account-auth-diagnostics.zip` (278,950 bytes) and `ChessBuddy-v0.5.0-source.zip`.
- The 5.0 final-dev branch builds by applying overlay parts to the v0.5.0 base ZIP; no complete standalone v5.0 source ZIP was found.

## Latest verified development build — v0.5.0, not final 5.0
- GitHub Actions run #37 / ID `44071209046`, branch `Mahirabsar2-patch-3`: **SUCCESS**.
- Workflow extracted `ChessBuddy-0.5.0-account-auth-diagnostics.zip`, checked internal versionName 0.5.0, and built from that extracted source. Source archive SHA-256: `2c2937ade80691f0b1db80ca9477ba7849daf99426f1d2f945b2f607a77406c9`.
- Logic tests: **96/96 passed** — coach 9, coaches/clock 7, engine 16, lichess 2, online server validation 7, online 13, perft 5, prompts 13, review/openings 10, strength/models 14.
- Stockfish sf_19 compiled for arm64 with NDK 27.2.12479018; binary SHA-256 `0470a60d55495faaa56fa4a47a938569abdbeb80cd6b4c12dcc4efc139a11bd6`.
- APK verification: package `com.chessbuddy`, versionCode 1037, versionName 0.5.0, 79,778,392 bytes. APK ZIP integrity, Stockfish packaging and signature checks passed.
- Artifact `ChessBuddy-build-37`, ID `14322817023`, 80,046,593 bytes, uploaded successfully. Workflow packaging step copies the exact source ZIP used for the build beside the APK and includes build info, verification, Stockfish provenance and SHA256 manifest.
- Patch-1 and patch-2 builds #35 and #36 also completed successfully.
- This is a v0.5.0 development/account-auth-diagnostics build, **not a verified 4.0 or 5.0 release**.

## 5.0 development branch status
- Latest reviewed run #43911525393 failed during “Install Playwright and Chromium”: Playwright reports Chromium is unsupported on `ubuntu26.04-x64`.
- Node logic tests and Java policy/bridge compile tests passed before the failure. Headless UI, Deno validation, Stockfish build, APK build and artifact packaging were skipped.
- No complete standalone v5.0 source ZIP or verified v5.0 APK/source artifact exists in the inspected branch.

## Blockers and verification gaps
- Main CI still targets v0.4.0 rather than the available v0.5.0 source.
- No complete v4.0/v5.0 release source ZIP and matching release APK have been verified.
- Playwright/Chromium runner incompatibility blocks the 5.0 UI pipeline.
- Patch-3 source ZIP has not yet been independently inspected for embedded keystores/secrets.
- Current development workflows generate ephemeral signing keys; builds do not share a stable update-signing identity.
- Patch-3 CI did not run Playwright UI or Java policy tests.
- Physical Android behavior, piece-selection UX, both play modes on-device, live OpenAI/Claude calls and API-key save/reload remain unverified.

## Exact next steps
1. Align main CI with an explicitly selected v0.5.0 source ZIP and pin/verify its SHA-256; remove the hard-coded v0.4.0 fetch and version assertion.
2. Inspect the diagnostics and base source ZIP contents, internal version and signing material; exclude all keystores/secrets from distributable source.
3. Pin a Playwright-compatible Ubuntu/browser environment and rerun the 5.0 UI pipeline, Deno validation, logic and Java tests.
4. Produce a complete standalone v5.0 source ZIP from the final patched source tree; build the APK from that same tree and package the exact ZIP alongside it.
5. Configure persistent private signing via GitHub Secrets for update installs; never commit signing material.
6. Install on Android and test tabs/board/piece selection, full legal moves, human-vs-AI, AI-vs-AI, provider requests and API-key save/reload.
7. Inspect the final artifact and verify APK, exact matching source ZIP, provenance and SHA-256 manifest before calling it a release.
