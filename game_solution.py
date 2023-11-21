#1920x1080

import tkinter as tk
from random import randint, uniform
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

    def remove(self):
        canvas.delete(self.id)
        pass

    def get_centre(self):
        pos = canvas.coords(self.id)
        centre_x = (pos[0] + pos[2]) / 2
        centre_y = (pos[1] + pos[3]) / 2
        return (centre_x, centre_y)
    
    def move(self, x, y):
        canvas.move(self.id, x, y)

    
class Player(Ball):
    def __init__(self, radius = 10, colour = "black"):
        super().__init__(radius, colour)
    
    def repel(self, repelling_distance):
        for sheep in sheep_list:
            player_pos = player.get_centre()
            sheep_pos = sheep.get_centre()
            distance = sqrt((sheep_pos[0] - player_pos[0])**2 + (sheep_pos[1] - player_pos[1])**2)

            if (distance <= repelling_distance):
                vector_i = sheep_pos[0] - player_pos[0]
                vector_j = sheep_pos[1] - player_pos[1]
                vector_magnitude = sqrt(vector_i**2 + vector_j**2)
                unit_vector = [vector_i / vector_magnitude, vector_j / vector_magnitude]
                sheep.speed_x = unit_vector[0] * 2.5
                sheep.speed_y = unit_vector[1] * 2.5



# add super sheep 
class Sheep(Ball):
    def __init__(self, radius = 20, colour = "white", value = 10, is_super = False):
        if(is_super):
            radius = radius * 1.3
            value = value * 2
        super().__init__(radius, colour)
        self.is_super = is_super
        self.value = value

    def move(self, x, y):
        canvas.move(self.id, x, y)
        self.decelerate()
        sheep_removed = self.check_gate_collision()
        if(not sheep_removed):
            self.check_fence_collision()
        self.idle()

    def get_coords(self):
        sheep_coords = []
        sheep_coords.append(canvas.coords(self.id)[0])
        sheep_coords.append(canvas.coords(self.id)[1])
        sheep_coords.append(canvas.coords(self.id)[2])
        sheep_coords.append(canvas.coords(self.id)[3])
        return sheep_coords
    
    def decelerate(self):
        self.speed_x *= 0.99
        self.speed_y *= 0.99

    def check_gate_collision(self):
        global time_remaining

        sheep_coords = self.get_coords()

        gate_y1 = canvas.coords(gate)[1]
        gate_y2 = canvas.coords(gate)[3]

        # If sheep has collided with right side of fence
        if(sheep_coords[2] > fence_x2):
            if(sheep_coords[1] > gate_y1 and sheep_coords[3] < gate_y2):
                self.remove()
                sheep_list.remove(self)
                if(self.is_super):
                    add_to_score(self.value)
                    time_remaining += 2
                else:
                    add_to_score(self.value)
                update_ui(False, True, True)
                check_level_completed()
                return True

    def check_fence_collision(self):
        sheep_coords = self.get_coords()

        if(sheep_coords[0] < fence_x1 or sheep_coords[2] > fence_x2):
            self.speed_x = -self.speed_x
        if(sheep_coords[1] < fence_y1 or sheep_coords[3] > fence_y2):
            self.speed_y = -self.speed_y

        # Stop sheep from escaping fence
        if(sheep_coords[0] < fence_x1):
            sheep_coords = self.get_coords()
            sheep_fence_distance = fence_x1 - sheep_coords[0]
            canvas.coords(self.id, sheep_coords[0] + sheep_fence_distance, sheep_coords[1], sheep_coords[2] + sheep_fence_distance, sheep_coords[3])

        if(sheep_coords[1] < fence_y1):
            sheep_coords = self.get_coords()
            sheep_fence_distance = fence_y1 - sheep_coords[1]
            canvas.coords(self.id, sheep_coords[0], sheep_coords[1] + sheep_fence_distance, sheep_coords[2], sheep_coords[3] + sheep_fence_distance)

        if(sheep_coords[2] > fence_x2):
            sheep_coords = self.get_coords()
            sheep_fence_distance = sheep_coords[2] - fence_x2
            canvas.coords(self.id, sheep_coords[0] - sheep_fence_distance, sheep_coords[1], sheep_coords[2] - sheep_fence_distance, sheep_coords[3])

        if(sheep_coords[3] > fence_y2):
            sheep_coords = self.get_coords()
            sheep_fence_distance = sheep_coords[3] - fence_y2
            canvas.coords(self.id, sheep_coords[0], sheep_coords[1] - sheep_fence_distance, sheep_coords[2], sheep_coords[3] - sheep_fence_distance)


    def idle(self):
        speed = sqrt(self.speed_x**2 + self.speed_y**2)
        if(speed < 0.5):
            direction_x = randint(0,1)
            direction_y = randint(0,1)
            if(direction_x == 0):
                multiplier = -1
            else:
                multiplier = 1
            self.speed_x = 0.4 * multiplier

            if(direction_y == 0):
                multiplier = -1
            else:
                multiplier = 1
            self.speed_y = 0.4 * multiplier




