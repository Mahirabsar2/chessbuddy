from pathlib import Path

def edit(path, pairs):
    p = Path(path)
    source = p.read_text(encoding="utf-8")
    for old, new in pairs:
        if new in source:
            continue
        if old not in source:
            raise SystemExit("Updater patch could not find expected source in " + path + ": " + old[:100].replace("\n", "\\n"))
        source = source.replace(old, new, 1)
    p.write_text(source, encoding="utf-8")

# A checksum-verified updater. DownloadManager handles background transfer; Android still
# owns the final package-installer confirmation and the signing-key compatibility check.
edit("app/src/main/java/com/chessbuddy/NativeBridge.java", [
("import android.app.ActivityManager;\n", "import android.app.ActivityManager;\nimport android.app.DownloadManager;\n"),
("import android.content.Intent;\n", "import android.content.Intent;\nimport android.content.SharedPreferences;\nimport android.database.Cursor;\n"),
("import android.net.Uri;\n", "import android.net.Uri;\nimport android.provider.Settings;\n"),
("import android.os.Build;\n", "import android.os.Build;\nimport android.os.Environment;\nimport android.os.ParcelFileDescriptor;\n"),
("import java.io.File;\n", "import java.io.File;\nimport java.io.FileInputStream;\n"),
("""    /* ---------------- speech ---------------- */
""", """    /* ---------------- verified app updates ---------------- */
    private static final String UPDATE_PREFS = "chessbuddy.verified_updates";
    private static final String UPDATE_ID = "download_id";
    private static final String UPDATE_SHA = "sha256";
    private static final String UPDATE_VERIFIED = "verified_sha256";

    private void updateStatus(final String state, final String message) {
        js("window.CBUpdaterNativeStatus&&window.CBUpdaterNativeStatus(" + Json.quote(state) + "," + Json.quote(message) + ")");
    }

    private boolean trustedUpdateUrl(String raw) {
        if (raw == null || raw.length() > 2048) return false;
        try {
            Uri u = Uri.parse(raw.trim());
            String path = u.getPath();
            return "https".equalsIgnoreCase(u.getScheme())
                && "github.com".equalsIgnoreCase(u.getHost())
                && u.getUserInfo() == null && u.getPort() == -1
                && path != null
                && path.startsWith("/Mahirabsar2/chessbuddy/releases/download/")
                && path.toLowerCase(java.util.Locale.US).endsWith(".apk");
        } catch (RuntimeException e) { return false; }
    }

    private SharedPreferences updatePrefs() {
        return activity.getSharedPreferences(UPDATE_PREFS, Activity.MODE_PRIVATE);
    }

    @JavascriptInterface
    public String downloadAndInstallUpdate(final String url, final String expectedSha256) {
        if (!trustedUpdateUrl(url) || expectedSha256 == null || !expectedSha256.matches("[0-9a-fA-F]{64}"))
            return "{\\"ok\\":false,\\"error\\":\\"untrusted_update_asset\\"}";
        try {
            final DownloadManager manager = (DownloadManager) activity.getSystemService(Activity.DOWNLOAD_SERVICE);
            if (manager == null) return "{\\"ok\\":false,\\"error\\":\\"download_manager_unavailable\\"}";
            final SharedPreferences prefs = updatePrefs();
            final String sha = expectedSha256.toLowerCase(java.util.Locale.US);
            String oldId = prefs.getString(UPDATE_ID, "");
            if (sha.equals(prefs.getString(UPDATE_SHA, "")) && oldId.matches("[0-9]{1,20}")) {
                final long existing = Long.parseLong(oldId);
                if (sha.equals(prefs.getString(UPDATE_VERIFIED, ""))) {
                    main.post(new Runnable() { @Override public void run() { openVerifiedUpdate(manager, existing); } });
                    return "{\\"ok\\":true,\\"installing\\":true}";
                }
                Cursor existingCursor = manager.query(new DownloadManager.Query().setFilterById(existing));
                if (existingCursor != null) {
                    try {
                        if (existingCursor.moveToFirst()) {
                            int status = existingCursor.getInt(existingCursor.getColumnIndex(DownloadManager.COLUMN_STATUS));
                            if (status == DownloadManager.STATUS_PENDING || status == DownloadManager.STATUS_RUNNING)
                                return "{\\"ok\\":true,\\"already_downloading\\":true}";
                        }
                    } finally { existingCursor.close(); }
                }
            }
            if (oldId.matches("[0-9]{1,20}")) {
                try { manager.remove(Long.parseLong(oldId)); } catch (RuntimeException ignored) { }
            }
            DownloadManager.Request request = new DownloadManager.Request(Uri.parse(url));
            request.setTitle("ChessBuddy Update");
            request.setDescription("Downloading a verified ChessBuddy update");
            request.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
            request.setAllowedNetworkTypes(DownloadManager.Request.NETWORK_WIFI | DownloadManager.Request.NETWORK_MOBILE);
            request.setAllowedOverRoaming(false);
            request.setDestinationInExternalFilesDir(activity, Environment.DIRECTORY_DOWNLOADS, "ChessBuddy-NextGen-update.apk");
            request.addRequestHeader("User-Agent", "ChessBuddy-Android-Updater");
            final long id = manager.enqueue(request);
            prefs.edit().putString(UPDATE_ID, String.valueOf(id)).putString(UPDATE_SHA, sha).remove(UPDATE_VERIFIED).commit();
            updateStatus("downloading", "Downloading the update in the background. Android will confirm installation.");
            pool.execute(new Runnable() {
                @Override public void run() {
                    try {
                        boolean done = false;
                        for (int attempt = 0; attempt < 7200 && !destroyed; attempt++) {
                            Cursor cursor = manager.query(new DownloadManager.Query().setFilterById(id));
                            if (cursor == null) throw new IllegalStateException("Android download status is unavailable");
                            int status, reason = 0;
                            try {
                                if (!cursor.moveToFirst()) throw new IllegalStateException("The update download disappeared");
                                status = cursor.getInt(cursor.getColumnIndex(DownloadManager.COLUMN_STATUS));
                                reason = cursor.getInt(cursor.getColumnIndex(DownloadManager.COLUMN_REASON));
                            } finally { cursor.close(); }
                            if (status == DownloadManager.STATUS_SUCCESSFUL) { done = true; break; }
                            if (status == DownloadManager.STATUS_FAILED)
                                throw new IllegalStateException("Android download manager failed (" + reason + ")");
                            try { Thread.sleep(1000L); }
                            catch (InterruptedException e) {
                                Thread.currentThread().interrupt();
                                throw new IllegalStateException("Update download interrupted");
                            }
                        }
                        if (!done) throw new IllegalStateException("Update download timed out");
                        if (!verifyDownloadedUpdate(manager, id, sha))
                            throw new IllegalStateException("Update SHA-256 verification failed");
                        prefs.edit().putString(UPDATE_VERIFIED, sha).commit();
                        updateStatus("verified", "Update downloaded and verified. Opening Android installation approval…");
                        main.post(new Runnable() { @Override public void run() { openVerifiedUpdate(manager, id); } });
                    } catch (Exception e) {
                        updateStatus("failed", e.getMessage() == null ? "Update verification failed." : e.getMessage());
                    }
                }
            });
            return "{\\"ok\\":true,\\"queued\\":true}";
        } catch (Exception e) {
            return "{\\"ok\\":false,\\"error\\":\\"update_start_failed\\"}";
        }
    }

    private boolean verifyDownloadedUpdate(DownloadManager manager, long id, String expectedSha) {
        ParcelFileDescriptor descriptor = null;
        InputStream input = null;
        try {
            descriptor = manager.openDownloadedFile(id);
            input = new FileInputStream(descriptor.getFileDescriptor());
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] buffer = new byte[65536];
            long total = 0;
            int count;
            while ((count = input.read(buffer)) != -1) {
                total += count;
                if (total > 350L * 1024L * 1024L) return false;
                digest.update(buffer, 0, count);
            }
            StringBuilder actual = new StringBuilder();
            for (byte b : digest.digest()) actual.append(String.format(java.util.Locale.US, "%02x", b & 0xff));
            return total > 1024L * 1024L && expectedSha.equals(actual.toString());
        } catch (Exception e) { return false; }
        finally {
            try { if (input != null) input.close(); } catch (Exception ignored) { }
            try { if (descriptor != null) descriptor.close(); } catch (Exception ignored) { }
        }
    }

    private void openVerifiedUpdate(DownloadManager manager, long id) {
        try {
            SharedPreferences prefs = updatePrefs();
            String expected = prefs.getString(UPDATE_SHA, "");
            if (!expected.matches("[0-9a-f]{64}") || !expected.equals(prefs.getString(UPDATE_VERIFIED, ""))) {
                updateStatus("failed", "The update has not passed checksum verification."); return;
            }
            if (Build.VERSION.SDK_INT >= 26 && !activity.getPackageManager().canRequestPackageInstalls()) {
                updateStatus("permission_required", "Allow ChessBuddy to install this verified update, then tap Install Update.");
                Intent settings = new Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES, Uri.parse("package:" + activity.getPackageName()));
                settings.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                activity.startActivity(settings);
                return;
            }
            Uri apk = manager.getUriForDownloadedFile(id);
            if (apk == null) { updateStatus("failed", "The verified APK is no longer available."); return; }
            Intent install = new Intent(Intent.ACTION_VIEW);
            install.setDataAndType(apk, "application/vnd.android.package-archive");
            install.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_GRANT_READ_URI_PERMISSION);
            activity.startActivity(install);
            updateStatus("install_prompt", "Approve the Android install prompt to finish updating ChessBuddy.");
        } catch (Exception e) {
            updateStatus("failed", "Android could not open the package installer.");
        }
    }

    @JavascriptInterface
    public String installDownloadedUpdate() {
        try {
            SharedPreferences prefs = updatePrefs();
            String idText = prefs.getString(UPDATE_ID, ""), sha = prefs.getString(UPDATE_SHA, "");
            if (!idText.matches("[0-9]{1,20}") || !sha.matches("[0-9a-f]{64}") || !sha.equals(prefs.getString(UPDATE_VERIFIED, "")))
                return "{\\"ok\\":false,\\"error\\":\\"no_verified_update\\"}";
            final long id = Long.parseLong(idText);
            final DownloadManager manager = (DownloadManager) activity.getSystemService(Activity.DOWNLOAD_SERVICE);
            if (manager == null) return "{\\"ok\\":false,\\"error\\":\\"download_manager_unavailable\\"}";
            main.post(new Runnable() { @Override public void run() { openVerifiedUpdate(manager, id); } });
            return "{\\"ok\\":true,\\"installing\\":true}";
        } catch (Exception e) { return "{\\"ok\\":false,\\"error\\":\\"install_start_failed\\"}"; }
    }

    /* ---------------- speech ---------------- */
""")
])

