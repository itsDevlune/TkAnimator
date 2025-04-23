import tkinter as tk
import math
import colorsys
import random
from typing import Union, Callable, Optional, Tuple, List, Any


class TkAnimations:
    """
    A collection of reusable animations for Tkinter widgets.
    
    This class provides various animation effects that can be applied to Tkinter widgets
    such as Canvas, Label, Frame, Button, etc. Each animation is implemented as a method
    that can be called with appropriate parameters.
    """
    
    @staticmethod
    def animate_fade_in(widget: tk.Widget, duration: int = 1000, callback: Optional[Callable] = None) -> None:
        """
        Fade in a widget from transparent to fully visible.
        
        Args:
            widget: The Tkinter widget to animate
            duration: Animation duration in milliseconds
            callback: Optional function to call when animation completes
        """
        
        if not hasattr(widget, '_original_alpha'):
            widget._original_alpha = 1.0
        
        
        widget.attributes('-alpha', 0.0) if hasattr(widget, 'attributes') else None
        
        steps = 20
        step_time = duration // steps
        step_alpha = widget._original_alpha / steps
        
        def step(count):
            if count <= steps:
                alpha = min(step_alpha * count, widget._original_alpha)
                if hasattr(widget, 'attributes'):
                    widget.attributes('-alpha', alpha)
                elif hasattr(widget, 'master') and hasattr(widget.master, 'attributes'):
                    
                    widget.master.attributes('-alpha', alpha)
                widget.after(step_time, lambda: step(count + 1))
            elif callback:
                callback()
        
        step(1)
    
    @staticmethod
    def animate_fade_out(widget: tk.Widget, duration: int = 1000, callback: Optional[Callable] = None) -> None:
        """
        Fade out a widget from fully visible to transparent.
        
        Args:
            widget: The Tkinter widget to animate
            duration: Animation duration in milliseconds
            callback: Optional function to call when animation completes
        """
        
        if not hasattr(widget, '_original_alpha'):
            if hasattr(widget, 'attributes'):
                try:
                    widget._original_alpha = widget.attributes('-alpha')
                except:
                    widget._original_alpha = 1.0
            else:
                widget._original_alpha = 1.0
        
        steps = 20
        step_time = duration // steps
        current_alpha = widget._original_alpha
        step_alpha = current_alpha / steps
        
        def step(count):
            if count <= steps:
                alpha = current_alpha - (step_alpha * count)
                alpha = max(0.0, alpha) 
                if hasattr(widget, 'attributes'):
                    widget.attributes('-alpha', alpha)
                elif hasattr(widget, 'master') and hasattr(widget.master, 'attributes'):
                    widget.master.attributes('-alpha', alpha)
                widget.after(step_time, lambda: step(count + 1))
            elif callback:
                callback()
        
        step(1)
    
    @staticmethod
    def animate_slide(widget: tk.Widget, direction: str = 'right', distance: int = 100, 
                      duration: int = 1000, callback: Optional[Callable] = None) -> None:
        """
        Slide a widget in the specified direction.
        
        Args:
            widget: The Tkinter widget to animate
            direction: Animation direction ('left', 'right', 'up', 'down')
            distance: The distance to slide in pixels
            duration: Animation duration in milliseconds
            callback: Optional function to call when animation completes
        """
        steps = 20
        step_time = duration // steps
        
       
        x, y = widget.winfo_x(), widget.winfo_y()
        
       
        if direction == 'left':
            dx, dy = -distance / steps, 0
        elif direction == 'right':
            dx, dy = distance / steps, 0
        elif direction == 'up':
            dx, dy = 0, -distance / steps
        elif direction == 'down':
            dx, dy = 0, distance / steps
        else:
            raise ValueError("Direction must be 'left', 'right', 'up', or 'down'")
        
        def step(count):
            if count <= steps:
                widget.place(x=x + dx * count, y=y + dy * count)
                widget.update()
                widget.after(step_time, lambda: step(count + 1))
            elif callback:
                callback()
        
        step(1)
    
    @staticmethod
    def animate_bounce(widget: tk.Widget, height: int = 30, bounces: int = 3, 
                       duration: int = 1500, callback: Optional[Callable] = None) -> None:
        """
        Create a bouncing effect for a widget.
        
        Args:
            widget: The Tkinter widget to animate
            height: Maximum bounce height in pixels
            bounces: Number of bounces to perform
            duration: Total animation duration in milliseconds
            callback: Optional function to call when animation completes
        """
        # Get the current position of the widget
        original_y = widget.winfo_y()
        
        # Calculate total steps and time per step
        steps = 40
        step_time = duration // steps
        
        def step(count):
            if count <= steps:
               
                progress = count / steps
                decay = 1 - (progress * 0.8)  # Decay factor
                cycle = progress * bounces * 2 * math.pi
                offset = math.sin(cycle) * height * decay
                
               
                widget.place(y=original_y - offset)
                widget.update()
                
                widget.after(step_time, lambda: step(count + 1))
            else:
                
                widget.place(y=original_y)
                if callback:
                    callback()
        
        step(1)
    
    @staticmethod
    def animate_pulse(widget: tk.Widget, scale_factor: float = 1.2, pulses: int = 3, 
                      duration: int = 1000, callback: Optional[Callable] = None) -> None:
        """
        Create a pulsing (growing and shrinking) effect for a widget.
        
        Args:
            widget: The Tkinter widget to animate
            scale_factor: How much to scale the widget at maximum pulse
            pulses: Number of pulse cycles to perform
            duration: Total animation duration in milliseconds
            callback: Optional function to call when animation completes
        """
       
        original_width = widget.winfo_width()
        original_height = widget.winfo_height()
        original_x = widget.winfo_x()
        original_y = widget.winfo_y()
        
        steps = 30
        step_time = duration // steps
        
        def step(count):
            if count <= steps:
                
                progress = count / steps
                cycle = progress * pulses * 2 * math.pi
                scale = 1 + (math.sin(cycle) * (scale_factor - 1) / 2)
                
                
                new_width = int(original_width * scale)
                new_height = int(original_height * scale)
                
                
                new_x = original_x - (new_width - original_width) // 2
                new_y = original_y - (new_height - original_height) // 2
                
               
                widget.place(x=new_x, y=new_y, width=new_width, height=new_height)
                widget.update()
                
                widget.after(step_time, lambda: step(count + 1))
            else:
                
                widget.place(x=original_x, y=original_y, width=original_width, height=original_height)
                if callback:
                    callback()
        
        step(1)
    
    @staticmethod
    def animate_wiggle(widget: tk.Widget, angle: float = 10.0, wiggles: int = 5, 
                       duration: int = 1000, callback: Optional[Callable] = None) -> None:
        """
        Create a wiggling (rotating back and forth) effect for a widget.
        
        Args:
            widget: The Tkinter widget to animate
            angle: Maximum rotation angle in degrees
            wiggles: Number of wiggle cycles to perform
            duration: Total animation duration in milliseconds
            callback: Optional function to call when animation completes
        """
        steps = 30
        step_time = duration // steps
        
        width = widget.winfo_width()
        height = widget.winfo_height()
        center_x = width / 2
        center_y = height / 2
        
        def step(count):
            if count <= steps:
                
                progress = count / steps
                cycle = progress * wiggles * 2 * math.pi
                current_angle = math.sin(cycle) * angle
                
                if hasattr(widget, 'rotate'):
                    widget.rotate(widget.find_all(), current_angle, center_x, center_y)
                else:
                   
                    if hasattr(widget, 'config') and 'text' in widget.config():
                        try:
                            widget.config(angle=current_angle)
                        except:
                            pass
                
                widget.update()
                widget.after(step_time, lambda: step(count + 1))
            else:
                if hasattr(widget, 'rotate'):
                    widget.rotate(widget.find_all(), 0, center_x, center_y)
                elif hasattr(widget, 'config') and 'text' in widget.config():
                    try:
                        widget.config(angle=0)
                    except:
                        pass
                
                if callback:
                    callback()
        
        step(1)
    
    @staticmethod
    def animate_color_transition(widget: tk.Widget, start_color: str = '#FFFFFF', 
                                end_color: str = '#3498db', duration: int = 1000,
                                property_name: str = 'bg', callback: Optional[Callable] = None) -> None:
        """
        Transition the color of a widget property (e.g., background, foreground).
        
        Args:
            widget: The Tkinter widget to animate
            start_color: Starting color in hex format
            end_color: Ending color in hex format
            duration: Animation duration in milliseconds
            property_name: Widget property to animate ('bg', 'fg', etc.)
            callback: Optional function to call when animation completes
        """
        steps = 30
        step_time = duration // steps
        
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        start_rgb = hex_to_rgb(start_color)
        end_rgb = hex_to_rgb(end_color)
        
        def step(count):
            if count <= steps:
                progress = count / steps
                current_rgb = tuple(int(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * progress) for i in range(3))
                
                current_color = f'#{current_rgb[0]:02x}{current_rgb[1]:02x}{current_rgb[2]:02x}'
                
                try:
                    if property_name == 'bg':
                        widget.config(bg=current_color)
                    elif property_name == 'fg':
                        widget.config(fg=current_color)
                    else:
                        widget.config(**{property_name: current_color})
                except tk.TclError:
                    pass
                
                widget.update()
                widget.after(step_time, lambda: step(count + 1))
            elif callback:
                callback()
        
        step(1)
    
    @staticmethod
    def animate_expand_shrink(widget: tk.Widget, expand_factor: float = 1.5, 
                             duration: int = 1000, shrink_back: bool = True,
                             callback: Optional[Callable] = None) -> None:
        """
        Expand a widget and optionally shrink it back to its original size.
        
        Args:
            widget: The Tkinter widget to animate
            expand_factor: How much to expand the widget (multiplier)
            duration: Animation duration in milliseconds
            shrink_back: Whether to shrink back to original size after expanding
            callback: Optional function to call when animation completes
        """
        original_width = widget.winfo_width()
        original_height = widget.winfo_height()
        original_x = widget.winfo_x()
        original_y = widget.winfo_y()
        
        steps = 20
        step_time = duration // steps
        
        if shrink_back:
            total_steps = steps * 2
            mid_point = steps
        else:
            total_steps = steps
            mid_point = total_steps
        
        def step(count):
            if count <= total_steps:
                if count <= mid_point:
                    progress = count / mid_point
                    scale = 1 + (expand_factor - 1) * progress
                else:
                    progress = (count - mid_point) / (total_steps - mid_point)
                    scale = expand_factor - (expand_factor - 1) * progress
                
                new_width = int(original_width * scale)
                new_height = int(original_height * scale)
                
                new_x = original_x - (new_width - original_width) // 2
                new_y = original_y - (new_height - original_height) // 2
                
                widget.place(x=new_x, y=new_y, width=new_width, height=new_height)
                widget.update()
                
                widget.after(step_time, lambda: step(count + 1))
            else:
                widget.place(x=original_x, y=original_y, width=original_width, height=original_height)
                if callback:
                    callback()
        
        step(1)
    
    @staticmethod
    def animate_shake(widget: tk.Widget, intensity: int = 10, shakes: int = 5, 
                     duration: int = 800, callback: Optional[Callable] = None) -> None:
        """
        Create a shaking effect for a widget (horizontal movement).
        
        Args:
            widget: The Tkinter widget to animate
            intensity: Maximum shake displacement in pixels
            shakes: Number of shake cycles to perform
            duration: Total animation duration in milliseconds
            callback: Optional function to call when animation completes
        """
        original_x = widget.winfo_x()
        original_y = widget.winfo_y()
        
        steps = 30
        step_time = duration // steps
        
        def step(count):
            if count <= steps:
                progress = count / steps  # 0 to 1
                decay = 1 - (progress * 0.7)  
                cycle = progress * shakes * 2 * math.pi
                offset = math.sin(cycle) * intensity * decay
                
                widget.place(x=original_x + offset, y=original_y)
                widget.update()
                
                widget.after(step_time, lambda: step(count + 1))
            else:
                widget.place(x=original_x, y=original_y)
                if callback:
                    callback()
        
        step(1)
    
    @staticmethod
    def animate_hover(widget: tk.Widget, hover_lift: int = 10, 
                     duration: int = 300, callback: Optional[Callable] = None) -> None:
        """
        Create a hovering effect for a widget (vertical movement).
        
        Args:
            widget: The Tkinter widget to animate
            hover_lift: How many pixels to lift the widget
            duration: Animation duration in milliseconds
            callback: Optional function to call when animation completes
        """
        original_x = widget.winfo_x()
        original_y = widget.winfo_y()
        
        steps = 15
        step_time = duration // steps
        
        def step_up(count):
            if count <= steps:
                progress = count / steps
                ease = 1 - (1 - progress) ** 3
                offset = hover_lift * ease
                
                widget.place(x=original_x, y=original_y - offset)
                widget.update()
                
                widget.after(step_time, lambda: step_up(count + 1))
            else:
                widget.after(duration, step_down)
        
        def step_down(count=0):
            if count <= steps:
                progress = count / steps
                ease = progress ** 3
                offset = hover_lift * (1 - ease)
                
                widget.place(x=original_x, y=original_y - offset)
                widget.update()
                
                widget.after(step_time, lambda: step_down(count + 1))
            else:
                widget.place(x=original_x, y=original_y)
                if callback:
                    callback()
        
        step_up(1)


