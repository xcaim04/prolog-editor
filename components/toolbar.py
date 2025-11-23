import tkinter as tk

class ToolBar(tk.Frame):
    def __init__(self, master, on_new, on_open, on_save, on_run, on_export):
        super().__init__(master, bg="#21252b")
        self.pack(side="top", fill="x")

        btn_style = {"bg": "#3a3f4b", "fg": "white",
                     "activebackground": "#61afef", "activeforeground": "black"}

        tk.Button(self, text="📄 Nuevo", command=on_new, **btn_style).pack(side="left", padx=4, pady=4)
        tk.Button(self, text="📂 Abrir", command=on_open, **btn_style).pack(side="left", padx=4, pady=4)
        tk.Button(self, text="💾 Guardar", command=on_save, **btn_style).pack(side="left", padx=4, pady=4)
        tk.Button(self, text="▶ Ejecutar", command=on_run, **btn_style).pack(side="left", padx=8, pady=4)
        tk.Button(self, text="📤 Exportar salida", command=on_export, **btn_style).pack(side="left", padx=4, pady=4)

        self.status = tk.Label(self, text="...", anchor="w", bg="#21252b", fg="#98c379")
        self.status.pack(side="right", padx=8)

    def update_status(self, msg):
        self.status.config(text=msg)
