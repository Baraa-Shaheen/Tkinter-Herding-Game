#1920x1080

import tkinter as tk
from tkinter import messagebox
from random import randint
from math import sqrt
from PIL import Image, ImageTk

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
                sheep.velocity_x = unit_vector[0] * 3
                sheep.velocity_y = unit_vector[1] * 3


class Sheep(Ball):
    def __init__(self, radius = 20, colour = "white", value = 10, is_super = False):
        if(is_super):
            radius = radius * 1.5
            value = value * 5
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

        gate_x1 = canvas.coords(gate)[0]
        gate_y1 = canvas.coords(gate)[1]
        gate_x2 = canvas.coords(gate)[2]
        gate_y2 = canvas.coords(gate)[3]

        # If sheep has collided with right side of fence

        sheep_touched_fence = False
        sheep_between_gate = False
        if(gate_position == 1):
            sheep_touched_fence = sheep_coords[2] > fence_x2
            sheep_between_gate = sheep_coords[1] > gate_y1 and sheep_coords[3] < gate_y2
        
        elif (gate_position == 2):
            sheep_touched_fence = sheep_coords[0] < fence_x1
            sheep_between_gate = sheep_coords[1] > gate_y1 and sheep_coords[3] < gate_y2

        elif(gate_position == 3):
            sheep_touched_fence = sheep_coords[1] < fence_y1
            sheep_between_gate = sheep_coords[0] > gate_x1 and sheep_coords[2] < gate_x2

        elif(gate_position == 4):
            sheep_touched_fence = sheep_coords[3] > fence_y2
            sheep_between_gate = sheep_coords[0] > gate_x1 and sheep_coords[2] < gate_x2

        if(sheep_touched_fence):
            if(sheep_between_gate):
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
            self.velocity_x = 0.55 * multiplier

            if(direction_y == 0):
                multiplier = -1
            else:
                multiplier = 1
            self.velocity_y = 0.55 * multiplier


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

    
def create_gate(create_loaded_gate = False):
    global gate, gate_position

    if(not create_loaded_gate):
        gate_position = randint(1,4)

    if(gate_position == 1):
        x1 = fence_x2 - 2
        y1 = (canvas_height / 2) - 75
        x2 = fence_x2 + 10
        y2 = (canvas_height / 2) + 75
    
    elif(gate_position == 2):
        x1 = fence_x1 - 10
        y1 = (canvas_height / 2) - 75
        x2 = fence_x1 + 2
        y2 = (canvas_height / 2) + 75

    elif(gate_position == 3):
        x1 = (canvas_width / 2) - 75
        y1 = fence_y1 - 10
        x2 = (canvas_width / 2) + 75
        y2 = fence_y1 + 2

    elif(gate_position == 4):
        x1 = (canvas_width / 2) - 75
        y1 = fence_y2 - 2
        x2 = (canvas_width / 2) + 75
        y2 = fence_y2 + 10

    try:
        gate
    except NameError:
        gate = canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline = "green", width = 0)
    else:
        canvas.delete(gate)
        gate = canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline = "green", width = 0)


def spawn_sheep(spawn_loaded_sheep = False):
    global sheep_list
    sheep_list = []
    
    if(not spawn_loaded_sheep):
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
    
    else:
        for sheep_data in loaded_sheep_data_list:
            if(sheep_data[2] == 0):
                sheep = Sheep()
                sheep_list.append(sheep)
                sheep.place(sheep_data[0], sheep_data[1])
            else:
                sheep = Sheep(is_super = True)
                sheep_list.append(sheep) 
                sheep.place(sheep_data[0], sheep_data[1])


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



def check_level_completed():
    global level_completed, level
    if len(sheep_list) == 0:
        add_to_score(time_remaining * 20)
        level += 1
        start_new_level()


def update_timer():
    global time_remaining, game_over
    
    if(game_running and not game_paused):
        if(time_remaining > 0):
            time_remaining -= 1
            update_ui(False, True, False)
        if(time_remaining == 0):
            game_over = True
            end_game()
    
    # if(not game_paused):
    if(not game_over):
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


