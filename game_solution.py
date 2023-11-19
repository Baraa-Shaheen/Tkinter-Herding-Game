#1920x1080

import tkinter as tk

class Ball:
    def __init__(self, radius, colour):
        self.x_speed = 0
        self.y_speed = 0
        self.radius = radius
        self.colour = colour
        self.ball_id = None
    
    def place_ball(self, x, y):
        x1 = x - self.radius
        y1 = y - self.radius
        x2 = x + self.radius
        y2 = y + self.radius
        self.ball_id = canvas.create_oval(x1, y1, x2, y2, fill=self.colour)

    def get_position(self):
        pos = canvas.coords(self.ball_id)
        centre_x = (pos[0] + pos[2]) / 2
        centre_y = (pos[1] + pos[3]) / 2
        return (centre_x, centre_y)


def on_mouse_motion(event):
    x = player.get_position()[0]
    y = player.get_position()[1]
    canvas.move(player.ball_id, event.x - x, event.y - y)

def update_game():
    window.update()
    window.after(1, update_game)


# class Player(Ball):
#     pass


# Create 1920x1080 window with green canvas
window = tk.Tk()
window.geometry("1920x1080")
canvas_width = 1920
canvas_height = 1080
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="green")
canvas.pack()

player = Ball(12, "black")
player.place_ball(canvas_width/2, canvas_height/2)
print(player.get_position())

window.bind('<Motion>', on_mouse_motion)
update_game()

window.mainloop()
