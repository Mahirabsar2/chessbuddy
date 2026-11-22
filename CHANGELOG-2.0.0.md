# ChessBuddy 2.0.0

## Next Gen overhaul
- Reworked the mobile information architecture around Play, Puzzles, Learn, Watch and More, with dedicated Profile, Stats, Coach, Archive and Settings destinations.
- Added visible profile access, local practice-rating cards, rating history, recent games, profile editing and a structured More dashboard.
- Refined the responsive layout, iconography, button sizing and safe-area handling for narrow Android screens.
- Added Maia/Lc0 failure recovery to a Stockfish practice move so an engine start failure does not automatically strand the game.

## Chess training
- Added the guided Opening & Gambit Coach with a searchable repertoire, practice as either colour, coach replies, step-by-step/automatic demonstrations and local three-star progress.
- Added broad opening-book selection and dedicated Alien Gambit lines; Fool's Mate is correctly presented as a mating pattern rather than a gambit.
- Added Chess960 start-position generation, custom FEN setup, 3-Check and King of the Hill. Chess960 castling remains disabled in this beta and is clearly labelled.
- Added Opening Lab, lessons, Lichess Daily Puzzle, timed Puzzle Rush, Survival practice, local best scores, analysis and endgame tablebase lookup.

## ChessBuddy 2.0 expansion
- Added 14 progress achievements with local XP and levels.
- Added 3-, 5- and 7-round Solo Bot Cups with local opponent selection, saved scores and results.
- Added local PGN collections, Favorites, archived-game organization and copyable PGN export.
- Added independent navigation destinations and regression coverage for all three modules.

## Important scope notes
- ChessBuddy uses original branding, illustrations, bots and training content; it does not copy Chess.com's proprietary assets or character roster.
- Solo Bot Cups, achievements, practice ratings and collections are local features, not Chess.com online services.
- Real-time matchmaking, rated online ladders, live tournaments, clubs, activity feed, social chat, community collections, Puzzle Battle/Worlds and complete variant coverage are not claimed as implemented.
- The 2.0.0 APK must pass CI and be tested on physical Android devices before being called release-ready.
