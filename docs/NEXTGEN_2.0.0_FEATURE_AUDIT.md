# ChessBuddy Next Gen 2.0.0 — Feature audit

Reviewed: 22 November 2026

This is a feature comparison and implementation tracker, not a claim of Chess.com parity. ChessBuddy uses its own branding, code, artwork, bot identities and training content. The comparison is based on public Chess.com product information; it does not copy private code, paid content, proprietary artwork, or exact bot identities.

## What the current Chess.com mobile product includes

The official Chess.com product-update page says feature releases are staged across Android, iOS and web. Its November 2026 updates include an Activity Feed, multiple premoves on the new Live/Daily game screens, expanded analysis move lists with variations/comments/annotations, Streak milestones, and new bot collections. Earlier 2026 updates include puzzle worlds, a five-life daily puzzle, local clubs, bot challenges/rewards, Opening Explorer integration, animated coach improvements, advanced stats, archives, game collections, game-review takeaways and more. Not every feature is available on every platform or account at the same time.

The official Android app listing also describes live/friend games, tournaments, daily chess, variants, Puzzle Rush, Puzzle Battle, lessons, a large puzzle library, and a broad bot roster. Chess.com’s Help Center describes the core product areas as Play, Puzzles, Learn, Game Review, Coach/Bots, Analysis, Archive, community, clubs, tournaments, achievements and collections.

## ChessBuddy 2.0.0 implementation status

| Area | Current ChessBuddy implementation | Status / remaining work |
|---|---|---|
| Play and time controls | Human vs Stockfish bots, local pass-and-play, AI-vs-AI, configurable clocks and custom start-position support | Implemented in source; device testing remains |
| Online play | Sign-in, profiles/presence, direct challenges, server-validated moves and game-row Realtime subscription with REST refresh fallback | Partial; matchmaking, rated ladders, live two-device testing and broader social graph remain |
| Player profile | Local display name/bio, account profile bridge, practice stats and recent local games | Partial; cloud history, friend graph, avatars/country/profile privacy controls remain |
| Ratings and stats | Separate local practice Elo buckets for bullet/blitz/rapid/classical, local rating history and performance summaries | Practice-only; not official or online-rated Elo |
| Bots and coaches | Stockfish profiles, Maia roster, original bot portraits, coach/gambit demonstrations and an Lc0-to-Stockfish fallback | Partial; bot profiles are not Chess.com bots or unique human simulations; validate Maia on real devices |
| Openings and gambits | At least 100 existing opening-book lines, 49+ opening/gambit/mating-pattern courses, legal-move validation, guided practice, coach replies and three-star line progress | Implemented in source; extend catalogue and verify lines/analysis quality over time |
| Chess960 and variants | Chess960 start-rank generator, custom FEN, 3-Check and King of the Hill | Partial; Chess960 castling is explicitly disabled in this beta; other variants need independent rules implementations |
| Puzzles | Lichess Daily Puzzle, offline Puzzle Rush and Survival, local personal bests, puzzle hints/reset | Partial; offline Rush set is small, no million-puzzle rated pool, no Puzzle Battle or Puzzle Worlds |
| Lessons and study | Structured lesson path, Opening Lab, opening explorer and endgame tablebase lookup | Partial; not the full Chess.com course catalogue, paid course library or cloud study ecosystem |
| Analysis and review | Stockfish analysis, review UI, move classifications and PGN/FEN tools | Partial; device performance, deeper multi-PV/annotation workflows and complete review/skills coverage remain |
| Archive and collections | Local game archive and PGN import/export; 2.0.0 adds user-created local collections and Favorites | Partial; cloud sync, shared/community collections, advanced filtering and archive-scale search remain |
| Events | 2.0.0 adds local Solo Bot Cups with 3/5/7 rounds and result history | Offline practice only; real-time tournaments, arenas, pairings, standings and tie-breaks are not implemented |
| Achievements | 2.0.0 adds 14 local progress achievements and an XP/level display | Local-only; no account sync, community leaderboards or official Chess.com award system |
| Watch and community | Lichess TV channels and existing friend/challenge entry points | Partial; no full Activity Feed, clubs, forums, classroom, spectating chat or broadcast sharing |
| Settings and presentation | Profile/Stats/Settings destinations, board/engine/coach/data/privacy shortcuts, responsive controls and original SVG icons | Implemented in source; comprehensive accessibility/localization and device-size QA remain |
| Notifications and account | Auth/session handling and update checker; Android prompts before installing an update | Partial; push notifications, daily reminders, deep social notifications and stable release signing remain |

## 2.0.0 additions in this branch

- Achievements: 14 measurable milestones, unlock state, XP totals and levels.
- Solo Bot Cups: 3-, 5- and 7-round local events with opponent selection based on the local rapid practice rating and saved results.
- Game Collections: create collections, organize archived PGNs, add/remove games, and copy PGN text.
- Dedicated destinations for Achievements, Events & Cups and Collections from the More dashboard.
- Dedicated regression tests for the new screens and controller wiring.

## Release gates that a successful CI build cannot prove

- Install and navigate the APK on physical Android devices of different screen sizes.
- Test login, profile sync and token refresh against the live Supabase project.
- Test online challenge/accept/moves/reconnect on two separate Android devices.
- Verify the Realtime WebSocket subscription with the live service.
- Verify Stockfish and all Maia models on-device; an ARM64 compile does not prove every engine starts successfully on the target phone.
- Validate every Chess960 castling edge case before removing the beta warning.
- Configure a persistent release keystore before expecting future APKs to update an installed preview build in place.

## Public reference material

- [Chess.com product updates](https://www.chess.com/blog/Product/whats-new-on-chess-com)
- [Chess.com Android app listing](https://play.google.com/store/apps/details?id=com.chess)
- [Chess.com welcome and feature map](https://support.chess.com/en/articles/8615318-welcome-to-chess-com)
- [Chess.com Help Center: Learn, analysis, coach, bots and puzzles](https://support.chess.com/en/collections/6118686-learn)
- [Chess.com game history and archive](https://support.chess.com/en/articles/8598090-how-do-i-view-my-own-games)
- [Chess.com game collections](https://support.chess.com/en/articles/13557248-how-do-i-use-game-collections)
- [Chess.com membership feature matrix](https://support.chess.com/en/articles/8562418-what-does-each-level-of-premium-membership-get-me)

The official feature matrix includes account-tier limits and paid membership benefits. ChessBuddy does not reproduce Chess.com membership, ads, player data or paid content.
