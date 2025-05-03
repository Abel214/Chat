import tkinter as tk
from itertools import cycle
from tkinter import messagebox

from PIL import Image, ImageTk

from chatInterfaz import crear_automata_interfaz


def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Pequeño Chat")
    x=ventana.winfo_screenwidth() // 2 - 350
    y=ventana.winfo_screenheight() // 2 - 200
    ventana.geometry(f"700x400+{x}+{y}")
    ventana.geometry("700x400")

    # Cargar el GIF (animado)
    frames = []
    gif = Image.open("resources/CartaFondo.gif")

    try:
        while True:
            frame = ImageTk.PhotoImage(gif.copy())
            frames.append(frame)
            gif.seek(len(frames))   #Se pasa al siguiente frame del gif
    except EOFError:
        pass

    frame_cycle = cycle(frames)

    fondo_label = tk.Label(ventana)
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

    def actualizar_frame():
        frame = next(frame_cycle)
        fondo_label.config(image=frame)
        ventana.after(100, actualizar_frame)

    actualizar_frame()

    def acerca_de():
        messagebox.showinfo("Acerca de", "Desarrollado por:  Brian Aguinsaca-Abel Mora")

    def abrir_programa():
        #Función para cerrar la interfaz de menú
        ventana.withdraw()
        ventana_automata = crear_automata_interfaz()
        def al_cerrar_automata():
            # Volver a mostrar la ventana principal
            ventana.deiconify()
            ventana_automata.destroy()
        ventana_automata.protocol("WM_DELETE_WINDOW", al_cerrar_automata)
    # Crear el menú
    menu = tk.Menu(ventana)
    ventana_principal = tk.Menu(menu, tearoff=0)
    ventana_principal.add_command(label="Programa", command=abrir_programa)
    ventana_principal.add_command(label="Creditos", command= acerca_de)
    ventana_principal.add_command(label="Salir", command=ventana.destroy)
    menu.add_cascade(label="Menú", menu=ventana_principal)
    ventana.config(menu=menu)

    ventana.mainloop()

