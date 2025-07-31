import re

def implica(a, b):
    return int((not a) or b)

def equivale(a, b):
    return int(a == b)

def tokenize(expr):
    token_spec = [
        ('NOT',      r'¬'),
        ('AND',      r'∧'),
        ('OR',       r'∨'),
        ('IMP',      r'→'),
        ('EQ',       r'↔'),
        ('LPAREN',   r'\('),
        ('RPAREN',   r'\)'),
        ('VAR',      r'[a-z]'),
        ('SKIP',     r'\s+'),
        ('MISMATCH', r'.'),  
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_spec)
    for mo in re.finditer(tok_regex, expr):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise ValueError(f"Carácter inválido {value} en expresión.")
        else:
            yield (kind, value)

class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return (None, None)

    def consume(self, expected_kind=None):
        if self.pos < len(self.tokens):
            tok = self.tokens[self.pos]
            if expected_kind and tok[0] != expected_kind:
                raise ValueError(f"Se esperaba {expected_kind} pero se encontró {tok[0]}")
            self.pos +=1
            return tok
        raise ValueError("No hay más tokens")

    def parse(self):
        result = self.parse_equivalence()
        if self.pos != len(self.tokens):
            raise ValueError("Tokens extra después de la expresión completa")
        return result

    def parse_equivalence(self):
        left = self.parse_implication()
        while True:
            tok = self.peek()
            if tok[0] == 'EQ':
                self.consume('EQ')
                right = self.parse_implication()
                left = ('equivale', left, right)
            else:
                break
        return left

    def parse_implication(self):
        left = self.parse_or()
        while True:
            tok = self.peek()
            if tok[0] == 'IMP':
                self.consume('IMP')
                right = self.parse_or()
                left = ('implica', left, right)
            else:
                break
        return left

    def parse_or(self):
        left = self.parse_and()
        while True:
            tok = self.peek()
            if tok[0] == 'OR':
                self.consume('OR')
                right = self.parse_and()
                left = ('or', left, right)
            else:
                break
        return left

    def parse_and(self):
        left = self.parse_not()
        while True:
            tok = self.peek()
            if tok[0] == 'AND':
                self.consume('AND')
                right = self.parse_not()
                left = ('and', left, right)
            else:
                break
        return left

    def parse_not(self):
        tok = self.peek()
        if tok[0] == 'NOT':
            self.consume('NOT')
            operand = self.parse_not()
            return ('not', operand)
        else:
            return self.parse_atom()

    def parse_atom(self):
        tok = self.peek()
        if tok[0] == 'VAR':
            self.consume('VAR')
            return ('var', tok[1])
        elif tok[0] == 'LPAREN':
            self.consume('LPAREN')
            expr = self.parse_equivalence()
            if self.peek()[0] != 'RPAREN':
                raise ValueError("Falta paréntesis de cierre")
            self.consume('RPAREN')
            return expr
        else:
            raise ValueError(f"Token inesperado {tok}")

def evaluar(arbol, contexto):
    tipo = arbol[0]

    if tipo == 'var':
        var = arbol[1]
        if var not in contexto:
            raise ValueError(f"Variable {var} sin valor asignado")
        return contexto[var]

    elif tipo == 'not':
        val = evaluar(arbol[1], contexto)
        return int(not val)

    elif tipo == 'and':
        val1 = evaluar(arbol[1], contexto)
        val2 = evaluar(arbol[2], contexto)
        return int(val1 and val2)

    elif tipo == 'or':
        val1 = evaluar(arbol[1], contexto)
        val2 = evaluar(arbol[2], contexto)
        return int(val1 or val2)

    elif tipo == 'implica':
        val1 = evaluar(arbol[1], contexto)
        val2 = evaluar(arbol[2], contexto)
        return implica(val1, val2)

    elif tipo == 'equivale':
        val1 = evaluar(arbol[1], contexto)
        val2 = evaluar(arbol[2], contexto)
        return equivale(val1, val2)

    else:
        raise ValueError(f"Tipo de nodo desconocido: {tipo}")

def procesar_expresion(expresion):
    expresion = expresion.replace("[", "(").replace("]", ")")
    expresion = expresion.replace("{", "(").replace("}", ")")

    tokens = tokenize(expresion)
    parser = Parser(tokens)
    arbol = parser.parse()
    return arbol

def obtener_subexpresiones(arbol):
    subexpresiones = []

    def recorrer(nodo):
        if isinstance(nodo, tuple):
            tipo = nodo[0]
            if tipo == 'var':
                texto = nodo[1]
            elif tipo == 'not':
                hijo = recorrer(nodo[1])
                texto = f'¬{hijo}'
            elif tipo in ('and', 'or', 'implica', 'equivale'):
                izq = recorrer(nodo[1])
                der = recorrer(nodo[2])
                op = {'and': '∧', 'or': '∨', 'implica': '→', 'equivale': '↔'}[tipo]
                texto = f'({izq} {op} {der})'
            else:
                raise ValueError(f"Nodo desconocido: {tipo}")

            if texto not in [s[0] for s in subexpresiones]:
                subexpresiones.append((texto, nodo))

            return texto
        return str(nodo)

    recorrer(arbol)
    return subexpresiones