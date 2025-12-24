#!/usr/bin/env python3
"""Simple test to see if a Tkinter window can open."""
from tkinter import Tk, Label

root = Tk()
root.title("Test Window")
root.geometry("400x200")
label = Label(root, text="If you see this, Tkinter works!", font=("Arial", 16))
label.pack(pady=50)
print("Window should be visible now. Close it to continue.")
root.mainloop()
print("Window closed.")
