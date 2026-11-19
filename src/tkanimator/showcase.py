"""Interactive TkAnimator learning and smoke-test application."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from . import Animator, Easing, Parallel, Sequence
from .animations import bounce, color_transition, follow_path, pulse, shake, slide
from .core.animation import Animation


class Showcase:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("TkAnimator Showcase")
        root.geometry("940x680")
        root.minsize(760, 560)
        root.configure(bg="#10151d")
        self.active: Animation | Sequence | Parallel | None = None
        self._build()
        root.after(100, self._draw_curve)

    def _build(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#10151d")
        style.configure("TLabel", background="#10151d", foreground="#e6edf3")
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("TButton", padding=6)
        outer = ttk.Frame(self.root, padding=18)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="TkAnimator", style="Title.TLabel").pack(anchor="w")
        ttk.Label(outer, text="Interactive previews use the same public animation handles.").pack(anchor="w", pady=(2, 12))

        controls = ttk.Frame(outer)
        controls.pack(fill="x", pady=(0, 12))
        ttk.Label(controls, text="Duration (ms)").pack(side="left")
        self.duration = tk.IntVar(value=800)
        ttk.Scale(controls, from_=100, to=3000, variable=self.duration, orient="horizontal", length=180).pack(side="left", padx=8)
        self.duration_label = ttk.Label(controls, text="800")
        self.duration_label.pack(side="left", padx=(0, 14))
        self.duration.trace_add("write", lambda *_: self.duration_label.configure(text=str(self.duration.get())))
        ttk.Label(controls, text="Easing").pack(side="left")
        names = ["LINEAR", "EASE_IN_OUT_CUBIC", "EASE_OUT_BOUNCE", "EASE_OUT_ELASTIC", "EASE_OUT_SPRING"]
        self.easing = tk.StringVar(value=names[1])
        ttk.Combobox(controls, state="readonly", values=names, textvariable=self.easing, width=23).pack(side="left", padx=8)

        body = ttk.Frame(outer)
        body.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(body, bg="#182230", highlightthickness=0, height=400, scrollregion=(0, 0, 1200, 900))
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_text(24, 22, anchor="nw", fill="#9fb0c3", text="Canvas and widget preview area")
        self.item = self.canvas.create_oval(100, 90, 160, 150, fill="#4cc9f0", outline="")
        self.widget = tk.Label(self.canvas, text="place() widget", bg="#4361ee", fg="white", padx=12, pady=8)
        self.widget.place(x=100, y=220)
        self.widget2 = tk.Label(self.canvas, text="parallel", bg="#2a9d8f", fg="white", padx=10, pady=6)
        self.widget2.place(x=100, y=290)
        side = ttk.Frame(body, padding=(14, 0, 0, 0))
        side.pack(side="right", fill="y")
        for title, fn in [
            ("Move widget", self._move_widget), ("Slide", self._slide), ("Bounce", self._bounce),
            ("Pulse", self._pulse), ("Shake", self._shake), ("Color", self._color),
            ("Path motion", self._path), ("Canvas item", self._canvas_move),
            ("Parallel group", self._parallel), ("Sequence", self._sequence),
        ]:
            ttk.Button(side, text=title, command=fn).pack(fill="x", pady=3)
        ttk.Separator(side).pack(fill="x", pady=9)
        for label, fn in [("Pause", self._pause), ("Resume", self._resume), ("Cancel", self._cancel), ("Replay", self._replay)]:
            ttk.Button(side, text=label, command=fn).pack(fill="x", pady=3)
        ttk.Label(side, text="Easing curve").pack(anchor="w", pady=(12, 3))
        self.curve = tk.Canvas(side, width=230, height=130, bg="#182230", highlightthickness=0)
        self.curve.pack()
        self.status = tk.StringVar(value="Ready")
        ttk.Label(outer, textvariable=self.status).pack(anchor="w", pady=(9, 0))

    def _opts(self):
        return {"duration": self.duration.get(), "easing": getattr(Easing, self.easing.get())}

    def _launch(self, handle) -> None:
        if self.active and self.active.state in ("running", "paused"):
            self.active.cancel()
        self.active = handle
        if isinstance(handle, Animation):
            handle.on_complete = lambda: self.status.set("Completed")
            handle.on_cancel = lambda: self.status.set("Cancelled")
        else:
            handle.on_complete = lambda: self.status.set("Completed")
        self.status.set("Running")
        handle.start()

    def _move_widget(self):
        x = float(self.widget.place_info().get("x", 0))
        target = (500, 260) if x < 300 else (100, 220)
        self._launch(Animator(self.widget).move(x=target[0], y=target[1], **self._opts()))

    def _slide(self): self._launch(slide(self.widget, "right", 160, **self._opts()))
    def _bounce(self): self._launch(bounce(self.widget, duration=self.duration.get(), easing=self._opts()["easing"]))
    def _pulse(self): self._launch(pulse(self.widget, duration=self.duration.get(), easing=self._opts()["easing"]))
    def _shake(self): self._launch(shake(self.widget, duration=self.duration.get(), easing=self._opts()["easing"]))
    def _color(self):
        start = self.widget.cget("bg")
        self._launch(color_transition(self.widget, start, "#f72585", **self._opts()))
    def _path(self): self._launch(follow_path(self.widget, [(100, 220), (250, 120), (450, 220), (250, 330)], **self._opts()))
    def _canvas_move(self):
        cx, cy = self.canvas.coords(self.item)[0:2]
        dest = (cx + 150, cy + 80) if cx < 300 else (100, 90)
        from .adapters.canvas import move_item
        self._launch(move_item(self.canvas, self.item, *dest, **self._opts()))
    def _parallel(self):
        first = slide(self.widget, "right", 120, **self._opts())
        second = color_transition(self.widget2, self.widget2.cget("bg"), "#f72585", **self._opts())
        group = Parallel([first, second])
        self._launch(group)
    def _sequence(self):
        group = Sequence([bounce(self.widget, duration=self.duration.get()), shake(self.widget, duration=self.duration.get())])
        self._launch(group)
    def _pause(self):
        if self.active: self.active.pause(); self.status.set("Paused")
    def _resume(self):
        if self.active: self.active.resume(); self.status.set("Running")
    def _cancel(self):
        if self.active: self.active.cancel()
    def _replay(self):
        if self.active: self.active.restart(); self.status.set("Running")

    def _draw_curve(self) -> None:
        self.curve.delete("all")
        self.curve.create_line(10, 110, 220, 110, fill="#496176")
        self.curve.create_line(10, 10, 10, 110, fill="#496176")
        fn = getattr(Easing, self.easing.get())
        points: list[float] = []
        for index in range(101):
            t = index / 100
            value = fn(t)
            points.extend((10 + 210 * t, 110 - max(-.2, min(1.2, value)) * 90))
        self.curve.create_line(*points, fill="#4cc9f0", width=2, smooth=True)
        self.root.after(100, self._draw_curve)


def main() -> None:
    root = tk.Tk()
    Showcase(root)
    root.mainloop()


if __name__ == "__main__":
    main()
