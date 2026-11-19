import tkinter as tk

import pytest

from tkanimator import Animation
from tkanimator.core.scheduler import Scheduler


class FakeRoot:
    def __init__(self):
        self.pending = {}
        self.next_id = 0

    def after(self, delay, callback):
        self.next_id += 1
        self.pending[str(self.next_id)] = callback
        return str(self.next_id)

    def after_cancel(self, ident):
        self.pending.pop(ident, None)

    def bind(self, *_args, **_kwargs):
        return "binding"


class FakeWidget:
    def __init__(self, root):
        self.root = root

    def winfo_toplevel(self):
        return self.root

    def after(self, delay, callback):
        return self.root.after(delay, callback)


def test_animation_progress_pause_resume_cancel(monkeypatch):
    root = FakeRoot()
    widget = FakeWidget(root)
    scheduler = Scheduler(root, frame_ms=16)
    monkeypatch.setattr("tkanimator.core.animation.scheduler_for", lambda *_: scheduler)
    values = []
    clock = [10.0]
    monkeypatch.setattr("tkanimator.core.animation.time.monotonic", lambda: clock[0])
    animation = Animation(widget, values.append, duration=1000)
    animation.start()
    clock[0] = 10.5
    animation._tick(clock[0])
    assert values[-1] == pytest.approx(.5)
    animation.pause()
    clock[0] = 12.0
    animation.resume()
    assert animation._started_at == pytest.approx(11.5)
    animation.cancel()
    assert animation.state == "cancelled"
    assert animation._tick not in scheduler._callbacks


def test_delay_speed_callbacks_repeat(monkeypatch):
    root = FakeRoot()
    widget = FakeWidget(root)
    scheduler = Scheduler(root)
    monkeypatch.setattr("tkanimator.core.animation.scheduler_for", lambda *_: scheduler)
    clock = [0.0]
    monkeypatch.setattr("tkanimator.core.animation.time.monotonic", lambda: clock[0])
    events = []
    values = []
    animation = Animation(widget, values.append, duration=100, delay=50, repeat=1,
                          on_start=lambda: events.append("start"), on_complete=lambda: events.append("done"))
    monkeypatch.setattr("tkanimator.core.animation.time.monotonic", lambda: 0.0)
    animation.speed = 2
    animation.start()
    assert animation._tick(.02)
    assert not events
    assert animation._tick(.05)
    assert events == ["start"]
    assert animation._tick(.10)
    assert not animation._tick(.151)
    assert events == ["start", "done"]
    with pytest.raises(ValueError):
        animation.speed = 0


def test_zero_duration_and_repeat_yoyo():
    root = FakeRoot()
    scheduler = Scheduler(root)
    widget = FakeWidget(root)
    animation = Animation(widget, lambda _: None, duration=0)
    animation.scheduler = scheduler
    animation.start()
    assert not animation._tick(animation._started_at)
    assert animation.state == "completed"


def test_start_after_completion_and_empty_timeline(monkeypatch):
    from tkanimator import Timeline

    root = FakeRoot()
    scheduler = Scheduler(root)
    widget = FakeWidget(root)
    monkeypatch.setattr("tkanimator.core.animation.scheduler_for", lambda *_: scheduler)
    monkeypatch.setattr("tkanimator.core.timeline.scheduler_for", lambda *_: scheduler)
    clock = [1.0]
    monkeypatch.setattr("tkanimator.core.animation.time.monotonic", lambda: clock[0])
    values = []
    animation = Animation(widget, values.append, duration=0)
    animation.start()
    animation._tick(1.0)
    assert animation.state == "completed"
    animation.start()
    animation._tick(1.0)
    assert animation.state == "completed"
    timeline = Timeline(widget).start()
    assert timeline.state == "completed"


def test_cancelled_sequence_does_not_advance(monkeypatch):
    from tkanimator import Sequence

    root = FakeRoot()
    scheduler = Scheduler(root)
    widget = FakeWidget(root)
    monkeypatch.setattr("tkanimator.core.animation.scheduler_for", lambda *_: scheduler)
    monkeypatch.setattr("tkanimator.sequences.sequence.scheduler_for", lambda *_: scheduler)
    first = Animation(widget, lambda _: None)
    second = Animation(widget, lambda _: None)
    sequence = Sequence([first, second]).start()
    sequence.cancel()
    assert sequence._tick(0) is False
    assert second.state == "idle"


