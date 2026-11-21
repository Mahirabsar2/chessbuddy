# ChessBuddy daily progress — 2026-11-21

## Required scope
- Fresh Android chess app powered by native Stockfish.
- Clear tab navigation and a polished Chess.com-inspired board/piece experience.
- Human-vs-AI and AI-vs-AI.
- Correct piece selection and legal move handling, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI-compatible and Claude provider/model/API-key settings; keep keys in Android Keystore-backed encrypted storage.
- Every release must ship the exact complete source ZIP used to build its APK beside that APK, with provenance and SHA-256 checksums.

## Latest source reviewed
- Repository: `Mahirabsar2/chessbuddy`.
- Current development branch: `next-gen-1.0.0`, HEAD `da20f25c289970e887517a2eb8209d7ed0450ea4` — “Fix mobile regression test string quoting”.
- The branch contains five split inputs: Parts 1–4 for Stockfish and Part 5 for app source. All are still named `ChessBuddy-2.0.0-Part*-*.zip`. CI extracts Part 5, applies the repair/Next Gen overlays, rebuilds native components and assembles the Android app. The expanded app tree is reconstructed during CI; it is not checked in at the branch root.
- No complete standalone, final post-overlay source ZIP is present in the branch. The CI source snapshot is a `.tar.gz`, not the required ZIP.
- Workflow filename `.github/workflows/chessbuddy-2.0.0-split-build.yml`, input ZIPs and changelog still use 2.0.0 naming while the workflow/preview candidate is Next Gen 1.0.0. The overlay step checks for Gradle `versionName '1.0.0'`.
- Default branch `main` remains a legacy path: `.github/workflows/android-build.yml` is still pinned to v0.4.0. Do not confuse its build with the current Next Gen branch.

## Latest verified CI candidate
- [GitHub Actions run #98](https://github.com/Mahirabsar2/chessbuddy/actions/runs/44898901503), commit `da20f25c289970e887517a2eb8209d7ed0450ea4`: **SUCCESS**, 2026-11-21.
- All five input ZIP integrity checks passed; source extraction and all Next Gen overlays completed.
- Rust JNI core, Lc0/BLAS and Maia runtime built; nine-model Maia manifest normalized/validated; Stockfish was reassembled and hash-verified (`0470a60d55495faaa56fa4a938569abdbeb80cd6b4c12dcc4efc139a11bd6`). Native ARM64 checks passed for Stockfish, Lc0 and the ChessBuddy core.
- Original character portraits/voice media were installed and checked.
- Main JavaScript logic suite: **103/103 passed** across 11 suites. Additional workflow checks passed: authenticated online/realtime subscription checks; Puzzle Rush (8 FENs); Study Lab (9 courses, 128 legal half-moves and 4 tablebase endgames); repertoire/gambit checks (101 opening lines, 49 gambit/mating courses, 372 legal plies and 960 Chess960 layouts); five-tab navigation, Game Review layout, startup-auth and mobile Profile/Stats/Settings/responsive-layout checks.
- Java policy test: `OK PolicyTest`.
- Gradle `assembleRelease`: **BUILD SUCCESSFUL**. APK signature verification passed. APK size: **82,699,444 bytes**. The workflow checked the Gradle source for `versionName '1.0.0'`, but did not independently dump/assert the packaged APK's package name/version metadata.
- Earlier run #97 failed in `tests/logic/mobile-experience.test.js:49` with a JavaScript quoting `SyntaxError`; commit `da20f25` corrected the test string and run #98 passed the complete pipeline.

## Files and artifacts produced
- Preview APK artifact: `ChessBuddy-NextGen-1.0.0-preview-apk`, artifact ID `14705436740` (artifact ZIP 82,614,721 bytes; APK 82,699,444 bytes).
- Extracted-source artifact: `ChessBuddy-NextGen-1.0.0-extracted-source`, artifact ID `14704304757` (224,093,818 bytes); contains `chessbuddy-nextgen-1.0.0-source.tar.gz` made from the reconstructed build tree.
- [Preview release](https://github.com/Mahirabsar2/chessbuddy/releases/tag/nextgen-1.0.0-preview-build98) contains `ChessBuddy-NextGen-1.0.0-preview.apk` and its `.sha256` file.
- **Release packaging requirement is not met:** APK and source are separate Actions artifacts; the source is tar.gz, not the exact matching source ZIP, and the preview release has no source ZIP. No single APK + matching source ZIP + provenance/checksum bundle was produced.
- No new complete source ZIP was produced today.

## Blockers / verification gaps
- Persistent signing secrets were empty. The persistent-signing step was skipped; CI generated a temporary preview keystore. The stable in-app-update release step was skipped. This APK is preview-only and cannot be treated as a stable update build.
- The separate Playwright/browser UI suite is not run by this workflow. The mobile-experience test is a Node-based regression/static check, not a real Android UI session.
- No physical Android-device test is verified. Touch-based piece selection, special-move UX, full human-vs-AI and AI-vs-AI gameplay, cold-start/session behavior and device performance remain unverified.
- Source tests cover legal move generation/perft and AI move validation, but do not prove the touch-selection bug is fixed on-device.
- OpenAI/Claude provider configuration is described in the source README and provider logic is tested; live provider calls and Android Keystore API-key save/reload have not been verified on a device.
- No APK manifest metadata assertion is present in the workflow. A full content-based secret/keystore scan of the final reconstructed source snapshot remains outstanding.
- Version naming remains inconsistent (2.0.0 input/workflow filenames vs Next Gen 1.0.0 candidate); main CI remains v0.4.0.

## Exact next steps
1. After all overlays and native reassembly, generate a deterministic complete source ZIP from the exact tree used by Gradle.
2. Put that ZIP, the APK, provenance, APK/source SHA-256 values and a verification report in one Actions artifact; fail CI if any required file is absent or hashes mismatch.
3. Add APK package/version/versionCode extraction and assertions before upload.
4. Configure one persistent private release keystore through GitHub Secrets; verify signing continuity and keep preview signing clearly separate.
5. Run Playwright UI tests on a supported runner and install the candidate on a physical Android device.
6. Verify board selection, captures, castling, en passant, promotion, undo, human-vs-AI, AI-vs-AI, all tabs, OpenAI/Claude requests and encrypted key save/reload.
7. Run a full source secret/keystore audit and align workflow, input ZIP, changelog and app version names. Explicitly label or migrate the legacy v0.4.0 main workflow.
8. Do not call this a production release until the combined exact APK/source-ZIP artifact, metadata, checksums, persistent signing and device tests are verified.

## Review activity
- No app code or APK was changed by this review. This entry records the already completed run #98 and the remaining release gates.
