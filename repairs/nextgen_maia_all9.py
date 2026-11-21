#!/usr/bin/env python3
"""Make the extracted Maia/Lc0 build and APK verifier agree on all nine official Maia-1 weights."""
from pathlib import Path

RATINGS = "1100 1200 1300 1400 1500 1600 1700 1800 1900"
IDS = "{'maia-1100','maia-1200','maia-1300','maia-1400','maia-1500','maia-1600','maia-1700','maia-1800','maia-1900'}"

def replace_exact(path: str, old: str, new: str, expected_count: int = 1) -> None:
    p = Path(path)
    s = p.read_text(encoding="utf-8")
    count = s.count(old)
    if count == 0 and new in s:
        return
    if count != expected_count:
        raise SystemExit(f"{path}: expected {expected_count} copies of fragment, found {count}")
    p.write_text(s.replace(old, new), encoding="utf-8")

# The native build creates model files and the manifest. The previous three-model
# loop silently overwrote the nine-model manifest prepared earlier in CI.
replace_exact(
    "scripts/build_lc0_android.sh",
    "for rating in 1100 1500 1900; do",
    f"for rating in {RATINGS}; do",
    expected_count=2,
)
replace_exact(
    "scripts/build_lc0_android.sh",
    "assert {m['id'] for m in d['models']} == {'maia-1100','maia-1500','maia-1900'}",
    f"assert {{m['id'] for m in d['models']}} == {IDS}",
)

# APK verification must enforce the same full model set as the selector and native bridge.
replace_exact(
    "scripts/verify_apk.sh",
    "assert set(models)=={'maia-1100','maia-1500','maia-1900'}",
    f"assert set(models)=={IDS}",
)
replace_exact(
    "scripts/verify_apk.sh",
    'pass "Maia 1100/1500/1900 manifest contains official URLs, byte sizes and SHA-256 hashes"',
    'pass "All nine Maia-1 models (1100–1900) contain official URLs, byte sizes and SHA-256 hashes"',
)

# Keep the documentation aligned with the behavior actually built.
doc = Path("docs/MAIA_LC0_STATUS.md")
if doc.exists():
    s = doc.read_text(encoding="utf-8")
    s = s.replace("1100/1500/1900", "1100–1900 (nine 100-Elo steps)")
    s = s.replace("all three Maia manifest records", "all nine Maia manifest records")
    s = s.replace("maia-1100, maia-1500, or maia-1900", "any official Maia-1 model from 1100 through 1900")
    s = s.replace("Maia 1100 and Maia 1500 and Maia 1900", "all nine Maia-1 models")
    doc.write_text(s, encoding="utf-8")

print("Maia build, manifest and APK verification now cover all nine official models.")
