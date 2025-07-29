import tkinter as tk
from tkinter import ttk
from utilidades_tabla import generar_tabla

def main():
    ventana = tk.Tk()
    ventana.title("Generador de Tablas de Verdad")
    ventana.geometry("1000x600")

    etiqueta = tk.Label(ventana, text="Ingrese la expresión lógica:", font=("Poppins", 20))
    etiqueta.pack(pady=20)

    entrada = tk.Entry(ventana, width=80, font=("Poppins Light", 13))
    entrada.pack(pady=5)

    boton = tk.Button(ventana, text="Generar tabla", font=("Poppins", 12), bg="#4CAF50", fg="white",
                      command=lambda: generar_tabla(entrada.get(), tree))
    boton.pack(pady=10)

    tree = ttk.Treeview(ventana)
    tree.pack(padx=10, pady=20, fill="both", expand=True)

    scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    ventana.mainloop()

if __name__ == "__main__":
    main()
