# ChessBuddy Next Gen 1.0.0 — Acceptance Checklist

This is the release tracker for the Next Gen branch. "Implemented" means the code path exists; "CI verified" means the repository workflow exercised it. Neither means a physical Android device or live third-party service was tested. Do not advertise a feature as production-ready until its release gate below passes.

## Release blockers

- [ ] **APK size: 200 MiB minimum.** Latest candidate was 81,502,317 bytes (about 77.7 MiB). The 200 MiB requirement is not met. Grow the package only with real assets, licensed models, databases, engines or voice packs; never add dummy padding.
- [ ] **Persistent Android signing key.** Configure the stable release keystore as GitHub Actions secrets: `CB_RELEASE_KEYSTORE_BASE64`, `CB_RELEASE_STORE_PASSWORD`, `CB_RELEASE_KEY_ALIAS`, and `CB_RELEASE_KEY_PASSWORD`. Never commit the keystore or passwords. The current workflow falls back to a preview-only key.
- [ ] **Real in-app update release.** The verified updater must pass CI, then publish an official stable GitHub Release with `ChessBuddy-NextGen-1.0.0.apk` and its `.sha256` checksum. Auto-download can run in the background; Android must still ask the user to approve package installation. Same signing key and increasing versionCode are required.
- [ ] **Physical-device install/update test.** Install, download a signed update, verify checksum, approve the Android installer, and confirm app data and login survive the update.

## Authentication and profiles

- [x] Startup account gate: fresh installs display account creation/sign-in instead of the chess lobby.
- [x] Encrypted refresh-token storage via Android Keystore and native session restoration code.
- [x] Signup defaults to Create Account; successful session restoration unlocks the app automatically.
- [x] Sign-out returns to the account screen.
- [ ] Test account creation, email confirmation, sign-in and app relaunch on physical Android hardware.
- [ ] Test token refresh after access-token expiry, process kill, device restart and network interruption.
- [ ] Test Google OAuth PKCE and deep-link return on device.
- [ ] Verify profile creation, username uniqueness, profile edit, country/avatar and rating/stat persistence with live Supabase.
- [ ] Test login on two devices with the same account and verify session behavior.

## Chess, engines and bots

- [x] chess.js legal move rules, special moves, PGN/FEN and perft regression tests.
- [x] Real Stockfish ARM64 engine included in the build; engine UCI and strength-handicap tests pass.
- [x] Stockfish beginner-to-master difficulty profiles and AI-vs-AI/pass-and-play code paths.
- [x] Bot roster expansion: original bot personalities plus 80+ named chess-player tribute profiles, explicitly labelled as Stockfish practice profiles, not simulations.
- [x] Original per-bot vector avatar renderer and deterministic portrait tests.
- [x] Maia selection roster includes official Maia-1 levels 1100–1900 (nine levels).
- [x] Lc0/maia model download and integrity-verification code exists in source.
- [ ] Verify Lc0 binary starts on physical ARM64 hardware and each of the nine Maia models loads, selects the correct network and plays a legal move.
- [ ] Verify Maia process restarts when switching model IDs; test low-memory recovery and interrupted downloads.
- [ ] Add more genuinely integrated engines (for example Arasan/Berserk) only after licenses, ARM64 builds, UCI tests and UI selection are complete.
- [ ] Make Stockfish's human-like mode a calibrated playing-strength profile, not a claim that Stockfish reproduces a human player's style.
- [ ] Test 100+ bot portraits and engine mappings on a small-memory Android phone.

## Gameplay and analysis

- [x] Board interaction, promotion, legal highlights, move history, clocks, sounds, themes, archive and review code paths.
- [x] Quick analysis first pass now requests one principal variation and renders live engine info.
- [x] Analysis time setting: Quick 0.5s, Balanced 0.9s, Strong 1.5s, Deep 3s, Maximum 5s.
- [x] Review's deeper second pass is narrowed to critical positions instead of routine captures.
- [ ] Benchmark analysis latency, NPS, battery and thermal throttling on target Android devices.
- [ ] Add cached position evaluations and cancel stale searches immediately on board navigation.
- [ ] Add multi-PV, engine lines, eval arrows, threat arrows and deeper analysis controls with device performance testing.
- [ ] Add up to five premoves, auto-queen, optional confirmation prompts and low-time settings where supported; test race conditions.
- [ ] Test resign, draw, rematch, timeouts, disconnects and unfinished-game resume.
- [ ] Do not claim perfectly accurate engine analysis at zero time: exact legal move detection is separate from progressively deeper evaluation.

## Online play and Lichess

- [x] Supabase account/profile/presence/challenge client code.
- [x] Five-minute challenge expiry is defined in the database schema.
- [x] Direct challenges, accept/decline/cancel, game polling, server move validation and server-side game end RPCs exist in source; online move function was deployed previously.
- [x] Online move submissions are sent immediately; the client currently polls for remote changes about every 2.2 seconds.
- [x] Live Supabase `cb_send_challenge` already serializes both participants with transaction-scoped advisory locks and blocks a second pending invite involving either player. A rollback-only SQL test confirmed the recipient cannot immediately send another challenge; the test left zero active pending challenges. The same guard is included in the Next Gen source overlay for reproducible fresh deployments.
- [ ] Run a concurrent two-request stress test against Supabase and confirm expired invites are cleaned up under load.
- [ ] Test two separate accounts on two physical Android devices: invite, accept, first move, sync, clocks, reconnect, resign, draw and timeout.
- [ ] Replace or supplement 2.2-second polling with Supabase Realtime subscriptions for near-instant remote move updates; retain polling fallback.
- [ ] Verify server clock integrity, replay rejection, stale move rejection and permissions against the deployed SQL + Edge Function.
- [x] Lichess public opening explorer/tablebase integration is present.
- [ ] Test Lichess endpoints live, handle rate limits/offline mode and show connection/source state.
- [ ] Add Lichess OAuth/account sync only if separately requested and secured; current public data integration is not an authenticated Lichess account.

