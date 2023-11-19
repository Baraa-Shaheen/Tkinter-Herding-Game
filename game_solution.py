#1920x1080

import tkinter as tk

window = tk.Tk()
window.geometry("1920x1080")
canvas = tk.Canvas(window, width=1920, height=1080)
canvas.configure(bg="green")
canvas.pack()

window.mainloop()
