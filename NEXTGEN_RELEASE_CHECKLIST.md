# ChessBuddy Next Gen 2.0.0 — Release Checklist

Last reviewed: 22 November 2026.

## Implemented in source overlays
- [x] Five primary sections: Play, Puzzles, Learn, Watch and More.
- [x] Dedicated Profile, Stats, Coach, Archive and Settings screens accessible from More.
- [x] Local practice ratings by bullet/blitz/rapid/classical time-control bucket; local rating history and recent-game summary.
- [x] Stockfish ARM64 engine, Maia 1100–1900 roster, Lc0/BLAS native build and Stockfish fallback code.
- [x] Original bot avatar renderer and original character art/voice packaging.
- [x] Direct online challenges, authenticated profile/presence code, server-validated move submission and Realtime game-row subscription with REST refresh fallback.
- [x] Daily Lichess puzzle, offline Puzzle Rush/Survival, nine structured lessons, Opening Lab and endgame tablebase lookup.
- [x] Existing opening book (100+ lines) and searchable gambit/coach repertoire (49+ lines), with legal-line tests and course-star progress.
- [x] Custom FEN, Chess960 start-rank generation, 3-Check and King of the Hill. Chess960 castling is not enabled yet.
- [x] Review and archive source flows, FEN/PGN tools and local practice summaries.
- [x] 2.0.0 expansion: 14 local achievements with XP, solo bot cups (3/5/7 rounds), and local PGN collections.

## CI verification required for this branch
- [ ] Full JavaScript suite.
- [ ] Realtime subscription, Puzzle Rush, Opening Lab, gambit repertoire, mobile Profile/Stats and 2.0.0 expansion regression tests.
- [ ] Java policy tests and native ARM64 engine checks.
- [ ] Signed APK build and signature verification.
- [ ] Source snapshot, APK and checksum published from the same workflow run.

## External and device release gates
- [ ] Configure persistent release-key secrets before publishing a stable update-compatible release. The preview fallback key is temporary.
- [ ] Install and exercise the APK on a physical Android phone at several display sizes.
- [ ] Verify account creation, sign-in, profile synchronization and token refresh against Supabase.
- [ ] Test challenge/accept/move/reconnect/end-to-end play on two physical devices.
- [ ] Verify the Realtime socket against the live Supabase service (CI's fake socket test is not live-network validation).
- [ ] Verify Stockfish startup and all nine Maia model downloads/loads/moves on device.
- [ ] Confirm the app remains usable under memory pressure and after interrupted network/engine operations.
- [ ] Test custom FEN and all Chess960 edge cases before enabling Chess960 castling.
- [ ] Review copy, responsive UI, accessibility, localization, and privacy handling on device.

## Known 2.0.0 scope gaps
- Real-time ranked matchmaking and official online ratings/leaderboards.
- Live online tournaments/arenas, club management, forums, classrooms and social/activity feeds.
- Full cloud-synced friend graph, messaging and game chat.
- A large rated puzzle database, Puzzle Battle, Puzzle Worlds and cloud puzzle history.
- Full cloud/shared/community Game Collections and advanced archive search.
- Complete Chess960 castling and the additional variants in the feature audit.
- Full cross-device profile, achievements, collections and rating synchronization.

A successful CI build proves that the tested source compiles and the listed automated tests pass. It does not prove the live services or physical Android experience.
