import tkinter as tk

def append_to_text_area(text):
    text_area.insert(tk.END, text)
    text_area.see(tk.END) 

root = tk.Tk()
root.title("GRAMATICA 6 - método descendente: Predictivo No Recursivo")

entry = tk.Entry(root, width=50)
entry.pack(padx=10, pady=10)

boton_procesar = tk.Button(root, text="PROCESAR", command=procesar_input)
boton_procesar.pack(padx=10, pady=10)

text_area = tk.Text(root, height=30, width=80)
text_area.pack(padx=10, pady=10)

root.mainloop()
