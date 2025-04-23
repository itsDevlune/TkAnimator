# TkAnimations

⚠️ **WARNING**: This library is still under development and may contain bugs.  
If you encounter any issues, please report them. Contributions are welcome!

**TkAnimations** is a collection of reusable animation effects for Tkinter widgets, designed to bring life and motion to your desktop apps — all from a single, lightweight Python file.

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

- Copy `tk_animations.py` into your project folder  
- Or (if published): `pip install tk-animations`

## 🚀 Usage

### Basic Setup

```python
from tkinter import *
from tk_animations import TkAnimations

root = Tk()
animations = TkAnimations()
```

### Applying Animations

```python
button = Button(root, text="Click me")
button.pack()

animations.animate_fade_in(button)

label = Label(root, text="Hello")
label.pack()

animations.animate_bounce(label)
```

## 🧩 Available Methods

### 🔹 Basic Animations

- `animate_fade_in(widget, duration=1000, callback=None)`  
    Fades in a widget from transparent.

- `animate_fade_out(widget, duration=1000, callback=None)`  
    Fades out a widget to transparent.

### 🔹 Movement Animations

- `animate_slide(widget, direction='right', distance=100, duration=1000)`  
    Slides a widget in a given direction (`left`, `right`, `up`, `down`).

- `animate_bounce(widget, height=30, bounces=3, duration=1500)`  
    Bouncing motion effect.

- `animate_hover(widget, hover_lift=10, duration=300)`  
    Hover "lift" animation.

### 🔹 Transformation Animations

- `animate_pulse(widget, scale_factor=1.2, pulses=3, duration=1000)`  
    Scale up/down to simulate pulsing.

- `animate_wiggle(widget, angle=10.0, wiggles=5, duration=1000)`  
    Wiggle with simulated rotation.

- `animate_expand_shrink(widget, expand_factor=1.5, duration=1000)`  
    Expand and shrink widget.

### 🔹 Visual Effects

- `animate_color_transition(widget, start_color, end_color, property_name='bg', duration=1000)`  
    Smoothly transitions color (background or foreground).

- `animate_shake(widget, intensity=10, shakes=5, duration=800)`  
    Shaking effect (left-right).

## 🧪 Example

```python
from tkinter import *
from tk_animations import TkAnimations

def demo():
        root = Tk()
        btn = Button(root, text="Animate Me!")
        btn.pack(pady=20)
        
        anim = TkAnimations()
        anim.animate_pulse(btn)
        
        root.mainloop()

demo()
```

## 📝 Notes

- Works best with widgets using the `place()` geometry manager.  
- `duration` values are in milliseconds (1000ms = 1s).  
- Optional `callback` functions can run after the animation completes.  

## 🪪 License

MIT License — Free to use, modify, and distribute.