def start_new_level(start_loaded_level = False):
    global time_remaining
    if(not start_loaded_level):
        time_remaining = 15
    update_ui()
    create_fence()
    create_gate(start_loaded_level)
    spawn_sheep(start_loaded_level)


def toggle_pause_game():
    global game_paused

    if(game_running and not game_paused):
        game_paused = True
        toggle_pause_menu()
    else:
        unpause_game()

 
def unpause_game():
    global game_paused
    game_paused = False
    toggle_pause_menu()
    update_game()


def toggle_pause_menu(from_game_over_menu = False):
    global resume_button, save_game_button, main_menu_button

    if(from_game_over_menu):
        return

    if(game_paused):
        resume_button = tk.Button(canvas, text = "Resume", font = ("Calibri", 40), width = 15, command = toggle_pause_game)
        save_game_button = tk.Button(canvas, text = "Save Game", font = ("Calibri", 40), width = 15, command = save_game)
        main_menu_button = tk.Button(canvas, text = "Main Menu", font = ("Calibri", 40), width = 15, command = return_to_main_menu)

        resume_button.place(x = (canvas_width / 2) - 208, y = 325)
        save_game_button.place(x = (canvas_width / 2) - 208, y = 450)
        main_menu_button.place(x = (canvas_width / 2) - 208, y = 575)

    else:
        resume_button.destroy()
        save_game_button.destroy()
        main_menu_button.destroy()
        

def show_main_menu():
     global main_menu_button_list, sheep_image_tk_id, title_text
     main_menu_button_list = []

     title_text = canvas.create_text(canvas_width / 2, 25, text = "Super Sheep Frenzy", font = ("Calibri", 60), fill = "white", anchor = "n")
     title_text_coords = canvas.coords(title_text)

     # cartoon sheep designed By Techchennai from https://pngtree.com/freepng/cartoon-sheep_3584615.html?sol=downref&id=bef
     sheep_image = Image.open("sheep.png")
     sheep_image = sheep_image.resize((130,95))
     sheep_image_tk = ImageTk.PhotoImage(sheep_image)
     sheep_image_tk_id = canvas.create_image((canvas_width / 2) - 65, 135, anchor=tk.NW, image=sheep_image_tk)
     canvas.image = sheep_image_tk

     start_game_button = tk.Button(canvas, text = "Start Game", font = ("Calibri", 40), width = 15, command = start_game)
     main_menu_button_list.append(start_game_button)

     load_game_button = tk.Button(canvas, text = "Load Game", font = ("Calibri", 40), width = 15, command = load_game)
     main_menu_button_list.append(load_game_button)

     leaderboard_button = tk.Button(canvas, text = "Leaderboard", font = ("Calibri", 40), width = 15, command = show_leaderboard)
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
    canvas.delete(title_text)
    canvas.delete(sheep_image_tk_id)



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

def show_leaderboard():
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
        leaderboard_text += f"{(i + 1):4}. {name:30} {level:4} {score:18}\n"

    leaderboard_window= tk.Toplevel(window)
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry(f"500x280+{(canvas_width // 2) - 250}+{(canvas_height // 2) - 140}")
    leaderboard_window.grab_set()

    leaderboard_text_widget = tk.Text(leaderboard_window)
    leaderboard_text_widget.pack()

    # Insert the leaderboard_text into the Text widget
    leaderboard_text_widget.insert(tk.END, leaderboard_text)

    
def show_controls_menu():
    controls_menu = tk.Toplevel(window)
    controls_menu.title("Change controls")
    controls_menu.geometry(f"500x280+{(canvas_width // 2) - 250}+{(canvas_height // 2) - 140}")
    controls_menu.grab_set()

    global radio_value
    radio_value = tk.StringVar()

    try:
        controls_rb_value
    except NameError:
        radio_value.set("cursor")
    else:
        radio_value.set(controls_rb_value)

    radio_button1 = tk.Radiobutton(controls_menu, text="Cursor", variable=radio_value, value="cursor", font = ("Calibri", 20), command = set_controls_rb_value)
    radio_button1.pack()

    radio_button2 = tk.Radiobutton(controls_menu, text="Arrow Keys", variable=radio_value, value="arrow", font = ("Calibri", 20), command = set_controls_rb_value)
    radio_button2.pack()

    radio_button3 = tk.Radiobutton(controls_menu, text="W A S D Keys", variable=radio_value, value="wasd", font = ("Calibri", 20), command = set_controls_rb_value)
    radio_button3.pack()

