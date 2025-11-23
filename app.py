import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from components.menu_bar import MenuBar
from components.toolbar import ToolBar
from components.history_panel import HistoryPanel
from components.editor_panel import EditorPanel
from components.output_panel import OutputPanel
from components.status_bar import StatusBar
from prolog_runner import run_query, check_swipl_available
from dialogs import prompt_query

APP_TITLE = "Prolog Editor (Python + SWI-Prolog)"

class PrologEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1100x700")
        self.configure(bg="#21252b")

        self.current_path = None
        self.last_query = "member(X,[1,2,3])"
        self.swipl_ok = check_swipl_available()

        # Menu
        self.menu = MenuBar(self, self._new_file, self._open_file, self._save_file,
                            self._save_as, self._ask_and_run, self._run_last_query)
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

        # Layout principal (historial | editor+salida)
        paned = tk.PanedWindow(self, orient="horizontal", bg="#21252b")
        paned.pack(fill="both", expand=True)

        self.history = HistoryPanel(paned, on_select=self._run_selected_history)
        paned.add(self.history)

        main_paned = tk.PanedWindow(paned, orient="vertical", bg="#21252b")
        paned.add(main_paned)

        self.editor = EditorPanel(main_paned)
        main_paned.add(self.editor)

        self.output = OutputPanel(main_paned)
        main_paned.add(self.output)

        # Status bar
        self.status = StatusBar(self)
        self.toolbar.update_status("Listo.")

        # Atajos
        self._bind_shortcuts()

    # --------- Atajos ----------
    def _bind_shortcuts(self):
        self.bind_all("<Control-o>", lambda e: self._open_file())
        self.bind_all("<Control-s>", lambda e: self._save_file())
        self.bind_all("<Control-Return>", lambda e: self._ask_and_run())
        self.bind_all("<Control-Shift-Return>", lambda e: self._run_last_query())

    # --------- Archivo ----------
    def _new_file(self):
        self.editor.set_code("")
        self.current_path = None
        self._update_status("Nuevo archivo")

    def _open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Prolog", "*.pl"), ("Todos", "*.*")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.editor.set_code(f.read())
            self.current_path = path
            self._update_status(f"Abierto: {path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

    def _save_file(self):
        if not self.current_path:
            return self._save_as()
        try:
            with open(self.current_path, "w", encoding="utf-8") as f:
                f.write(self.editor.get_code())
            self._update_status(f"Guardado: {self.current_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

    def _save_as(self):
        path = filedialog.asksaveasfilename(defaultextension=".pl", filetypes=[("Prolog", "*.pl"), ("Todos", "*.*")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.editor.get_code())
            self.current_path = path
            self._update_status(f"Guardado como: {path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

    # --------- Estado / Salida ----------
    def _update_status(self, msg):
        self.toolbar.update_status(msg)
        self.status.update_status(msg)

    def _export_output(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Texto", "*.txt")])
        if not path:
            return
        try:
            content = self.output.text.get("1.0", "end-1c")
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
        code = self.editor.get_code()
        if not self.swipl_ok:
            self.output.write("SWI-Prolog (swipl) no está disponible.\nInstálalo para ejecutar consultas.\n")
            self._update_status("swipl no disponible")
            return

        self._update_status("Ejecutando...")
        self.output.write(f"> {query}\n")

        # Guardar en historial
        self.history.add_query(query)

        def worker():
            out = run_query(code, query, timeout=8)
            self.after(0, lambda: self._on_run_done(out))

        threading.Thread(target=worker, daemon=True).start()

    def _on_run_done(self, result_text):
        if result_text:
            if not result_text.endswith("\n"):
                result_text += "\n"
            self.output.write(result_text)
        else:
            self.output.write("(sin salida)\n")
        self._update_status("Hecho.")

if __name__ == "__main__":
    # Ajuste para pantallas HiDPI en Windows (opcional)
    if sys.platform.startswith("win"):
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    PrologEditor().mainloop()
