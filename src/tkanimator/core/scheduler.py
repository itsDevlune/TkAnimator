"""Shared Tk after()-based scheduler; all callbacks run on Tk's owning thread."""
from __future__ import annotations

import time
import tkinter as tk
from collections.abc import Callable
from typing import Any


class Scheduler:
    def __init__(self, root: tk.Misc, frame_ms: int = 16) -> None:
        if frame_ms < 1:
            raise ValueError("frame_ms must be positive")
        self.root: Any = root
        self.frame_ms = frame_ms
        self._callbacks: set[Callable[[float], bool]] = set()
        self._after_id: str | None = None
        self._closed = False
        self._last = time.monotonic()

    def add(self, callback: Callable[[float], bool]) -> None:
        if self._closed:
            self._closed = False
            self._last = time.monotonic()
        self._callbacks.add(callback)
        if self._after_id is None:
            self._schedule()

    def remove(self, callback: Callable[[float], bool]) -> None:
        self._callbacks.discard(callback)
        if not self._callbacks:
            self._cancel_after()

    def close(self) -> None:
        self._closed = True
        self._callbacks.clear()
        self._cancel_after()

    def _cancel_after(self) -> None:
        if self._after_id is not None:
            try:
                self.root.after_cancel(self._after_id)
            except tk.TclError:
                pass
            self._after_id = None

    def _schedule(self) -> None:
        if not self._closed and self._callbacks and self._after_id is None:
            try:
                self._after_id = self.root.after(self.frame_ms, self._tick)
            except tk.TclError:
                self.close()

    def _tick(self) -> None:
        self._after_id = None
        now = time.monotonic()
        self._last = now
        for callback in tuple(self._callbacks):
            if callback not in self._callbacks:
                continue
            try:
                keep = callback(now)
            except tk.TclError:
                keep = False
                self._closed = True
            if not keep:
                self._callbacks.discard(callback)
        if self._closed:
            self._callbacks.clear()
            return
        self._schedule()


_SCHEDULERS: dict[int, Scheduler] = {}


def scheduler_for(widget: tk.Misc, frame_ms: int = 16) -> Scheduler:
    root = widget.winfo_toplevel()
    key = id(root)
    scheduler = _SCHEDULERS.get(key)
    if scheduler is None or scheduler._closed:
        scheduler = Scheduler(root, frame_ms)
        _SCHEDULERS[key] = scheduler
        try:
            def on_destroy(event: Any) -> None:
                if event.widget is root:
                    scheduler.close()
            root.bind("<Destroy>", on_destroy, add="+")
        except tk.TclError:
            scheduler.close()
        except AttributeError:
            # Non-Tk scheduler hosts are useful for deterministic core tests.
            pass
    elif scheduler.frame_ms != frame_ms:
        scheduler.frame_ms = min(scheduler.frame_ms, frame_ms)
    return scheduler