def set_controls_rb_value():
    global controls_rb_value
    controls_rb_value = radio_value.get()


def show_game_over_menu():
    global try_again_button, main_menu_button2

    try_again_button = tk.Button(canvas, text = "Try Again", font = ("Calibri", 40), width = 15, command=lambda: start_game(play_again = True))
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
    player.remove()
    window.unbind("<Motion>")
    canvas.delete(fence)
    canvas.delete(gate)
    

def return_to_main_menu(play_again = False):
    if(play_again):
        hide_game_over_menu()
    global game_over, game_running, game_paused
    game_over = True
    game_running = False
    game_paused = False
    toggle_pause_menu(play_again)
    remove_all_elements()
    show_main_menu()


def save_game():
    sheep_data_list = []
    for sheep in sheep_list:
        if(sheep.is_super):
            sheep_data = sheep.get_centre()
            sheep_data = sheep_data + (1,)
        else:
            sheep_data = sheep.get_centre()
            sheep_data = sheep_data + (0,)
        sheep_data_list.append(sheep_data)

    with open('save.txt', 'w') as file:
        file.write(f"{level} {time_remaining} {score} {gate_position}\n")
        for sheep_data in sheep_data_list:
            sheep_data_string = ""
            for coord in sheep_data:
                sheep_data_string+=str(coord) + " "
            sheep_data_string = sheep_data_string[:-1]
            file.write(f"{sheep_data_string}\n")
    tk.messagebox.showinfo("", "Game Saved") 


def load_game():
    global level, time_remaining, score, gate_position, loaded_sheep_data_list
    loaded_sheep_data_list = []
    with open("save.txt", 'r') as file:
    # Read the first line to get level, score, and time_remaining values
        first_line = file.readline().split()
        level = int(first_line[0])
        time_remaining = int(first_line[1])
        score = int(first_line[2])
        gate_position = int(first_line[3])
    
        for line in file:
            loaded_data_line = [float(value) for value in line.split()]
            loaded_sheep_data_list.append(loaded_data_line)
    start_game(start_loaded_game = True)
            


def on_key_press(event):
    global score_cheat_code_index, time_cheat_code_index, super_sheep_cheat_code_index

    key = event.keysym

    if(key == "Up" or key == "w"):
        player.move(0,-20)
    
    elif(key == "Down" or key =="s"):
        player.move(0,20)

    elif(key == "Left" or key =="a"):
        player.move(-20,0)

    elif(key == "Right" or key =="d"):
        player.move(20,0)

    if(game_running and not game_paused):
        if(key == score_cheat_code[score_cheat_code_index]):
            score_cheat_code_index += 1
        else:
            score_cheat_code_index = 0

        if(key == time_cheat_code[time_cheat_code_index]):
            time_cheat_code_index += 1    
        else:
            time_cheat_code_index = 0

        if(key == super_sheep_cheat_code[super_sheep_cheat_code_index]):
            super_sheep_cheat_code_index += 1    
        else:
            super_sheep_cheat_code_index = 0

        if(key == "b" and not boss_image_showing):
            show_boss_image()
        
    else:
        if(key == "b" and boss_image_showing):
            hide_boss_image()

    if(score_cheat_code_index == len(score_cheat_code)):
        activate_cheat("score")
        score_cheat_code_index = 0
    if(time_cheat_code_index == len(time_cheat_code)):
        activate_cheat("time")
        time_cheat_code_index = 0
    if(super_sheep_cheat_code_index == len(super_sheep_cheat_code)):
        activate_cheat("super_sheep")
        super_sheep_cheat_code_index = 0


