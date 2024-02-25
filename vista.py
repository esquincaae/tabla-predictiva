import tkinter as tk
from tkinter import messagebox
from autopila import procesar_entrada  

def procesar():
    entrada = text_area_entrada.get('1.0', tk.END)  
    try:  
        token_counts = procesar_entrada(entrada)
        text_area_resultado.delete('1.0', tk.END)  
        for token_type, count in token_counts.items():
            text_area_resultado.insert(tk.END, f"Token: {token_type}, Conteo: {count}\n")
    except Exception as e:
        messagebox.showerror("Error de análisis", str(e))

root = tk.Tk()
root.title("Gramatica 6: Estructura Repetitida do-while")


text_area_entrada = tk.Text(root, height=10, width=100)
text_area_entrada.pack(padx=10, pady=10)

boton_procesar = tk.Button(root, text="PROCESAR", command=procesar)
boton_procesar.pack(padx=10, pady=10)

text_area_resultado = tk.Text(root, height=15, width=100)
text_area_resultado.pack(padx=10, pady=10)

root.mainloop()