create table if not exists public.chessbuddy_user_state (
  user_id uuid primary key references auth.users(id) on delete cascade,
  profile jsonb not null default '{}'::jsonb check (jsonb_typeof(profile) = 'object'),
  settings jsonb not null default '{}'::jsonb check (jsonb_typeof(settings) = 'object'),
  progress jsonb not null default '{}'::jsonb check (jsonb_typeof(progress) = 'object'),
  updated_at timestamptz not null default now()
);

alter table public.chessbuddy_user_state enable row level security;

drop policy if exists "Users can read their own ChessBuddy state" on public.chessbuddy_user_state;
create policy "Users can read their own ChessBuddy state"
on public.chessbuddy_user_state for select to authenticated
using ((select auth.uid()) = user_id);

drop policy if exists "Users can create their own ChessBuddy state" on public.chessbuddy_user_state;
create policy "Users can create their own ChessBuddy state"
on public.chessbuddy_user_state for insert to authenticated
with check ((select auth.uid()) = user_id);

drop policy if exists "Users can update their own ChessBuddy state" on public.chessbuddy_user_state;
create policy "Users can update their own ChessBuddy state"
on public.chessbuddy_user_state for update to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

drop policy if exists "Users can delete their own ChessBuddy state" on public.chessbuddy_user_state;
create policy "Users can delete their own ChessBuddy state"
on public.chessbuddy_user_state for delete to authenticated
using ((select auth.uid()) = user_id);

grant select, insert, update, delete on public.chessbuddy_user_state to authenticated;

create table if not exists public.chessbuddy_saved_games (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  client_game_id text not null check (char_length(client_game_id) between 1 and 128),
  pgn text not null,
  metadata jsonb not null default '{}'::jsonb check (jsonb_typeof(metadata) = 'object'),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (user_id, client_game_id)
);

create index if not exists chessbuddy_saved_games_user_updated_idx
on public.chessbuddy_saved_games (user_id, updated_at desc);

alter table public.chessbuddy_saved_games enable row level security;

drop policy if exists "Users can read their own saved games" on public.chessbuddy_saved_games;
create policy "Users can read their own saved games"
on public.chessbuddy_saved_games for select to authenticated
using ((select auth.uid()) = user_id);

drop policy if exists "Users can create their own saved games" on public.chessbuddy_saved_games;
create policy "Users can create their own saved games"
on public.chessbuddy_saved_games for insert to authenticated
with check ((select auth.uid()) = user_id);

drop policy if exists "Users can update their own saved games" on public.chessbuddy_saved_games;
create policy "Users can update their own saved games"
on public.chessbuddy_saved_games for update to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

drop policy if exists "Users can delete their own saved games" on public.chessbuddy_saved_games;
create policy "Users can delete their own saved games"
on public.chessbuddy_saved_games for delete to authenticated
using ((select auth.uid()) = user_id);

grant select, insert, update, delete on public.chessbuddy_saved_games to authenticated;

create or replace function public.cb_touch_updated_at()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists chessbuddy_user_state_touch_updated_at on public.chessbuddy_user_state;
create trigger chessbuddy_user_state_touch_updated_at
before update on public.chessbuddy_user_state
for each row execute function public.cb_touch_updated_at();

drop trigger if exists chessbuddy_saved_games_touch_updated_at on public.chessbuddy_saved_games;
create trigger chessbuddy_saved_games_touch_updated_at
before update on public.chessbuddy_saved_games
for each row execute function public.cb_touch_updated_at();