def demo_app():
    """
    Demo application to showcase different animations.
    This function creates a Tkinter window and demonstrates various animations.
    """
    root = tk.Tk()
    root.title("TkAnimations Demo")
    root.geometry("800x600")
    
    animations = TkAnimations()
    
    control_frame = tk.Frame(root, padx=10, pady=10)
    control_frame.pack(side=tk.TOP, fill=tk.X)
    
    button_frame = tk.Frame(control_frame)
    button_frame.pack(side=tk.TOP, fill=tk.X)
    
    canvas = tk.Canvas(root, bg='white', width=750, height=450)
    canvas.pack(pady=20)
    
    demo_frame = tk.Frame(canvas, bg='#3498db', width=100, height=100)
    demo_frame.place(x=325, y=175)  # Position within canvas
    
    demo_label = tk.Label(demo_frame, text="Demo", fg="white", bg="#3498db", font=("Arial", 14))
    demo_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    def reset_demo():
        demo_frame.config(bg='#3498db', width=100, height=100)
        demo_label.config(text="Demo", fg="white", bg="#3498db")
        demo_frame.place(x=325, y=175)
        status_label.config(text="Demo ready")
    
    status_label = tk.Label(control_frame, text="Select an animation to demo", font=("Arial", 10))
    status_label.pack(side=tk.BOTTOM, pady=5)
    
    animations_list = [
        ("Fade In", lambda: animations.animate_fade_in(demo_frame, callback=lambda: status_label.config(text="Fade In completed"))),
        ("Fade Out", lambda: animations.animate_fade_out(demo_frame, callback=lambda: status_label.config(text="Fade Out completed"))),
        ("Slide Right", lambda: animations.animate_slide(demo_frame, 'right', 150, callback=lambda: status_label.config(text="Slide Right completed"))),
        ("Bounce", lambda: animations.animate_bounce(demo_frame, callback=lambda: status_label.config(text="Bounce completed"))),
        ("Pulse", lambda: animations.animate_pulse(demo_frame, callback=lambda: status_label.config(text="Pulse completed"))),
        ("Wiggle", lambda: animations.animate_wiggle(demo_frame, callback=lambda: status_label.config(text="Wiggle completed"))),
        ("Color Transition", lambda: animations.animate_color_transition(demo_frame, '#3498db', '#e74c3c', property_name='bg', callback=lambda: status_label.config(text="Color Transition completed"))),
        ("Expand/Shrink", lambda: animations.animate_expand_shrink(demo_frame, callback=lambda: status_label.config(text="Expand/Shrink completed"))),
        ("Shake", lambda: animations.animate_shake(demo_frame, callback=lambda: status_label.config(text="Shake completed"))),
        ("Hover", lambda: animations.animate_hover(demo_frame, callback=lambda: status_label.config(text="Hover completed"))),
        ("Reset", reset_demo)
    ]
    
    for i, (label, command) in enumerate(animations_list):
        if i % 5 == 0:
            row_frame = tk.Frame(button_frame)
            row_frame.pack(side=tk.TOP, fill=tk.X, pady=2)
            
        btn = tk.Button(row_frame, text=label, command=command, width=12)
        btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    instructions = tk.Label(root, text="Click a button to see the animation in action", font=("Arial", 12))
    instructions.pack(side=tk.BOTTOM, pady=10)
    
    root.mainloop()


if __name__ == "__main__":
    demo_app()
