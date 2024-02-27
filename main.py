from vista import *
from parser import Parser

def procesar_input():
    entrada = entry.get()
    parser = Parser(entrada)
    try:
        parser.parse()
    except SyntaxError as e:
        append_to_text_area(f"Error de sintaxis: {str(e)}\n")

if __name__ == "__main__":
    root.mainloop()
