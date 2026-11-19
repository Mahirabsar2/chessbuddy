# ChessBuddy daily progress — 2026-11-19

Reviewed at 2026-11-19 19:45 Asia/Dhaka. Repository: [Mahirabsar2/chessbuddy](https://github.com/Mahirabsar2/chessbuddy).

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
