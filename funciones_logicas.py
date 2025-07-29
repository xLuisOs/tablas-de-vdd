import re

def implica(a, b):
    return int((not a) or b)

def equivale(a, b):
    return int(a == b)

def procesar_expresion(expresion):
    expresion = expresion.replace("[", "(").replace("]", ")")
    expresion = expresion.replace("{", "(").replace("}", ")")
    expresion = expresion.replace('¬', 'not ')
    expresion = expresion.replace('∧', 'and')
    expresion = expresion.replace('∨', 'or')

    while '→' in expresion:
        expresion = re.sub(r'(\([^()]+\)|\b[a-z]\b)\s*→\s*(\([^()]+\)|\b[a-z]\b)', r'implica(\1, \2)', expresion)

    while '↔' in expresion:
        expresion = re.sub(r'(\([^()]+\)|\b[a-z]\b)\s*↔\s*(\([^()]+\)|\b[a-z]\b)', r'equivale(\1, \2)', expresion)

    return expresion