import tkinter as tk
from tkinter import ttk


class GuiHandler:
    def __init__(self, start_callback, exit_callback, start_gui_ready_event, game_gui_ready_event):
        self.root = None
        self.status_frame = None
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
        self.root.geometry("600x450")

        # Status Frame (Red Box)
        self.status_frame = tk.Frame(self.root, bd=2, relief="solid", bg="#FFCCCC")  # Light Red Background
        self.status_frame.pack(pady=10, padx=10, fill="x")

        self.camera_label = tk.Label(self.status_frame, text="Cameras not connected", fg="red", font=("Arial", 12, "bold"),
                                     bg="#FFCCCC")
        self.camera_label.pack(pady=5)

        self.basket_label = tk.Label(self.status_frame, text="Basket not found", fg="red", font=("Arial", 12, "bold"),
                                     bg="#FFCCCC")
        self.basket_label.pack(pady=5)

        # Number of Players Selection
        player_frame = tk.Frame(self.root)
        player_frame.pack(pady=10)

        player_label = tk.Label(player_frame, text="Number of players:", font=("Arial", 12))
        player_label.pack(side="left", padx=5)

        player_var = tk.StringVar(value="1")
        player_dropdown = ttk.Combobox(self.root, textvariable=player_var, state="readonly")
        player_dropdown['values'] = ("1", "2", "3", "4")
        player_dropdown.pack(pady=5)

        def update_players(event):
            self.num_players = int(player_var.get())

        player_dropdown.bind("<<ComboboxSelected>>", update_players)

        # Buttons Frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.start_button = tk.Button(button_frame, text="Start", state=tk.DISABLED, font=("Arial", 12), width=10,
                                      height=1, bg="#6495ED", command=self.start_callback)
        self.start_button.pack(side="left", padx=10)

        exit_button = tk.Button(button_frame, text="Exit", font=("Arial", 12), width=10, height=1, bg="#FF6666",
                                command=self.exit_callback)
        exit_button.pack(side="left")

        self.start_gui_ready_event.set()
        self.root.mainloop()

    def updateBootStrapWindow(self, number):
        if number == 1:
            self.camera_label.config(text="Cameras connected", fg="green",bg="#90EE90")
        elif number == 2:
            self.camera_label.config(text="Cameras not connected", fg="red", bg="#FFCCCC")
        elif number == 3:
            self.basket_label.config(text="Basket found", fg="green", bg="#90EE90")
        elif number == 4:
            self.basket_label.config(text="Basket not found", fg="red", bg="#FFCCCC")

        # Enable the start button only if both messages are green
        if self.camera_label.cget("fg") == "green" and self.basket_label.cget("fg") == "green":
            self.status_frame.config(bg="#90EE90")
            self.start_button.config(state=tk.NORMAL)
        else:
            self.start_button.config(state=tk.DISABLED)

    def CreateGameWindow(self):
        if self.root:
            self.root.destroy()

        self.root = tk.Tk()
        self.root.title("Game Window")
        self.root.geometry("600x450")

        # Player Scores Frame (Blue Box)
        score_frame = tk.Frame(self.root, bd=2, relief="solid", bg="#E0F7FA")  # Light Blue Background
        score_frame.pack(pady=10, padx=10, fill="x")

        self.player_labels = []
        self.player_score = []

        for i in range(1, self.num_players + 1):
            label = tk.Label(score_frame, text=f"Player {i} Score: 0", font=("Arial", 14, "bold"), bg="#E0F7FA")
            label.pack(pady=5)
            self.player_labels.append(label)
            self.player_score.append(0)

        # Prompt Label (Who should play next)
        self.prompt_label = tk.Label(self.root, text="Player 1, Please Throw!", font=("Arial", 14, "bold"), fg="black")
        self.prompt_label.pack(pady=15)

        # Buttons Frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Next Player Button
        next_player_button = tk.Button(button_frame, text="Next Player", font=("Arial", 12, "bold"), width=12, height=1,
                                       bg="#32CD32", fg="white", command=lambda: self.updateGameWindow(0))
        next_player_button.pack(side="left", padx=10)

        # Exit Button
        exit_button = tk.Button(button_frame, text="Exit", font=("Arial", 12, "bold"), width=12, height=1,
                                bg="#FF6666", fg="white", command=self.exit_callback)
        exit_button.pack(side="left")

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
        #self.player_score[self.current_player - 1] += score
        self.updateGameWindow(self.current_player)

    def Exit(self):
        self.root.destroy()