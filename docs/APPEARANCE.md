# Familiar appearance — 20 September 2026

This pass adopts a restrained version of Marvin's rounded, softly raised surfaces: 12px corners, shadows at approximately 14% opacity (7% inactive), 8/16px window gaps, 36px shell control rows, 16px panel padding and 1px neutral menu outlines. The light palette, charcoal bar and blue keyboard focus are retained. Animations remain user-owned.

## Implementation boundary

Focus refinement: the appearance preset now explicitly sets a 3px window border. Theme palette keys `hyprland_active_border` and `hyprland_inactive_border` select opaque Familiar blue (`#0067b8`) and muted grey (`#aeb7c2`). Quattro's generated Hyprland template uses these for ordinary and grouped windows. Previously applied appearance presets must be restored and reapplied to receive the width change. Border colours follow the selected theme; the width remains part of the optional preset.

`shell.spacing.toml` and the existing menu, launcher and control sections contain theme-owned settings. `optional/familiar-appearance.lua` contains compositor geometry. `familiar-preset appearance` manages that file separately from the existing bar preset. Theme switching does not uninstall compositor settings.

Source reference: Omarchy Quattro `e38c1d1289252d2adb96372eeac48d02e489c5b7`, specifically `default/themed/shell.toml.tpl`, `default/hypr/looknfeel.lua`, `config/hypr/hyprland.lua` and `shell/Commons/Style.qml`. The shell's `cornerRadius` reads `decoration:rounding`; explicit spacing tokens pin logical sizes while compositor display scaling continues to apply. Large custom font sizes need visual checking because pinned rows do not automatically grow with the font.

## Automated checks

- Existing bar-preset tests pass.
- Nine isolated appearance tests cover read-only planning, round-trip restoration, file modes, repeat application, preservation of unrelated edits, edited-file/include refusal, failed reload recovery, interrupted application, existing files, symlinks and legacy configuration refusal.
- Bash syntax, TOML parsing and Lua syntax are checked. These do not establish compatibility with a running Hyprland session.

## XPS verification

Use a clean checkout of the PR branch for a preview, or update the installed theme after merge. Before switching the installed checkout to a PR branch, record its revision and ensure `git status --short` is empty:

```sh
cd "$HOME/.config/omarchy/themes/theme-familiar"
git status --short
git rev-parse HEAD  # retain this revision to return to it after previewing
git fetch origin feat/softer-familiar-appearance
git switch --detach FETCH_HEAD
omarchy theme set theme-familiar
bash optional/familiar-preset appearance plan
bash optional/familiar-preset appearance apply
hyprctl configerrors
```

Stop if there are local edits; preserve them before switching. If the theme is installed under another directory name, use that directory and theme name. To finish previewing, restore appearance first, switch back to the recorded revision or `main`, and reapply that theme version. After merge, `git switch main` followed by `git pull --ff-only` updates the checkout.

1. Record `omarchy-version`, the installed Omarchy source revision and display scale. Confirm `hyprctl configerrors` is empty.
2. Inspect tiled and floating windows, fullscreen windows and maximized application content. Check corner clipping and shadows against all four wallpapers.
3. Open the launcher, Omarchy menu, bar calendar, audio/network popup, notification and a tooltip. Confirm rounded shared surfaces and no clipped rows or empty-state text.
4. Navigate controls using Tab and the keyboard cursor. Blue focus must remain distinguishable from hover and selection.
5. Inspect lock screen, terminal, editor and a GTK app. Confirm readable light-theme text, especially plugin popups previously checked on the XPS.
6. Repeat at the XPS's normal fractional scale and with any custom font size. Check long menu items and searchable dropdowns.
7. Switch themes and verify that the optional geometry remains active as documented. Restore appearance, confirm the previous geometry returns, and check `hyprctl configerrors` again. The bottom bar must remain where it was.

Live XPS/compositor rendering and these new spacing values are **not yet verified**. Repository README/validation notes predate the user's later desktop checks; this document makes no claim about their results or the separate popup fix.
