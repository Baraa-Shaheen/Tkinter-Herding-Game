#1920x1080

import tkinter as tk
from random import randint
from math import sqrt

class Ball:
    def __init__(self, radius, colour):
        self.speed_x = 0
        self.speed_y = 0
        self.radius = radius
        self.colour = colour
        self.id = None
    
    def place(self, x, y):
        x1 = x - self.radius
        y1 = y - self.radius
        x2 = x + self.radius
        y2 = y + self.radius
        self.id = canvas.create_oval(x1, y1, x2, y2, fill=self.colour)

    def get_position(self):
        pos = canvas.coords(self.id)
        centre_x = (pos[0] + pos[2]) / 2
        centre_y = (pos[1] + pos[3]) / 2
        return (centre_x, centre_y)
    
    def move(self, x, y):
        canvas.move(self.id, x, y)
    

class Player(Ball):
    def repel(self, repelling_distance):
        for sheep in sheep_list:
            player_pos = player.get_position()
            sheep_pos = sheep.get_position()
            distance = sqrt((sheep_pos[0] - player_pos[0])**2 + (sheep_pos[1] - player_pos[1])**2)

            if (distance <= repelling_distance):
                vector_i = sheep_pos[0] - player_pos[0]
                vector_j = sheep_pos[1] - player_pos[1]
                vector_magnitude = sqrt(vector_i**2 + vector_j**2)
                unit_vector = [vector_i / vector_magnitude, vector_j / vector_magnitude]
                sheep.speed_x = unit_vector[0]
                sheep.speed_y = unit_vector[1]


class Sheep(Ball):
    pass


def create_fence_and_gate():
    dimensions = [400,225]
    if (dimensions[0] < 1920):
        dimensions[0] = dimensions[0] + (level * 15)
    if (dimensions[1] < 1080):
        dimensions[1] = dimensions[1] + (level * 8)

    global fence_x1, fence_y1, fence_x2, fence_y2
    fence_x1 = (canvas_width / 2) - (dimensions[0] / 2)
    fence_y1 = (canvas_height / 2) - (dimensions[1] / 2)
    fence_x2 = (canvas_width / 2) + (dimensions[0] / 2)
    fence_y2 = (canvas_height / 2) + (dimensions[1] / 2)

    canvas.create_rectangle(fence_x1, fence_y1, fence_x2, fence_y2, fill="", outline="black", width=4)


def spawn_sheep():
    global sheep_list
    sheep_list = []
    for i in range (level):
        sheep = Sheep(15, "white")
        sheep_list.append(sheep)
    for sheep in sheep_list:
        x = randint(int(fence_x1 + 30), int(fence_x2 - 30))
        y = randint(int(fence_y1 + 30), int(fence_y2 - 30))
        sheep.place(x, y)


def on_mouse_motion(event):
    x = player.get_position()[0]
    y = player.get_position()[1]
    player.move(event.x - x, event.y - y)


def update_game():
    player.repel(100)
    for sheep in sheep_list:
        sheep.move(sheep.speed_x, sheep.speed_y)
    window.after(10, update_game)

# Create 1920x1080 window with green canvas
window = tk.Tk()
window.geometry("1920x1080")
# window.attributes("-fullscreen", True)
canvas_width = 1920
canvas_height = 1080
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="green")
canvas.pack()

level = 50

player = Player(10, "black")
player.place(canvas_width / 2, canvas_height / 2)

create_fence_and_gate()
spawn_sheep()
update_game()

window.bind('<Motion>', on_mouse_motion)

window.mainloop()
