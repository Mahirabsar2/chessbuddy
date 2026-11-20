## 2026-11-18 — latest source upload and release-candidate review
- Reviewed main HEAD `a8741119c5279b3250f4cbff17f8768abc3b7e39` (2026-11-18 11:51:08 UTC). The latest commit adds `ChessBuddy-2.0.0-Part1-Stockfish.zip` (Git blob `a19fd393abf12a604b5d0b18413d538182015c95`). The binary fetch returned an empty payload, so its contents/version cannot be inspected; no complete 2.0.0 source ZIP or matching APK is verified.
- Reviewed patch-7 HEAD `05afe3caac9bcf3cdf98bea6ddd330039af4aa6c`. Its candidate source archive `ChessBuddy-v1.0.0-rc1-lc0-patch5-rustfix-source-1.zip` is 319,941 bytes with 205 entries and contains the full app tree, tests, Rust core, Stockfish/Lc0 scripts and Supabase functions. Archive filename suggests v1.0.0-rc1, but internal Gradle version was not independently confirmed. ZIP filename scan found no obvious keystore/JKS/P12/.env/credential files; this is not a complete source-text secret audit.
- Patch-7 workflow runs Node logic tests and Maia/static checks, builds Stockfish, Lc0/Maia and Rust, then Gradle-builds/verifies and packages the same source ZIP with provenance/checksums. It omits Playwright UI, Java policy and Deno tests, uses ephemeral signing, and no successful patch-7 run was verified.
- Main workflow remains pinned to v0.4.0. The 5.0 final-dev run #43911525393 failed installing Playwright/Chromium on ubuntu26.04-x64; Node logic and Java policy/bridge compile tests passed, later UI/Deno/native/APK/artifact steps were skipped.
- Re-verified v0.5.0 development build #37 / run ID `44071209046`: all job steps succeeded, 96/96 logic tests passed, Stockfish sf_19 arm64 built, APK verification passed, and artifact `ChessBuddy-build-37` (ID `14322817023`) contains the exact v0.5.0 diagnostics source ZIP used for that build plus APK/provenance/checksums. APK versionCode 1037, versionName 0.5.0. Artifact expires 2026-12-01 11:09:33 UTC. This is not a final 1.0.0/2.0.0/4.0/5.0 release.
- No new APK or test result was produced/verified today. Exact next steps are recorded in `PROJECT_STATUS.md` and `PROJECT_LOG_2026-11-18.md`.

## Requirements retained
- Fresh Android chess app with native Stockfish.
- Play, Coach, Archive/History and Settings tabs; polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Correct selection and legal moves, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI-compatible and Claude provider/API-key settings, with keys held in Android Keystore.
- Every release must ship the exact source ZIP used for its APK in the same release artifact, with provenance and SHA-256 checksums.

## Latest source reviewed
- Current development branch: `chessbuddy-2.0.0-rebuild`, HEAD `22474e7358f18f381957c4b29d09f452dbfc6677` — “Fix online move sync and clock reconciliation”.
- The branch contains five source parts: Part1–Part4 Stockfish payloads and Part5 app source. CI successfully checked all five ZIPs. The app tree is reconstructed during CI from Part5, then the repair overlay is applied and Stockfish is reassembled; the expanded app source is not checked into the branch root.
- `README.md` and `CHANGELOG-2.0.0.md` describe the 2.0.0 candidate and its features. These are source/documentation claims, not proof of on-device behavior.

