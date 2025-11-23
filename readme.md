# 🧠 Prolog Editor (Python + SWI-Prolog)

Un editor gráfico hecho en **Python + Tkinter** para escribir, ejecutar y aprender Prolog de manera sencilla.  
Incluye historial de consultas, pestañas cerrables, barra de estado y exportación de resultados.  
Pensado para estudiantes, docentes y curiosos que quieran experimentar con lógica declarativa.

---

## 🚀 Características

- ✍️ **Editor de código** con soporte para múltiples pestañas.
- 📜 **Historial de consultas**: guarda y reutiliza tus queries.
- ⚡ **Integración con SWI-Prolog**: ejecuta consultas directamente desde el editor.
- 🗂️ **Abrir/guardar archivos `.pl`** fácilmente.
- 🖱️ **Cerrar pestañas con clic derecho**.
- 📤 **Exportar salida** a `.txt`.
- 🎨 **Interfaz oscura** estilo moderno.

---

## 📦 Instalación

1. Clona este repositorio:

```bash
   git clone https://github.com/xcaim04/prolog-editor.git
   cd prolog-editor
```

## Instala depencias

```bash
pip install -r requirements.txt
```

### Asegurate de tener swipl en el path

```bash
swipl --version
```

## Uso

```bash
python app.py
```

## Atajos de teclado

* Ctrl+O → Abrir archivo

* Ctrl+S → Guardar archivo

* Ctrl+Enter → Ejecutar consulta

* Ctrl+Shift+Enter → Ejecutar última consulta

## Genera el .exe

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --name PrologEditor app.py
```

Nota: En las consultas no terminan en `.` para poder ejecutarlas.