# Contributing

Install development dependencies with `python -m pip install -e ".[dev]"`. Keep Tk operations on the event-loop thread, use monotonic time for elapsed durations, and do not call `update()` from animation callbacks. Add deterministic tests for math and lifecycle changes. GUI tests should skip cleanly when no display is available. Document any platform-specific effect limits.
