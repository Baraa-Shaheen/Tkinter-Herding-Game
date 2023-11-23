#1920x1080

import tkinter as tk
from random import randint, uniform
from math import sqrt

class Ball:
    def __init__(self, radius, colour):
        self.velocity_x = 0
        self.velocity_y = 0
        self.radius = radius
        self.colour = colour
        self.hidden_state = "normal"
        self.id = None
    
    def place(self, x, y):
        x1 = x - self.radius
        y1 = y - self.radius
        x2 = x + self.radius
        y2 = y + self.radius

        self.id = canvas.create_oval(x1, y1, x2, y2, fill=self.colour, state = f"{self.hidden_state}")

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
        self.hidden_state = "hidden"
    
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
                sheep.velocity_x = unit_vector[0] * 2.5
                sheep.velocity_y = unit_vector[1] * 2.5


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
        self.velocity_x *= 0.99
        self.velocity_y *= 0.99

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
            self.velocity_x = -self.velocity_x
        if(sheep_coords[1] < fence_y1 or sheep_coords[3] > fence_y2):
            self.velocity_y = -self.velocity_y

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
        speed = sqrt(self.velocity_x**2 + self.velocity_y**2)
        if(speed < 0.5):
            direction_x = randint(0,1)
            direction_y = randint(0,1)
            if(direction_x == 0):
                multiplier = -1
            else:
                multiplier = 1
            self.velocity_x = 0.4 * multiplier

            if(direction_y == 0):
                multiplier = -1
            else:
                multiplier = 1
            self.velocity_y = 0.4 * multiplier




def create_fence():
    global fence
    fence_dimensions = [400,225]
    if (fence_dimensions[0] < 1900):
        fence_dimensions[0] = fence_dimensions[0] + (level * 10)
    if (fence_dimensions[1] < 1060):
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
    else:
        if(update_level_text):
            canvas.delete(level_text)
            level_text = canvas.create_text(50, 0, text = f"Level: {level}", font = ("Calibri", 30), fill = "white", anchor = "nw")

    try:
        time_remaining_text
    except NameError:
        time_remaining_text = canvas.create_text(canvas_width / 2, 0, text = f"{time_remaining}", font = ("Calibri", 60), fill = "white", anchor = "n")
    else:
         if(update_time_remaining_text):
            canvas.delete(time_remaining_text)
            time_remaining_text = canvas.create_text(canvas_width / 2, 0, text = f"{time_remaining}", font = ("Calibri", 60), fill = "white", anchor = "n")

    try:
        score_text
    except NameError:
        score_text = canvas.create_text(canvas_width - 50, 0, text = f"Score: {score}", font = ("Calibri", 30), fill = "white", anchor = "ne")
    else:
        if(update_score_text):
            canvas.delete(score_text)
            score_text = canvas.create_text(canvas_width - 50, 0, text = f"Score: {score}", font = ("Calibri", 30), fill = "white", anchor = "ne")
    

def remove_ui():
    canvas.delete(level_text)
    canvas.delete(time_remaining_text)
    canvas.delete(score_text)

    # try:
    #     game_over_text
    # except NameError:
    #     pass
    # else:
    #     canvas.delete(game_over_text)


def check_level_completed():
    global level_completed, level
    if len(sheep_list) == 0:
        add_to_score(time_remaining * 5)
        level += 1
        start_new_level()


def update_timer():
    global time_remaining, game_over
    
    if(game_running):
        if(time_remaining > 0):
            time_remaining -= 1
            update_ui(False, True, False)
        if(time_remaining == 0):
            game_over = True
            end_game()
    
    if(not game_paused):
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
        sheep.move(sheep.velocity_x, sheep.velocity_y)
    if(not game_paused):
        window.after(15, update_game)


def start_new_level():
    global time_remaining
    time_remaining = 15
    update_ui()
    create_fence()
    create_gate()
    spawn_sheep()


def toggle_pause_game():
    global game_paused

    if(game_running):
        if(not game_paused):
            game_paused = True
            toggle_pause_menu()
        else:
            unpause_game()

 
def unpause_game():
    global game_paused
    game_paused = False
    toggle_pause_menu()
    update_timer()
    update_game()


def toggle_pause_menu():
    global resume_button, save_game_button, main_menu_button

    if(game_paused):
        resume_button = tk.Button(canvas, text = "Resume", font = ("Calibri", 40), width = 15, command = toggle_pause_game)
        save_game_button = tk.Button(canvas, text = "Save Game", font = ("Calibri", 40), width = 15, command = save_game)
        main_menu_button = tk.Button(canvas, text = "Main Menu", font = ("Calibri", 40), width = 15, command = return_to_main_menu)

        resume_button.place(x = (canvas_width / 2 - 208), y = 325)
        save_game_button.place(x = (canvas_width / 2) - 208, y = 450)
        main_menu_button.place(x = (canvas_width / 2) - 208, y = 575)

    else:
        resume_button.destroy()
        save_game_button.destroy()
        main_menu_button.destroy()
        

