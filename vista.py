import tkinter as tk
from tkinter import messagebox
from autopila import analizador

def procesar():
    entrada = entry.get()  # Obtiene el texto del usuario
    resultado = analizador(entrada)  # Procesa la entrada
    text_area.delete('1.0', tk.END)  # Limpia el área de texto
    text_area.insert(tk.END, resultado)  # Muestra el resultado

root = tk.Tk()
root.title("Gramatica 6: LL1")

# Creación de la entrada de texto
entry = tk.Entry(root, width=100)
entry.pack(padx=10, pady=10)

# Botón para procesar la entrada
boton_procesar = tk.Button(root, text="PROCESAR", command=procesar)
boton_procesar.pack(padx=10, pady=10)

# Área de texto para mostrar los resultados
text_area = tk.Text(root, height=15, width=150)
text_area.pack(padx=10, pady=10)

root.mainloop()