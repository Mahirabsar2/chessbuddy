# ChessBuddy cloud persistence foundation

## Status

The connected Supabase project has the schema foundation deployed and verified. This is a backend schema change; it does **not** by itself make the Android app sync data. The Android client still needs the matching persistence adapter, startup hydration, debounced writes, conflict handling, and sign-out behavior before this can be called complete.

## Tables

- `public.chessbuddy_user_state`: one row per authenticated account, with JSON objects for profile customisation, app settings, and progress. The primary key is the Auth user ID.
- `public.chessbuddy_saved_games`: cloud archive of PGNs keyed by the user's ID and stable client game ID. Metadata can hold result, opponent, time control, variant, and dates.

Both tables have RLS enabled. Authenticated users can read, insert, update, and delete only rows whose `user_id` equals `auth.uid()`. The database does not accept a client-supplied owner ID belonging to another account.

## Client integration contract

1. Configure the Supabase client with persistent storage and token auto-refresh. For the Android WebView build, persist the refresh token in Android Keystore-backed storage rather than relying solely on volatile JavaScript memory.
2. On startup, restore the saved session, refresh it if necessary, call `getSession()`, then hydrate the account's cloud state before showing the signed-in profile.
3. Save profile/settings/progress with an upsert on `user_id`; merge partial updates deliberately instead of overwriting unrelated sections.
4. Sync saved games with an upsert on `(user_id, client_game_id)`; pull cloud rows at sign-in and reconcile against local offline games.
5. Debounce writes, retry transient network failures, preserve unsynced local changes, and expose a visible sync status.
6. On explicit sign-out, clear the Supabase session and account-scoped in-memory caches. Never sign out just because the Android Activity is paused or destroyed.
7. Never put API-provider secrets, refresh tokens, or private credentials in the JSONB settings document. Keep secrets in native secure storage.

## Verification

- Supabase migration applied successfully.
- Schema inspection confirmed both tables, expected columns, primary keys, foreign keys, and RLS enabled.
- Security advisor still reports seven pre-existing callable SECURITY DEFINER RPC warnings and leaked-password protection disabled. Those findings were not changed by this migration.
- End-to-end Android sign-in persistence and profile/settings/game sync remain unverified until the app-side adapter is implemented and exercised on-device.