def create_fence():
    global fence
    fence_dimensions = [400,225]
    if (fence_dimensions[0] < 1920):
        fence_dimensions[0] = fence_dimensions[0] + (level * 10)
    if (fence_dimensions[1] < 1080):
        fence_dimensions[1] = fence_dimensions[1] + (level * 6)

    global fence_x1, fence_y1, fence_x2, fence_y2
    fence_x1 = (canvas_width / 2) - (fence_dimensions[0] / 2)
    fence_y1 = (canvas_height / 2) - (fence_dimensions[1] / 2)
    fence_x2 = (canvas_width / 2) + (fence_dimensions[0] / 2)
    fence_y2 = (canvas_height / 2) + (fence_dimensions[1] / 2)

    # If there is no fence on the canvas, create and add one
    try:
        fence
    except NameError:
        fence = canvas.create_rectangle(fence_x1, fence_y1, fence_x2, fence_y2, fill="", outline="black", width=4)
    else:
        canvas.delete(fence)
        fence = canvas.create_rectangle(fence_x1, fence_y1, fence_x2, fence_y2, fill="", outline="black", width=4)

    

    
def create_gate():
    global gate
    x1 = fence_x2 - 2
    y1 = (canvas_height / 2) - 75
    x2 = fence_x2 + 10
    y2 = (canvas_height / 2) + 75

    try:
        gate
    except NameError:
        gate = canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline = "green", width = 0)
    else:
        canvas.delete(gate)
        gate = canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline = "green", width = 0)


def spawn_sheep():
    global sheep_list
    sheep_list = []
    
    for i in range (level):
        # 10% chance of sheep being super sheep
        x = randint(0,9)
        if(x != 0):
            sheep = Sheep()
            sheep_list.append(sheep)
        else:
            sheep = Sheep(is_super = True)
            sheep_list.append(sheep)
    for sheep in sheep_list:
        x = randint(int(fence_x1 + 30), int(fence_x2 - 30))
        y = randint(int(fence_y1 + 30), int(fence_y2 - 30))
        sheep.place(x, y)

def update_ui(update_level_text = True, update_time_remaining_text = True, update_score_text = True):
    global level_text, time_remaining_text, score_text

    # If text does not exist, create it
    try:
        level_text
    except NameError:
        level_text = canvas.create_text(50, 0, text = f"Level: {level}", font = ("Calibri", 30), fill = "white", anchor = "nw")

    try:
        time_remaining_text
    except NameError:
        time_remaining_text = canvas.create_text(canvas_width / 2, 0, text = f"{time_remaining}", font = ("Calibri", 60), fill = "white", anchor = "n")

    try:
        score_text
    except NameError:
        score_text = canvas.create_text(canvas_width - 50, 0, text = f"Score: {score}", font = ("Calibri", 30), fill = "white", anchor = "ne")

    if(update_level_text):
        canvas.delete(level_text)
        level_text = canvas.create_text(50, 0, text = f"Level: {level}", font = ("Calibri", 30), fill = "white", anchor = "nw")

    if(update_time_remaining_text):
        canvas.delete(time_remaining_text)
        time_remaining_text = canvas.create_text(canvas_width / 2, 0, text = f"{time_remaining}", font = ("Calibri", 60), fill = "white", anchor = "n")

    if(update_score_text):
        canvas.delete(score_text)
        score_text = canvas.create_text(canvas_width - 50, 0, text = f"Score: {score}", font = ("Calibri", 30), fill = "white", anchor = "ne")


def check_level_completed():
    global level_completed, level
    if len(sheep_list) == 0:
        add_to_score(time_remaining * 5)
        level += 1
        start_new_level()


def update_timer():
    global time_remaining, game_over
    
    if(time_remaining > 0):
        time_remaining -= 1
        update_ui(False, True, False)
    if(time_remaining == 0):
        game_over = True
    window.after(1000, update_timer)


def add_to_score(value):
    global score
    score += value


def on_mouse_motion(event):
    x = player.get_centre()[0]
    y = player.get_centre()[1]
    player.move(event.x - x, event.y - y)


def update_game():
    player.repel(100)
    for sheep in sheep_list:
        sheep.move(sheep.speed_x, sheep.speed_y)
    window.after(15, update_game)

# Create 1920x1080 window with green canvas
window = tk.Tk()
window.geometry("1920x1080")
window.title("Sheep Herding Game")
# window.attributes("-fullscreen", True)
canvas_width = 1920
canvas_height = 1080
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="green")
canvas.pack()

level = 1
time_remaining = 30
score = 0
game_over = False

player = Player()
player.place(canvas_width / 2, canvas_height / 2)

def start_new_level():
    global time_remaining
    time_remaining = 30
    update_ui()
    create_fence()
    create_gate()
    spawn_sheep()


start_new_level()
update_timer()
update_game()


window.bind('<Motion>', on_mouse_motion)

window.mainloop()
