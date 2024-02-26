import re

class Parser:
    def __init__(self, input_text):
        self.tokens = self.tokenize(input_text)
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]
        self.stack = []

    def tokenize(self, input_text):
        return re.findall(r'do|{}|mientras|\(|\)|[a-z]+|==|!=|true|false', input_text)

    def advance(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def match(self, expected_token):
        if self.current_token == expected_token:
            self.advance()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}. Expected: {expected_token}")

    def REPETITIVA(self):
        self.match("do")
        self.CUERPO()
        self.MIENTRAS()

    def CUERPO(self):
        self.match("{}")

    def MIENTRAS(self):
        self.match("mientras")
        self.CONDICIONAL()

    def CONDICIONAL(self):
        self.match("(")
        self.EXPRESION()
        self.match(")")

    def EXPRESION(self):
        self.VALOR()
        self.OPERADOR()
        self.V()

    def VALOR(self):
        palabra = self.current_token.split()
        letra = palabra[0]
        self.LETRA(letra)
        palabra.pop(0)
        self.RESTO(palabra)

    def RESTO(self, palabra):
        if not palabra:  # Si la lista de letras está vacía
            return
        else:
            if palabra:
                letra = palabra[0]  
                self.LETRA(letra)
                palabra.pop(0)  
                self.RESTO(palabra)
            elif self.current_token == '':
                pass
            else:
                raise SyntaxError(f"Unexpected token: {self.current_token}. Expected: 'letra(s)' or ε")

    def LETRA(self, letra):
        letra_pattern = re.compile(r'[a-z]+')
        if letra_pattern.match(letra):
            self.match(letra)
        else:
            raise SyntaxError(f"Unexpected token: {letra}. Expected: 'letra(s)'")

    def OPERADOR(self):
        if self.current_token in {"==", "!="}:
            self.match(self.current_token)
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}. Expected: '==' or '!='")
    
    def V(self):
        if self.current_token == "true":
            self.match("true")
        elif self.current_token == "false":
            self.match("false")
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}. Expected: 'true' or 'false'")

    def parse(self):
        self.REPETITIVA()
        if self.current_token is not None:
            raise SyntaxError(f"Unexpected token at the end: {self.current_token}")