# Bridge adapter exposes only checksum-verified update operations; it never handles signing secrets.
edit("app/src/main/assets/js/native.js", [
("""    hasKey: function (p) { return call('hasKey', [p], false) === true; },
""",
"""    downloadAndInstallUpdate: function (url, sha256) {
      return safeJson(call('downloadAndInstallUpdate', [String(url || ''), String(sha256 || '')], null), { ok: false, error: 'updater_unavailable' });
    },
    installDownloadedUpdate: function () {
      return safeJson(call('installDownloadedUpdate', [], null), { ok: false, error: 'updater_unavailable' });
    },

    hasKey: function (p) { return call('hasKey', [p], false) === true; },
""")
])

edit("app/src/main/AndroidManifest.xml", [
("""    <uses-permission android:name="android.permission.INTERNET" />
""",
"""    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES" />
""")
])

# Release metadata and checksum are verified before Android is asked to install anything.
Path("app/src/main/assets/js/updater.js").write_text(r'''(function (root) {
  'use strict';
  var API = 'https://api.github.com/repos/Mahirabsar2/chessbuddy/releases/latest';
  var current = null, listeners = [];
  function notify(state, message) {
    listeners.slice().forEach(function (fn) { try { fn(state, message); } catch (e) { /* isolate */ } });
  }
  function nativeStatus(state, message) { notify(state, message); }
  root.CBUpdaterNativeStatus = nativeStatus;
  function versionCodeFromTag(tag) {
    var m = String(tag || '').match(/build(\d+)/i);
    return m ? 10000 + Number(m[1]) : 0;
  }
  function asset(release, name) {
    return (release.assets || []).find(function (a) { return a && a.name === name && a.browser_download_url; }) || null;
  }
  async function check() {
    current = null;
    var native = root.CBNative;
    if (!native || !native.available) return { ok: false, error: 'Updates require the Android app.' };
    var res = await native.httpGet(API, 'Accept: application/vnd.github+json\nX-GitHub-Api-Version: 2022-11-28').promise;
    if (res.status !== 200) return { ok: false, error: res.message || ('Release check failed (' + res.status + ').') };
    var release;
    try { release = JSON.parse(res.body); } catch (e) { return { ok: false, error: 'Invalid update metadata.' }; }
    if (!release || release.draft || release.prerelease) return { ok: false, error: 'No stable release is available.' };
    var code = versionCodeFromTag(release.tag_name);
    var installed = native.deviceInfo().versionCode || 0;
    if (!code) return { ok: false, error: 'The release tag has no valid build number.' };
    if (code <= installed) return { ok: true, available: false, versionCode: code };
    var apk = asset(release, 'ChessBuddy-NextGen-1.0.0.apk');
    var checksum = asset(release, 'ChessBuddy-NextGen-1.0.0.apk.sha256');
    if (!apk || !checksum) return { ok: false, error: 'The release is missing its APK or checksum.' };
    var hashRes = await native.httpGet(checksum.browser_download_url, 'Accept: text/plain').promise;
    var match = hashRes.status === 200 && String(hashRes.body || '').match(/\b([a-f0-9]{64})\b/i);
    if (!match) return { ok: false, error: 'The release checksum could not be verified.' };
    current = { versionCode: code, version: release.name || release.tag_name, url: apk.browser_download_url, sha256: match[1].toLowerCase(), notes: String(release.body || '').slice(0, 4000) };
    return { ok: true, available: true, update: current };
  }
  function downloadAndInstall() {
    if (!current) return { ok: false, error: 'Check for an update first.' };
    var result = root.CBNative.downloadAndInstallUpdate(current.url, current.sha256);
    if (!result.ok) notify('failed', 'Could not start update: ' + result.error);
    else notify('downloading', 'Downloading and verifying ChessBuddy ' + current.version + '.');
    return result;
  }
  function installDownloaded() {
    var result = root.CBNative.installDownloadedUpdate();
    if (!result.ok) notify('failed', 'No verified update is ready.');
    return result;
  }
  function onStatus(fn) { if (typeof fn === 'function') listeners.push(fn); return function () { listeners = listeners.filter(function (x) { return x !== fn; }); }; }
  root.CBUpdater = { check: check, downloadAndInstall: downloadAndInstall, installDownloaded: installDownloaded, onStatus: onStatus, versionCodeFromTag: versionCodeFromTag };
})(window);
''', encoding="utf-8")

