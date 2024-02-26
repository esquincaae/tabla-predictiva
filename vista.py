import tkinter as tk
from tkinter import messagebox
from autopila import Parser

def procesar_input():
    entrada = entry.get()
    parser = Parser(entrada)
    try:
        parser.parse()
        text_area.insert(tk.END, "La entrada es aceptada por la gramática.\n")
    except SyntaxError as e:
        text_area.insert(tk.END, f"Error de sintaxis: {str(e)}\n")

root = tk.Tk()
root.title("GRAMATICA 6 - método descendente: Predictivo No Recursivo")

entry = tk.Entry(root, width=50)
entry.pack(padx=10, pady=10)

boton_procesar = tk.Button(root, text="PROCESAR", command=procesar_input)
boton_procesar.pack(padx=10, pady=10)

text_area = tk.Text(root, height=30, width=80)
text_area.pack(padx=10, pady=10)

root.mainloop()