# TkAnimations

⚠️ **WARNING**: This library is still under development and may contain bugs.  
If you encounter any issues, please report them. Contributions are welcome!

**TkAnimations** is a collection of reusable animation effects for Tkinter widgets, designed to bring life and motion to your desktop apps all from a single, lightweight Python file.

## ✨ Features

- Fade in/out effects  
- Slide animations in all directions  
- Bouncing effects  
- Pulsing effects  
- Wiggle effects  
- Color transitions  
- Expand/shrink animations  
- Shake effects  
- Hover animations  

## 📦 Installation

Simply copy the `tk_animations.py` file into your project folder.
-or `pip install tk-animations`

## 🚀 Basic Usage

```python
from tkinter import *
from tk_animations import TkAnimations

root = Tk()
animations = TkAnimations()

# Apply to any widget
button = Button(root, text="Click me")
button.pack()

animations.animate_fade_in(button)
```

## 🧩 Complete Method Reference

### 🔹 Fade Effects

```python
animate_fade_in(
    widget: tk.Widget, 
    duration: int = 1000, 
    callback: Optional[Callable] = None
)

animate_fade_out(
    widget: tk.Widget, 
    duration: int = 1000, 
    callback: Optional[Callable] = None
)
```

### 🔹 Movement Animations

```python
animate_slide(
    widget: tk.Widget, 
    direction: str = 'right',  # 'left'/'right'/'up'/'down'
    distance: int = 100,
    duration: int = 1000,
    callback: Optional[Callable] = None
)

animate_bounce(
    widget: tk.Widget,
    height: int = 30,  # Max bounce height
    bounces: int = 3,
    duration: int = 1500,
    callback: Optional[Callable] = None
)

animate_hover(
    widget: tk.Widget,
    hover_lift: int = 10,  # Lift distance
    duration: int = 300,
    callback: Optional[Callable] = None
)
```

### 🔹 Transformation Effects

```python
animate_pulse(
    widget: tk.Widget,
    scale_factor: float = 1.2,  # Max scale
    pulses: int = 3,
    duration: int = 1000,
    callback: Optional[Callable] = None
)

animate_wiggle(
    widget: tk.Widget,
    angle: float = 10.0,  # Max rotation
    wiggles: int = 5,
    duration: int = 1000,
    callback: Optional[Callable] = None
)

animate_expand_shrink(
    widget: tk.Widget,
    expand_factor: float = 1.5,
    duration: int = 1000,
    shrink_back: bool = True,  # Return to original size
    callback: Optional[Callable] = None
)
```

### 🔹 Visual Effects

```python
animate_color_transition(
    widget: tk.Widget,
    start_color: str = '#FFFFFF',
    end_color: str = '#3498db',
    duration: int = 1000,
    property_name: str = 'bg',  # 'fg' for text color
    callback: Optional[Callable] = None
)

animate_shake(
    widget: tk.Widget,
    intensity: int = 10,  # Shake strength
    shakes: int = 5,
    duration: int = 800,
    callback: Optional[Callable] = None
)
```

## 🧪 Demo Application

The library includes a ready-to-run demo:

```python
if __name__ == "__main__":
    demo_app()  # Shows all animations
```

## 📝 Important Notes

### Geometry Managers:
- Works best with `place()` manager for precise control.

### Performance:
- Complex animations may affect performance on older hardware.
- Alpha effects may not work on all platforms.

### Duration:
- All durations are in milliseconds (1000ms = 1s).

### Callbacks:
- Optional callback functions execute after animation completes.

## 🪪 License

MIT License — Free to use, modify and distribute.
