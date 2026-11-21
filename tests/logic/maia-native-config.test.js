const assert = require('assert');
const fs = require('fs');
const native = fs.readFileSync('app/src/main/java/com/chessbuddy/NativeBridge.java', 'utf8');
const lc0Build = fs.readFileSync('scripts/build_lc0_android.sh', 'utf8');
const manifest = JSON.parse(fs.readFileSync('app/src/main/assets/models/maia-models.json', 'utf8'));
const ratings = manifest.models.map(x => x.rating).sort((a,b) => a-b);
assert.deepStrictEqual(ratings, [1100,1200,1300,1400,1500,1600,1700,1800,1900]);
assert(lc0Build.includes('-Ddefault_search=policyhead'), 'Lc0 build defaults to Maia policyhead search');
assert(native.includes('"--weights=" + model.getAbsolutePath()'), 'Lc0 receives the selected verified weights path');
assert(native.includes('"--backend=blas"'), 'Lc0 uses the bundled CPU BLAS backend');
assert(!native.includes('--search-algorithm=policyhead'), 'do not pass unsupported search-algorithm CLI flag');
assert(native.includes('gitBlobSha1(file)'), 'Maia models without published SHA-256 use pinned upstream Git blob verification');
for (const model of manifest.models) {
  assert(model.bytes > 1000000 && model.bytes < 2000000, model.id + ' has a plausible pinned file size');
  assert(model.url.endsWith('/' + model.file), model.id + ' URL matches its manifest filename');
  assert(/^[a-f0-9]{64}$/.test(model.sha256) || /^[a-f0-9]{40}$/.test(model.gitBlobSha1 || ''), model.id + ' has a pinned integrity digest');
}
console.log('OK Maia native config: nine pinned models, supported Lc0 policyhead startup and verified weights');
