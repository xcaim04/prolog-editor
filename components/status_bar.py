import tkinter as tk

class StatusBar(tk.Label):
    def __init__(self, master):
        super().__init__(master, text="...", anchor="w", bg="#21252b", fg="#98c379")
        self.pack(side="bottom", fill="x")

    def update_status(self, msg):
        self.config(text=msg)