edit("app/src/main/assets/index.html", [
("""      <div class="card" id="cardEngine"><h3>Stockfish engine</h3>
""",
"""      <div class="card" id="cardUpdates"><h3>Software Updates</h3>
        <p class="muted tiny">ChessBuddy checks its official releases on launch. Updates are downloaded in the background, SHA-256 verified and passed to Android's package installer.</p>
        <div id="updateStatus" class="muted" role="status" aria-live="polite">Checking release status…</div>
        <div class="controls"><button id="btnCheckUpdates" class="btn" type="button">Check for updates</button><button id="btnDownloadUpdate" class="btn primary" type="button" hidden>Download Update</button><button id="btnInstallUpdate" class="btn primary" type="button" hidden>Install Update</button></div>
      </div>
      <div class="card" id="cardEngine"><h3>Stockfish engine</h3>
"""),
("""<script src="js/native.js"></script>
<script src="js/lichess.js"></script>
""",
"""<script src="js/native.js"></script>
<script src="js/updater.js"></script>
<script src="js/lichess.js"></script>
""")
])

edit("app/src/main/assets/js/app.js", [
("""  function bindExtras() {
""",
"""  let availableAppUpdate = null;
  async function checkAppUpdates(silent) {
    const status = $('updateStatus');
    if (!status || !window.CBUpdater) return;
    if (!silent) status.textContent = 'Checking official ChessBuddy releases…';
    $('btnDownloadUpdate').hidden = true;
    try {
      const result = await CBUpdater.check();
      if (!result.ok) { status.textContent = silent ? 'Automatic update check unavailable. Open Settings to retry.' : result.error; return; }
      if (!result.available) { availableAppUpdate = null; status.textContent = 'You are using the latest available ChessBuddy build.'; return; }
      availableAppUpdate = result.update;
      status.textContent = 'Update available: ' + result.update.version + ' · build ' + result.update.versionCode + '. ' + (result.update.notes ? result.update.notes.slice(0, 160) : '');
      $('btnDownloadUpdate').hidden = false;
      // Download in the background automatically; Android still asks before installation.
      const started = CBUpdater.downloadAndInstall();
      if (started.ok) {
        $('btnDownloadUpdate').disabled = true;
        status.textContent = 'Update found. Background download started; Android will ask before installing.';
      }
    } catch (e) { status.textContent = silent ? 'Automatic update check will retry on the next launch.' : (e.message || 'Could not check for updates.'); }
  }

  function bindExtras() {
"""),
("""    $('btnSelfTest').onclick = selfTest;
""",
"""    $('btnSelfTest').onclick = selfTest;
    $('btnCheckUpdates').onclick = () => checkAppUpdates(false);
    $('btnDownloadUpdate').onclick = () => {
      if (!availableAppUpdate) { checkAppUpdates(false); return; }
      const result = CBUpdater.downloadAndInstall();
      if (result.ok) { $('updateStatus').textContent = 'Update download queued. Android will verify the APK first.'; $('btnDownloadUpdate').disabled = true; }
    };
    $('btnInstallUpdate').onclick = () => CBUpdater.installDownloaded();
    CBUpdater.onStatus((state, message) => {
      const status = $('updateStatus'); if (status) status.textContent = message;
      if (state === 'permission_required' || state === 'install_prompt' || state === 'verified') $('btnInstallUpdate').hidden = false;
      if (state === 'downloading') $('btnDownloadUpdate').disabled = true;
      if (state === 'failed') $('btnDownloadUpdate').disabled = false;
    });
"""),
("""    refreshDiagnosticsUi();
    startEngine().then(() => renderEngineUi()).catch(e => Native.logEvent('engine.startup_failed', 'Engine initialization failed: ' + (e && e.name || 'Error')));
""",
"""    refreshDiagnosticsUi();
    // Check once per launch; the updater downloads only a published, checksummed release.
    setTimeout(() => checkAppUpdates(true), 1800);
    startEngine().then(() => renderEngineUi()).catch(e => Native.logEvent('engine.startup_failed', 'Engine initialization failed: ' + (e && e.name || 'Error')));
""")
])

