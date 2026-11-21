#!/usr/bin/env python3
"""Integrate the versioned ElevenLabs character media into the Next Gen app source."""
from pathlib import Path
import re

def replace_once(path: str, old: str, new: str, label: str) -> None:
    p = Path(path)
    s = p.read_text(encoding="utf-8")
    if new in s:
        return
    if old not in s:
        raise SystemExit("Character-media patch could not find " + label + " in " + path)
    p.write_text(s.replace(old, new, 1), encoding="utf-8")

# Add four original reusable chess characters and attach the Mittens media to the
# existing Mittens bot. Their voice files are archetype samples, not clones.
strength = Path("app/src/main/assets/js/strength.js")
s = strength.read_text(encoding="utf-8")
if "var MEDIA_CAST =" not in s:
    anchor = "  var MAIA = ["
    if anchor not in s:
        raise SystemExit("Could not find Maia roster anchor in strength.js")
    cast = """  var MEDIA_CAST = [
    { id: 'cb_streamer', name: 'The Commentator', elo: 1500, avatar: 'streamer', voice: 'streamer', desc: 'An original ChessBuddy chess-stream commentator: quick, playful and tactical.' },
    { id: 'cb_mentor', name: 'The Mentor', elo: 1650, avatar: 'coach', voice: 'coach', desc: 'A calm, encouraging ChessBuddy coach who looks for forcing moves and clear plans.' },
    { id: 'cb_veteran', name: 'The Endgame Sage', elo: 1850, avatar: 'veteran', voice: 'veteran', desc: 'A patient veteran who likes technical endings and long-term plans.' },
    { id: 'cb_prodigy', name: 'The Young Prodigy', elo: 1250, avatar: 'prodigy', voice: 'streamer', desc: 'An upbeat young rival who spots tactical chances and plays with confidence.' }
  ].map(function (p) {
    var b = bot(p.id, p.name, p.elo, 'ChessBuddy Originals', p.desc, genSpec(p.id));
    b.mediaAvatarKey = p.avatar;
    b.mediaVoiceKey = p.voice;
    b.isOriginal = true;
    return b;
  });
  var mittensMedia = BOTS.find(function (b) {
    return /mittens/i.test(String(b.id || '') + ' ' + String(b.name || ''));
  });
  if (mittensMedia) {
    mittensMedia.mediaAvatarKey = 'mittens';
    mittensMedia.mediaVoiceKey = 'mittens';
  }
"""
    s = s.replace(anchor, cast + anchor, 1)
if "BOTS.concat(GM, LEGENDS, CHARACTERS, GENERATED, VIS, REAL_PLAYERS, MEDIA_CAST, MAIA)" not in s:
    old = "BOTS = BOTS.concat(GM, LEGENDS, CHARACTERS, GENERATED, VIS, REAL_PLAYERS, MAIA);"
    new = "BOTS = BOTS.concat(GM, LEGENDS, CHARACTERS, GENERATED, VIS, REAL_PLAYERS, MEDIA_CAST, MAIA);"
    if old not in s:
        raise SystemExit("Could not find bot roster concat point")
    s = s.replace(old, new, 1)
s = s.replace("'Personalities', 'Characters', 'Visualization', 'Chess Personalities', 'Maia'];",
              "'Personalities', 'Characters', 'Visualization', 'Chess Personalities', 'ChessBuddy Originals', 'Maia'];")
strength.write_text(s, encoding="utf-8")

# Render the generated portraits directly in the bot list for the matching bots.
app = Path("app/src/main/assets/js/app.js")
a = app.read_text(encoding="utf-8")
if "cb-bot-portrait" not in a:
    anchor = "  const sfPlayer = b =>"
    injected = """  // Use original generated character portraits for the ChessBuddy media cast.
  if (window.Avatars && typeof Avatars.forBot === 'function' && !Avatars.__cbMediaWrapped) {
    const previousBotAvatar = Avatars.forBot.bind(Avatars);
    Avatars.forBot = function (botProfile) {
      const key = botProfile && botProfile.mediaAvatarKey;
      if (key && /^(mittens|streamer|coach|veteran|prodigy)$/.test(key)) {
        const label = String(botProfile.name || 'ChessBuddy character').replace(/[&<>\"]/g, '');
        return '<img class="cb-bot-portrait" src="media/avatars/' + key + '.jpg" alt="' + label + '" loading="lazy">';
      }
      return previousBotAvatar(botProfile);
    };
    Avatars.__cbMediaWrapped = true;
  }

"""
    if anchor not in a:
        raise SystemExit("Could not find sfPlayer anchor for portrait integration")
    a = a.replace(anchor, injected + anchor, 1)

