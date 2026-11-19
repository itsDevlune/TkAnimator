# Animation reference

- `Animator(widget).move(x, y, duration=..., easing=...)`: move a placed widget to absolute coordinates.
- `follow_path(widget, points, ...)`: move a placed widget over a distance-weighted polyline.
- `slide(widget, direction, distance, ...)`: offset a placed widget in one of four directions.
- `shake`, `bounce`, `pulse`, `expand_shrink`: geometry effects for placed widgets.
- `color_transition(widget, start_color, end_color, property_name="bg", ...)`: interpolate `#RRGGBB` colors.
- `fade_toplevel(window, fade_in=True, ...)`: fade a whole root/toplevel using native window alpha where supported.
- `move_item(canvas, item, x, y, ...)`: move a Canvas item center; implemented with Canvas coordinates.
- `scroll(canvas, target, axis="y", ...)`: animate Canvas viewport position to a normalized fraction.
- `rotate_image(canvas, item, pillow_image, angle, ...)`: rotate a Canvas image using the optional Pillow dependency.

Each function returns a handle. Call `start()` to begin. The legacy `animate_wiggle` entry point deliberately raises because Tk cannot rotate standard widgets; image rotation must be rendered through Canvas or another image backend.

Geometry and view animations default to conflict replacement by property or Canvas item. `Animation(..., conflict="ignore")` declines to start if that key is occupied, while `conflict="allow"` opts into multiple writers.
