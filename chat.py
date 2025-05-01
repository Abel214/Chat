import tkinter as tk
import re

# Palabras reservadas para el resaltado
palabras_reservadas_Saludo = {"Hola", "Que tal", "Buenos días", "Buenas tardes", "Buenas noches"}
palabras_reservadas_Despedida = {"Hasta luego", "Adios", "Hasta pronto", "Nos vemos", "Chao"}


# Función para analizar la entrada
def analizar_entrada(texto):
    lineas = texto.strip().split('\n')
    resultado = ""

    # Verificar si hay al menos 1 línea
    if len(lineas) < 1:
        return "Error: No se ingresó texto."

    # Analizar cada línea del texto
    for idx, linea in enumerate(lineas, 1):
        linea = linea.strip()

        # Analizar saludo (debe estar en la primera línea si se encuentra)
        if idx == 1:
            if linea in palabras_reservadas_Saludo:
                resultado += f"Saludo '{linea}' reconocido correctamente.\n"
            else:
                resultado += f"Error en la línea {idx}: La primera línea debe ser un saludo válido: {', '.join(palabras_reservadas_Saludo)}.\n"

        # Analizar oración (Sujeto + Verbo + Complemento)
        elif idx == 2:
            estructura = analizar_estructura_oracion(linea)
            resultado += f"Análisis de la oración en la línea {idx}: {estructura}\n"

        # Analizar despedida (debe estar en la última línea si se encuentra)
        elif idx == len(lineas):
            if linea in palabras_reservadas_Despedida:
                resultado += f"Despedida '{linea}' reconocida correctamente.\n"
            else:
                resultado += f"Error en la línea {idx}: La última línea debe ser una despedida válida: {', '.join(palabras_reservadas_Despedida)}.\n"

        # Otras líneas
        else:
            resultado += f"Línea {idx}: Contenido adicional - '{linea}'\n"

    return resultado


# Función para analizar la estructura de una oración
def analizar_estructura_oracion(oracion):
    # Patrón simple para detectar estructura Sujeto + Verbo + Complemento
    palabras = oracion.split()

    if len(palabras) < 3:
        return "No cumple con la estructura Sujeto + Verbo + Complemento (muy corta)"

    # Verificación simple: primera palabra como sujeto, segunda como verbo, resto como complemento
    sujeto = palabras[0]
    verbo = palabras[1]
    complemento = " ".join(palabras[2:])

    # Reglas muy básicas para verificar
    # Verbos en español suelen terminar en ar, er, ir o sus conjugaciones
    patron_verbo = r'.*[aei]r$|.*[aeiáéíóú][^aeiáéíóú]+$'

    if re.match(patron_verbo, verbo.lower()):
        return f"Correcto: Estructura SVC detectada\nSujeto: {sujeto}\nVerbo: {verbo}\nComplemento: {complemento}"
    else:
        return "No cumple con la estructura Sujeto + Verbo + Complemento"


def resaltar_palabras(text_widget):
    contenido = text_widget.get("1.0", tk.END)
    text_widget.tag_remove("resaltado_saludo", "1.0", tk.END)
    text_widget.tag_remove("resaltado_despedida", "1.0", tk.END)

    # Resaltar palabras de saludo
    for palabra in palabras_reservadas_Saludo:
        inicio = "1.0"
        while True:
            inicio = text_widget.search(rf"\m{palabra}\M", inicio, stopindex=tk.END, regexp=True)
            if not inicio:
                break
            fin = f"{inicio}+{len(palabra)}c"
            text_widget.tag_add("resaltado_saludo", inicio, fin)
            inicio = fin

    # Resaltar palabras de despedida
    for palabra in palabras_reservadas_Despedida:
        inicio = "1.0"
        while True:
            inicio = text_widget.search(rf"\m{palabra}\M", inicio, stopindex=tk.END, regexp=True)
            if not inicio:
                break
            fin = f"{inicio}+{len(palabra)}c"
            text_widget.tag_add("resaltado_despedida", inicio, fin)
            inicio = fin

    text_widget.tag_config("resaltado_saludo", foreground="green", font=("Times New Roman", 11, "bold"))
    text_widget.tag_config("resaltado_despedida", foreground="orange", font=("Times New Roman", 11, "bold"))


def abrir_editor_codigo():
    editor = tk.Toplevel()
    editor.title("Autómata de Reconocimiento")
    x = editor.winfo_screenwidth() // 2 - 350
    y = editor.winfo_screenheight() // 2 - 200
    editor.geometry(f"700x450+{x}+{y}")
    editor.configure(bg="#2b2b2b")

    # Encabezado
    label = tk.Label(
        editor,
        text=f"Ingresa texto con el siguiente formato:\nLínea 1: Saludo ({', '.join(palabras_reservadas_Saludo)})\nLínea 2: Oración (Sujeto + Verbo + Complemento)\nLínea 3: Despedida ({', '.join(palabras_reservadas_Despedida)})",
        font=("Times New Roman", 12, "bold"),
        bg="#2b2b2b",
        fg="white",
        anchor="w",
        justify="left"
    )
    label.pack(fill="x", padx=10, pady=(10, 0))

    # Área de texto para entrada
    text_area = tk.Text(
        editor,
        font=("Times New Roman", 12),
        wrap="word",
        background="#363636",
        foreground="white",
        insertbackground="white",
        height=8
    )
    text_area.pack(expand=False, fill="both", padx=10, pady=10)

    # Área para mostrar resultados
    resultado_label = tk.Label(
        editor,
        text="Resultado del análisis:",
        font=("Times New Roman", 12, "bold"),
        bg="#2b2b2b",
        fg="white",
        anchor="w"
    )
    resultado_label.pack(fill="x", padx=10, pady=(5, 0))

    resultado_area = tk.Text(
        editor,
        font=("Times New Roman", 12),
        wrap="word",
        background="#363636",
        foreground="#00ff00",
        insertbackground="white",
        height=8,
        state="disabled"
    )
    resultado_area.pack(expand=True, fill="both", padx=10, pady=10)

    # Función para analizar automáticamente el texto
    def analizar_texto_automatico(event=None):
        texto = text_area.get("1.0", tk.END)
        resultado = analizar_entrada(texto)

        resultado_area.config(state="normal")
        resultado_area.delete("1.0", tk.END)
        resultado_area.insert("1.0", resultado)
        resultado_area.config(state="disabled")

        resaltar_palabras(text_area)

    # Evento de escritura
    text_area.bind("<KeyRelease>", analizar_texto_automatico)

    # Ejecutar análisis inicial si hay texto predeterminado
    editor.after(100, analizar_texto_automatico)
