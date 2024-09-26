import heapq
from collections import Counter
import tkinter as tk
from tkinter import ttk, scrolledtext

# Paso 1: Calcular la probabilidad de cada letra
def calcular_probabilidades(frase):
    frase = frase.replace(" ", "").lower()
    frecuencias = Counter(frase)
    total_letras = sum(frecuencias.values())
    probabilidades = {letra: frecuencia / total_letras for letra, frecuencia in frecuencias.items()}
    return probabilidades

# Paso 2: Aplicar la codificación de Huffman
class Nodo:
    def __init__(self, simbolo, probabilidad):
        self.simbolo = simbolo
        self.probabilidad = probabilidad
        self.izquierda = None
        self.derecha = None
    
    def __lt__(self, otro):
        return self.probabilidad < otro.probabilidad

def crear_arbol_huffman(probabilidades):
    cola_prioridad = [Nodo(simbolo, probabilidad) for simbolo, probabilidad in probabilidades.items()]
    heapq.heapify(cola_prioridad)
    
    while len(cola_prioridad) > 1:
        nodo_izquierdo = heapq.heappop(cola_prioridad)
        nodo_derecho = heapq.heappop(cola_prioridad)
        
        nuevo_nodo = Nodo(None, nodo_izquierdo.probabilidad + nodo_derecho.probabilidad)
        nuevo_nodo.izquierda = nodo_izquierdo
        nuevo_nodo.derecha = nodo_derecho
        
        heapq.heappush(cola_prioridad, nuevo_nodo)
    
    return cola_prioridad[0]

def asignar_codigos_huffman(nodo, codigo_actual="", codigos={}):
    if nodo.simbolo is not None:
        codigos[nodo.simbolo] = codigo_actual
    else:
        asignar_codigos_huffman(nodo.izquierda, codigo_actual + "1", codigos)
        asignar_codigos_huffman(nodo.derecha, codigo_actual + "0", codigos)
    return codigos

def codificacion_huffman(frase):
    probabilidades = calcular_probabilidades(frase)
    arbol_huffman = crear_arbol_huffman(probabilidades)
    codigos_huffman = asignar_codigos_huffman(arbol_huffman)
    frase_codificada = ''.join([codigos_huffman[letra] for letra in frase.replace(" ", "").lower()])
    return probabilidades, codigos_huffman, frase_codificada

# Función para actualizar la interfaz con los resultados
def mostrar_resultados():
    frase = entrada_frase.get()
    probabilidades, codigos_huffman, frase_codificada = codificacion_huffman(frase)
    
    # Limpiar los cuadros de texto
    area_probabilidades.delete(1.0, tk.END)
    area_codigos.delete(1.0, tk.END)
    area_codificada.delete(1.0, tk.END)
    
    # Mostrar las probabilidades
    area_probabilidades.insert(tk.END, "Probabilidades:\n")
    for letra, prob in probabilidades.items():
        area_probabilidades.insert(tk.END, f"{letra}: {prob:.4f}\n")
    
    # Mostrar los códigos de Huffman
    area_codigos.insert(tk.END, "Códigos de Huffman:\n")
    for letra, codigo in codigos_huffman.items():
        area_codigos.insert(tk.END, f"{letra}: {codigo}\n")
    
    # Mostrar la frase codificada
    area_codificada.insert(tk.END, "Frase codificada:\n")
    area_codificada.insert(tk.END, frase_codificada)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Codificación Huffman")
ventana.geometry("600x400")

# Etiqueta y campo de entrada para la frase
etiqueta_frase = ttk.Label(ventana, text="Introduce una frase:")
etiqueta_frase.pack(pady=10)

entrada_frase = ttk.Entry(ventana, width=50)
entrada_frase.pack(pady=5)

# Botón para realizar la codificación
boton_codificar = ttk.Button(ventana, text="Codificar", command=mostrar_resultados)
boton_codificar.pack(pady=10)

# Área de texto para mostrar probabilidades
area_probabilidades = scrolledtext.ScrolledText(ventana, width=30, height=10)
area_probabilidades.pack(side=tk.LEFT, padx=10)

# Área de texto para mostrar los códigos de Huffman
area_codigos = scrolledtext.ScrolledText(ventana, width=30, height=10)
area_codigos.pack(side=tk.LEFT, padx=10)

# Área de texto para mostrar la frase codificada
area_codificada = scrolledtext.ScrolledText(ventana, width=60, height=5)
area_codificada.pack(pady=10)

# Iniciar la ventana
ventana.mainloop()