# Next Gen feature overlay trigger

The following overlay is part of the Next Gen 1.0.0 build: `repairs/nextgen_updater_and_challenges.py`. It adds a checksum-verified Android DownloadManager update path and a race-safe server migration enforcing one pending challenge per participant.

The server migration must still be applied to the live Supabase project before the challenge constraint is active online. The updater will not work until a stable GitHub Release with the exact APK/checksum assets exists and the APK uses the persistent release signing key.