import tkinter as tk
from tkinter import ttk
from utilidades_tabla import generar_tabla
from tkinter import messagebox

def animar_texto(label, texto, indice=0):
    if indice <= len(texto):
        label.config(text=texto[:indice])
        label.after(100, animar_texto, label, texto, indice + 1)

def agregar_efecto_hover(boton, color_normal, color_hover):
    boton.bind("<Enter>", lambda e: boton.config(bg=color_hover))
    boton.bind("<Leave>", lambda e: boton.config(bg=color_normal))

def mostrar_ventana_principal():
    splash.destroy()
    main()

def mostrar_ayuda():
    messagebox.showinfo("Ayuda", "Ingresa una expresión lógica y presiona 'Generar tabla'.\n\n"
                                 "Puedes usar los símbolos lógicos que aparecen en los botones.\n\n"
                                 "Recuerda que no puedes exceder las 10 variables y debes usar letras minúsculas.")


splash = tk.Tk()
splash.title("Bienvenida")
splash.geometry("1000x600")
splash.configure(bg="#D7D2E6")
splash.eval('tk::PlaceWindow . center')
splash.state('zoomed')

mensaje = tk.Label(splash, text="", font=("Poppins", 52, "bold"), bg="#D7D2E6", fg="#342F3C")
mensaje.pack(pady=(235, 5))
animar_texto(mensaje, "¡Bienvenido, Usuario!")

submensaje = tk.Label(splash, text="Este programa es un generador de tablas de verdad, deberás", font=("Poppins", 20), bg="#D7D2E6", fg="#342F3C")
submensaje.pack(pady=0)
submensaje = tk.Label(splash, text="ingresar una expresión lógica de máximo 10 variables con letras minúsculas.", font=("Poppins", 20), bg="#D7D2E6", fg="#342F3C")
submensaje.pack(pady=0)

boton_comenzar = tk.Button(splash, text="Comenzar", font=("Poppins", 20, "bold"), bg="#68AAB9", fg="white",
                           activebackground="#90BCC6", activeforeground="white", bd=0, relief=tk.FLAT, width=14, height=2,
                           command=mostrar_ventana_principal)
boton_comenzar.pack(pady=25)
agregar_efecto_hover(boton_comenzar, "#68AAB9", "#90BCC6")

def main():
    def insertar_simbolo(simbolo):
        entrada.insert(tk.INSERT, simbolo)
    
    def limpiar():
        entrada.delete(0, tk.END)

        for item in tree.get_children():
            tree.delete(item)
        
        tree["columns"] = ()
        tree["show"] = ""

    ventana = tk.Tk()
    ventana.title("Generador de Tablas de Verdad")
    ventana.geometry("1000x600")
    ventana.configure(bg="#B1A5D4")
    ventana.state('zoomed')

    etiqueta = tk.Label(ventana, text="Ingrese la expresión lógica:", font=("Poppins", 20, "bold"), bg="#B1A5D4", fg="#342F3C")
    etiqueta.pack(pady=(35, 5))

    entrada = tk.Entry(ventana, width=80, font=("Poppins Light", 15), bg="#D7D2E6")
    entrada.pack(pady=7)

    frame_botones = tk.Frame(ventana, bg="#B1A5D4")
    frame_botones.pack()
    
    simbolos = ["¬", "∧", "∨", "→", "↔", "(", ")", "[", "]", "{", "}"]
    
    for simbolo in simbolos:
        boton = tk.Button(frame_botones, text=simbolo, width=6, height= 2, font=("Poppins", 13, "bold"),
                  bg="#D777A7", fg="white", activebackground="#D59DB9", activeforeground= "white", bd=0, relief=tk.FLAT,
                  command=lambda s=simbolo: insertar_simbolo(s))
        boton.pack(side=tk.LEFT, padx=4, pady=10)
        agregar_efecto_hover(boton, "#D777A7", "#D59DB9")
    
    boton_limpiar = tk.Button(frame_botones, text="Limpiar", width=8, height=2, font=("Poppins", 13, "bold"),
                  bg="#9E88C9", fg="white", activebackground="#B1A5D4", activeforeground="white", bd=0, relief=tk.FLAT,
                  command=limpiar)
    boton_limpiar.pack(side=tk.LEFT, padx=4)
    agregar_efecto_hover(boton_limpiar, "#9E88C9", "#A798D4")

    boton = tk.Button(ventana, text="  Generar tabla  ", font=("Poppins", 14), height=2,
                      bg="#68AAB9", fg="white", activebackground="#90BCC6", activeforeground="white", bd=0, relief=tk.FLAT,
                      command=lambda: generar_tabla(entrada.get(), tree))
    boton.pack(pady=(10, 0))
    agregar_efecto_hover(boton, "#68AAB9", "#90BCC6")

    style = ttk.Style()
    style.theme_use("default")
    
    style.configure("Treeview", background="#CFCBDB", fieldbackground="#CFCBDB", foreground="black")
    
    style.map("Treeview", background=[('selected', "#958BD6")], foreground=[('selected', 'white')])
    
    style.configure("Treeview.Heading", relief="flat", background="#CFCBDB", foreground="black")

    tree = ttk.Treeview(ventana)
    tree.pack(padx=20, pady=20, fill="both", expand=True)

    scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    boton_ayuda = tk.Button(ventana, text="Ayuda", font=("Poppins", 12, "bold"), bg="#9E88C9", fg="white",
                        activebackground="#A798D4", activeforeground="white", bd=0, relief=tk.FLAT,
                        command=mostrar_ayuda)
    boton_ayuda.pack(pady=(0, 0))
    agregar_efecto_hover(boton_ayuda, "#9E88C9", "#A798D4")

    ventana.mainloop()

splash.mainloop()
