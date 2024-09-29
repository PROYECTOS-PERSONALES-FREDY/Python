
import tkinter as tk
from collections import Counter, defaultdict
import heapq
import math

# Función para calcular las probabilidades de los caracteres
def calcular_probabilidades(texto):
    contador = Counter(texto)
    total = len(texto)
    return {char: freq / total for char, freq in contador.items()}

# Función para construir el árbol de Huffman
def construir_arbol_huffman(probabilidades):
    heap = [[peso, [simbolo, ""]] for simbolo, peso in probabilidades.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for par in lo[1:]:
            par[1] = '0' + par[1]
        for par in hi[1:]:
            par[1] = '1' + par[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    
    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

# Función para calcular la entropía
def calcular_entropia(probabilidades):
    return -sum(p * math.log2(p) for p in probabilidades.values())

# Función para calcular el largo medio
def calcular_largo_medio(codigo_huffman, probabilidades):
    return sum(len(codigo) * probabilidades[char] for char, codigo in codigo_huffman)

# Función para calcular la eficiencia
def calcular_eficiencia(entropia, largo_medio):
    return entropia / largo_medio if largo_medio != 0 else 0

# Función que se ejecuta al presionar el botón
def procesar_frase():
    frase = entrada_frase.get()
    if not frase:
        return
    
    # Calcular probabilidades
    probabilidades = calcular_probabilidades(frase)
    
    # Construir código de Huffman
    codigo_huffman = construir_arbol_huffman(probabilidades)
    
    # Calcular entropía
    entropia = calcular_entropia(probabilidades)
    
    # Calcular largo medio
    largo_medio = calcular_largo_medio(codigo_huffman, probabilidades)
    
    # Calcular eficiencia
    eficiencia = calcular_eficiencia(entropia, largo_medio)
    
    # Mostrar resultados
    resultados_probabilidad.config(text=f"Probabilidades: {probabilidades}")
    resultados_huffman.config(text=f"Código Huffman: {codigo_huffman}")
    resultados_entropia.config(text=f"Entropía: {entropia:.4f}")
    resultados_largo_medio.config(text=f"Largo medio: {largo_medio:.4f}")
    resultados_eficiencia.config(text=f"Eficiencia: {eficiencia:.4f}")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Análisis de Información de Frase")

# Etiqueta y entrada de frase
etiqueta_frase = tk.Label(ventana, text="Introduce una frase:")
etiqueta_frase.pack()

entrada_frase = tk.Entry(ventana)
entrada_frase.pack()

# Botón para procesar la frase
boton_procesar = tk.Button(ventana, text="Procesar", command=procesar_frase)
boton_procesar.pack()

# Resultados
resultados_probabilidad = tk.Label(ventana, text="")
resultados_probabilidad.pack()

resultados_huffman = tk.Label(ventana, text="")
resultados_huffman.pack()

resultados_entropia = tk.Label(ventana, text="")
resultados_entropia.pack()

resultados_largo_medio = tk.Label(ventana, text="")
resultados_largo_medio.pack()

resultados_eficiencia = tk.Label(ventana, text="")
resultados_eficiencia.pack()

# Ejecutar la ventana principal
ventana.mainloop()
