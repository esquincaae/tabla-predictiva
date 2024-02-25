from lark import Lark, Tree, exceptions

# Cargar la gramática desde el archivo
with open("grammar.lark") as file:
    grammar = file.read()

# Crear el parser
parser = Lark(grammar, start='start', parser='lalr')

# Función para analizar una entrada
def parse_input(input_string):
    try:
        parsed = parser.parse(input_string)
        print(parsed.pretty())
    except exceptions.LarkError as e:
        print(f"Error en el análisis: {e}")

# Ejemplo de uso
input_string = "do{}mientras(verdad == false)"
parse_input(input_string)
