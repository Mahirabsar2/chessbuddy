# ChessBuddy Next Gen 1.0.0 — Release Checklist

Last checked: 2026-11-21. This is a factual implementation checklist, not a promise that every Chess.com feature is already complete.

## Implemented in the current source/build pipeline

- [x] Five primary destinations: Play, Puzzles, Learn, Watch, More.
- [x] Existing Coach, Archive and Settings remain reachable from More.
- [x] Daily puzzle screen with board input, solution validation, hint and reset.
- [x] Structured local lesson path and saved completion progress.
- [x] Lichess TV channel discovery and opening of live public games.
- [x] Game Review summary layout: responsive two-column actions, fixed icon sizing, compact move table and safe-area-aware sheet sizing.
- [x] Account gate on cold launch; signup is the default mode.
- [x] Refresh token stored in Android Keystore-backed encrypted storage and restored on launch.
- [x] Online moves are validated by the deployed `apply-online-move` Edge Function.
- [x] Challenge policy is deployed: five-minute expiry, one active pending challenge per participant, ordered advisory locks, unique pending-pair index, and no anon/public execute grant.
- [x] Nine official Maia-1 model choices (1100–1900) are represented in the manifest and downloaded on demand with integrity verification.
- [x] Stockfish, Rust chess core and Lc0/BLAS ARM64 source-build scripts are present.
- [x] In-app updater checks stable GitHub releases, verifies SHA-256 and starts a background download.
- [x] Regression tests added for five-tab content, Maia native configuration, startup auth persistence, and Game Review button sizing.

## Current verification status

- [x] Build 41 produced a signed preview APK and passed its existing JS and Java tests.
- [x] Native Rust ARM64 build succeeded in build 43.
- [x] Lc0 ARM64 build succeeded in build 43; source archives and provenance were emitted.
- [x] A Maia startup regression was identified and patched: the app no longer passes an unsupported `--search-algorithm=policyhead` CLI argument; policyhead is compiled as Lc0's default.
- [ ] Re-run the complete CI pipeline after the native verification-step ordering fix (build 46 is currently running).
- [ ] Run the updated regression suite against the exact final source snapshot.
- [ ] Install and test on a physical Android device, including a second device for online games.
- [ ] Confirm Maia model download, UCI handshake and legal move output on-device.

## Not complete / release blockers

- [ ] Real recorded coach/bot voice assets are not bundled. The connected voiceover account currently has 0 credits; Android speech synthesis is not a substitute for the requested recorded voices.
- [ ] Generated realistic portrait artwork has not yet been integrated into the APK; the current bundled bot roster uses original SVG character art.
- [ ] Full translated UI strings for the requested language set are not complete.
- [ ] Full Puzzle Rush, Puzzle Battle, rated puzzle ladder, large course library, complete messaging, clubs, tournaments, achievements sync, opening database and full broadcast experience are not complete. The five tabs are not equivalent to full Chess.com parity.
- [ ] Online game updates still use REST polling (2.2 seconds while a game is active); database Realtime publication currently contains no tables. Instant push requires a reviewed migration and user approval before applying it to the live database.
- [ ] The current preview APK is about 81.5 MB, below the requested 200 MiB. It must not be padded with meaningless bytes; only real offline assets/models/content should increase size.
- [ ] Stable release signing secrets are not configured. Without the same persistent signing key, Android cannot install future APKs as in-place updates.
- [ ] Android will always require the package installer/user confirmation for a sideloaded APK update. The app can auto-check and auto-download, but cannot silently bypass Android's installation confirmation.
- [ ] No public stable release has been published because the persistent signing key and release gates are not satisfied.
- [ ] The deployed Supabase security advisor still reports leaked-password protection disabled. The SECURITY DEFINER warnings were reviewed: the listed RPCs check `auth.uid()` and are executable by authenticated users only, not anon or PUBLIC.

## Release acceptance gates

1. CI passes on the final branch commit, including native build, JS tests, Java policy tests, APK signature verification and artifact inspection.
2. The release is signed with one persistent keystore used for every future version.
3. Online two-device tests pass for challenges, move validation, clock sync, reconnect and game end states.
4. Maia passes on-device tests for every model family selected for release.
5. No placeholder voice/portrait feature is described as finished.
6. The APK size is reported honestly; no artificial padding.
