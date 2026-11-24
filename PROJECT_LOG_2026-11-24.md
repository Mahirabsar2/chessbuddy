# ChessBuddy project log — 2026-11-24

## Cloud persistence foundation

- Connected Supabase project `chessbuddy` (ref `npicptuurxuqxepxzumi`).
- Applied migration `chessbuddy_cloud_user_state_and_game_archive`.
- Added `public.chessbuddy_user_state` for account-owned profile customisation, app settings, and progress.
- Added `public.chessbuddy_saved_games` for account-owned PGN archives and metadata.
- Enabled RLS and added owner-scoped SELECT/INSERT/UPDATE/DELETE policies to both tables; granted Data API access only to the authenticated role.
- Added updated-at triggers and an index for per-user game archive retrieval.
- Re-inspected the live schema: both tables exist and RLS is enabled.
- Re-ran Supabase security advisors. Seven existing SECURITY DEFINER RPC warnings and the disabled leaked-password protection warning remain; they were not modified here.
- Important: this is the database foundation only. The Android client still requires persistent native session storage, startup session restoration, cloud hydration, upsert/reconciliation logic, and integration tests. No claim is made that sign-in or profile persistence is fixed in the APK yet.
