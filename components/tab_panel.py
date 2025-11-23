import tkinter as tk
from tkinter import ttk
from components.editor_panel import EditorPanel
from components.output_panel import OutputPanel

class ClosableNotebook(ttk.Notebook):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Forzar tema que permite colores personalizados
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("TNotebook", background="#21252b")
        style.configure(
            "TNotebook.Tab",
            background="#3a3f4b",
            foreground="white",
            padding=(12, 6)  # más aire para que el texto no “desaparezca”
        )
        style.map("TNotebook.Tab",
                  background=[("selected", "#4a5060")],
                  foreground=[("selected", "white")])

        # Cerrar pestaña con clic derecho sobre la pestaña
        self.bind("<Button-3>", self._on_right_click)

    def add_tab(self, title="Nuevo"):
        frame = tk.Frame(self, bg="#21252b")
        # Layout interno de la pestaña
        editor = EditorPanel(frame)
        editor.pack(side="top", fill="both", expand=True)
        output = OutputPanel(frame)
        output.pack(side="bottom", fill="x")

        # Añadir la pestaña con texto (sin imágenes ni emojis)
        self.add(frame, text=title)
        # Asegurar que el Notebook se vea
        self.pack(fill="both", expand=True)
        return editor, output

    def _on_right_click(self, event):
        try:
            idx = self.index("@%d,%d" % (event.x, event.y))
            self.forget(idx)
        except Exception:
            pass
