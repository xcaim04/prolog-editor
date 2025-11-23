import tkinter as tk

class HistoryPanel(tk.Frame):
    def __init__(self, master, on_select):
        super().__init__(master, bg="#21252b", width=200)
        tk.Label(self, text="Historial de consultas:", bg="#21252b", fg="white").pack(anchor="w")
        self.listbox = tk.Listbox(self, bg="#3a3f4b", fg="white", font=("Consolas", 11))
        self.listbox.pack(fill="both", expand=True)
        self.listbox.bind("<Double-Button-1>", lambda e: on_select())

    def add_query(self, query):
        if query not in self.listbox.get(0, "end"):
            self.listbox.insert("end", query)

    def get_selected(self):
        sel = self.listbox.curselection()
        if sel:
            return self.listbox.get(sel[0])
        return None
