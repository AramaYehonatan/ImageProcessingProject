import tkinter as tk
from tkinter import ttk


class GuiHandler:
    def __init__(self, start_callback, exit_callback):
        self.root = None
        self.camera_label = None
        self.basket_label = None
        self.start_button = None
        self.start_callback = start_callback
        self.exit_callback = exit_callback

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

    def Exit(self):
        self.root.destroy()