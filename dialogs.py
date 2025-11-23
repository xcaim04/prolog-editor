import tkinter as tk

def prompt_query(root, title: str, prompt: str, initial: str = ""):
    """
    Diálogo modal para pedir la consulta Prolog.
    Retorna el string o None si se cancela.
    """
    win = tk.Toplevel(root)
    win.title(title)
    win.transient(root)
    win.grab_set()

    tk.Label(win, text=prompt, anchor="w").pack(padx=10, pady=(10, 4), fill="x")
    entry = tk.Entry(win, width=80)
    entry.insert(0, initial or "")
    entry.pack(padx=10, pady=(0, 10), fill="x")
    entry.focus_set()

    res = {"val": None}

    def ok():
        res["val"] = entry.get().strip()
        win.destroy()

    def cancel():
        res["val"] = None
        win.destroy()

    btns = tk.Frame(win)
    btns.pack(pady=8)
    tk.Button(btns, text="Aceptar", command=ok).pack(side="left", padx=6)
    tk.Button(btns, text="Cancelar", command=cancel).pack(side="left", padx=6)

    root.wait_window(win)
    return res["val"]
