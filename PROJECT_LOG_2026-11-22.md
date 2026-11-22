# ChessBuddy daily progress — 2026-11-22

## Required scope
- Fresh Android chess app powered by native Stockfish.
- Clear tabs and a polished Chess.com-inspired board/pieces.
- Human-vs-AI and AI-vs-AI.
- Correct piece selection and legal moves, including captures, castling, en passant, promotion and undo.
- GPT/OpenAI-compatible and Claude provider/model/API-key settings, with keys protected by Android Keystore-backed encryption.
- Every release must include the exact complete source ZIP used for its APK beside the APK in one artifact, with provenance and SHA-256 checksums.

## Source and branch review
- Repository: `Mahirabsar2/chessbuddy`; default branch: `main`.
- Active Next Gen development branch: `next-gen-1.0.0`, still at HEAD `da20f25c289970e887517a2eb8209d7ed0450ea4` (2026-11-21, “Fix mobile regression test string quoting”). No newer development commit or Next Gen workflow run was found on 2026-11-22.
- The branch root contains five split inputs: Parts 1–4 for Stockfish and Part 5 for app source. The expanded post-overlay app tree is not checked in at the branch root; CI reconstructs it. No standalone final post-overlay source ZIP is present.
- The workflow `.github/workflows/chessbuddy-2.0.0-split-build.yml` still calls the candidate Next Gen 1.0.0 while input archives and workflow filename say 2.0.0.
- The README says the build artifact contains the APK and exact matching source ZIP, but the current Next Gen workflow actually uploads the APK and a separate `.tar.gz` source artifact. The README is inaccurate for this pipeline.
- Default-branch `.github/workflows/android-build.yml` remains pinned to v0.4.0. Its latest run #52 / ID `44779798532` (2026-11-20) succeeded and uploaded `ChessBuddy-build-52` (artifact ID `14651381404`), but it builds v0.4.0 with a temporary personal sideload key. It is not the current Next Gen build.

## Latest verified candidate
- [Next Gen Actions run #98 / ID 44898901503](https://github.com/Mahirabsar2/chessbuddy/actions/runs/44898901503), commit `da20f25c289970e887517a2eb8209d7ed0450ea4`: **SUCCESS**, 2026-11-21. The job is completed with conclusion `success`.
- Verified checks recorded for run #98: 103/103 JavaScript logic tests across 11 suites; Java policy test; Stockfish reassembly/hash verification; Rust JNI and Lc0/BLAS native builds; nine-model Maia manifest validation; ARM64 binary checks; Gradle `assembleRelease`; APK signature verification; mobile/navigation and additional puzzle/study/repertoire regression checks.
- APK size recorded by CI: 82,699,444 bytes. Packaged APK package/version metadata was not independently asserted by the workflow.
- APK artifact: `ChessBuddy-NextGen-1.0.0-preview-apk`, ID `14705436740` (82,614,721-byte artifact).
- Source artifact: `ChessBuddy-NextGen-1.0.0-extracted-source`, ID `14704304757` (224,093,818 bytes), containing `chessbuddy-nextgen-1.0.0-source.tar.gz`.
- These are two separate artifacts; the source is tar.gz, not the required exact matching source ZIP. The preview release contains the APK and checksum but no source ZIP. This is not a release-compliant package.
- No new APK, source archive, code change, or test run was produced on 2026-11-22. The run #98 artifacts remain available; their expiry is 2027-02-19.

## Blockers / verification gaps
- No single exact matching post-overlay source ZIP packaged beside the APK; APK and source are separate artifacts.
- Persistent release signing secrets are absent for run #98; it used a temporary preview keystore. Stable auto-update release publication was skipped.
- No Playwright/browser UI run or physical Android-device test is verified.
- Touch-based piece selection, on-device special moves, complete human-vs-AI and AI-vs-AI flows, live OpenAI/Claude calls, and encrypted API-key save/reload remain unverified.
- Workflow does not independently assert packaged APK package/version/versionCode.
- Full content-based source secret/keystore audit remains outstanding.
- Version naming is inconsistent (2.0.0 inputs/workflow vs Next Gen 1.0.0 candidate); main CI is still v0.4.0.

## Exact next steps
1. Generate a deterministic source ZIP from the exact post-overlay/native-rebuilt tree used by Gradle; do not substitute the input Part 5 ZIP or a tar.gz snapshot.
2. Upload one combined artifact containing the APK, exact matching source ZIP, provenance, APK/source SHA-256 values and a verification report; fail CI if any required file is absent or a hash differs.
3. Extract APK metadata and assert package name, versionName and versionCode before upload.
4. Configure a private persistent release keystore through GitHub Secrets; verify signing continuity and keep preview signing separate.
5. Run Playwright UI tests on a supported runner and install the candidate on a physical Android device.
6. Verify touch selection, captures, castling, en passant, promotion, undo, both play modes, all tabs, live OpenAI/Claude requests and encrypted key save/reload.
7. Run a content-based source secret/keystore audit; align workflow, input ZIP, changelog, README and app version labels.
8. Migrate or clearly isolate the legacy v0.4.0 main workflow so it cannot be mistaken for the Next Gen pipeline.
9. Do not call this a production release until the combined exact APK/source-ZIP artifact, metadata, checksums, persistent signing and device tests are verified.

## Review activity
- Documentation only. No app source, APK or tests were changed/run on 2026-11-22.
