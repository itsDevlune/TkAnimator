# TkAnimator

TkAnimator is a dependency-free animation engine for Tkinter. It uses a monotonic clock and Tk `after()` scheduling so widget updates run on the event-loop thread. The project keeps the original `TkAnimations` API while adding a typed package API.

## Install

```bash
python -m pip install .
```

For development: `python -m pip install -e ".[dev]"`. Python 3.10+ is supported. Tkinter must be available in your Python installation.

Optional Canvas image rotation needs Pillow: `python -m pip install "tk-animator[images]"`.

## Quick start

```python
import tkinter as tk
from tkanimator import Animator, Easing

root = tk.Tk()
button = tk.Button(root, text="Animate me")
button.place(x=20, y=50)
animator = Animator(button)
animator.move(x=300, y=50, duration=1000, easing=Easing.EASE_IN_OUT_CUBIC).start()
root.mainloop()
```

`Animation.start()` returns immediately. Keep a handle to pause/resume/cancel/restart it. Durations and delays are milliseconds; `repeat` is the number of additional cycles (`-1` means infinite), and `yoyo=True` reverses every other cycle. `speed=2` doubles playback speed. Built-in property animations replace a running animation on the same target property; pass `conflict="allow"` to opt into concurrent writes.

## Effects

```python
from tkanimator.animations import slide, shake, bounce, pulse, color_transition, follow_path, scroll
from tkanimator.adapters.canvas import move_item, rotate_image

handle = slide(button, "left", 120, duration=500).start()
handle.pause()
handle.resume()
handle.cancel()
```

Canvas items can be animated with `move_item(canvas, item, x, y)` and Canvas viewports with `scroll(canvas, target=.5, axis="y")`. `follow_path(widget, [(x1, y1), ...])` uses distance-weighted polyline motion. `rotate_image` uses Pillow and rotates a Canvas image item; retain your `PhotoImage` reference.

Geometry effects (`move`, `slide`, `follow_path`, `shake`, `bounce`, `pulse`, `expand_shrink`) require `place()` because Tk's `pack` and `grid` own layout. Color transitions update a named Tk option such as `bg` or `fg`. Arbitrary widget rotation and per-widget opacity are not supported by Tk; `fade_toplevel` is provided for whole-window alpha on platforms that support it. Use a Canvas image item for transforms.

`Sequence([a, b])` plays handles serially; `Parallel([a, b])` starts them together. `Timeline(widget).add(animation, at_ms=250)` schedules multiple handles from one start. `stagger(handles, delay_ms)` returns a sequential group with each handle offset by the requested delay.

## Easing reference

`Easing` includes linear, in/out/in-out quad, cubic, quart, quint, sine, expo, and circ, plus back, elastic, bounce, and spring-inspired out curves. A custom easing can be any callable from progress to eased progress.

## Compatibility and migration

The original `tk_animations.py` module and `TkAnimations.animate_*` methods remain. They now return `Animation` handles (previously they returned `None`). Fade methods work on a root or toplevel only. `animate_wiggle` now raises `ValueError` because ordinary Tk widgets cannot rotate; use `rotate_image` on a Canvas image. Movement and size methods require `place()`. Calls to `update()` were removed, avoiding reentrant event processing.

Launch the interactive showcase with `tkanimator-showcase` (or `python -m tkanimator.showcase`). It includes standard widget and Canvas previews, easing and duration controls, a curve visualizer, and playback controls. The original calculator demo remains as `demo.py`; a basic modern example is in `examples/basic.py`.

## Architecture

`src/tkanimator/core` contains lifecycle, scheduler, interpolation, easing and timeline primitives. `sequences` composes handles. `animations` contains concrete effects. Tk callbacks are shared per interpreter, use `time.monotonic()`, and stop their pending `after()` callback when idle. Pillow is optional; there are no required runtime dependencies.

See [docs/architecture.md](docs/architecture.md), [docs/animations.md](docs/animations.md), and [CHANGELOG.md](CHANGELOG.md).

## Development

Run `pytest`, `ruff check src tests`, `mypy src/tkanimator`, and `python -m build`. CI runs these checks on Python 3.10. GUI integration needs a display server; math, scheduler, and validation tests do not.

## License

MIT. Original attribution is retained in [LICENSE](LICENSE).
