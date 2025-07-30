import tkinter as tk
from tkinter import ttk
from utilidades_tabla import generar_tabla

def main():
    def insertar_simbolo(simbolo):
        entrada.insert(tk.INSERT, simbolo)

    ventana = tk.Tk()
    ventana.title("Generador de Tablas de Verdad")
    ventana.geometry("1000x600")
    ventana.configure(bg="#B1A5D4")

    etiqueta = tk.Label(ventana, text="Ingrese la expresión lógica:", font=("Poppins", 20), bg="#B1A5D4")
    etiqueta.pack(pady=20)

    entrada = tk.Entry(ventana, width=80, font=("Poppins Light", 15), bg="#D7D2E6")
    entrada.pack(pady=5)

    frame_botones = tk.Frame(ventana, bg="#B1A5D4")
    frame_botones.pack()
    
    simbolos = ["¬", "∧", "∨", "→", "↔", "(", ")", "[", "]", "{", "}"]
    
    for simbolo in simbolos:
        boton = tk.Button(frame_botones, text=simbolo, width=6, height= 2, font=("Poppins", 13, "bold"),
                  bg="#D777A7", fg="white", activebackground="#D59DB9", activeforeground= "white", bd=0, relief=tk.FLAT,
                  command=lambda s=simbolo: insertar_simbolo(s))
        boton.pack(side=tk.LEFT, padx=4, pady=10)

    boton = tk.Button(ventana, text="  Generar tabla  ", font=("Poppins", 14), height=2,
                      bg="#68AAB9", fg="white", activebackground="#90BCC6", activeforeground="white", bd=0, relief=tk.FLAT,
                      command=lambda: generar_tabla(entrada.get(), tree))
    boton.pack(pady=10)

    style = ttk.Style()
    style.theme_use("default")
    
    style.configure("Treeview", background="#CFCBDB", fieldbackground="#CFCBDB", foreground="black")
    
    style.map("Treeview", background=[('selected', "#958BD6")], foreground=[('selected', 'white')])
    
    style.configure("Treeview.Heading", relief="flat", background="#CFCBDB", foreground="black")

    tree = ttk.Treeview(ventana)
    tree.pack(padx=10, pady=20, fill="both", expand=True)

    scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    ventana.mainloop()

if __name__ == "__main__":
    main()