## Additional product tabs and modules

Current main navigation is still **Play, Coach, Archive and Settings**. The following Chess.com-inspired sections are not yet full implementations. Do not count a tab shell or placeholder card as completion.

- [ ] **Puzzles:** rated adaptive puzzles, puzzle rating/history, daily puzzle, custom themes, missed-puzzle practice, Puzzle Rush (3/5 minute and survival), Puzzle Battle, mistakes/hearts, hints, streaks and leaderboards.
- [ ] **Learn:** New to Chess / Beginner / Intermediate / Advanced paths, interactive courses, opening/tactics/strategy/endgame lessons, lesson library, progress, streaks and coach feedback.
- [ ] **Watch:** spectate active games, live move stream, friends playing, tournaments, events and streams; define a legal/maintainable content source.
- [ ] **More:** profile, ratings/statistics, friends/followers, inbox/messages, achievements, streaks, drills, privacy and blocked-user settings.
- [ ] Add original navigation with **Play, Puzzles, Learn, Watch and More**; keep Coach, Archive, Analysis and Settings accessible as organized sub-pages.
- [ ] Add player profiles with avatar, username, country, ratings, recent games, achievements and privacy controls.
- [ ] Add social controls (friend requests, block/unblock, safe chat, message inbox) with server-side permissions and abuse controls.
- [ ] Add fair, abuse-resistant ratings/leaderboards only after rating calculations and backend protections are specified.

## Visual design, voices, avatars and localization

- [x] Existing app has an animated startup splash and custom ChessBuddy interface; current build is not a complete new visual redesign.
- [x] Existing code uses original SVG vector portraits for its bot roster.
- [x] Game Review summary responsive-layout repair: fixed SVG icon bounds, moved Close into a compact header control, equal-width primary actions, responsive score table/graph and safe-area-aware sheet sizing. CI build #38 passed JS and Java test suites and APK signature verification.
- [ ] Integrate the prepared realistic portrait assets into the actual app and map each portrait consistently to the bot catalogue; verify image crop, compression, accessibility labels and attribution.
- [ ] Add custom recorded/AI-generated character voice packs. Current implementation is Android/browser system TTS, not recorded character voices. The connected voice-generation balance was zero during this work, so no recorded voices are claimed or bundled.
- [ ] Add multiple distinct voice packs and coach voice controls only when their audio files, licenses and playback path are available.
- [ ] Create a real localization framework with translated strings, plural forms, RTL layout and persisted language selection.
- [ ] Translate the full UI and lessons into Bengali, English, Spanish, French, German, Portuguese, Russian, Arabic, Hindi, Japanese, Korean and Chinese; verify fonts and long-string layouts.
- [ ] Complete original brand identity: app icon, in-app logo, tab icons, loading visuals, empty/error states, and accessible contrast.
- [ ] Test the revised Game Review summary visually on several Android screen sizes and with large system font scaling. The plus/minus overlay in the supplied screenshot is Android's OS-level magnification UI, not a ChessBuddy control (WebView zoom is disabled).
- [ ] Profile, board, piece, background, sound and animation customization settings must persist across restarts and app updates.

## Updates, reliability, privacy and performance

- [x] Native update download/verification implementation is now added to the Next Gen repair overlay.
- [x] Release workflow is configured to publish only if the APK is at least 200 MiB and uses the persistent signing key.
- [ ] Run the updater overlay in CI; test checksum mismatch, wrong host, interrupted download, no install permission, no network and already-downloaded update.
- [ ] Configure the permanent signing secrets and preserve a backup of the keystore outside GitHub.
- [ ] Produce and publish the first stable signed GitHub Release; verify update discovery uses the exact expected asset names and build-number tag.
- [ ] Add robust startup, crash and network retry handling; audit every asynchronous task for cancellation and stale UI updates.
- [ ] Profile performance on low-memory ARM64 devices: cold start, WebView memory, engine start/stop, puzzle load, review, scrolling and online sync.
- [ ] Add offline behavior and clear status for unavailable services; do not silently fake engine, Lichess, puzzle or server responses.
- [ ] Run dependency, permission, storage, network, RLS, Edge Function and privacy review before release.

## Current verification snapshot

- Latest prior baseline build: CI run #31, all JS logic tests and Java policy tests passed; Gradle APK build and signature verification passed.
- Latest CI #38 APK artifact: 81,503,408 bytes. This does **not** pass the 200 MiB release requirement.
- Baseline signing mode: preview-only (the persistent release keystore secrets were not configured).
- The verified updater and one-pending-challenge code, plus the responsive Game Review UI repair, passed CI #38.
- Physical Android testing, two-device multiplayer testing, all nine Maia model runtime tests, live updater installation and full UI browser tests remain outstanding.

**Release rule:** Do not deliver or label a build as “final”, “bug-free”, “200+ MB”, “auto-updating” or “Chess.com complete” until the corresponding checkboxes are completed with evidence. A 1.0.0 version label is not a guarantee of feature completeness or zero defects.