# Persist exactly one pending challenge per participant, including cross-device races.
Path("supabase/migrations/20261120180000_chessbuddy_single_pending_challenge_per_user.sql").write_text(r'''-- Enforce one active pending challenge involving a player, regardless of whether
-- they sent or received it. Advisory transaction locks make the check race-safe.
create or replace function public.cb_send_challenge(p_to_user uuid,p_time_control text,p_color text default 'r')
returns uuid language plpgsql security definer set search_path = '' as $$
declare v_id uuid; v_low text; v_high text;
begin
  if auth.uid() is null then raise exception 'Sign in first'; end if;
  if p_to_user is null or p_to_user=auth.uid() then raise exception 'Choose another player'; end if;
  if p_time_control not in ('none','1+0','3+0','3+2','5+0','10+0','15+10','30+0') then raise exception 'Invalid time control'; end if;
  if p_color not in ('w','b','r') then raise exception 'Invalid colour preference'; end if;
  if not exists(select 1 from public.chessbuddy_profiles where user_id=p_to_user) then raise exception 'Player not found'; end if;

  v_low := least(auth.uid()::text,p_to_user::text);
  v_high := greatest(auth.uid()::text,p_to_user::text);
  perform pg_advisory_xact_lock(hashtextextended(v_low, 0));
  perform pg_advisory_xact_lock(hashtextextended(v_high, 0));

  update public.chessbuddy_challenges
    set status='expired'
    where status='pending' and expires_at<=now()
      and (from_user_id in (auth.uid(),p_to_user) or to_user_id in (auth.uid(),p_to_user));

  if exists (
    select 1 from public.chessbuddy_challenges
    where status='pending' and expires_at>now()
      and (from_user_id in (auth.uid(),p_to_user) or to_user_id in (auth.uid(),p_to_user))
  ) then
    raise exception 'One pending challenge per player. Wait for it to be answered or expire.';
  end if;

  insert into public.chessbuddy_challenges(from_user_id,to_user_id,time_control,from_color)
    values(auth.uid(),p_to_user,p_time_control,p_color) returning id into v_id;
  return v_id;
end; $$;

revoke all on function public.cb_send_challenge(uuid,text,text) from public, anon;
grant execute on function public.cb_send_challenge(uuid,text,text) to authenticated;
''', encoding="utf-8")

