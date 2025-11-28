import tkinter as tk
from syntax import apply_highlight

DEFAULT_FONT = ("Consolas", 13)

# Diccionario de completado: predicados de listas y formas típicas
PROLOG_COMPLETIONS = {
    # Búsqueda y pertenencia
    "member": "member(X, List)",
    "memberchk": "memberchk(X, List)",
    "select": "select(Elem, List, Rest)",
    "selectchk": "selectchk(Elem, List, Rest)",
    "nth0": "nth0(Index, List, Elem)",
    "nth1": "nth1(Index, List, Elem)",
    "last": "last(List, Elem)",

    # Concatenación y división
    "append": "append(List1, List2, Result)",
    "prefix": "prefix(Prefix, List)",
    "suffix": "suffix(Suffix, List)",
    "sublist": "sublist(Sub, List)",

    # Longitud y estructura
    "length": "length(List, Len)",
    "same_length": "same_length(List1, List2)",

    # Transformaciones
    "reverse": "reverse(List, Rev)",
    "flatten": "flatten(Nested, Flat)",
    "maplist": "maplist(Pred, List)",
    "foldl": "foldl(Pred, List, Acc0, Acc)",
    "foldr": "foldr(Pred, List, Acc0, Acc)",

    # Ordenación y conjuntos
    "sort": "sort(List, Sorted)",
    "msort": "msort(List, Sorted)",
    "keysort": "keysort(Pairs, Sorted)",
    "list_to_set": "list_to_set(List, Set)",
    "intersection": "intersection(List1, List2, Inter)",
    "union": "union(List1, List2, Union)",
    "subtract": "subtract(List, Remove, Result)",

    # Operaciones avanzadas
    "nextto": "nextto(X, Y, List)",
    "permutation": "permutation(List, Perm)",
    "exclude": "exclude(Pred, List, Result)",
    "include": "include(Pred, List, Result)",

    # Otros básicos
    "true": "true",
    "fail": "fail",
    "consult": "consult('file.pl')",
    "assert": "assert(Fact)",
    "retract": "retract(Fact)",
    "write": "write(Term)",
    "read": "read(Term)",
    "nl": "nl",
    "is": "Var is Expr",
    "=:=": "Expr1 =:= Expr2",
    "=/=": "Expr1 =/= Expr2",
    "<": "Expr1 < Expr2",
    ">": "Expr1 > Expr2",
    "=<": "Expr1 =< Expr2",
    ">=": "Expr1 >= Expr2"
}


class EditorPanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#21252b")
        self.text = tk.Text(self, font=DEFAULT_FONT, undo=True, wrap="none",
                            bg="#282c34", fg="white", insertbackground="white")
        self.text.pack(side="left", fill="both", expand=True)

        scroll_y = tk.Scrollbar(self, command=self.text.yview)
        scroll_y.pack(side="right", fill="y")
        self.text.configure(yscrollcommand=scroll_y.set)

        # Caja de sugerencias
        self.suggestion_box = tk.Listbox(self, height=6, bg="#333", fg="#fff")
        self.suggestion_box.bind("<<ListboxSelect>>", self.insert_suggestion)

        # Eventos
        self.text.bind("<KeyRelease>", self.on_key_release)
        self.text.bind("<KeyPress>", self.auto_close_pairs)

    # ---------- Autocierre de pares ----------
    def auto_close_pairs(self, event):
        pairs = {"(": ")", "[": "]", "{": "}", "\"": "\"", "'": "'"}
        if event.char in pairs:
            self.text.insert(tk.INSERT, event.char + pairs[event.char])
            # mover cursor una posición atrás para quedar en medio
            self.text.mark_set(tk.INSERT, f"{self.text.index(tk.INSERT)} -1c")
            return "break"

    # ---------- Autocompletado ----------
    def on_key_release(self, event):
        apply_highlight(self.text)

        cursor_pos = self.text.index(tk.INSERT)
        line = self.text.get(f"{cursor_pos} linestart", cursor_pos)
        word = line.split()[-1] if line.split() else ""

        matches = [kw for kw in PROLOG_COMPLETIONS.keys() if kw.startswith(word)]

        if matches and word:
            self.show_suggestions(matches)
        else:
            self.suggestion_box.place_forget()

    def show_suggestions(self, matches):
        self.suggestion_box.delete(0, tk.END)
        for m in matches:
            self.suggestion_box.insert(tk.END, m)
        try:
            x, y, _, _ = self.text.bbox(tk.INSERT)
            self.suggestion_box.place(x=x, y=y+20)
        except Exception:
            pass

    def insert_suggestion(self, event):
        selection = self.suggestion_box.get(tk.ACTIVE)
        self.suggestion_box.place_forget()

        cursor_pos = self.text.index(tk.INSERT)
        line_start = f"{cursor_pos} linestart"
        line = self.text.get(line_start, cursor_pos)
        words = line.split()
        if words:
            self.text.delete(f"{cursor_pos} - {len(words[-1])}c", cursor_pos)

        if selection in PROLOG_COMPLETIONS:
            self.text.insert(tk.INSERT, PROLOG_COMPLETIONS[selection])
        else:
            self.text.insert(tk.INSERT, selection)

    # ---------- Helpers ----------
    def get_code(self):
        return self.text.get("1.0", "end-1c")

    def set_code(self, code):
        self.text.delete("1.0", "end")
        self.text.insert("1.0", code)
        apply_highlight(self.text)
