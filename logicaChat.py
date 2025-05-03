import tkinter as tk
import re
palabras_reservadas_Saludo = {
    "Hola", "Que tal", "Buenos días", "Buenas tardes", "Buenas noches"
}
palabras_reservadas_Despedida = {
    "Hasta luego", "Adios", "Hasta pronto", "Nos vemos", "Chao"
}
# Función para limpiar texto de puntuación al verificar palabras clave
def limpiar_texto(texto):
    return texto.strip().rstrip(',.;:!?')


# Función para analizar la entrada
def analizar_entrada(texto):
    lineas = [line.strip() for line in texto.strip().split('\n') if line.strip()]
    resultado = ""

    # Verificar si hay al menos 2 líneas (saludo y despedida)
    if len(lineas) < 2:
        return "Error: Se requieren al menos un saludo y una despedida."

    # Analizar primera línea (saludo)
    primera_linea_limpia = limpiar_texto(lineas[0])
    if primera_linea_limpia in palabras_reservadas_Saludo:
        resultado += f"✓ Saludo '{primera_linea_limpia}' reconocido correctamente.\n"
    else:
        resultado += f"✗ Error: La primera línea debe ser un saludo válido: {', '.join(sorted(palabras_reservadas_Saludo))}.\n"

    # Analizar última línea (despedida)
    ultima_linea_limpia = limpiar_texto(lineas[-1])
    if ultima_linea_limpia in palabras_reservadas_Despedida:
        resultado += f"✓ Despedida '{ultima_linea_limpia}' reconocida correctamente.\n"
    else:
        resultado += f"✗ Error: La última línea debe ser una despedida válida: {', '.join(sorted(palabras_reservadas_Despedida))}.\n"

    # Analizar líneas intermedias (oraciones con estructura S+V+P)
    if len(lineas) >= 3:
        # Analizar solo la primera oración después del saludo y antes de la despedida
        oracion = lineas[1]
        estructura = analizar_estructura_oracion(oracion)
        resultado += f"\nAnálisis de la oración principal:\n{estructura}\n"

        # Analizar oraciones adicionales si existen
        if len(lineas) > 3:
            resultado += f"\nSe encontraron {len(lineas) - 3} oraciones adicionales entre el saludo y la despedida.\n"
            for i, linea in enumerate(lineas[2:-1], start=3):
                resultado += f"- Línea {i}: '{linea}'\n"
    else:
        resultado += "\n✗ Error: No hay oración principal entre el saludo y la despedida.\n"

    return resultado
def analizar_estructura_oracion(oracion):
    oracion = oracion.strip().rstrip(',.;:!?')
    palabras = oracion.split()

    if len(palabras) < 3:
        return "✗ No cumple con la estructura Sujeto + Verbo + Complemento (muy corta)"

    patron_verbo = r'.*(ar|er|ir|[óéí])$'

    for i in range(len(palabras)):
        if re.match(patron_verbo, palabras[i].lower()):
            sujeto = " ".join(palabras[:i])
            verbo = palabras[i]
            complemento = " ".join(palabras[i + 1:]) if i + 1 < len(palabras) else ""
            if sujeto and verbo:
                if complemento:
                    return f"✓ Estructura S+V+P detectada\n   Sujeto: {sujeto}\n   Verbo: {verbo}\n   Complemento: {complemento}"
                else:
                    return f"✓ Estructura S+V detectada (sin complemento)\n   Sujeto: {sujeto}\n   Verbo: {verbo}"
            else:
                break

    return "✗ No se detectó un verbo válido"



# Función para resaltar palabras clave
def resaltar_palabras(text_widget):
    contenido = text_widget.get("1.0", tk.END)
    text_widget.tag_remove("resaltado_saludo", "1.0", tk.END)
    text_widget.tag_remove("resaltado_despedida", "1.0", tk.END)
    text_widget.tag_remove("resaltado_sujeto", "1.0", tk.END)
    text_widget.tag_remove("resaltado_verbo", "1.0", tk.END)
    text_widget.tag_remove("resaltado_complemento", "1.0", tk.END)

    # Resaltar palabras de saludo
    for palabra in palabras_reservadas_Saludo:
        inicio = "1.0"
        while True:
            inicio = text_widget.search(rf"\y{palabra}\y", inicio, stopindex=tk.END, regexp=True)
            if not inicio:
                break
            fin = f"{inicio}+{len(palabra)}c"
            text_widget.tag_add("resaltado_saludo", inicio, fin)
            inicio = fin

    # Resaltar palabras de despedida
    for palabra in palabras_reservadas_Despedida:
        inicio = "1.0"
        while True:
            inicio = text_widget.search(rf"\y{palabra}\y", inicio, stopindex=tk.END, regexp=True)
            if not inicio:
                break
            fin = f"{inicio}+{len(palabra)}c"
            text_widget.tag_add("resaltado_despedida", inicio, fin)
            inicio = fin

    # Configurar estilos de resaltado
    text_widget.tag_config("resaltado_saludo", foreground="#4CAF50", font=("Times New Roman", 12, "bold"))
    text_widget.tag_config("resaltado_despedida", foreground="#FF9800", font=("Times New Roman", 12, "bold"))
    text_widget.tag_config("resaltado_sujeto", foreground="#2196F3", font=("Times New Roman", 12, "bold"))
    text_widget.tag_config("resaltado_verbo", foreground="#E91E63", font=("Times New Roman", 12, "bold"))
    text_widget.tag_config("resaltado_complemento", foreground="#9C27B0", font=("Times New Roman", 12, "bold"))
