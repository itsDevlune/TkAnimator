import pytest

from tkanimator import Animation, Timeline
from tkanimator.sequences.sequence import stagger


class Root:
    def after(self, *_):
        return "timer"

    def after_cancel(self, *_):
        pass

    def bind(self, *_args, **_kwargs):
        return "binding"


class Widget:
    def __init__(self):
        self.root = Root()

    def winfo_toplevel(self):
        return self.root

    def after(self, *args):
        return self.root.after(*args)


def test_stagger_offsets_and_validation(monkeypatch):
    widget = Widget()
    monkeypatch.setattr("tkanimator.core.animation.scheduler_for", lambda *_: type("S", (), {"add": lambda *a: None, "remove": lambda *a: None})())
    animations = [Animation(widget, lambda _: None) for _ in range(3)]
    seq = stagger(animations, 100)
    assert [a.delay for a in seq.animations] == pytest.approx([0, .1, .2])
    with pytest.raises(ValueError):
        stagger(animations, -1)


def test_timeline_validation_and_completion(monkeypatch):
    widget = Widget()
    scheduler = type("S", (), {"add": lambda *a: None, "remove": lambda *a: None})()
    monkeypatch.setattr("tkanimator.core.timeline.scheduler_for", lambda *_: scheduler)
    monkeypatch.setattr("tkanimator.core.animation.scheduler_for", lambda *_: scheduler)
    timeline = Timeline(widget)
    with pytest.raises(ValueError):
        timeline.add(Animation(widget, lambda _: None), -1)
    assert timeline.start().state == "completed"


def test_timeline_starts_at_offset(monkeypatch):
    widget = Widget()
    scheduler = type("S", (), {"add": lambda *a: None, "remove": lambda *a: None})()
    monkeypatch.setattr("tkanimator.core.timeline.scheduler_for", lambda *_: scheduler)
    monkeypatch.setattr("tkanimator.core.animation.scheduler_for", lambda *_: scheduler)
    clock = [2.0]
    monkeypatch.setattr("tkanimator.core.timeline.time.monotonic", lambda: clock[0])
    monkeypatch.setattr("tkanimator.core.animation.time.monotonic", lambda: clock[0])
    animation = Animation(widget, lambda _: None)
    timeline = Timeline(widget).add(animation, 100).start()
    timeline._tick(2.05)
    assert animation.state == "idle"
    timeline._tick(2.1)
    assert animation.state == "running"
    timeline.cancel()