def show_boss_image():
    global boss_image_showing, boss_image_tk_id, game_paused
    game_paused = True

    boss_image = Image.open("boss.png")
    boss_image = boss_image.resize((canvas_width, canvas_height))
    boss_image_tk = ImageTk.PhotoImage(boss_image)
    boss_image_tk_id = canvas.create_image(0, 0, anchor=tk.NW, image=boss_image_tk)
    canvas.image = boss_image_tk

    window.unbind("<Escape>")
    boss_image_showing = True


def hide_boss_image():
    global boss_image_showing, game_paused
    game_paused = False
    update_game()

    canvas.delete(boss_image_tk_id)
    window.bind("<Escape>", lambda event: toggle_pause_game())
    boss_image_showing = False


def activate_cheat(cheat):
    global score, time_remaining, sheep_list

    if(cheat == "score"):
        add_to_score(1000)
        update_ui(False, False, True)

    elif(cheat == "time"):
        time_remaining += 15
        update_ui(False, True, False)

    else:
        for i in range(10):
            sheep = Sheep(is_super = True)
            sheep_list.append(sheep)
            x = randint(int(fence_x1 + 30), int(fence_x2 - 30))
            y = randint(int(fence_y1 + 30), int(fence_y2 - 30))
            sheep.place(x, y)


def bind_controls():
    if(controls == "cursor"):
        window.bind("<Motion>", on_mouse_motion)

    elif(controls == "arrow"):
        window.bind("<KeyPress-Left>", on_key_press)
        window.bind("<KeyPress-Right>", on_key_press)
        window.bind("<KeyPress-Up>", on_key_press)
        window.bind("<KeyPress-Down>", on_key_press)

    else:
        window.bind("<KeyPress-w>", on_key_press)
        window.bind("<KeyPress-a>", on_key_press)
        window.bind("<KeyPress-s>", on_key_press)
        window.bind("<KeyPress-d>", on_key_press)


def unbind_other_controls():
    if(controls == "cursor"):
        window.unbind("<KeyPress-Left>")
        window.unbind("<KeyPress-Right>")
        window.unbind("<KeyPress-Up>")
        window.unbind("<KeyPress-Down>")

        window.unbind("<KeyPress-w>")
        window.unbind("<KeyPress-a>")
        window.unbind("<KeyPress-s>")
        window.unbind("<KeyPress-d>")

    elif(controls == "arrow"):
        window.unbind("<Motion>")

        window.unbind("<KeyPress-w>")
        window.unbind("<KeyPress-a>")
        window.unbind("<KeyPress-s>")
        window.unbind("<KeyPress-d>")

    else:
        window.unbind("<Motion>")

        window.unbind("<KeyPress-Left>")
        window.unbind("<KeyPress-Right>")
        window.unbind("<KeyPress-Up>")
        window.unbind("<KeyPress-Down>")



def exit_game():
    window.destroy()

def start_game(play_again = False, start_loaded_game = False):
    global game_running, game_paused, game_over, level, score, controls, player
    game_running = True
    game_paused = False
    game_over = False
    player = Player()

    try:
        controls_rb_value
    except NameError:
        controls = "cursor"
    else:
        controls = controls_rb_value

    if(not start_loaded_game):
        level = 1
        score = 0

    if(play_again):
        remove_all_elements()
        hide_game_over_menu()
    else:
        hide_main_menu()
    
    bind_controls()
    unbind_other_controls()

    # Show player ball if not using cursor control
    if(controls == "arrow" or controls == "wasd"):
        player.hidden_state = "normal"

    player.place(canvas_width / 2, canvas_height / 2)
    start_new_level(start_loaded_game)
    update_timer()
    update_game()


# Create 1920x1080 window with green canvas
window = tk.Tk()
window.geometry("1920x1080")
window.title("Super Sheep Frenzy")
window.attributes("-fullscreen", True)
canvas_width = 1920
canvas_height = 1080
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="green")
canvas.pack()

show_main_menu()

window.bind("<Escape>", lambda event: toggle_pause_game())
window.bind("<KeyPress>", on_key_press)

score_cheat_code = "score"
time_cheat_code = "time"
super_sheep_cheat_code = "supersheep"

score_cheat_code_index = 0
time_cheat_code_index = 0
super_sheep_cheat_code_index = 0

boss_image_showing = False

window.mainloop()