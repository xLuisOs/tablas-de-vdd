import itertools
import re
from tkinter import messagebox
from funciones_logicas import implica, equivale, procesar_expresion

def extraer_subexpresiones_anidadas(expresion):
    expr = expresion.replace("[", "(").replace("]", ")").replace("{", "(").replace("}", ")")
    subexpresiones = set()

    def extraer(expr):
        stack = []
        res = []
        for i, c in enumerate(expr):
            if c == '(':
                stack.append(i)
            elif c == ')' and stack:
                start = stack.pop()
                sub = expr[start:i+1]
                res.append(sub)
        return res

    todas = extraer(expr)

    for s in todas:
        subexpresiones.add(s)

    variables = set(re.findall(r'\b[a-z]\b', expr))
    for v in variables:
        neg = f'¬{v}'
        if neg in expresion:
            subexpresiones.add(neg)

    return sorted(subexpresiones, key=lambda x: len(x))

def generar_tabla(expresion, tree):
    expresion_original = expresion
    expr = expresion.replace("[", "(").replace("]", ")").replace("{", "(").replace("}", ")")
    expresion_procesada = procesar_expresion(expr)

    variables = sorted(set(re.findall(r'\b[a-z]\b', expr)))
    if len(variables) > 10:
        messagebox.showerror("Error", "Máximo 10 variables permitidas.")
        return

    combinaciones = list(itertools.product([0, 1], repeat=len(variables)))
    subexpresiones = extraer_subexpresiones_anidadas(expresion_original)

    columnas_extra = []
    agregados = set()
    for s in subexpresiones:
        if s not in agregados:
            columnas_extra.append((s, procesar_expresion(s)))
            agregados.add(s)

    if expresion_original not in agregados:
        columnas_extra.append((expresion_original, expresion_procesada))

    for i in tree.get_children():
        tree.delete(i)

    columnas = variables + [c[0] for c in columnas_extra]
    tree["columns"] = columnas
    tree["show"] = "headings"

    for c in columnas:
        tree.heading(c, text=c)
        tree.column(c, width=120, anchor="center")

    for valores in combinaciones:
        contexto = dict(zip(variables, valores))
        fila = list(valores)
        try:
            for _, expr_proc in columnas_extra:
                val = eval(expr_proc, {"implica": implica, "equivale": equivale}, contexto)
                fila.append(int(bool(val)))
        except Exception as e:
            messagebox.showerror("Error al evaluar la expresión:", str(e))
            return
        tree.insert("", "end", values=fila)
