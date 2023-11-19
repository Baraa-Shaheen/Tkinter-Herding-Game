#1920x1080

import tkinter as tk

class Ball:
    def __init__(self, x, y, diameter, colour):
        self.x_speed = 0
        self.y_speed = 0
        self.x = x
        self.y = y
        self.diameter = diameter 
        self.colour = colour
    
    def place_ball(canvas):
        pass



# Create 1920x1080 window with green canvas
window = tk.Tk()
window.geometry("1920x1080")
canvas = tk.Canvas(window, width=1920, height=1080, bg="green")
canvas.pack()

circle = canvas.create_oval(0,0,30,30, fill="black")



window.mainloop()