def test_sequence_and_parallel_completion(monkeypatch):
    from tkanimator import Parallel, Sequence

    root = FakeRoot()
    widget = FakeWidget(root)
    scheduler = Scheduler(root)
    monkeypatch.setattr("tkanimator.core.animation.scheduler_for", lambda *_: scheduler)
    monkeypatch.setattr("tkanimator.sequences.sequence.scheduler_for", lambda *_: scheduler)
    clock = [0.0]
    monkeypatch.setattr("tkanimator.core.animation.time.monotonic", lambda: clock[0])
    first_values, second_values = [], []
    first = Animation(widget, first_values.append, duration=100)
    second = Animation(widget, second_values.append, duration=100)
    sequence = Sequence([first, second]).start()
    first._tick(.1)
    sequence._tick(.1)
    assert second.state == "running"
    second._tick(.2)
    assert sequence._tick(.2) is False
    assert sequence.state == "completed"
    a = Animation(widget, lambda _: None, duration=10)
    b = Animation(widget, lambda _: None, duration=20)
    parallel = Parallel([a, b]).start()
    a._tick(parallel._started + .02)
    b._tick(parallel._started + .03)
    assert parallel._tick(parallel._started + .03) is False
    assert parallel.state == "completed"


def test_parallel_pause_preserves_children_already_paused(monkeypatch):
    from tkanimator import Parallel

    root = FakeRoot()
    widget = FakeWidget(root)
    scheduler = Scheduler(root)
    monkeypatch.setattr("tkanimator.core.animation.scheduler_for", lambda *_: scheduler)
    monkeypatch.setattr("tkanimator.sequences.sequence.scheduler_for", lambda *_: scheduler)
    first = Animation(widget, lambda _: None)
    second = Animation(widget, lambda _: None)
    parallel = Parallel([first, second]).start()
    second.pause()
    parallel.pause()
    parallel.resume()
    assert first.state == "running"
    assert second.state == "paused"


def test_repeat_yoyo_returns_to_start(monkeypatch):
    root = FakeRoot()
    widget = FakeWidget(root)
    scheduler = Scheduler(root)
    monkeypatch.setattr("tkanimator.core.animation.scheduler_for", lambda *_: scheduler)
    clock = [0.0]
    monkeypatch.setattr("tkanimator.core.animation.time.monotonic", lambda: clock[0])
    values = []
    animation = Animation(widget, values.append, duration=100, repeat=1, yoyo=True)
    animation.start()
    animation._tick(0)
    clock[0] = .1
    assert animation._tick(.1)
    clock[0] = .2
    assert not animation._tick(.2)
    assert animation.state == "completed"
    assert values[-1] == pytest.approx(0)


def test_conflict_policy_replaces_and_can_ignore(monkeypatch):
    root = FakeRoot()
    widget = FakeWidget(root)
    scheduler = Scheduler(root)
    monkeypatch.setattr("tkanimator.core.animation.scheduler_for", lambda *_: scheduler)
    first = Animation(widget, lambda _: None, conflict_key="x")
    second = Animation(widget, lambda _: None, conflict_key="x")
    first.start()
    second.start()
    assert first.state == "cancelled"
    assert second.state == "running"
    ignored = Animation(widget, lambda _: None, conflict_key="x", conflict="ignore")
    ignored.start()
    assert ignored.state == "cancelled"
    with pytest.raises(ValueError):
        Animation(widget, lambda _: None, conflict="unknown")


def test_gui_move_if_display_available():
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("no graphical display available")
    try:
        from tkanimator import Animator
        widget = tk.Label(root)
        widget.place(x=0, y=0, width=20, height=20)
        root.update_idletasks()
        animation = Animator(widget).move(x=10, y=5)
        animation.start()
        animation._tick(animation._started_at)
        assert int(float(widget.place_info()["x"])) == 0
        animation._tick(animation._started_at + 2)
        assert int(float(widget.place_info()["x"])) == 10
    finally:
        root.destroy()
