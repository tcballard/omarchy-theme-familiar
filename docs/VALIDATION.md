# Validation — 14 September 2026

## Correction audit after PR #1

Audited theme implementation: `0cfbf1f068b636472a60e0aa6cd3860b18183416` (merged by PR #1). This correction changes documentation only.

| Check | Result | Evidence / limit |
| --- | --- | --- |
| Official Theme badge | PASS | Exact SVG URL from the bundle README, pinned to badge revision `75975e5b5bf75e7ede3764bcd2950046f7abfe2c`; fetched successfully; displayed at 20px with natural proportions. |
| Compatibility wording | PASS | Target is Omarchy Quattro. No installed Omarchy version has been tested. |
| Root palette and five shell TOML files | PASS | All six parsed with `tomllib`; required semantic colours and explicit light mode present. |
| Main text contrast | PASS | Recomputed foreground/background: 14.89:1. |
| App template generation | PASS | Regenerated all 19 retained upstream templates with upstream Bash scripts; no unresolved placeholders. |
| Shell section replacement | PASS | All five generated sections equal their theme overrides. |
| Wallpapers | PASS | Fully decoded all four final PNGs: 1672 × 941 each. |
| Symlinks | PASS | None found. |
| Preset syntax and rollback | PASS | `bash -n optional/familiar-preset` and `python optional/test-preset.py`; existing/default configuration, unknown settings, repeat application, conflict refusal, reload recovery and malformed input covered. |
| Rust scaffold helper | NOT RERUN | Passed during the original build; no Cargo executable in this audit environment. |
| Mocked QML checks | NOT RERUN | Original build recorded parser/offscreen checks; no new QML runtime result claimed here. |
| Live Omarchy / Git installation | NOT RUN | No live desktop, installed-version result, compositor activation, application reload, theme switching or display-scaling evidence. |
| Registry validator | NOT RUN | This is a development preview, not a registry-ready release. |
| Real desktop preview | MISSING | The README image is explicitly a wallpaper contact sheet. |
| Release licensing | OUTSTANDING | Artwork provenance recorded; release licence and redistribution declarations remain unresolved. |

Template checks use the retained source snapshot identified during the original build as Quattro `b679363bed05415771a1b1dc92c6899a908236f7`. They are isolated generation checks, not a test against today's installed Omarchy release.

## Corrections made

Added the required official category badge and explicit target/development labels. Removed stale credits for `familiar-blue.png`, which is not included in the repository. Separated checks reproduced in this audit from historical results and missing live/release evidence.

The original build also recorded further palette contrast and mocked QML sizing/activation-request checks. Those historical results do not establish live compatibility. No production-readiness or full accessibility claim is made.
