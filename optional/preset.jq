# Keep unrelated configuration, custom widgets and per-widget options.
def widget_id: if type == "string" then . else .id end;
def entry($items; $id):
  ([$items[] | select(widget_id == $id)][0] // {id:$id})
  | if type == "string" then {id:.} else . end;
(.bar.layout.left + .bar.layout.center + .bar.layout.right) as $items
| ["omarchy.menu", "local.familiar-tasks", "omarchy.tray", "omarchy.network", "omarchy.audio", "omarchy.power", "omarchy.clock"] as $managed
| .bar.id = "omarchy.bar"
| .bar.position = "bottom"
| .bar.transparent = false
| .bar.centerAnchor = ""
| .bar.layout.left = [entry($items; "omarchy.menu"), entry($items; "local.familiar-tasks")]
| .bar.layout.center = []
| .bar.layout.right = ([$items[] | select((widget_id as $id | $managed | index($id)) == null)]
  + [entry($items; "omarchy.tray"), entry($items; "omarchy.network"), entry($items; "omarchy.audio"), entry($items; "omarchy.power"), (entry($items; "omarchy.clock") | .format = "HH:mm  dd/MM")])
