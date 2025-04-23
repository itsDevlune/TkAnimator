import tkinter as tk
from tkinter import font as tkfont
import random
import time

# Import the TkAnimations class from your code
from tk_animations import TkAnimations

class AnimatedCalculator:
    """
    A not calculator application with animations using the TkAnimations library.
    Fixed to prevent layout disruption after animations.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Animated Example")
        self.root.geometry("380x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")
        
        # Initialize the TkAnimations class
        self.animations = TkAnimations()
        
        # Calculator state
        self.current_input = "0"
        self.stored_value = None
        self.operation = None
        self.result_shown = False
        
        # Create UI elements
        self.create_display()
        self.create_buttons()
        
        # Store original button positions and sizes for restoration after animations
        self.store_original_button_states()
        
        # Add a periodic layout check to fix any disruptions
        self.root.after(100, self.check_layout)
    
    def store_original_button_states(self):
        """Store original button positions and dimensions for restoration."""
        self.original_button_states = {}
        for text, button in self.button_widgets.items():
            # Wait for button to be properly placed
            self.root.update()
            self.original_button_states[text] = {
                'x': button.winfo_x(),
                'y': button.winfo_y(),
                'width': button.winfo_width(),
                'height': button.winfo_height()
            }
    
    def check_layout(self):
        """Periodically check if layout is disrupted and fix it."""
        for text, button in self.button_widgets.items():
            if text in self.original_button_states:
                original = self.original_button_states[text]
                current_x = button.winfo_x()
                current_y = button.winfo_y()
                current_width = button.winfo_width()
                current_height = button.winfo_height()
                
                # If position or size has changed significantly, restore it
                if (abs(current_x - original['x']) > 5 or 
                    abs(current_y - original['y']) > 5 or
                    abs(current_width - original['width']) > 5 or
                    abs(current_height - original['height']) > 5):
                    
                    button.place_forget()  # Remove from current layout manager
                    button.place(
                        x=original['x'],
                        y=original['y'],
                        width=original['width'],
                        height=original['height']
                    )
        
        # Schedule the next check
        self.root.after(100, self.check_layout)
    
    def create_display(self):
        """Create the calculator display area."""
        display_frame = tk.Frame(self.root, bg="#2c3e50", height=150)
        display_frame.pack(fill=tk.X, padx=20, pady=(30, 20))
        
        # Display area for calculations
        self.display = tk.Label(
            display_frame,
            text="0",
            font=tkfont.Font(family="Arial", size=40, weight="bold"),
            bg="#34495e",
            fg="white",
            anchor="e",
            padx=15,
            pady=20
        )
        self.display.pack(fill=tk.BOTH, expand=True)
        
        # Secondary display for showing operations
        self.operation_display = tk.Label(
            display_frame,
            text="",
            font=tkfont.Font(family="Arial", size=14),
            bg="#34495e",
            fg="#bdc3c7",
            anchor="e",
            padx=15,
            pady=5
        )
        self.operation_display.pack(fill=tk.X)
    
    def create_buttons(self):
        """Create calculator buttons with fixed absolute positioning."""
        self.buttons_frame = tk.Frame(self.root, bg="#2c3e50")
        self.buttons_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Define button positions and sizes
        button_specs = [
            # Text, x, y, width, height, bg_color
            ("C", 0, 0, 80, 80, "#e74c3c"),
            ("±", 85, 0, 80, 80, "#3498db"),
            ("%", 170, 0, 80, 80, "#3498db"),
            ("÷", 255, 0, 80, 80, "#f39c12"),
            
            ("7", 0, 85, 80, 80, "#7f8c8d"),
            ("8", 85, 85, 80, 80, "#7f8c8d"),
            ("9", 170, 85, 80, 80, "#7f8c8d"),
            ("×", 255, 85, 80, 80, "#f39c12"),
            
            ("4", 0, 170, 80, 80, "#7f8c8d"),
            ("5", 85, 170, 80, 80, "#7f8c8d"),
            ("6", 170, 170, 80, 80, "#7f8c8d"),
            ("-", 255, 170, 80, 80, "#f39c12"),
            
            ("1", 0, 255, 80, 80, "#7f8c8d"),
            ("2", 85, 255, 80, 80, "#7f8c8d"),
            ("3", 170, 255, 80, 80, "#7f8c8d"),
            ("+", 255, 255, 80, 80, "#f39c12"),
            
            ("0", 0, 340, 165, 80, "#7f8c8d"),  # Zero is wider (2x)
            (".", 170, 340, 80, 80, "#7f8c8d"),
            ("=", 255, 340, 80, 80, "#f39c12"),
        ]
        
        # Create all buttons with absolute positioning
        self.button_widgets = {}
        
        for (text, x, y, width, height, bg_color) in button_specs:
            button = tk.Button(
                self.buttons_frame,
                text=text,
                font=tkfont.Font(family="Arial", size=20, weight="bold"),
                bg=bg_color,
                fg="white",
                activebackground=self.lighten_color(bg_color),
                activeforeground="white",
                relief=tk.FLAT,
                borderwidth=0,
                command=lambda t=text: self.on_button_click(t)
            )
            button.place(x=x, y=y, width=width, height=height)
            self.button_widgets[text] = button
            
            # Bind hover effect
            button.bind("<Enter>", lambda event, btn=button: self.on_hover_enter(btn))
            button.bind("<Leave>", lambda event, btn=button: self.on_hover_leave(btn))
    
    def lighten_color(self, hex_color, factor=0.2):
        """Lighten a given hex color by the specified factor."""
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def on_hover_enter(self, button):
        """Handle mouse hover enter event with subtle animation."""
        original_bg = button.cget("bg")
        lighter_bg = self.lighten_color(original_bg, 0.1)
        self.animations.animate_color_transition(button, original_bg, lighter_bg, duration=150, property_name="bg")
    
    def on_hover_leave(self, button):
        """Handle mouse hover leave event with subtle animation."""
        lighter_bg = button.cget("bg")
        original_bg = self.lighten_color(lighter_bg, -0.1)  # Reverse the lightening
        self.animations.animate_color_transition(button, lighter_bg, original_bg, duration=150, property_name="bg")
    
    def on_button_click(self, button_text):
        """Handle button clicks with animations and calculate results."""
        # Get the button and save its current state
        button = self.button_widgets[button_text]
        original_x = button.winfo_x()
        original_y = button.winfo_y()
        original_width = button.winfo_width()
        original_height = button.winfo_height()
        
        # Choose a simpler animation to minimize layout disruption
        # Instead of random animations, just use color transition which is safer
        self.animations.animate_color_transition(
            button,
            button.cget("bg"),
            self.lighten_color(button.cget("bg"), 0.3),
            duration=100,
            property_name="bg",
            callback=lambda: self.animations.animate_color_transition(
                button,
                self.lighten_color(button.cget("bg"), 0.3),
                self.original_button_states[button_text].get('bg', button.cget("bg")),
                duration=100,
                property_name="bg"
            )
        )
        
        # Force button back to original position and size after animation
        def restore_button():
            button.place(
                x=original_x,
                y=original_y,
                width=original_width,
                height=original_height
            )
            self.root.update()
        
        # Schedule restoration after animation
        self.root.after(200, restore_button)
        
        # Process the button input
        if button_text in "0123456789.":
            self.handle_number_input(button_text)
        elif button_text in "+-×÷":
            self.handle_operation(button_text)
        elif button_text == "=":
            self.calculate_result()
        elif button_text == "C":
            self.clear_calculator()
        elif button_text == "±":
            self.negate_value()
        elif button_text == "%":
            self.calculate_percentage()
    
    def handle_number_input(self, digit):
        """Handle numeric input from the calculator buttons."""
        # If we just displayed a result, start fresh
        if self.result_shown:
            self.current_input = "0"
            self.result_shown = False
        
        # Handle decimal point
        if digit == ".":
            if "." not in self.current_input:
                self.current_input += "."
        # Handle digits
        else:
            if self.current_input == "0":
                self.current_input = digit
            else:
                self.current_input += digit
        
        self.update_display()
    
    def handle_operation(self, op):
        """Handle operation buttons (+, -, ×, ÷)."""
        # If there's a pending operation, calculate the result first
        if self.stored_value is not None and self.operation and not self.result_shown:
            self.calculate_result()
        
        # Store the current value and operation
        self.stored_value = float(self.current_input)
        self.operation = op
        
        # Reset for new input
        self.current_input = "0"
        self.result_shown = False
        
        # Update operation display
        self.operation_display.config(text=f"{self.format_number(self.stored_value)} {op}")
        
        # Animate the operation display with color only
        self.animations.animate_color_transition(
            self.operation_display, 
            "#34495e", 
            "#2c3e50", 
            duration=300, 
            property_name="bg",
            callback=lambda: self.animations.animate_color_transition(
                self.operation_display,
                "#2c3e50",
                "#34495e",
                duration=300,
                property_name="bg"
            )
        )
    
    def calculate_result(self):
        """Calculate and display result of the operation."""
        if self.stored_value is None or self.operation is None:
            return
        
        # Parse current input
        current_value = float(self.current_input)
        
        # Perform calculation
        if self.operation == "+":
            result = self.stored_value + current_value
        elif self.operation == "-":
            result = self.stored_value - current_value
        elif self.operation == "×":
            result = self.stored_value * current_value
        elif self.operation == "÷":
            # Handle division by zero
            if current_value == 0:
                self.display.config(text="Error")
                self.operation_display.config(text="")
                self.stored_value = None
                self.operation = None
                self.current_input = "0"
                self.result_shown = True
                return
            result = self.stored_value / current_value
        
        # Update state
        self.current_input = str(result)
        self.stored_value = None
        self.operation = None
        self.result_shown = True
        
        # Clear operation display
        self.operation_display.config(text="")
        
        # Update display
        self.update_display()
        
        # Use color animation instead of pulse for result display
        self.animations.animate_color_transition(
            self.display,
            "#34495e",
            "#2c3e50",
            duration=200,
            property_name="bg",
            callback=lambda: self.animations.animate_color_transition(
                self.display,
                "#2c3e50",
                "#34495e",
                duration=200,
                property_name="bg"
            )
        )
    
    def negate_value(self):
        """Negate the current input value."""
        if self.current_input != "0":
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
            
            self.update_display()
    
    def calculate_percentage(self):
        """Calculate percentage of current value."""
        if self.current_input != "0":
            current_value = float(self.current_input)
            self.current_input = str(current_value / 100)
            
            self.update_display()
    
    def clear_calculator(self):
        """Reset calculator to initial state."""
        self.current_input = "0"
        self.stored_value = None
        self.operation = None
        self.result_shown = False
        
        self.operation_display.config(text="")
        self.update_display()
        
        # Use only color animation for clear
        self.animations.animate_color_transition(
            self.display,
            "#34495e",
            "#2c3e50",
            duration=200,
            property_name="bg",
            callback=lambda: self.animations.animate_color_transition(
                self.display,
                "#2c3e50",
                "#34495e",
                duration=200,
                property_name="bg"
            )
        )
    
    def format_number(self, number):
        """Format number for display, removing trailing zeros after decimal point."""
        if isinstance(number, str):
            number = float(number)
            
        # Check if the number is an integer
        if number.is_integer():
            return str(int(number))
        else:
            # Remove trailing zeros
            return str(number).rstrip('0').rstrip('.') if '.' in str(number) else str(number)
    
    def update_display(self):
        """Update the calculator display with current input."""
        formatted_number = self.format_number(self.current_input)
        self.display.config(text=formatted_number)


if __name__ == "__main__":
    root = tk.Tk()
    app = AnimatedCalculator(root)
    root.mainloop()