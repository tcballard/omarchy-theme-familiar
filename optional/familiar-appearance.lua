-- Apply Familiar's geometry only while its theme is selected.
-- Omarchy writes theme.name before reloading Hyprland on each theme switch.
local theme_file = io.open(os.getenv("HOME") .. "/.local/state/omarchy/current/theme.name", "r")
local theme_name = theme_file and theme_file:read("*l") or ""
if theme_file then theme_file:close() end
if theme_name ~= "theme-familiar" then return end

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
