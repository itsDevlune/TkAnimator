"""Compatibility facade shipped alongside the modern ``tkanimator`` package."""
from __future__ import annotations

from tkanimator import Animation, Animator, Easing, Parallel, Sequence, Timeline
from tkanimator.animations import bounce, color_transition, expand_shrink, fade_toplevel, pulse, shake, slide


class TkAnimations:
    """Compatibility methods from TkAnimator 1.x."""

    @staticmethod
    def animate_fade_in(widget, duration=1000, callback=None):
        return fade_toplevel(widget, True, duration, on_complete=callback)

    @staticmethod
    def animate_fade_out(widget, duration=1000, callback=None):
        return fade_toplevel(widget, False, duration, on_complete=callback)

    @staticmethod
    def animate_slide(widget, direction="right", distance=100, duration=1000, callback=None):
        return slide(widget, direction, distance, duration=duration, on_complete=callback)

    @staticmethod
    def animate_bounce(widget, height=30, bounces=3, duration=1500, callback=None):
        return bounce(widget, height, bounces, duration, on_complete=callback)

    @staticmethod
    def animate_pulse(widget, scale_factor=1.2, pulses=3, duration=1000, callback=None):
        return pulse(widget, scale_factor, pulses, duration, on_complete=callback)

    @staticmethod
    def animate_wiggle(widget, angle=10.0, wiggles=5, duration=1000, callback=None):
        raise ValueError("Tk cannot rotate ordinary widgets; use tkanimator.rotate_image on a Canvas image")

    @staticmethod
    def animate_color_transition(widget, start_color="#FFFFFF", end_color="#3498db", duration=1000,
                                 property_name="bg", callback=None):
        return color_transition(widget, start_color, end_color, property_name,
                                duration=duration, on_complete=callback)

    @staticmethod
    def animate_expand_shrink(widget, expand_factor=1.5, duration=1000, shrink_back=True, callback=None):
        return expand_shrink(widget, expand_factor, duration, shrink_back, on_complete=callback)

    @staticmethod
    def animate_shake(widget, intensity=10, shakes=5, duration=800, callback=None):
        return shake(widget, intensity, shakes, duration, on_complete=callback)

    @staticmethod
    def animate_hover(widget, hover_lift=10, duration=300, callback=None):
        if widget.winfo_manager() != "place":
            raise ValueError("hover movement requires place() geometry management")
        info = widget.place_info()
        x, y = float(info.get("x", widget.winfo_x())), float(info.get("y", widget.winfo_y()))
        def update(progress):
            offset = hover_lift * (progress * 2 if progress < .5 else 2 - progress * 2)
            widget.place_configure(x=round(x), y=round(y - offset))
        def complete():
            widget.place_configure(x=round(x), y=round(y))
            if callback:
                callback()
        return Animation(widget, update, duration=duration, on_complete=complete,
                         conflict_key=("geometry", "y"))


__all__ = ["Animation", "Animator", "Easing", "Parallel", "Sequence", "Timeline", "TkAnimations"]
