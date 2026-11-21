# ChessBuddy Next Gen 1.0.0 — Release Checklist

Last checked: 2026-11-21. This is the live implementation checklist, not a claim of full Chess.com feature parity.

## Implemented in source and verified by build #49

- [x] Five primary destinations: Play, Puzzles, Learn, Watch, More.
- [x] Coach, Archive and Settings remain reachable from More.
- [x] Daily Lichess puzzle screen with legal board input, hints and reset.
- [x] Local structured lesson path and saved completion progress.
- [x] Lichess TV channel discovery and opening live public games.
- [x] Responsive Game Review sheet, consistent action-button sizing, fixed icon bounds and Android safe-area padding.
- [x] Signup-first account gate on cold launch.
- [x] Refresh token stored in Android Keystore-backed encrypted storage and restored on app relaunch.
- [x] Online moves submitted through the server-side `apply-online-move` Edge Function.
- [x] Challenge policy: one active pending challenge per participant and five-minute expiry; authenticated server-side execution.
- [x] Nine Maia-1 model IDs (1100–1900) represented; native build now generates and validates all nine model weights.
- [x] Stockfish, Rust JNI core and Lc0/BLAS ARM64 binaries rebuilt and verified.
- [x] In-app updater code checks releases, verifies SHA-256 and downloads with Android DownloadManager.
- [x] Review-layout, auth/session, chess rules, move validation, engine roster, Maia and Java policy tests pass in build #49.

## Current build #49

- [x] GitHub Actions run #49 completed successfully: `44877811788`.
- [x] JavaScript test suite passed.
- [x] Java policy tests passed.
- [x] Native ARM64 engine checks passed.
- [x] APK signature verification passed.
- [x] APK artifact uploaded: `ChessBuddy-NextGen-1.0.0-preview-apk`, 81,511,023 bytes (~77.7 MiB).
- [ ] This is preview-only signing, not a public stable release.
- [ ] APK is below the requested 200 MiB target.

## Character media — generated, not integrated

- [x] Mittens 1080×1080 original portrait generated with hurt/offended/contained-fury expression.
- [x] Mittens 6.8-second ElevenLabs character voice generated.
- [x] Four-character 2×2 portrait sheet generated (streamer, coach, veteran, prodigy).
- [x] Three additional reusable character voice clips generated (streamer, coach, veteran).
- [ ] Export media files to stable project storage, crop portrait sheet and package files into the APK.
- [ ] Map packaged portraits/voices to real bot profiles and test playback on Android.
- [ ] See `docs/NEXTGEN_MEDIA_ASSETS.md` for generation IDs and voice/character mapping.

## Not complete / release blockers

- [ ] 200 MiB APK goal. Current build is ~77.7 MiB. Do not pad it with meaningless bytes; use real, licensed offline chess resources that are actually usable in-app.
- [ ] Persistent release keystore. GitHub repository secrets `CB_RELEASE_KEYSTORE_BASE64`, `CB_RELEASE_STORE_PASSWORD`, `CB_RELEASE_KEY_ALIAS` and `CB_RELEASE_KEY_PASSWORD` are not configured. Without one stable signing identity, Android cannot install later builds as in-place updates.
- [ ] Android requires the package-installer confirmation for sideloaded updates; the app can check and download automatically but cannot silently bypass Android's confirmation.
- [ ] Physical Android-device verification of cold launch/signup, persistent login, Maia UCI startup and gameplay has not been performed.
- [ ] Two-device online game testing for challenge, move sync, clock drift, reconnect and finish states remains outstanding.
- [ ] Online game updates still use REST polling; Supabase Realtime publication is not enabled, so instant push sync is not yet complete.
- [ ] Full translated UI strings and RTL layout review are not complete.
- [ ] Full rated puzzle ladder, Puzzle Rush, Puzzle Battle, custom/theme-based offline puzzles and puzzle-history sync are not complete.
- [ ] Full lesson library, animated coach, long-form courses and cross-device progress sync are not complete.
- [ ] Friends/followers, messaging, clubs, tournaments, spectator chat, event feeds and synced achievements are not complete.
- [ ] Full opening explorer database and advanced variation study workspace are not complete.
- [ ] Verified generated portrait/audio bytes are not yet packaged into the Android app.
- [ ] Supabase leaked-password protection remains disabled; enable it in the project Auth security settings before public launch.

## Release acceptance gates

1. Final branch CI passes from the exact release commit.
2. Persistent signing secrets are configured and the release is signed with the same keystore for every subsequent version.
3. APK is at least 209,715,200 bytes because of useful chess content, not padding.
4. All media assets are bundled, mapped to profiles and verified on a physical Android device.
5. Maia model loading and move output are tested on-device for all nine levels.
6. Online play is tested with two physical devices, including reconnect and server-authoritative clocks.
7. No visible control is inert; all screens fit supported phone widths and safe areas.
