# ChessBuddy — clean rebuild

This branch is a clean-room Android rebuild. The app source lives under `clean-rebuild/`; it does not extract or patch any previous ChessBuddy ZIP.

## Current first milestone
- Native Android shell with an offline-first WebView.
- Responsive chess lobby and mobile navigation.
- Legal chess rules through pinned `chess.js`: selection, legal destinations, captures, castling, en passant, promotion, check, checkmate, draws, undo and FEN/PGN.
- Pass-and-play clocks, move history, board flip, a verified mate-in-one puzzle and a guided opening line.
- Local profile counters and Android share sheet for PGN/FEN.

## Build
GitHub Actions builds and verifies an APK on pushes to `chessbuddy-zero-rebuild`. The APK is published as a prerelease for fresh installation; it is not signed with a permanent update key. The pipeline also runs legal-rule checks for the opening line, castling, en passant, promotion, illegal-move rejection and the mate puzzle.

## Scope honesty
This is the new foundation, not a claim that every Chess.com service is already implemented. Accounts, cloud sync, ranked matchmaking, tournaments, clubs, messaging, live broadcasts, subscriptions, and a full puzzle/lesson catalogue require separate backend and product work. The interface uses ChessBuddy identity and original implementation/assets.
