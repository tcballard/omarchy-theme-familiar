# Validation — 14 September 2026

PASS — Rust theme helper, six theme TOML files, supported section keys.
PASS — all 19 templates from Quattro b679363bed05415771a1b1dc92c6899a908236f7 generated with actual upstream Bash scripts; no unresolved tokens; bar/font/launcher values verified.
PASS — foreground/background 14.89:1; accent/background 5.35:1; white selected text on blue 5.78:1; white bar text 15.93:1; minimum checked semantic/bright text contrast 5.34:1.
PASS — wallpaper decoded at 1672 × 941 pixels. No symlinks.
PASS — Bash syntax and isolated apply/restore tests (see test-preset.py).
PASS — QML parser and offscreen Qt instantiation, using real upstream UI base components with mocked theme and window APIs. Empty/two-window/overflow/vertical sizing and activation request checked.

NOT RUN — live Omarchy application, actual window activation, keyboard traversal into bar, multi-monitor/display scaling, real app reload, theme switching, real desktop screenshot and registry validator.

The mocked tests verify implementation paths, not compatibility with a running compositor. No production-readiness or full accessibility certification is claimed.
