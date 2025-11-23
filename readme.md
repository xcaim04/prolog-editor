# Prolog Editor (Python + SWI-Prolog)

Editor simple con ejecución integrada de consultas Prolog.

## Requisitos
- Python 3.8+
- SWI-Prolog instalado y accesible como `swipl`

## Uso
- `python app.py`
- Escribe código `.pl`, guarda/abre archivos.
- Presiona `Ctrl+Enter` para ejecutar una consulta (sin `?-` ni punto final).
- Ejemplos:
  - `padre(X, Y)`
  - `member(X, [1,2,3])`
  - `(member(5, [1,2,3]))` → salida `false`

## Empaquetar (opcional)
- `pip install pyinstaller`
- `pyinstaller --onefile app.py`
