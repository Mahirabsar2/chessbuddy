#!/usr/bin/env python3
"""Apply responsive, touch-friendly sizing rules to all Next Gen screens."""
from pathlib import Path

css = Path("app/src/main/assets/css/app.css")
s = css.read_text(encoding="utf-8")
marker = "/* Next Gen global responsive layout and touch-target pass */"
if marker not in s:
    s += """
/* Next Gen global responsive layout and touch-target pass */
*, *::before, *::after { box-sizing: border-box; }
button, .btn, input, select, textarea { max-width: 100%; min-width: 0; }
button, .btn {
  overflow-wrap: anywhere;
  white-space: normal;
  touch-action: manipulation;
}
button:not(.icon-btn):not(.tab), .btn:not(.icon-btn) {
  min-height: 42px;
}
button svg, .btn svg { flex: 0 0 auto; max-width: 22px; max-height: 22px; }
.view, .view > *, .card, .content-head, .row-btn, .rt { min-width: 0; }
.view { width: 100%; max-width: 100%; overflow-x: clip; }
.card { max-width: 100%; overflow-wrap: anywhere; }
input, select, textarea { width: 100%; }
.tabbar {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 2px;
  width: 100%;
  padding-left: max(5px, env(safe-area-inset-left));
  padding-right: max(5px, env(safe-area-inset-right));
}
.tabbar .tab {
  min-width: 0;
  min-height: 54px;
  padding: 5px 2px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  overflow: hidden;
}
.tabbar .tab i {
  display: block;
  max-width: 100%;
  font-size: clamp(9px, 2.7vw, 11px);
  line-height: 1.15;
  font-style: normal;
  text-overflow: ellipsis;
  overflow: hidden;
}
.tabbar .tab span { width: 21px; height: 21px; flex: 0 0 21px; }
.tabbar .tab svg { width: 21px; height: 21px; }
.controls, .puzzle-actions, .rv-summary-actions {
  display: flex;
  flex-wrap: wrap;
  align-items: stretch;
  gap: 8px;
}
.controls > *, .puzzle-actions > * { flex: 1 1 120px; min-width: 0; }
.modal, .sheet, .modal-card {
  max-width: calc(100vw - 16px);
  max-height: calc(100dvh - env(safe-area-inset-top, 0px) - 8px);
  overflow-x: hidden;
  overscroll-behavior: contain;
}
@media (max-width: 360px) {
  .tabbar .tab { padding-left: 1px; padding-right: 1px; }
  .tabbar .tab i { font-size: 9px; letter-spacing: -.15px; }
  .content-head { flex-wrap: wrap; }
  .controls > *, .puzzle-actions > * { flex-basis: 100%; }
}
"""
    css.write_text(s + "\n", encoding="utf-8")

# Fail early if any essential responsive sizing rule was accidentally removed.
for required in ["touch-action: manipulation", "repeat(5, minmax(0, 1fr))", "min-height: 42px", "max-height: calc(100dvh"]:
    if required not in s:
        raise SystemExit("Missing responsive layout rule: " + required)
print("Next Gen responsive layout and touch-target pass applied.")