# Update settings/UI regression tests and add an offline updater parser test.
Path("tests/logic/updater.test.js").write_text(r'''const assert = require('assert');
const fs = require('fs');
const vm = require('vm');
const src = fs.readFileSync('app/src/main/assets/js/updater.js', 'utf8');
const context = { window: {}, Promise: Promise, String: String, Number: Number };
vm.runInNewContext(src, context);
const U = context.window.CBUpdater;
assert.strictEqual(U.versionCodeFromTag('nextgen-1.0.0-build31'), 10031);
assert.strictEqual(U.versionCodeFromTag('v1.0.0'), 0);
assert.strictEqual(typeof U.check, 'function');
assert.strictEqual(typeof U.downloadAndInstall, 'function');
assert.strictEqual(typeof U.installDownloaded, 'function');
console.log('OK updater: version parsing and verified update API');
''', encoding="utf-8")

# Update minimal Java stubs used by the policy test compiler.
edit("tests/java/stubs/android/content/Context.java", [
('public static final String CLIPBOARD_SERVICE="clipboard", ACTIVITY_SERVICE="activity";',
 'public static final String CLIPBOARD_SERVICE="clipboard", ACTIVITY_SERVICE="activity", DOWNLOAD_SERVICE="download";')
])
edit("tests/java/stubs/android/database/Cursor.java", [
('boolean moveToFirst(); String getString(int i); long getLong(int i);',
 'boolean moveToFirst(); int getColumnIndex(String name); int getInt(int i); String getString(int i); long getLong(int i);')
])
edit("tests/java/stubs/android/content/Intent.java", [
('public static final String ACTION_SEND="a", ACTION_VIEW="view", EXTRA_SUBJECT="s", EXTRA_TEXT="t";',
 'public static final String ACTION_SEND="a", ACTION_VIEW="view", EXTRA_SUBJECT="s", EXTRA_TEXT="t"; public static final int FLAG_ACTIVITY_NEW_TASK=0x10000000, FLAG_GRANT_READ_URI_PERMISSION=1;'),
('public Intent setType(String t){return this;}',
 'public Intent setType(String t){return this;} public Intent setDataAndType(Uri u,String t){data=u;return this;} public Intent addFlags(int f){return this;}')
])
edit("tests/java/stubs/android/os/Environment.java", [
('public static final String DIRECTORY_DOCUMENTS="Documents";',
 'public static final String DIRECTORY_DOCUMENTS="Documents", DIRECTORY_DOWNLOADS="Download";')
])
edit("tests/java/stubs/android/content/pm/PackageManager.java", [
('public abstract class PackageManager { public static class NameNotFoundException',
 'public abstract class PackageManager { public boolean canRequestPackageInstalls(){return true;} public static class NameNotFoundException')
])
Path("tests/java/stubs/android/app/DownloadManager.java").write_text('''package android.app;
import android.content.Context; import android.database.Cursor; import android.net.Uri; import android.os.ParcelFileDescriptor;
public class DownloadManager {
 public static final String COLUMN_STATUS="status", COLUMN_REASON="reason";
 public static final int STATUS_PENDING=1, STATUS_RUNNING=2, STATUS_PAUSED=4, STATUS_SUCCESSFUL=8, STATUS_FAILED=16;
 public long enqueue(Request r){return 1L;} public Cursor query(Query q){return null;} public int remove(long... ids){return 0;}
 public ParcelFileDescriptor openDownloadedFile(long id){return null;} public Uri getUriForDownloadedFile(long id){return null;}
 public static class Request {
  public static final int VISIBILITY_VISIBLE_NOTIFY_COMPLETED=1, NETWORK_WIFI=1, NETWORK_MOBILE=2;
  public Request(Uri u){} public Request setTitle(CharSequence s){return this;} public Request setDescription(CharSequence s){return this;}
  public Request setNotificationVisibility(int n){return this;} public Request setAllowedNetworkTypes(int n){return this;}
  public Request setAllowedOverRoaming(boolean b){return this;} public Request setDestinationInExternalFilesDir(Context c,String d,String f){return this;}
  public Request addRequestHeader(String k,String v){return this;}
 }
 public static class Query { public Query setFilterById(long... ids){return this;} }
}
''', encoding="utf-8")
Path("tests/java/stubs/android/os/ParcelFileDescriptor.java").write_text('''package android.os; public class ParcelFileDescriptor implements java.io.Closeable { public java.io.FileDescriptor getFileDescriptor(){return new java.io.FileDescriptor();} public void close(){} }
''', encoding="utf-8")
Path("tests/java/stubs/android/provider/Settings.java").write_text('''package android.provider; public class Settings { public static final String ACTION_MANAGE_UNKNOWN_APP_SOURCES="android.settings.MANAGE_UNKNOWN_APP_SOURCES"; }
''', encoding="utf-8")

print("Verified updater and one-pending-challenge overlays applied.")
