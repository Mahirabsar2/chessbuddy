# ChessBuddy project status — reviewed 2026-11-22

## 2026-11-22 review delta
- No newer Next Gen source commit or workflow run exists after branch HEAD `da20f25c289970e887517a2eb8209d7ed0450ea4` and successful run #98 / ID `44898901503` (2026-11-21). No new build or tests were run on 2026-11-22.
- Rechecked run #98 job and artifacts: success; APK artifact `14705436740` and separate source artifact `14704304757`. The latter contains `chessbuddy-nextgen-1.0.0-source.tar.gz`, not a matching source ZIP. Both artifacts remain available until 2027-02-19.
- Reconfirmed the default-branch workflow still downloads/asserts v0.4.0. Main run #52 / ID `44779798532` succeeded on 2026-11-20 and uploaded `ChessBuddy-build-52` (ID `14651381404`), but uses a temporary personal sideload key and is a legacy v0.4.0 build.
- README packaging instructions do not match the Next Gen workflow: README claims a matching source ZIP in the build artifact; Next Gen CI uploads the APK and a separate tar.gz source artifact.
- Release blockers and exact next steps remain as listed below: combined exact APK/source ZIP, metadata assertions, persistent signing, Playwright/device tests, source secret audit and version/workflow alignment.

## Required product scope
- Fresh Android chess app powered by native Stockfish.
- Clear tabs and a polished Chess.com-inspired board/piece experience.
- Human-vs-AI and AI-vs-AI.
- Correct piece selection and legal moves, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI-compatible and Claude provider/model/API-key settings, with API keys protected by Android Keystore-backed encryption.
- Every release must include the exact complete source ZIP used for its APK beside the APK in one artifact, with provenance and SHA-256 checksums.

## Current source and branch
- Repository: https://github.com/Mahirabsar2/chessbuddy
- Current development branch: next-gen-1.0.0, HEAD da20f25c289970e887517a2eb8209d7ed0450ea4.
- CI reconstructs the app from five split input ZIPs: Parts 1–4 contain Stockfish payloads and Part 5 contains app source. It extracts Part 5, applies the repair/Next Gen overlays, rebuilds native components and then builds the APK. The expanded app source is not checked in at the branch root.
- No complete standalone post-overlay source ZIP is present. CI currently creates a .tar.gz source snapshot instead.
- Naming is inconsistent: input ZIPs and workflow filename still say 2.0.0, while the workflow and preview candidate are Next Gen 1.0.0. The overlay checks for Gradle versionName 1.0.0.
- Default branch main remains a legacy path: .github/workflows/android-build.yml is still pinned to v0.4.0. Do not mistake its build for the current Next Gen pipeline.

## Latest verified CI candidate
- [GitHub Actions run #98 / ID 44898901503](https://github.com/Mahirabsar2/chessbuddy/actions/runs/44898901503), commit da20f25c289970e887517a2eb8209d7ed0450ea4: **SUCCESS**, 2026-11-21.
- All five input ZIP integrity checks, source extraction and overlays passed.
- Rust JNI core, Lc0/BLAS and Maia runtime built; nine-model Maia manifest validated; Stockfish reassembly/hash verification passed (0470a60d55495faaa56fa4a938569abdbeb80cd6b4c12dcc4efc139a11bd6). Native ARM64 checks passed for Stockfish, Lc0 and ChessBuddy core.
- Character portraits and voice media were installed and checked.
- JavaScript logic suite: **103/103 passed** across 11 suites. Additional checks passed for online/realtime subscriptions, Puzzle Rush (8 FENs), Study Lab (9 courses, 128 legal half-moves, 4 tablebase endgames), repertoire/gambit (101 opening lines, 49 gambit/mating courses, 372 legal plies, 960 Chess960 layouts), five-tab navigation, Game Review layout, startup auth and mobile Profile/Stats/Settings/responsive checks.
- Java policy test: OK PolicyTest.
- Gradle assembleRelease: **BUILD SUCCESSFUL**. APK signature verification passed. APK size: 82,699,444 bytes. Workflow checks the Gradle source for versionName 1.0.0 but does not independently assert packaged APK package/version metadata.
- Run #97 failed at tests/logic/mobile-experience.test.js:49 due to a JavaScript string-quoting SyntaxError. Commit da20f25 corrected the test string; run #98 passed.

## Artifacts from run #98
- Preview APK artifact: ChessBuddy-NextGen-1.0.0-preview-apk, ID 14705436740 (82,614,721 bytes; contained APK is 82,699,444 bytes).
- Extracted-source artifact: ChessBuddy-NextGen-1.0.0-extracted-source, ID 14704304757 (224,093,818 bytes), containing chessbuddy-nextgen-1.0.0-source.tar.gz.
- [Preview release](https://github.com/Mahirabsar2/chessbuddy/releases/tag/nextgen-1.0.0-preview-build98) contains the preview APK and its SHA-256 file.
- **Release packaging is not compliant:** APK and source are separate artifacts; source is tar.gz, not the required exact matching source ZIP; no combined APK + source ZIP + provenance/checksum artifact exists.

## Implemented in source; runtime verification still needed
- Source README describes native Stockfish, human-vs-AI, AI-vs-AI, board interaction, Claude/OpenAI-compatible model settings and Android Keystore-backed API-key storage.
- CI tests legal-move generation/perft, AI move validation, engine behavior, provider request logic, tab/navigation structure, mobile settings/profile checks and several study/puzzle features.
- These checks do not prove touch-based piece selection, special-move UX or full play modes on a physical Android device. Live provider calls and API-key save/reload are also unverified.

## Blockers / verification gaps
- No exact matching source ZIP beside the APK; no combined release artifact.
- Persistent signing secrets are empty. Run #98 used a temporary preview keystore; stable release publication was skipped.
- No Playwright/browser UI suite or physical Android-device test was run.
- Piece-selection touch behavior, on-device special moves, human-vs-AI and AI-vs-AI end-to-end, live OpenAI/Claude requests and encrypted key persistence remain unverified.
- APK package/version/versionCode are not independently asserted from the packaged manifest.
- Full content-based source secret/keystore audit remains outstanding.
- Version labels remain inconsistent; main CI remains v0.4.0.

## Exact next steps
1. Generate a deterministic complete source ZIP from the exact post-overlay/native-rebuilt tree used by Gradle.
2. Bundle that ZIP, the APK, provenance, APK/source SHA-256 values and verification report into one artifact; fail CI if any required file is missing or a hash differs.
3. Extract APK metadata and assert package, versionName and versionCode before upload.
4. Configure one persistent private release keystore through GitHub Secrets and verify signing continuity; keep preview signing separate.
5. Run Playwright UI tests on a supported runner and install the candidate on a physical Android device.
6. Verify board selection, captures, castling, en passant, promotion, undo, both play modes, all tabs, OpenAI/Claude requests and encrypted key save/reload.
7. Audit the final source ZIP for secrets/keystores and align branch, workflow, input ZIP, changelog and app version names. Clearly label or migrate the legacy v0.4.0 main workflow.
8. Do not call this a production release until the combined exact APK/source-ZIP artifact, metadata, checksums, persistent signing and device tests are verified.

## Daily records
- [2026-11-21](PROJECT_LOG_2026-11-21.md)
- [2026-11-20](PROJECT_LOG_2026-11-20.md)
- [2026-11-19](PROJECT_LOG_2026-11-19.md)
- [2026-11-18](PROJECT_LOG_2026-11-18.md)
- Earlier entries remain in [PROJECT_LOG.md](PROJECT_LOG.md).