def show_main_menu():
     global main_menu_button_list
     main_menu_button_list = []


     start_game_button = tk.Button(canvas, text = "Start Game", font = ("Calibri", 40), width = 15, command = start_game)
     main_menu_button_list.append(start_game_button)

     load_game_button = tk.Button(canvas, text = "Load Game", font = ("Calibri", 40), width = 15, command = load_game)
     main_menu_button_list.append(load_game_button)

     leaderboard_button = tk.Button(canvas, text = "Leaderboard", font = ("Calibri", 40), width = 15, command = display_leaderboard)
     main_menu_button_list.append(leaderboard_button)

     controls_button = tk.Button(canvas, text = "Controls", font = ("Calibri", 40), width = 15, command = show_controls_menu)
     main_menu_button_list.append(controls_button)

     exit_game_button = tk.Button(canvas, text = "Exit Game", font = ("Calibri", 40), width = 15, command = exit_game)
     main_menu_button_list.append(exit_game_button)

     start_game_button.place(x = (canvas_width / 2 - 208), y = 275)
     load_game_button.place(x = (canvas_width / 2) - 208, y = 400)
     leaderboard_button.place(x = (canvas_width / 2) - 208, y = 525)
     controls_button.place(x = (canvas_width / 2) - 208, y = 650)
     exit_game_button.place(x = (canvas_width / 2) - 208, y = 775)


def hide_main_menu():
    for button in main_menu_button_list:
        button.destroy()




def end_game():
    global game_running, game_paused, game_over_text
    game_running = False
    game_paused = True
    show_game_over_menu()
    show_name_form()
    #...


def show_name_form():
    global entry, name_form_window
    name_form_window = tk.Toplevel(window)
    name_form_window.title("Enter your name: ")
    name_form_window.geometry(f"300x80+{(canvas_width // 2) - 150}+300")
    name_form_window.grab_set()
    
    entry = tk.Entry(name_form_window, width = 40)
    entry.pack(pady=10)
    submit_button = tk.Button(name_form_window, text="Submit", command=save_to_leaderboard)
    submit_button.pack()

def save_to_leaderboard():
    name = entry.get()
    name_form_window.grab_release()
    name_form_window.destroy()
    with open('leaderboard.txt', 'a') as file:
        file.write(f"{name} {level} {score}\n")

def display_leaderboard():
    scores = []
    with open('leaderboard.txt', 'r') as file:
        for line in file:
            name, level, score = line.split()
            scores.append((name, int(level), int(score)))
    
    # Sort scores in descending order based on score
    scores.sort(key=lambda x: x[2], reverse=True)

    leaderboard_text = "    Player                            Level           Score\n\n"
    for i in range(len(scores)):
        name, level, score = scores[i]
        leaderboard_text += f"{(i + 1):4}. {name:30} {level:4} {score:15}\n"

    leaderboard_window= tk.Toplevel(window)
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry(f"500x242+{(canvas_width // 2) - 250}+300")
    leaderboard_window.grab_set()

    leaderboard_text_widget = tk.Text(leaderboard_window) #height=10, width=30)
    leaderboard_text_widget.pack()

    # Insert the leaderboard_text into the Text widget
    leaderboard_text_widget.insert(tk.END, leaderboard_text)

    


def show_game_over_menu():
    global try_again_button, main_menu_button2

    try_again_button = tk.Button(canvas, text = "Try Again", font = ("Calibri", 40), width = 15, command=lambda: start_game(True))
    main_menu_button2 = tk.Button(canvas, text = "Main Menu", font = ("Calibri", 40), width = 15, command=lambda: return_to_main_menu(True))

    try_again_button.place(x = (canvas_width / 2 - 208), y = 200)
    main_menu_button2.place(x = (canvas_width / 2 - 208), y = 325)


def hide_game_over_menu():
    try_again_button.destroy()
    main_menu_button2.destroy()


def remove_all_elements():
    remove_ui()
    remove_ui()
    for sheep in sheep_list:
        sheep.remove()
    canvas.delete(fence)
    canvas.delete(gate)
    


def return_to_main_menu(play_again = False):
    if(play_again):
        hide_game_over_menu()
    global game_over, game_running, game_paused
    game_over = True
    game_running = False
    game_paused = False
    toggle_pause_menu()
    remove_all_elements()
    show_main_menu()


def save_game():

    pass


def load_game():

    pass


def show_leaderboard():

    pass


def show_controls_menu():

    pass


def exit_game():
    window.destroy()

def start_game(play_again = False):
    global game_running, game_paused, level, score
    game_running = True
    game_paused = False
    level = 1
    score = 0
    if(play_again):
        remove_all_elements()
        hide_game_over_menu()
    else:
        hide_main_menu()
    start_new_level()
    update_timer()
    update_game()


# Create 1920x1080 window with green canvas
window = tk.Tk()
window.geometry("1920x1080")
window.title("Sheep Herding Game")
# window.attributes("-fullscreen", True)
canvas_width = 1920
canvas_height = 1080
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="green")
canvas.pack()

# level = 1
# time_remaining = 15
# score = 0
game_over = False
game_paused = False
game_running = False

player = Player()
player.place(canvas_width / 2, canvas_height / 2)

show_main_menu()

window.bind('<Motion>', on_mouse_motion)
window.bind("<Escape>", lambda event: toggle_pause_game())


window.mainloop()
