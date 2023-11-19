#1920x1080

import tkinter as tk

class Ball:
    def __init__(self, radius, colour):
        self.x_speed = 0
        self.y_speed = 0
        self.radius = radius
        self.colour = colour
        self.ball_id = None
    
    def place_ball(self, canvas, x, y):
        x1 = x - self.radius
        y1 = y - self.radius
        x2 = x + self.radius
        y2 = y + self.radius
        self.ball_id = canvas.create_oval(x1, y1, x2, y2, fill=self.colour)


# Create 1920x1080 window with green canvas
window = tk.Tk()
window.geometry("1920x1080")
canvas_width = 1920
canvas_height = 1080
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="green")
canvas.pack()

player = Ball(15, "black")
player.place_ball(canvas, canvas_width/2, canvas_height/2)



window.mainloop()
