import tkinter as tk
from tkinter import messagebox

APP_TITLE = "Prolog Editor (Python + SWI-Prolog)"

class MenuBar(tk.Menu):
    def __init__(self, master, on_new, on_open, on_save, on_save_as, on_run, on_run_last):
        super().__init__(master)

        filem = tk.Menu(self, tearoff=0)
        filem.add_command(label="Nuevo", command=on_new)
        filem.add_command(label="Abrir...", command=on_open, accelerator="Ctrl+O")
        filem.add_command(label="Guardar", command=on_save, accelerator="Ctrl+S")
        filem.add_command(label="Guardar como...", command=on_save_as)
        filem.add_separator()
        filem.add_command(label="Salir", command=master.destroy)
        self.add_cascade(label="Archivo", menu=filem)

        runm = tk.Menu(self, tearoff=0)
        runm.add_command(label="Ejecutar consulta...", command=on_run, accelerator="Ctrl+Enter")
        runm.add_command(label="Ejecutar última consulta", command=on_run_last, accelerator="Ctrl+Shift+Enter")
        self.add_cascade(label="Prolog", menu=runm)

        helpm = tk.Menu(self, tearoff=0)
        helpm.add_command(label="Acerca de", command=lambda: messagebox.showinfo(APP_TITLE,
            "Editor de Prolog en Python\nEjecución integrada con SWI-Prolog.\nCtrl+Enter: ejecutar consulta."))
        self.add_cascade(label="Ayuda", menu=helpm)
