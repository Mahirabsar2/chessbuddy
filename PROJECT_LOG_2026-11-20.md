# ChessBuddy daily progress — 2026-11-20

Reviewed at 2026-11-20 19:29 Asia/Dhaka. Repository: [Mahirabsar2/chessbuddy](https://github.com/Mahirabsar2/chessbuddy).

## Requirements retained
- Fresh Android chess app powered by native Stockfish.
- Play, Coach, Archive/History and Settings tabs, with a polished Chess.com-inspired board and pieces (original ChessBuddy implementation, not a proprietary clone).
- Human-vs-AI and AI-vs-AI.
- Reliable piece selection and legal moves, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI-compatible and Claude API/model settings; store API keys encrypted with Android Keystore.
- Every release must include the exact complete source ZIP used to build its APK in the same artifact, plus provenance and SHA-256 checksums.

## Current source and version
- Active development branch: `chessbuddy-3.0.0`, HEAD `c217a62bf377849848e032ef5a38d00b781c236b` — “Add startup auth CI build checklist”.
- The branch contains five split inputs named `ChessBuddy-2.0.0-Part1-Stockfish.zip` through `Part4-Stockfish.zip` and `Part5-Source.zip`. CI checked all five archives successfully, extracts Part5, applies `repairs/apply_repairs.py`, and reassembles Stockfish.
- The extracted build source sets package `com.chessbuddy`, `versionName 3.0.0`, and `versionCode 10000 + GITHUB_RUN_NUMBER`. The downloaded APK manifest was independently parsed: package `com.chessbuddy`, versionName `3.0.0`, versionCode `10027` for run #27.
- Naming is inconsistent: source inputs, `CHANGELOG-2.0.0.md`, and `docs/2.0.0_IMPLEMENTATION_STATUS.md` still say 2.0.0 while the workflow and APK are 3.0.0.
- Main remains a separate legacy branch. Its `.github/workflows/android-build.yml` still downloads `ChessBuddy-v0.4.0-source.zip` and asserts version 0.4.0. Main HEAD at review: `71ea6c6a23e80725b12b4f64961bbdf48a449ece`.

## Latest verified CI build — 3.0.0
- [GitHub Actions run #27 / ID 44725957133](https://github.com/Mahirabsar2/chessbuddy/actions/runs/44725957133), branch `chessbuddy-3.0.0`, commit `c217a62bf377849848e032ef5a38d00b781c236b`: **completed successfully** on 2026-11-20.
- Five split source ZIP integrity checks passed; Stockfish was reassembled and hash-verified: `0470a60d55495faaa56fa4a47a938569abdbeb80cd6b4c12dcc4efc139a11bd6`.
- JavaScript logic tests: **103/103 passed** across 11 suites (coach 9, coaches/clock 8, engine 17, Lichess 2, online authentication 9, online move validation 6, online 7, perft 5, prompts 13, review/openings 11, strength/models 16).
- Rebuild smoke check passed (startup, home actions, native TTS bridge, bot profiles, version and 265 vector bot portraits).
- Java policy test: `OK PolicyTest`.
- Gradle `assembleRelease`: **BUILD SUCCESSFUL**.
- APK signature verification passed for v1 and v2. The APK was independently downloaded and inspected; it contains arm64 libraries `libstockfish.so`, `liblc0.so`, `libchessbuddy_core.so`, and `libc++_shared.so`.
- Earlier startup-auth attempts #22–25 failed; runs #26 and #27 then completed successfully. The latest successful run is #27.

## Files and artifacts produced by run #27
- APK artifact: `ChessBuddy-3.0.0-release-apk`, ID `14622884616`, 81,495,901 bytes. It contains only `ChessBuddy-3.0.0-release.apk`.
- Source artifact: `ChessBuddy-3.0.0-extracted-source`, ID `14623243658`, 164,110,532 bytes. It contains only `chessbuddy-3.0.0-source.tar.gz` (198 files), captured after repair overlay and Stockfish reassembly.
- APK SHA-256: `021e9e39ef4a05e96c14669a036fa209fc385cd9f2077f0d567e77a8d6410bd9`.
- Source tar.gz SHA-256: `ec0c99ca63ccba944b17373b1d99f9595c51eb581f5a60c47e696fa78d2bd348`.
- GitHub artifact ZIP digests: APK `f281aa4d94f71a6345bb4faedd2627f94ab389747dc512eca0cdb436d3a8e008`; source `76510cc71040d88e1d2510733a183d9e25ac9eb2781a0df40fba31a7e29e1487`.
- **Release packaging requirement is still NOT met:** APK and source are separate artifacts, and the source snapshot is tar.gz rather than the required exact matching source ZIP. No combined APK + source ZIP + provenance/checksum artifact exists.

## Code review observations
- Source contains Play/Coach/Archive/Settings navigation, human-vs-AI and AI-vs-AI mode selection, Stockfish and Maia/Lc0 engine paths, Claude and OpenAI-compatible provider configuration, and AES-GCM API-key storage using Android Keystore with fail-closed writes.
- Source-level tests cover chess perft/legal move behavior and provider request construction. These do not prove touch selection, real provider calls, or persistence on a physical device.
- The current repair overlay makes the startup account gate mandatory and hides the offline guest path. The expected sign-in/session-restore UX still needs device/backend verification.
- A filename scan of the extracted source found no obvious `.jks`, `.keystore`, `.p12`, `.pfx`, or `.env` files. This is not a complete source-text secret audit.

## Blockers / verification gaps
- Exact matching source ZIP is not bundled beside the APK; artifacts are split.
- Signing uses a newly generated temporary CI key, not a persistent private update-signing identity.
- The workflow does not assert APK package/version metadata before upload (metadata was verified after downloading this APK).
- `tests/run-all.js` runs pure Node logic tests; the separate `tests/ui/ui.test.js` is not invoked by this workflow. No Playwright/browser UI or physical Android test was run.
- Piece-selection UX, special-move interaction on-device, human-vs-AI and AI-vs-AI end-to-end, live OpenAI/Claude requests and API-key save/reload, Supabase auth/profile/restore, and two-device online play remain unverified.
- Main CI is still pinned to v0.4.0; 3.0.0 source names/docs still carry 2.0.0 labels.
- No production release is certified by this CI run.

## Exact next steps
1. In the 3.0.0 workflow, generate a deterministic complete source ZIP from the exact post-repair, Stockfish-reassembled tree used by Gradle.
2. Put that ZIP, the verified APK, build provenance, both SHA-256 values and a verification report in **one** artifact; fail the workflow unless both files and checksums are present.
3. Add an in-workflow APK metadata assertion for package `com.chessbuddy`, versionName `3.0.0`, and the expected versionCode.
4. Replace temporary signing with a persistent private key supplied only through GitHub Secrets; never commit or log signing material.
5. Run the UI test suite on a supported browser runner, then install on Android and test tabs, board selection, all special moves, both play modes, AI models, API-key save/reload, and startup authentication.
6. Run a full secret scan on the final source ZIP and align all 2.0.0/3.0.0 filenames, changelog and implementation docs.
7. Keep main's v0.4.0 workflow clearly labelled legacy or deliberately migrate it; do not let it be mistaken for the 3.0.0 pipeline.
8. Call it a release only after the combined APK/source-ZIP artifact, signing continuity, metadata, checksums and device tests are verified.