## Verified CI — 2.0.0 run #13
- [GitHub Actions run #44535399591](https://github.com/Mahirabsar2/chessbuddy/actions/runs/44535399591), commit `22474e7358f18f381957c4b29d09f452dbfc6677`: **completed / success** on 2026-11-19.
- All five input ZIP integrity checks passed.
- Stockfish reassembly/hash verification passed: `0470a60d55495faaa56fa4a47a938569abdbeb80cd6b4c12dcc4efc139a11bd6`.
- JavaScript logic suites: **102/102 passed** (coach, coaches/clock, engine, Lichess, online auth/move validation, online, perft, prompts, review/openings, strength/models). Startup/home/version/avatar smoke test passed.
- Java policy test: `OK PolicyTest`.
- Gradle `assembleRelease`: **BUILD SUCCESSFUL**. APK signature verification passed with APK Signature Scheme v2.
- Workflow job and artifact uploads completed successfully. This verifies a CI build, not a production-ready release or physical-device test.

## Artifacts produced
- `ChessBuddy-2.0.0-release-apk`, artifact ID `14536355615`, 81,494,454 bytes.
- `ChessBuddy-2.0.0-extracted-source`, artifact ID `14536315530`, 164,098,591 bytes. Workflow creates a `.tar.gz` source snapshot inside this artifact after applying repairs and reassembling Stockfish.
- **Release packaging requirement is not yet met:** the APK and source snapshot are separate Actions artifacts; the source snapshot is tar.gz, not the required exact matching source ZIP beside the APK. No single combined APK + source-ZIP + provenance/checksum artifact was produced.
- CI generated a temporary signing key. This is not a persistent update-signing identity.
- The workflow verified APK signature validity but did not independently dump/assert the APK package name and version metadata.

## Blockers / unverified
- No single exact matching source ZIP is packaged beside the APK; no combined release bundle or linked SHA-256 manifest.
- Temporary CI signing key prevents reliable signed updates across builds.
- Playwright/browser UI suite and physical Android tests were not run in this workflow.
- Live Supabase OAuth/email recovery/profile flows, live Lichess requests, two-device multiplayer, both play modes on-device, piece-selection UX, and OpenAI/Claude live calls plus key save/reload remain unverified.
- Main branch CI still fetches and asserts v0.4.0; it is not aligned with this 2.0.0 branch workflow.
- No production release should be claimed from this run.

## Exact next steps
1. In the 2.0.0 workflow, create one deterministic source ZIP from the exact post-repair, Stockfish-reassembled tree used by Gradle.
2. Package that ZIP, the verified APK, build provenance, APK/source SHA-256 values and verification report together in one artifact; assert both files are present before upload.
3. Extract APK metadata and assert expected package/version (2.0.0) before upload.
4. Replace temporary signing with a private, persistent signing identity supplied through GitHub Secrets; never commit the keystore.
5. Run browser UI tests on a supported Playwright runner and install/test on Android: tabs, piece selection, all special moves, human-vs-AI, AI-vs-AI, provider requests and API-key persistence.
6. Audit the final source ZIP for secrets/signing material and verify its hash matches the source used by the APK build.
7. Align or clearly isolate main CI so it cannot be mistaken for the current 2.0.0 pipeline.


## 2026-11-20 — 3.0.0 CI candidate verified; release packaging still blocked
- Reviewed active branch `chessbuddy-3.0.0`, HEAD `c217a62bf377849848e032ef5a38d00b781c236b`. Five split input ZIPs (still named 2.0.0 Parts 1–5) passed integrity checks; CI extracts Part5, applies the repair overlay and reassembles Stockfish.
- Verified [Actions run #27](https://github.com/Mahirabsar2/chessbuddy/actions/runs/44725957133): all steps completed successfully. JavaScript logic tests 103/103 passed across 11 suites; rebuild smoke check passed; Java policy test passed; Stockfish hash verified; Gradle assembleRelease succeeded; APK v1/v2 signature checks passed.
- Downloaded and inspected the APK: manifest package `com.chessbuddy`, versionName `3.0.0`, versionCode `10027`. APK SHA-256 `021e9e39ef4a05e96c14669a036fa209fc385cd9f2077f0d567e77a8d6410bd9`.
- Artifacts: APK artifact `14622884616` (81,495,901 bytes) contains only the APK; source artifact `14623243658` (164,110,532 bytes) contains only a 198-file `.tar.gz` source snapshot. Source tar SHA-256 `ec0c99ca63ccba944b17373b1d99f9595c51eb581f5a60c47e696fa78d2bd348`. These are separate artifacts and the source is not the required exact matching ZIP, so this is not release-compliant.
- Source review confirms Play/Coach/Archive/Settings navigation, human-vs-AI and AI-vs-AI selection, Stockfish/Maia paths, Claude/OpenAI-compatible provider settings, and AES-GCM Android Keystore key storage. Physical-device behavior, piece-selection UX, live provider calls/key persistence and backend auth remain unverified.
- The workflow generates a temporary signing key; it does not assert APK metadata before upload; it does not run the separate UI test file or Playwright/device tests. Main CI remains pinned to v0.4.0. Branch source names/docs still say 2.0.0 while the APK is 3.0.0.
- Exact next steps: generate a deterministic complete source ZIP from the post-repair/Stockfish tree; bundle it with APK/provenance/checksums in one artifact; add metadata assertions; use persistent signing from GitHub Secrets; run browser and physical Android tests; complete secret scan; align 2.0.0/3.0.0 labels and isolate or migrate legacy main CI.