# A compact Character Studio shows the original portraits and plays each generated
# voice only after an explicit tap, respecting Android audio/autoplay behavior.
if "function openCharacterStudio()" not in a:
    anchor = "  let availableAppUpdate = null;"
    if anchor not in a:
        raise SystemExit("Could not find Character Studio controller anchor")
    ui = """  let cbCharacterAudio = null;
  function stopCharacterVoice() {
    if (cbCharacterAudio) {
      try { cbCharacterAudio.pause(); cbCharacterAudio.currentTime = 0; } catch (e) { /* ignore */ }
      cbCharacterAudio = null;
    }
  }
  function playCharacterVoice(key) {
    const allowed = ['mittens', 'streamer', 'coach', 'veteran'];
    if (allowed.indexOf(key) < 0) return;
    stopCharacterVoice();
    try {
      cbCharacterAudio = new Audio('media/voices/' + key + '.mp3');
      cbCharacterAudio.play().catch(() => toast('Audio playback is unavailable on this device.'));
    } catch (e) { toast('Audio playback is unavailable on this device.'); }
  }
  function openCharacterStudio() {
    const cast = [
      { key: 'mittens', name: 'Mittens', role: 'Wounded pride, quiet fury', voice: 'mittens', text: 'A fiery little rival who remembers every blunder.' },
      { key: 'streamer', name: 'The Commentator', role: 'Chess streamer archetype', voice: 'streamer', text: 'An original, energetic commentator with a tactical eye.' },
      { key: 'coach', name: 'The Mentor', role: 'Grandmaster coach archetype', voice: 'coach', text: 'Calm guidance, clear plans and supportive feedback.' },
      { key: 'veteran', name: 'The Endgame Sage', role: 'Veteran strategist archetype', voice: 'veteran', text: 'Patient, thoughtful and dangerous in technical endings.' },
      { key: 'prodigy', name: 'The Young Prodigy', role: 'Rising talent archetype', voice: 'streamer', text: 'An upbeat young rival; shares the commentator voice preset.' }
    ];
    const cards = cast.map(c => '<article class="cb-character-card">' +
      '<img src="media/avatars/' + c.key + '.jpg" alt="' + esc(c.name) + '" loading="lazy">' +
      '<div class="cb-character-copy"><span class="eyebrow">' + esc(c.role) + '</span><h3>' + esc(c.name) + '</h3><p>' + esc(c.text) + '</p>' +
      '<button class="btn small" type="button" data-cb-voice="' + c.voice + '">Listen to Voice</button></div></article>').join('');
    openModal('<div class="cb-character-studio"><div class="content-head"><div><span class="eyebrow">ORIGINAL CHESSBUDDY CAST</span><h2>Character Studio</h2></div><button class="btn small" id="cbCharacterClose" type="button">Close</button></div><div class="cb-character-grid">' + cards + '</div></div>');
    $('cbCharacterClose').onclick = function () { stopCharacterVoice(); closeModal(); };
    document.querySelectorAll('[data-cb-voice]').forEach(function (button) {
      button.onclick = function () { playCharacterVoice(button.getAttribute('data-cb-voice')); };
    });
  }

"""
    a = a.replace(anchor, ui + anchor, 1)

# Bind the More-page entry point after the existing More hub actions.
replace_once(
    "app/src/main/assets/js/app.js",
    "    $('moreSettings').onclick = () => showTab('settings');",
    "    $('moreSettings').onclick = () => showTab('settings');\n    $('moreCharacters').onclick = openCharacterStudio;",
    "More > Character Studio action"
)
app.write_text(a, encoding="utf-8")

# Insert a real entry point into More; it is not an inert navigation tab.
replace_once(
    "app/src/main/assets/index.html",
    '      <div class="card"><h3>Achievements</h3>',
    """      <div class="card"><div class="content-head"><div><span class="eyebrow">MEET THE CAST</span><h3>Character Studio</h3></div><span class="chip">Original</span></div><p class="muted tiny">Meet the ChessBuddy characters, see their generated portraits and listen to their short voice introductions.</p><button class="btn primary" id="moreCharacters" type="button">Open Character Studio</button></div>
      <div class="card"><h3>Achievements</h3>""",
    "More page Character Studio card"
)

# Responsive avatar rendering and gallery layout.
css = Path("app/src/main/assets/css/app.css")
style = """
/* Original Next Gen character portraits and Character Studio */
.cb-bot-portrait { display:block; width:100%; height:100%; object-fit:cover; border-radius:inherit; }
.cb-character-studio { min-width:0; }
.cb-character-studio h2 { margin:0; font-size:20px; }
.cb-character-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px; max-height:70vh; overflow-y:auto; padding:2px; }
.cb-character-card { min-width:0; overflow:hidden; border:1px solid var(--line); border-radius:13px; background:var(--surface); }
.cb-character-card>img { width:100%; aspect-ratio:1; object-fit:cover; display:block; }
.cb-character-copy { padding:10px; min-width:0; }
.cb-character-copy h3 { margin:4px 0; font-size:14px; overflow-wrap:anywhere; }
.cb-character-copy p { min-height:40px; margin:0 0 8px; font-size:11px; color:var(--muted); line-height:1.35; }
.cb-character-copy .btn { width:100%; min-height:38px; padding:7px 6px; font-size:11px; }
@media (max-width:380px) { .cb-character-grid { grid-template-columns:1fr; } .cb-character-card { display:grid; grid-template-columns:104px minmax(0,1fr); } .cb-character-card>img { height:100%; aspect-ratio:auto; min-height:120px; } }
"""
marker = "/* Original Next Gen character portraits and Character Studio */"
s = css.read_text(encoding="utf-8")
if marker not in s:
    css.write_text(s + "\n" + style, encoding="utf-8")

# Regression tests: the test runs after the media pack has been downloaded.
smoke = Path("tests/logic/rebuild-smoke.test.js")
t = smoke.read_text(encoding="utf-8")
check = """for (const key of ['mittens','streamer','coach','veteran','prodigy']) {
  assert(fs.existsSync('app/src/main/assets/media/avatars/' + key + '.jpg'), 'portrait asset bundled: ' + key);
}
for (const key of ['mittens','streamer','coach','veteran']) {
  assert(fs.existsSync('app/src/main/assets/media/voices/' + key + '.mp3'), 'voice asset bundled: ' + key);
}
assert(app.includes('function openCharacterStudio()'), 'Character Studio is implemented');
"""
if "portrait asset bundled:" not in t:
    marker2 = "console.log('OK rebuild-smoke:"
    if marker2 not in t:
        raise SystemExit("Could not find rebuild-smoke test completion marker")
    t = t.replace(marker2, check + marker2, 1)
    smoke.write_text(t, encoding="utf-8")

print("Character media integration applied: portraits, original bot profiles, voice playback and Character Studio.")
