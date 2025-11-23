import tkinter as tk

class OutputPanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#21252b")
        tk.Label(self, text="Salida de Prolog:", anchor="w", bg="#21252b", fg="white").pack(side="top", fill="x")
        self.text = tk.Text(self, font=("Consolas", 12), height=12,
                            state="disabled", bg="#f0f0f0", fg="black", relief="solid", borderwidth=1)
        self.text.pack(side="left", fill="both", expand=True)

        out_scroll_y = tk.Scrollbar(self, command=self.text.yview)
        out_scroll_y.pack(side="right", fill="y")
        self.text.configure(yscrollcommand=out_scroll_y.set)

    def write(self, content):
        self.text.configure(state="normal")
        self.text.insert("end", content)
        self.text.see("end")
        self.text.configure(state="disabled")

    def clear(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")
