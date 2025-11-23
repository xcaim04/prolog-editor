import os
import shutil
import subprocess
import tempfile

def check_swipl_available():
    return shutil.which("swipl") is not None

def _quote_prolog_atom(s: str) -> str:
    """
    Devuelve s como átomo Prolog entre comillas simples,
    escapando comillas simples internas.
    """
    return "'" + s.replace("'", "\\'") + "'"

def run_query(source_text: str, query: str, timeout: int = 8) -> str:
    swipl = shutil.which("swipl")
    if not swipl:
        return "Error: SWI-Prolog (swipl) no encontrado en PATH."

    q = query.strip()
    # Limpieza mínima de prefijos/sufijos usuales del usuario
    if q.startswith("?-"):
        q = q[2:].strip()
    if q.endswith("."):
        q = q[:-1].strip()

    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "temp.pl")
        # Escribimos el código del usuario y nuestros helpers
        with open(path, "w", encoding="utf-8") as f:
            f.write(source_text)
            f.write("""

% Helpers para ejecutar consultas y mostrar sustituciones claras
print_var_bindings([]).
print_var_bindings([Name=Var|Rest]) :-
    write(Name), write(' = '), writeq(Var), nl,
    print_var_bindings(Rest).

run_query_atom(Atom) :-
    % Parseamos el término desde texto, preservando nombres de variables
    read_term_from_atom(Atom, Term, [variable_names(Vars)]),
    ( Vars == [] ->
        % Consulta cerrada: true/false
        ( call(Term) -> writeln(true) ; writeln(false) )
    ;
        % Consulta con variables: imprimir todas las soluciones
        forall(call(Term), (print_var_bindings(Vars), nl))
    ).
""")

        atom = _quote_prolog_atom(q)
        goal = f"run_query_atom({atom})"

        cmd = [swipl, "-q", "-f", "none", "-s", path, "-g", goal, "-t", "halt"]

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return "Error: tiempo de ejecución excedido."
        except Exception as e:
            return f"Error al ejecutar swipl: {e}"

        stdout = res.stdout.strip()
        stderr = res.stderr.strip()

        if res.returncode != 0:
            return f"Error de Prolog:\n{stderr or '(código de salida ' + str(res.returncode) + ')'}"

        return stdout or "(sin salida)"
