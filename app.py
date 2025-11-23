import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from components.menu_bar import MenuBar
from components.toolbar import ToolBar
from components.history_panel import HistoryPanel
from components.status_bar import StatusBar
from components.tab_panel import ClosableNotebook
from components.editor_panel import EditorPanel
from components.output_panel import OutputPanel
from prolog_runner import run_query, check_swipl_available
from dialogs import prompt_query

APP_TITLE = "Prolog Editor (Python + SWI-Prolog)"

class PrologEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1100x700")
        self.configure(bg="#21252b")

        # Estado general
        self.last_query = ""
        self.swipl_ok = check_swipl_available()
        self._tab_paths = {}  # Rutas por pestaña (frame -> path)

        # Menú
        self.menu = MenuBar(
            self,
            self._new_file,
            self._open_file,
            self._save_file,
            self._save_as,
            self._ask_and_run,
            self._run_last_query
        )
        self.config(menu=self.menu)

        # Toolbar
        self.toolbar = ToolBar(
            self,
            on_new=self._new_file,
            on_open=self._open_file,
            on_save=self._save_file,
            on_run=self._ask_and_run,
            on_export=self._export_output
        )

        # Layout principal: historial fijo a la izquierda, notebook a la derecha
        main_frame = tk.Frame(self, bg="#21252b")
        main_frame.pack(fill="both", expand=True)

        # Panel de historial a la izquierda
        left_frame = tk.Frame(main_frame, bg="#21252b", width=220)
        left_frame.pack(side="left", fill="y")
        self.history = HistoryPanel(left_frame, on_select=self._run_selected_history)
        self.history.pack(fill="both", expand=True)

        # Notebook a la derecha
        right_frame = tk.Frame(main_frame, bg="#21252b")
        right_frame.pack(side="left", fill="both", expand=True)
        self.notebook = ClosableNotebook(right_frame)
        self.notebook.pack(fill="both", expand=True)

        # Primera pestaña
        editor, output = self.notebook.add_tab("Archivo 1")
        self._focus_last_tab()
        first_frame = self._get_last_frame()
        if first_frame:
            self._tab_paths[first_frame] = None

        # Status bar
        self.status = StatusBar(self)
        self.toolbar.update_status("Listo.")

        # Atajos
        self._bind_shortcuts()

        # Ajuste de tema para visibilidad en Windows
        try:
            from tkinter import ttk
            ttk.Style().theme_use("clam")
        except Exception:
            pass

    # --------- Atajos ----------
    def _bind_shortcuts(self):
        self.bind_all("<Control-o>", lambda e: self._open_file())
        self.bind_all("<Control-s>", lambda e: self._save_file())
        self.bind_all("<Control-Return>", lambda e: self._ask_and_run())
        self.bind_all("<Control-Shift-Return>", lambda e: self._run_last_query())

    # --------- Archivo ----------
    def _new_file(self):
        editor, output = self.notebook.add_tab("Nuevo")
        self._focus_last_tab()
        frame = self._get_last_frame()
        if frame:
            self._tab_paths[frame] = None
        editor.set_code("")
        self._update_status("Nuevo archivo")

    def _open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Prolog", "*.pl"), ("Todos", "*.*")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()
            title = os.path.basename(path)
            editor, output = self.notebook.add_tab(title)
            self._focus_last_tab()
            frame = self._get_last_frame()
            if frame:
                self._tab_paths[frame] = path
            editor.set_code(code)
            self._update_status(f"Abierto: {path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

    def _save_file(self):
        frame = self._get_current_frame()
        if frame is None:
            self._new_file()
            frame = self._get_current_frame()

        editor, _ = self._get_current_tab()
        current_path = self._tab_paths.get(frame)
        if not current_path:
            return self._save_as()

        try:
            with open(current_path, "w", encoding="utf-8") as f:
                f.write(editor.get_code())
            self._update_status(f"Guardado: {current_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

    def _save_as(self):
        frame = self._get_current_frame()
        if frame is None:
            self._new_file()
            frame = self._get_current_frame()

        editor, _ = self._get_current_tab()
        path = filedialog.asksaveasfilename(defaultextension=".pl", filetypes=[("Prolog", "*.pl"), ("Todos", "*.*")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(editor.get_code())
            self._tab_paths[frame] = path
            basename = os.path.basename(path)
            self.notebook.tab(frame, text=basename)
            self._update_status(f"Guardado como: {path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

    # --------- Estado / Salida ----------
    def _update_status(self, msg):
        self.toolbar.update_status(msg)
        self.status.update_status(msg)

    def _export_output(self):
        _, output = self._get_current_tab()
        if output is None:
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Texto", "*.txt")])
        if not path:
            return
        try:
            content = output.text.get("1.0", "end-1c")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            self._update_status(f"Salida exportada a {path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar la salida:\n{e}")

    # --------- Consultas ----------
    def _ask_and_run(self):
        q = prompt_query(self, "Consulta Prolog", "Escribe la consulta, sin ?- (ej: member(X,[1,2,3])):", initial=self.last_query)
        if q:
            self.last_query = q.strip()
            self._run_query_async(self.last_query)

    def _run_last_query(self):
        if self.last_query:
            self._run_query_async(self.last_query)

    def _run_selected_history(self):
        selected = self.history.get_selected()
        if selected:
            self._run_query_async(selected)

    def _run_query_async(self, query):
        editor, output = self._get_current_tab()
        if editor is None or output is None:
            self._new_file()
            editor, output = self._get_current_tab()

        code = editor.get_code()
        if not self.swipl_ok:
            output.write("SWI-Prolog (swipl) no está disponible.\nInstálalo para ejecutar consultas.\n")
            self._update_status("swipl no disponible")
            return

        self._update_status("Ejecutando...")
        output.write(f"> {query}\n")

        # Guardar en historial
        self.history.add_query(query)

        def worker():
            out = run_query(code, query, timeout=8)
            self.after(0, lambda: self._on_run_done(out, output))

        threading.Thread(target=worker, daemon=True).start()

    def _on_run_done(self, result_text, output):
        if result_text:
            if not result_text.endswith("\n"):
                result_text += "\n"
            output.write(result_text)
        else:
            output.write("(sin salida)\n")
        self._update_status("Hecho.")

    # --------- Helpers ----------
    def _get_current_frame(self):
        sel = self.notebook.select()
        if not sel:
            return None
        return self.notebook.nametowidget(sel)

    def _get_last_frame(self):
        tabs = self.notebook.tabs()
        if not tabs:
            return None
        return self.notebook.nametowidget(tabs[-1])

    def _get_current_tab(self):
        frame = self._get_current_frame()
        if frame is None:
            return None, None
        editor = None
        output = None
        for child in frame.winfo_children():
            if isinstance(child, EditorPanel):
                editor = child
            elif isinstance(child, OutputPanel):
                output = child
        return editor, output

    def _focus_last_tab(self):
        """Selecciona la última pestaña del notebook si existe."""
        tabs = self.notebook.tabs()
        if tabs:
            self.notebook.select(tabs[-1])

                
if __name__ == "__main__":
    # Ajuste para pantallas HiDPI en Windows (opcional)
    if sys.platform.startswith("win"):
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    PrologEditor().mainloop()
