# ChessBuddy Atelier Artwork System

## Design boundary
This is an original ChessBuddy visual identity, not a reproduction of Chess.com's proprietary illustrations, logo, piece assets, or branded interface. It aims for the same level of consistency and polish while keeping ChessBuddy's own shapes, palette, and character identity.

## Included in the Next Gen build overlay
- A newly drawn vector Staunton-inspired piece family: white and black pawn, rook, knight, bishop, queen, and king (12 SVG variants).
- Shared sprite symbols preserve the existing board, promotion, move-list, and bot-preview renderer contract.
- An original shield-and-crown ChessBuddy brand mark used by the splash screen and top app bar.
- A matching adaptive Android launcher foreground and dark evergreen background.
- Six persistent board palettes: Emerald, Walnut, Arctic, Rose, Midnight, and Parchment. Existing saved values green, brown, and blue remain valid.
- A bundled editable SVG source for the brand mark under app/src/main/assets/artwork.

## Existing artwork retained
- The deterministic original vector bot portrait generator in js/avatars.js.
- The original generated character portraits and short voice clips under media/avatars and media/voices.
- The existing custom Lucide-style navigation and feature icons.

## Integration
The build workflow applies repairs/nextgen_artwork_system.py after extracting the versioned source archive. tests/logic/artwork-system.test.js runs as part of tests/run-all.js and verifies all 12 piece variants, sprite symbol IDs, brand integration, launcher palette, and all six board themes.

## Verification boundary
The artwork logic test and full JavaScript logic suite can verify asset wiring and SVG output. A successful CI build is still required to verify Android resource compilation and APK packaging. Physical-device checks are still needed for icon masking, piece visibility at board sizes, theme contrast, and screen-density rendering.
