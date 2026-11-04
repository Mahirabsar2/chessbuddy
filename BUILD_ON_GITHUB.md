# Build and install ChessBuddy

## Current repository setup

The repository workflow currently builds from the versioned source archive at the repository root:

- Source archive: `ChessBuddy-v0.4.0-source.zip`
- App version: `0.4.0`
- Workflow: `.github/workflows/android-build.yml`

A push to `main`/ `master` that changes build inputs, or a manual run from **Actions → Build ChessBuddy APK → Run workflow**, starts the build. Documentation-only changes are excluded from automatic builds.

## Downloading a build

1. Open the repository's **Actions** tab.
2. Open the successful **Build ChessBuddy APK** run.
3. Download its `ChessBuddy-build-N` artifact and extract it.

The artifact contains:
- the arm64 APK;
- the exact source ZIP used for that APK;
- `BUILD_INFO.txt` and Stockfish provenance;
- `VERIFIED_CHECKS.txt`;
- `SHA256SUMS.txt`.

Actions artifacts are temporary. The current verified build #12 expires **2026-11-17 13:58:42 UTC**. Download and retain the APK and matching source ZIP together.

Latest verified run: https://github.com/Mahirabsar2/chessbuddy/actions/runs/41648945256

## Building a future version

The workflow currently pins the v0.4.0 archive URL and checks that the extracted Gradle project declares versionName `0.4.0`. To release a new source version:

1. Add the new versioned source ZIP to the repository root.
2. Update the archive URL, extraction filename, version check and source-ZIP copy name in `.github/workflows/android-build.yml`.
3. Confirm the ZIP's Gradle versionName matches the workflow check.
4. Commit the source archive and workflow change; inspect the resulting Actions run and artifact.

Never pair an APK with a different source archive. Keep the exact archive used for that build in the same artifact and verify its checksum.

## Signing limitation

**The current workflow generates a fresh ephemeral sideload signing key for every run.** It does not currently read persistent signing-key secrets. APKs from later runs therefore cannot be assumed to update-install over earlier APKs.

Before distributing update builds, add workflow support for user-owned GitHub Actions secrets:
- `CB_KEYSTORE_BASE64`
- `CB_KEYSTORE_PASSWORD`
- `CB_KEY_ALIAS`
- `CB_KEY_PASSWORD`

Then configure those secrets with a securely backed-up signing key. Do not publish the keystore or its passwords. Until persistent signing support is implemented and verified, treat each build as a separate personal sideload build.

## Supported device

The current build targets 64-bit ARM (`arm64-v8a`). x86 Android emulators are not supported by this build.

## If a build fails

Open the failed Actions run, select the failed step and share the final relevant log lines. Do not report a build as successful unless the run conclusion is success and the verification/package steps completed.
