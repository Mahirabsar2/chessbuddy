# ChessBuddy project status — reviewed 2026-11-20

## Required product scope
- Fresh Android chess app powered by native Stockfish.
- Play, Coach, Archive/History and Settings tabs; polished Chess.com-inspired board and pieces using original ChessBuddy assets.
- Human-vs-AI and AI-vs-AI.
- Reliable piece selection and legal moves, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI-compatible and Claude provider/model/API-key settings; API keys encrypted with Android Keystore.
- Every release must include the exact complete source ZIP used for its APK in the same artifact, with provenance and SHA-256 checksums.

## Repository and current source
- Repository: [Mahirabsar2/chessbuddy](https://github.com/Mahirabsar2/chessbuddy).
- Active development branch: `chessbuddy-3.0.0`, HEAD `c217a62bf377849848e032ef5a38d00b781c236b`.
- The branch contains five split input archives named `ChessBuddy-2.0.0-Part1-Stockfish.zip` through `Part4-Stockfish.zip` and `Part5-Source.zip`. CI validates the ZIPs, extracts Part5, applies `repairs/apply_repairs.py`, and reassembles Stockfish.
- Extracted Gradle source: package `com.chessbuddy`, versionName `3.0.0`, versionCode formula `10000 + GITHUB_RUN_NUMBER`. The APK downloaded from run #27 was independently parsed: package `com.chessbuddy`, versionName `3.0.0`, versionCode `10027`.
- Version naming remains inconsistent: split inputs, `CHANGELOG-2.0.0.md`, and `docs/2.0.0_IMPLEMENTATION_STATUS.md` still identify 2.0.0; workflow/APK identify 3.0.0.
- Main HEAD at review: `71ea6c6a23e80725b12b4f64961bbdf48a449ece`. Main's `.github/workflows/android-build.yml` still downloads `ChessBuddy-v0.4.0-source.zip`, asserts version 0.4.0, and builds that legacy version.

## Latest verified build — 3.0.0 CI candidate
- [Actions run #27 / ID 44725957133](https://github.com/Mahirabsar2/chessbuddy/actions/runs/44725957133), commit `c217a62bf377849848e032ef5a38d00b781c236b`: **SUCCESS**, 2026-11-20.
- All five split source ZIP integrity checks passed.
- Stockfish reassembly/hash verification passed: `0470a60d55495faaa56fa4a938569abdbeb80cd6b4c12dcc4efc139a11bd6`.
- JavaScript logic tests: **103/103 passed** across 11 suites; rebuild startup/home/version/avatar smoke check passed.
- Java policy test: `OK PolicyTest`.
- Gradle `assembleRelease`: **BUILD SUCCESSFUL**.
- APK signature verification passed for v1 and v2. Downloaded APK manifest independently confirms package `com.chessbuddy`, versionName `3.0.0`, versionCode `10027`.
- APK includes arm64 `libstockfish.so`, `liblc0.so`, `libchessbuddy_core.so`, and `libc++_shared.so`.
- This proves a successful CI candidate build, not a production release or physical-device verification.

## Artifacts from run #27
- `ChessBuddy-3.0.0-release-apk`, artifact ID `14622884616`, 81,495,901 bytes; contains only `ChessBuddy-3.0.0-release.apk`.
- `ChessBuddy-3.0.0-extracted-source`, artifact ID `14623243658`, 164,110,532 bytes; contains only `chessbuddy-3.0.0-source.tar.gz` (198 files), captured after repair overlay and Stockfish reassembly.
- APK SHA-256: `021e9e39ef4a05e96c14669a036fa209fc385cd9f2077f0d567e77a8d6410bd9`.
- Source tar.gz SHA-256: `ec0c99ca63ccba944b17373b1d99f9595c51eb581f5a60c47e696fa78d2bd348`.
- Artifact ZIP digests: APK `f281aa4d94f71a6345bb4faedd2627f94ab389747dc512eca0cdb436d3a8e008`; source `76510cc71040d88e1d2510733a183d9e25ac9eb2781a0df40fba31a7e29e1487`.
- **Release packaging is not compliant yet:** APK and source are separate artifacts; source is tar.gz, not the required exact matching source ZIP. There is no single combined APK + source ZIP + provenance/checksum artifact.

## Implemented in source; runtime verification still needed
- Play/Coach/Archive/Settings navigation, human-vs-AI and AI-vs-AI mode selection, Stockfish and Maia/Lc0 paths.
- Claude and OpenAI-compatible provider configuration and AES-GCM API-key storage backed by Android Keystore; writes fail closed if encryption is unavailable.
- Legal-move/perft and provider request tests are present. They do not verify touch-selection behavior, real provider calls, or key persistence on a physical device.
- Current repair overlay makes startup authentication mandatory and hides the offline guest path; account/session restoration needs live backend/device verification.
- A filename scan found no obvious keystore or environment-secret files in the extracted source. A full content-based secret scan remains outstanding.

## Blockers / verification gaps
- Exact matching source ZIP is not bundled with the APK; two separate artifacts were uploaded.
- Signing uses a temporary CI-generated key, unsuitable for stable update installs.
- Workflow does not assert APK package/version metadata before upload; the downloaded APK was checked independently after the run.
- `tests/run-all.js` runs pure Node logic tests. The separate `tests/ui/ui.test.js` is not invoked; no Playwright/browser UI or physical Android test was run.
- Piece-selection UX, on-device special moves, both play modes end-to-end, live OpenAI/Claude calls and key save/reload, Supabase auth/profile/session restore, and two-device online play remain unverified.
- Main CI remains pinned to v0.4.0. The 3.0.0 branch still carries 2.0.0 source/document labels.
- No production release is certified.

## Exact next steps
1. Generate a deterministic complete source ZIP from the exact post-repair, Stockfish-reassembled tree used by Gradle.
2. Bundle that ZIP, the verified APK, provenance, APK/source SHA-256 values and a verification report into one artifact; fail CI if any required file is missing.
3. Add an in-workflow assertion for package `com.chessbuddy`, versionName `3.0.0`, and expected versionCode.
4. Use a persistent private signing key from GitHub Secrets; never commit or expose signing material.
5. Run browser UI tests on a supported runner and physical Android tests for tabs, board selection, special moves, both play modes, provider calls, key persistence and startup authentication.
6. Perform a full source ZIP secret scan and align 2.0.0/3.0.0 source filenames, changelog and implementation docs.
7. Keep main's v0.4.0 workflow explicitly labelled legacy or migrate it deliberately.
8. Do not call this a release until the combined artifact, signing continuity, metadata, checksums and device tests are verified.

## Daily records
- [2026-11-20](PROJECT_LOG_2026-11-20.md)
- [2026-11-19](PROJECT_LOG_2026-11-19.md)
- [2026-11-18](PROJECT_LOG_2026-11-18.md)
- [2026-11-17](PROJECT_LOG_2026-11-17.md)
- Earlier entries remain in [PROJECT_LOG.md](PROJECT_LOG.md).
