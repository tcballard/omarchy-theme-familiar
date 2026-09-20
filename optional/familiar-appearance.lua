-- Familiar's optional geometry. Colours and focus remain theme-owned.
-- Inspired by Marvin's separation of theme tokens and compositor settings.
hl.config({
  general = {
    border_size = 5,
    gaps_in = 8,
    gaps_out = 16,
  },
  decoration = {
    rounding = 12,
    shadow = {
      enabled = true,
      range = 24,
      render_power = 2,
      color = "rgba(00000024)",
      color_inactive = "rgba(00000012)",
    },
  },
})
