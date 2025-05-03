import tkinter as tk
import re
from tkinter import scrolledtext
from logicaChat import palabras_reservadas_Saludo, palabras_reservadas_Despedida, analizar_entrada, resaltar_palabras

# Función principal para crear la interfaz gráfica
def crear_automata_interfaz():
    ventana = tk.Tk()
    ventana.title("Autómata de Reconocimiento de Mensajes")
    ancho = 800
    alto = 600
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    pos_x = (ancho_pantalla // 2) - (ancho // 2)
    pos_y = (alto_pantalla // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")
    ventana.configure(bg="#2b2b2b")
    frame_encabezado = tk.Frame(ventana, bg="#2b2b2b")
    frame_encabezado.pack(fill="x", padx=10, pady=10)
    # Título
    titulo = tk.Label(
        frame_encabezado,
        text="Autómata de Reconocimiento de Mensajes",
        font=("Arial", 16, "bold"),
        bg="#2b2b2b",
        fg="white"
    )
    titulo.pack(anchor="w")

    # Instrucciones
    instrucciones = tk.Label(
        frame_encabezado,
        text=(
            "Ingresa un mensaje con la siguiente estructura:\n"
            "1. Debe comenzar con un saludo válido\n"
            "2. Debe contener al menos una oración con estructura Sujeto + Verbo + Complemento\n"
            "3. Debe finalizar con una despedida válida"
        ),
        font=("Arial", 11),
        bg="#2b2b2b",
        fg="#BBBBBB",
        justify="left"
    )
    instrucciones.pack(anchor="w", pady=(5, 0))

    # Crear marco para palabras clave
    frame_palabras = tk.Frame(ventana, bg="#2b2b2b")
    frame_palabras.pack(fill="x", padx=10, pady=(5, 10))
    tk.Label(
        frame_palabras,
        text=", ".join(sorted(palabras_reservadas_Despedida)),
        font=("Arial", 10),
        bg="#2b2b2b",
        fg="#AAAAAA"
    ).pack(side="left", padx=(5, 0))

    # Crear paneles para entrada y resultado
    panel = tk.PanedWindow(ventana, orient=tk.VERTICAL, bg="#1e1e1e", sashwidth=8)
    panel.pack(fill="both", expand=True, padx=10, pady=10)

    # Área de texto para entrada
    frame_entrada = tk.Frame(panel, bg="#1e1e1e")
    panel.add(frame_entrada, height=200)

    tk.Label(
        frame_entrada,
        text="Mensaje:",
        font=("Arial", 11, "bold"),
        bg="#1e1e1e",
        fg="white"
    ).pack(anchor="w", padx=5, pady=(0, 5))

    text_area = scrolledtext.ScrolledText(
        frame_entrada,
        font=("Consolas", 12),
        wrap="word",
        background="#2d2d2d",
        foreground="white",
        insertbackground="white",
        bd=0,
        padx=10,
        pady=10
    )
    text_area.pack(fill="both", expand=True)

    # Área para mostrar resultados
    frame_resultado = tk.Frame(panel, bg="#1e1e1e")
    panel.add(frame_resultado)

    tk.Label(
        frame_resultado,
        text="Análisis:",
        font=("Arial", 11, "bold"),
        bg="#1e1e1e",
        fg="white"
    ).pack(anchor="w", padx=5, pady=(0, 5))

    resultado_area = scrolledtext.ScrolledText(
        frame_resultado,
        font=("Consolas", 12),
        wrap="word",
        background="#2d2d2d",
        foreground="#BBBBBB",
        insertbackground="white",
        bd=0,
        padx=10,
        pady=10,
        state="disabled"
    )
    resultado_area.pack(fill="both", expand=True)

    # Función para analizar automáticamente el texto
    def analizar_texto_automatico(event=None):
        texto = text_area.get("1.0", tk.END)
        resultado = analizar_entrada(texto)

        resultado_area.config(state="normal")
        resultado_area.delete("1.0", tk.END)
        resultado_area.insert("1.0", resultado)

        # Se aplica un color al resultado para poder diferenciar si las palabras fueron escritas correctamente
        if "✓" in resultado:
            inicio = "1.0"
            while True:
                inicio = resultado_area.search("✓", inicio, stopindex=tk.END)
                if not inicio:
                    break
                linea = resultado_area.get(inicio + " linestart", inicio + " lineend")
                fin = inicio + " lineend"
                resultado_area.tag_add("correcto", inicio + " linestart", fin)
                inicio = fin + "+1c"

            resultado_area.tag_config("correcto", foreground="#4CAF50")

        if "✗" in resultado:
            inicio = "1.0"
            while True:
                inicio = resultado_area.search("✗", inicio, stopindex=tk.END)
                if not inicio:
                    break
                linea = resultado_area.get(inicio + " linestart", inicio + " lineend")
                fin = inicio + " lineend"
                resultado_area.tag_add("error", inicio + " linestart", fin)
                inicio = fin + "+1c"

            resultado_area.tag_config("error", foreground="#F44336")

        resultado_area.config(state="disabled")
        resaltar_palabras(text_area)

    # Cargar ejemplo para que el usuario pueda ver cómo funciona el programa
    def cargar_ejemplo(ejemplo):
        text_area.delete("1.0", tk.END)
        text_area.insert("1.0", ejemplo)
        analizar_texto_automatico()

    # Crear marco para ejemplos
    frame_ejemplos = tk.Frame(ventana, bg="#2b2b2b")
    frame_ejemplos.pack(fill="x", padx=10, pady=10)

    tk.Label(
        frame_ejemplos,
        text="Ejemplos:",
        font=("Arial", 11, "bold"),
        bg="#2b2b2b",
        fg="white"
    ).pack(side="left", padx=(0, 10))

    ejemplos = [
        ("Ejemplo 1", "Hola,\nEl día está lluvioso.\nHasta luego"),
        ("Ejemplo 2", "Buenos días\nMi nombre es Roberth.\nChao"),
        ("Ejemplo 3", "Que tal\nYo estudio Ingeniería en Computación en la UNL.\nAdiós"),
        ("Ejemplo 4", "Buen día,\nJuan disfruta programar aplicaciones\nNos vemos")
    ]

    for nombre, texto in ejemplos:
        btn = tk.Button(
            frame_ejemplos,
            text=nombre,
            command=lambda t=texto: cargar_ejemplo(t),
            bg="#3c3c3c",
            fg="white",
            activebackground="#555555",
            activeforeground="white",
            bd=0,
            padx=10,
            pady=5
        )
        btn.pack(side="left", padx=(0, 5))

    # Evento de escritura
    text_area.bind("<KeyRelease>", analizar_texto_automatico)

    # Ejecutar análisis inicial
    ventana.after(100, analizar_texto_automatico)

    # Configurar ejemplo inicial
    text_area.insert("1.0", "Hola,\nEl día está lluvioso.\nHasta luego")

    return ventana
