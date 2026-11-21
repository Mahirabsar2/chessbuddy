# Next Gen 1.0.0 — Character Media Register

This file records original ElevenLabs generations for ChessBuddy. A generated item is **not considered integrated** until its media bytes are committed to the app's packaged assets and a release test confirms it renders/plays on-device.

## Original Mittens

- Portrait: Seedream 4, 1080×1080, generation `XB4UZtJ0E3IGTDjUpLYL`, flow `Ngue2cxghyWmt0qjcZl9`, node `Iw4JpGCcH4FUYj3htQlA`.
- Voice: Eleven v3, 6.8 seconds, generation `Y7U9Mo1pLOQM52jLHMhl`, flow `zEHBkMqtTcTEyAPB4UO0`, voice library preset `Connery - Grumpy, Angry Character`.
- Character direction: hurt, offended and quietly furious; not a copy of any existing app mascot.
- Status: generated; not bundled into APK.

## Four-avatar character sheet

- Image: Seedream 4, generation `ztbYoQp1gY0SV5le8pve`, flow `1Sl3QbmAWk4lgCZw1Z7s`, node `d9Iap0BcuagbWdIRg9kM`.
- Four original archetypes: streamer commentator, composed coach, silver-haired endgame sage, upbeat young prodigy.
- Intended crops: four equal square portraits from the 2×2 sheet.
- Status: generated; individual crops and packaged integration pending.

## Reusable voice cast

| Archetype | Generation | Voice preset | Duration | Status |
|---|---|---|---:|---|
| Streamer commentator | `Xc2mMGDVCoBi5Iod5bt9` | Sheldon — Quirky, Clever, Enthusiastic | 3.68 s | Generated; not bundled |
| Coach | `YOCNTjNEQynRldVk3Wgg` | Georgia K — Happy, Comforting Character | 7.52 s | Generated; not bundled |
| Veteran | `PmpSgDrv118g5FeIC2BX` | Mister Gruff — Miserable old neighbor | 3.28 s | Generated; not bundled |
| Mittens | `Y7U9Mo1pLOQM52jLHMhl` | Connery — Grumpy, Angry Character | 6.8 s | Generated; not bundled |

These are four reusable character voices plus Mittens, not 100 individual cloned voices. The streamer role is a fictional ChessBuddy commentator, not a Levy/GothamChess voice clone or endorsement.

## Integration gates

- [ ] Export image/audio bytes from the generation workspace.
- [ ] Crop the four-up portrait sheet into four individual files.
- [ ] Package portraits and audio under app assets; use stable versioned files, not time-limited signed URLs.
- [ ] Connect portrait IDs to the bot roster and the voice set to matching character archetypes.
- [ ] Test audio playback, mute settings, focus/audio interruptions and portrait rendering on Android.
- [ ] Verify resulting APK artifact includes every media asset and its checksum.
