# Get your APK in 3 steps (no computer tools needed)

1. **Create a repository** on github.com (New repository, private is fine).
2. **Upload this folder's contents**: *Add file → Upload files*, then drag in *everything inside* the `ChessBuddy` folder
   (including the `.github` folder; on a Mac press Cmd+Shift+. in Finder to show it). Commit.
   Uploading triggers the build automatically on `main`/`master`.
3. Open the **Actions** tab → **Build ChessBuddy APK**. Wait about 10–15 minutes for the green tick, open the run and download
   the artifact `ChessBuddy-build-N` (or open **Releases** on the repo page for direct links).
   Unzip → install `ChessBuddy-v…-arm64.apk` on an Android phone (allow "install unknown apps").

You get: the APK, the exact source ZIP, `BUILD_INFO.txt`, `VERIFIED_CHECKS.txt` (what the build really checked), `STOCKFISH_PROVENANCE.txt`, `SHA256SUMS.txt`.

## If the build fails
Open the failed run, click the red step, copy the last ~60 lines of its log and send them to me. Typical culprits: NDK/SDK version names, the Stockfish `make` step.

## Updating the app later
Each build has a higher version code and is signed with the same key, so a new APK installs over the old one and keeps your games and settings.

## Signing with your own key (optional)
Repository → Settings → Secrets and variables → Actions: `CB_KEYSTORE_BASE64` (base64 of your .jks/.keystore), `CB_KEYSTORE_PASSWORD`, `CB_KEY_ALIAS`, `CB_KEY_PASSWORD`.
Without them the workflow uses `app/sideload.keystore` (password `android`) – a public throwaway key, fine for personal installs, **not for Google Play**.

## Phones
64-bit ARM (arm64-v8a), Android 6.0+ (API 23). Practically every phone since 2017. Android emulators on PCs (x86) are not supported by this build.

## Other ways
Android Studio: open the folder, run `scripts/build_stockfish_android.sh` first (needs the NDK, Linux/macOS shell), then Build → Build APK.
