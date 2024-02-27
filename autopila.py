import re

class Parser:
    def __init__(self, input_text, append_to_text_area):
        self.tokens = self.tokenize(input_text)
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]
        self.stack = []
        self.append_to_text_area = append_to_text_area 

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

    def parse(self):
        print("Parsing:")
        print("Input:", ' '.join(self.tokens))
        self.REPETITIVA()

    def REPETITIVA(self):
        self.stack.append(["do", "CUERPO", "MIENTRAS"])
        self.print_stack()
        self.update_stack(["CUERPO", "MIENTRAS"])  # Quitar "do"
        self.CUERPO()

    def CUERPO(self):
        self.update_stack(["{}", "MIENTRAS"])  # Reemplazar "CUERPO"
        self.update_stack(["MIENTRAS"])  # Reemplazar "{}"
        self.advance()
        self.MIENTRAS()

    def MIENTRAS(self):
        self.update_stack(["mientras", "CONDICIONAL"])  # Reemplazar "MIENTRAS"
        self.update_stack(["CONDICIONAL"])  # Eliminar "mientras"
        self.advance()
        self.CONDICIONAL()

    def CONDICIONAL(self):
        self.update_stack(["(", "EXPRESION", ")"])  # Reemplazar "CONDICIONAL"
        self.update_stack(["EXPRESION", ")"])  # Quitar "("
        self.advance()
        self.EXPRESION()

    def EXPRESION(self):
        self.update_stack(["VALOR", "OPERADOR", "V", ")"])  # Reemplazar "EXPRESION"
        self.advance()
        self.VALOR()
        self.OPERADOR()
        self.V()

    def VALOR(self):
        self.update_stack(["LETRA", "RESTO", "OPERADOR", "V", ")"]) 
        palabra = self.current_token
        self.update_stack([palabra, "RESTO", "OPERADOR", "V", ")"])  # Reemplazar "VALOR"
        palabra = self.LETRA(palabra)
        self.update_stack([palabra, "RESTO", "OPERADOR", "V", ")"])  # Reemplazar "VALOR"
        self.RESTO(palabra)  # Procesa el resto de la palabra

    def RESTO(self, palabra):
            if palabra:
                palabra = self.LETRA(palabra)
                self.update_stack([palabra, "RESTO", "OPERADOR", "V", ")"])
                self.RESTO(palabra)  # Procesa el resto de la palabra
            elif not palabra:
                self.update_stack(["OPERADOR", "V", ")"])
                self.advance()
                return

    def LETRA(self, palabra):
        if palabra.isalpha():
            palabra = palabra[1:]
            return palabra
        else:
            raise SyntaxError(f"Unexpected token: {palabra}. Expected: 'letra(s)'")

    def OPERADOR(self):
        if self.current_token in {"==", "!="}:
            self.update_stack(["OPERADOR", "V", ")"])
            self.update_stack([self.current_token, "V", ")"]) 
            self.match(self.current_token)
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}. Expected: '==' or '!='")
    
    def V(self):
        if self.current_token == "true":
            self.update_stack(["V", ")"])
            self.update_stack([self.current_token, ")"]) 
            self.match("true")
        elif self.current_token == "false":
            self.update_stack(["V", ")"])
            self.update_stack([self.current_token, ")"])
            self.match("false")
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}. Expected: 'true' or 'false'")
        
        self.update_stack([self.current_token])
        self.update_stack(["$"])

    def update_stack(self, new_elements):
        self.stack = new_elements  # Reemplazar la pila con los nuevos elementos
        self.print_stack()

    def print_stack(self):
        flat_stack = [item for sublist in self.stack for item in (sublist if isinstance(sublist, list) else [sublist])]
        self.append_to_text_area("Stack: " + ' '.join(flat_stack) + "\n")
