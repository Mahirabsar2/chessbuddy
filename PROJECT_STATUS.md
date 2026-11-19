# ChessBuddy project status — reviewed 2026-11-19

## Required product scope
- Fresh Android chess app powered by native Stockfish.
- Play, Coach, Archive/History and Settings tabs; polished Chess.com-inspired board and pieces.
- Human-vs-AI and AI-vs-AI.
- Reliable piece selection and legal moves, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI-compatible and Claude provider/API-key settings with secure Android Keystore storage.
- Every release must include the exact source ZIP used for its APK in the same artifact, with build provenance and SHA-256 checksums.

## Repository and source state
- Repository: `Mahirabsar2/chessbuddy`; main documentation is updated separately from the active build branch.
- Active 2.0.0 development branch: `chessbuddy-2.0.0-rebuild`, HEAD `22474e7358f18f381957c4b29d09f452dbfc6677` (“Fix online move sync and clock reconciliation”).
- Five split source ZIPs (Part1–Part5) are present on that branch. The workflow validates each ZIP, extracts Part5, applies `repairs/apply_repairs.py`, and reassembles Stockfish from Parts1–4. The expanded app source is reconstructed in CI rather than checked into the branch root.
- README/changelog describe version 2.0.0 and the intended product features. Those claims still require UI/device/live-service verification.

## Latest verified build — 2.0.0 CI candidate
- GitHub Actions run #13 / ID `44535399591`, commit `22474e7358f18f381957c4b29d09f452dbfc6677`: **SUCCESS**, 2026-11-19.
- All five input ZIP integrity checks passed.
- Stockfish reassembly/hash verification passed: `0470a60d55495faaa56fa4a47a938569abdbeb80cd6b4c12dcc4efc139a11bd6`.
- JavaScript logic tests: **102/102 passed**; startup/home/version/avatar smoke test passed.
- Java policy test: `OK PolicyTest`.
- Gradle `assembleRelease`: **BUILD SUCCESSFUL**; APK signature verification passed using APK Signature Scheme v2.
- Artifacts uploaded: APK artifact ID `14536355615` (81,494,454 bytes) and extracted-source artifact ID `14536315530` (164,098,591 bytes).
- The source artifact contains a `.tar.gz` snapshot of the post-repair/reassembled working tree. The APK and source are separate Actions artifacts.
- **Not a release-certified pair:** there is no exact matching source ZIP packaged beside the APK, no combined release bundle/linked checksum manifest, and signing uses a temporary CI key. CI did not independently dump/assert APK package/version metadata.
- [Run #13](https://github.com/Mahirabsar2/chessbuddy/actions/runs/44535399591).

## Other CI baseline and mismatches
- Main branch `.github/workflows/android-build.yml` remains hardcoded to download and assert `ChessBuddy-v0.4.0-source.zip`; it is not the 2.0.0 workflow.
- The 2.0.0 workflow runs on `chessbuddy-2.0.0-rebuild` and produces two separate artifacts; its current packaging does not satisfy the exact-source-ZIP-beside-APK requirement.

## Blockers and verification gaps
- Exact matching source ZIP is not bundled with the APK; no single artifact contains both plus provenance/checksums.
- Temporary signing key is unsuitable for stable update installs.
- Playwright/browser UI tests and physical Android testing are not verified by run #13.
- Live Supabase OAuth/email recovery/profile flows, live Lichess calls, two-device multiplayer, human-vs-AI/AI-vs-AI on-device, piece-selection UX, and OpenAI/Claude live calls/key persistence remain unverified.
- Source ZIP secret/signing-material audit and APK package/version extraction remain outstanding.

## Exact next steps
1. Generate a deterministic ZIP from the exact post-repair, Stockfish-reassembled source tree used by Gradle.
2. Bundle that ZIP, the APK, provenance, SHA-256 manifest and verification report in one artifact; fail CI unless both APK and source ZIP are present.
3. Extract APK metadata and assert expected package/version 2.0.0.
4. Use a persistent private signing identity from GitHub Secrets; do not commit signing material.
5. Run Playwright UI tests on a supported runner, then physical-device tests for tabs, board/piece selection, special moves, both play modes, API providers and key persistence.
6. Audit the final source ZIP for secrets/keystores and verify its checksum against the build provenance.
7. Align main CI with a selected current version or clearly label it as a legacy v0.4.0 workflow.

## Daily records
- [2026-11-19](PROJECT_LOG_2026-11-19.md)
- [2026-11-18](PROJECT_LOG_2026-11-18.md)
- [2026-11-17](PROJECT_LOG_2026-11-17.md)
- Earlier entries remain in [PROJECT_LOG.md](PROJECT_LOG.md).
