import re

# Patrones simples para resaltado
RE_KEYWORD = re.compile(r":-|\?-")
RE_COMMENT_LINE = re.compile(r"%.*$")
RE_FUNCTOR = re.compile(r"\b[a-z][A-Za-z0-9_]*\s*\(")
RE_VAR = re.compile(r"\b[A-Z_][A-Za-z0-9_]*\b")

def apply_highlight(text_widget):
    """
    Resalta sintaxis básica: keywords, comentarios, functors y variables.
    Este resaltado es aproximado y eficiente para uso didáctico.
    """
    for tag in ("keyword", "comment", "functor", "var"):
        text_widget.tag_remove(tag, "1.0", "end")

    content = text_widget.get("1.0", "end-1c")
    lines = content.splitlines()

    index = 1
    for line in lines:
        # Comentario de línea
        m = RE_COMMENT_LINE.search(line)
        if m:
            start = f"{index}.{m.start()}"
            end = f"{index}.{len(line)}"
            text_widget.tag_add("comment", start, end)
            index += 1
            continue

        # Keywords (:- y ?-)
        for m in RE_KEYWORD.finditer(line):
            start = f"{index}.{m.start()}"
            end = f"{index}.{m.end()}"
            text_widget.tag_add("keyword", start, end)

        # Functor (nombre en minúscula seguido de '(')
        for m in RE_FUNCTOR.finditer(line):
            start = f"{index}.{m.start()}"
            end = f"{index}.{m.start() + m.group(0).find('(')}"
            text_widget.tag_add("functor", start, end)

        # Variables (inician en mayúscula o _)
        for m in RE_VAR.finditer(line):
            start = f"{index}.{m.start()}"
            end = f"{index}.{m.end()}"
            text_widget.tag_add("var", start, end)

        index += 1
