import tkinter as tk
from syntax import apply_highlight

DEFAULT_FONT = ("Consolas", 13)

class EditorPanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#21252b")
        self.text = tk.Text(self, font=DEFAULT_FONT, undo=True, wrap="none",
                            bg="#282c34", fg="white", insertbackground="white")
        self.text.pack(side="left", fill="both", expand=True)

        scroll_y = tk.Scrollbar(self, command=self.text.yview)
        scroll_y.pack(side="right", fill="y")
        self.text.configure(yscrollcommand=scroll_y.set)

        self.text.bind("<KeyRelease>", lambda e: apply_highlight(self.text))

    def get_code(self):
        return self.text.get("1.0", "end-1c")

    def set_code(self, code):
        self.text.delete("1.0", "end")
        self.text.insert("1.0", code)
        apply_highlight(self.text)
