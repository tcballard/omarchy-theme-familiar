# Joined shell headers

Familiar opts into the shell's joined-header style through `shell.popups.toml`. It uses a light grey (`#e9edf2`) header on the existing light panel body, with the existing dark text and blue outline. The header fill follows the panel's top corners and reaches the frame.

## Compatibility

This requires the shell support in [tcballard/omarchy PR #13](https://github.com/tcballard/omarchy/pull/13), source `9ef8414a58220d89cfd8768b39c4262dd076dadf`. It is a draft change based on upstream Quattro `47caa9be439e1876b6048a32a868688e9c697d48`, and has not been submitted or merged upstream.

Older shells ignore the new tokens and keep the existing appearance. Panels identify their own header through the shell's headerItem property. Audio, Network, Dropbox and Tailscale are wired in the initial shell patch. Other panels and third-party plugins need to identify their header before the effect applies. Notification toasts are unaffected.

The optional Familiar appearance preset still owns compositor rounding. The header follows whatever corner radius the shell is currently using. This feature belongs to the theme and shell; it does not require Familiar Desktop.

## Verification

An isolated Quickshell 0.3.2 / Qt 6.12.0 component fixture passed twelve runtime assertions and its inset/joined render was visually checked. It covers theme opt-in/reset, user overrides, hidden/missing/scrolled headers, border widths and height clamping. This does not establish live service-panel acceptance.

Before merging, test both branches together on the XPS. Record both source SHAs, Omarchy/Qt versions and display scale. Check the four supported panel headers, mouse and keyboard controls, short/scrolling panels, fractional scaling and large fonts. Switch away from Familiar and back. Confirm ordinary popups and notification toasts still render correctly. Roll back by returning both checkouts to their recorded previous revisions and reapplying the previous theme.

Keep the theme change in draft until the shell dependency and desktop verification are resolved.
