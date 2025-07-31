import itertools
import re
from tkinter import messagebox
from funciones_logicas import procesar_expresion, evaluar, obtener_subexpresiones

def normalizar(expr):
    return expr.replace("[", "(").replace("]", ")").replace("{", "(").replace("}", ")")

def extraer_variables(expr):
    expr = normalizar(expr)
    return sorted(set(re.findall(r'\b[a-z]\b', expr)))

def filtrar_subexpresiones(subexpresiones, variables):
    variables_set = set(variables)
    resultado = []

    for texto, arbol in subexpresiones:
        # Excluir negaciones simples (¬p)
        if arbol[0] == 'not' and arbol[1][0] == 'var':
            continue
        # Variables simples las dejamos
        if texto in variables_set:
            resultado.append((texto, arbol))
            continue
        # Expresiones compuestas las dejamos
        if arbol[0] in ('and', 'or', 'implica', 'equivale'):
            resultado.append((texto, arbol))

    return resultado

def generar_tabla(expresion, tree):
    expr_limpia = normalizar(expresion)

    try:
        arbol_principal = procesar_expresion(expr_limpia)
        subexpresiones = obtener_subexpresiones(arbol_principal)
    except Exception as e:
        messagebox.showerror("Error al procesar expresión", str(e))
        return

    variables = extraer_variables(expr_limpia)
    if len(variables) > 10:
        messagebox.showerror("Error", "Máximo 10 variables permitidas.")
        return

    combinaciones = list(itertools.product([0, 1], repeat=len(variables)))

    subexpresiones_filtradas = filtrar_subexpresiones(subexpresiones, variables)

    # Separar variables y subexpresiones compuestas para ordenar
    solo_vars = set(variables)
    subexpr_solas = []
    subexpr_compuestas = []

    for texto, arbol in subexpresiones_filtradas:
        if texto in solo_vars:
            subexpr_solas.append((texto, arbol))
        else:
            subexpr_compuestas.append((texto, arbol))

    # Ordenamos: primero variables, luego expresiones compuestas
    subexpresiones_ordenadas = subexpr_solas + subexpr_compuestas

    # ¡Aquí la clave! columnas y filas usan exactamente este mismo orden
    columnas = [texto for texto, _ in subexpresiones_ordenadas]

    # Limpiar tabla
    for i in tree.get_children():
        tree.delete(i)

    tree["columns"] = columnas
    tree["show"] = "headings"

    for c in columnas:
        tree.heading(c, text=c)
        tree.column(c, width=120, anchor="center")

    for valores in combinaciones:
        contexto = dict(zip(variables, valores))
        fila = []
        try:
            for _, arbol in subexpresiones_ordenadas:
                val = evaluar(arbol, contexto)
                fila.append(val)
        except Exception as e:
            messagebox.showerror("Error al evaluar expresión", str(e))
            return
        tree.insert("", "end", values=fila)
