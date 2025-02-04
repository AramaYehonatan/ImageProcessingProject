import tkinter as tk
from tkinter import ttk


class GuiHandler:
    def __init__(self, start_callback, exit_callback, start_gui_ready_event, game_gui_ready_event):
        self.root = None
        self.camera_label = None
        self.basket_label = None
        self.start_button = None
        self.prompt_label = None
        self.start_callback = start_callback
        self.exit_callback = exit_callback
        self.player_labels = []
        self.player_score = []
        self.start_gui_ready_event = start_gui_ready_event
        self.game_gui_ready_event = game_gui_ready_event
        self.num_players = 1
        self.current_player = 1

    def CreateStartWindow(self):
        self.root = tk.Tk()
        self.root.title("Bootstrap Window")

        # Camera and Basket Status Messages
        self.camera_label = tk.Label(self.root, text="Cameras not connected", fg="red", font=("Arial", 12))
        self.camera_label.pack(pady=5)

        self.basket_label = tk.Label(self.root, text="Basket not found", fg="red", font=("Arial", 12))
        self.basket_label.pack(pady=5)

        # Start Button (Disabled)
        self.start_button = tk.Button(self.root, text="Start", state=tk.DISABLED, command=self.start_callback)
        self.start_button.pack(pady=10)

        # Exit Button
        exit_button = tk.Button(self.root, text="Exit", command=self.exit_callback)
        exit_button.pack(pady=5)

        # Number of Players Selection
        player_label = tk.Label(self.root, text="Number of players:")
        player_label.pack()

        player_var = tk.StringVar(value="1")
        player_dropdown = ttk.Combobox(self.root, textvariable=player_var, state="readonly")
        player_dropdown['values'] = ("1", "2", "3", "4")
        player_dropdown.pack(pady=5)

        def update_players(event):
            self.num_players = int(player_var.get())

        player_dropdown.bind("<<ComboboxSelected>>", update_players)

        self.start_gui_ready_event.set()
        self.root.mainloop()

    def updateBootStrapWindow(self, number):
        if number == 1:
            self.camera_label.config(text="Cameras connected", fg="green")
        elif number == 2:
            self.camera_label.config(text="Cameras not connected", fg="red")
        elif number == 3:
            self.basket_label.config(text="Basket found", fg="green")
        elif number == 4:
            self.basket_label.config(text="Basket not found", fg="red")

        # Enable the start button only if both messages are green
        if self.camera_label.cget("fg") == "green" and self.basket_label.cget("fg") == "green":
            self.start_button.config(state=tk.NORMAL)
        else:
            self.start_button.config(state=tk.DISABLED)

    def CreateGameWindow(self):
        if self.root:
            self.root.destroy()

        self.root = tk.Tk()
        self.root.title("Game Window")

        for i in range(1, self.num_players + 1):
            label = tk.Label(self.root, text=f"Player {i} Score: 0", font=("Arial", 12))
            label.pack(pady=2)
            self.player_labels.append(label)
            self.player_score.append(0)

        # Message prompting a player to start playing
        self.prompt_label = tk.Label(self.root, text="Player 1, Please Throw!", font=("Arial", 12, "bold"))
        self.prompt_label.pack(pady=10)

        # Exit Button
        exit_button = tk.Button(self.root, text="Exit", command=self.exit_callback)
        exit_button.pack(pady=5)

        next_player_button = tk.Button(self.root, text="Next Player", command=lambda: self.updateGameWindow(0))
        next_player_button.pack(pady=10)
        self.game_gui_ready_event.set()

        self.root.mainloop()

#in this function the number represent the player number (1-4). and 0 represents prompt next player.
    def updateGameWindow(self, number):
        if number == 0:
            self.current_player = (self.current_player % self.num_players) + 1
            self.prompt_label.config(text=f"Player {self.current_player}, Please Throw!")
        else :
            self.player_labels[number - 1].config(text=f"Player {number} Score: {self.player_score[number - 1]}")


    def UpdateScore(self, score):
        self.player_score[self.current_player - 1] += score
        self.updateGameWindow(self.current_player)

    def Exit(self):
        self.root.destroy()