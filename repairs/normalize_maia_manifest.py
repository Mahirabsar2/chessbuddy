#!/usr/bin/env python3
"""Repair the literal backslash-n suffix in the upstream Maia manifest and validate it."""
import json
from pathlib import Path

path = Path("app/src/main/assets/models/maia-models.json")
raw = path.read_text(encoding="utf-8")
if raw.endswith("\\n"):
    raw = raw[:-2] + "\n"
manifest = json.loads(raw)
models = manifest.get("models")
expected = [1100,1200,1300,1400,1500,1600,1700,1800,1900]
if not isinstance(models, list) or sorted(m.get("rating") for m in models) != expected:
    raise SystemExit("Maia manifest must contain exactly the nine official 1100-1900 models")
for model in models:
    if not model.get("url", "").endswith("/" + model.get("file", "")):
        raise SystemExit("Invalid Maia model URL: " + str(model.get("id")))
    if not (len(model.get("sha256", "")) == 64 or len(model.get("gitBlobSha1", "")) == 40):
        raise SystemExit("Missing pinned integrity digest: " + str(model.get("id")))
path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print("Maia manifest normalized and validated: 9 models")
