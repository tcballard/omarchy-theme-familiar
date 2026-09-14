# Familiar Tasks

A Quattro bar widget for selecting open windows. Uses Omarchy BarWidget/WidgetButton and Quickshell's existing ToplevelManager; no polling, network, background service or shell execution. All title text is rendered as plain text.

Left-click activates a window. Focused buttons also accept Enter/Space. Active windows have an underline; long titles elide with full titles in tooltips. The horizontal strip is capped at 420px and scrolls for overflow. Vertical bars use a single-letter list capped at 280px height. Every compositor-exposed window is listed on each monitor. The theme's foreground provides the active marker so it remains readable on either light or dark bars.

This does not minimize or close windows. It requests activation through the compositor API, which may decline it. Live host behaviour remains unverified. The optional parent preset installs/enables this widget; the theme alone does not.
