# Familiar

A Windows-inspired light theme for Omarchy Quattro: clean application surfaces, a charcoal bar, blue selections and four original wallpapers with the official Omarchy logo.

![Wallpaper collection — not a live desktop screenshot](docs/wallpapers.jpg)

Clockwise from top left: Blue Bloom, Pearl Silk, Aurora Tides and Violet Orbit. These change the wallpaper; the application palette remains the Familiar light theme.

## Install

Development preview targeting Quattro. Record your current theme and background before installation:

```sh
cat "$HOME/.local/state/omarchy/current/theme.name"
readlink -f "$HOME/.local/state/omarchy/current/background"
omarchy theme install https://github.com/tcballard/omarchy-theme-familiar
```

The installer applies the theme immediately and may replace an existing copy. This repository name produces the installed theme name **theme-familiar**. Select a wallpaper with Omarchy's background picker.

To restore your previous theme, run `omarchy-theme-set "PREVIOUS THEME NAME"`, substituting the recorded name, then select the previous wallpaper if needed.

## Optional familiar desktop layout

The theme alone changes colours, typography and bar size. The optional preset moves the bar to the bottom, puts the Omarchy menu and open-window buttons on the left, and keeps clock/system controls on the right. It preserves extra widgets and unrelated settings.

From a checkout of this repository:

```sh
bash optional/familiar-preset plan
bash optional/familiar-preset apply
# Undo the layout:
bash optional/familiar-preset restore
```

Requires Quattro's running shell, Bash, jq and flock. The plan is read-only. Apply installs the included task widget and saves your previous bar configuration. Restore refuses to overwrite later bar edits and retains unrelated setting changes. Widget files remain installed but inactive after restoration. Snapshots live under `${XDG_STATE_HOME:-$HOME/.local/state}/familiar-preset`. Keep this checkout for rollback. If Omarchy uses a nonstandard installation directory, set OMARCHY_PATH accordingly.

This is not a Windows shell replacement: there are no added title-bar buttons, pinned applications, minimize-to-taskbar, desktop icons or Windows snap behaviour. The menu remains Omarchy's menu, with normal Omarchy tiling and shortcuts. Application-provided window controls remain in use.

## Status

Built against Quattro commit b679363bed05415771a1b1dc92c6899a908236f7. Palette/TOML checks, all 19 upstream template-generation checks and isolated preset/widget checks passed. Live desktop, display scaling, compositor activation and registry validation remain unverified. See [validation evidence](docs/VALIDATION.md).

Five complete shell-section overrides customise bar, font, controls, launcher and menu; revisit these when upstream adds section settings. Other applications derive colours through Omarchy's templates. User templates may take precedence.

Artwork provenance and official logo source: [CREDITS.md](CREDITS.md). No Microsoft wallpaper files are included. Not affiliated with Microsoft. This preview has not been submitted to the theme registry; no fabricated desktop screenshot is provided.
