"""Run with: python examples/basic.py"""
import tkinter as tk
from tkanimator import Animator, Easing

root = tk.Tk()
root.geometry("420x180")
button = tk.Button(root, text="Move me")
button.place(x=20, y=60)
animator = Animator(button)
animator.move(x=300, y=60, duration=1200, easing=Easing.EASE_IN_OUT_CUBIC).start()
root.mainloop()
