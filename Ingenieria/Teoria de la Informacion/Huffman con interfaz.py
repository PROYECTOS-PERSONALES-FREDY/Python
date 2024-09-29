import heapq
from collections import Counter
import tkinter as tk
from tkinter import ttk, scrolledtext
import math
import json

# Paso 1: Calcular la probabilidad de cada letra
def calcular_probabilidades(frase):
    # Eliminar espacios y convertir a minúsculas
    frase = frase.replace(" ", "").lower()
    
    # Contar la frecuencia de cada letra
    frecuencias = Counter(frase)
    total_letras = sum(frecuencias.values())
    
    # Calcular la probabilidad de cada letra
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
        return self.probabilidad < otro.probabilidad #Compara dos objetos, self objeto actual < otro objeto a comparar
    
    # Sobrescribir el método __repr__ para visualizar correctamente
    def __repr__(self):
        return f"Nodo(simbolo={self.simbolo}, probabilidad={self.probabilidad})"

# Paso 3: Calcular la entropia
def calcular_entropia(probabilidades):
    entropia = sum(p * math.log2(1/p) for p in probabilidades.values() if p > 0)
    return entropia

# Paso 4: Calcular el largo medio
def calcular_largo_medio(probabilidades, longitudes_codigos):
    i = 0
    largo_medio = 0
    v_codigos = []
    letras_codigos =[]
    v_probabilidades = []
    letras_probabilidades =[]
    
    for letras, codigo in longitudes_codigos.items():
        letras_codigos.append(letras)
        v_codigos.append(len(codigo))
        
    for letras, pro in probabilidades.items():
        letras_probabilidades.append(letras)
        v_probabilidades.append(pro)
    
    v_codigos_letras = intercalar_vectores (letras_codigos, v_codigos)
    v_probabilidades_letras = intercalar_vectores (letras_probabilidades, v_probabilidades)
    print ("vector intercalado :", v_codigos_letras)
    print ("vector intercalado :", v_probabilidades_letras)
    
    # Identificadores comunes
    identificadores = list(v_codigos_letras.keys())

    # Construir el nuevo vector alineado
    resultado = []
    for identificador in identificadores:
        #resultado.append(identificador) #letra comun
        resultado.append(v_codigos_letras.get(identificador, None))  # Valor del primer vector
        resultado.append(v_probabilidades_letras.get(identificador, None))  # Valor del segundo vector
    
    print ("vector intercalado :", resultado)
    
    while(i < len(resultado)):
        largo_medio = resultado[i]*resultado[i+1] + largo_medio
        i += 2
    i = 0    
    return largo_medio

# Paso 5: Calcular la eficiencia
def calcular_eficiencia(entropia, largo_medio):
    if largo_medio > 0:
        eficiencia = (entropia / largo_medio) *100  #eficiencia en porcentaje
    else:
        eficiencia = 0
    return eficiencia

def crear_arbol_huffman(probabilidades):
    # Crear una cola de prioridad con objetos
    cola_prioridad = [Nodo(simbolo, probabilidad*100) for simbolo, probabilidad in probabilidades.items()] #Se hace el diccionario con las letras y la probabilidad
    print("\n Cola antes de heapify:", cola_prioridad)
    heapq.heapify(cola_prioridad) #Organizar de menor a mayor con el constructor __lt__(self, otro):
    print("Cola después de heapify:", cola_prioridad,"\n")
    
    # Crear el árbol de Huffman
    while len(cola_prioridad) > 1:
        cuenta = 0
        # Extraer los dos objetos con menor probabilidad nodo
        nodo_izquierdo = heapq.heappop(cola_prioridad)
        nodo_derecho = heapq.heappop(cola_prioridad)
        
        suma_nodo_izquierdo_derecho = nodo_izquierdo.probabilidad + nodo_derecho.probabilidad

        while (cuenta < len(cola_prioridad)):
            if cola_prioridad[cuenta].probabilidad == suma_nodo_izquierdo_derecho:
                if cola_prioridad[1].probabilidad != suma_nodo_izquierdo_derecho:
                    suma_nodo_izquierdo_derecho -= 0.1
            cuenta += 1

        print("nodo izquierdo",nodo_izquierdo)
        print("nodo derecho",nodo_derecho)
        
        # Crear un nuevo objeto con la suma de sus probabilidades, sin simbolo
        nuevo_nodo = Nodo(None,suma_nodo_izquierdo_derecho )
        print("suma ultimas dos probabilidades",nuevo_nodo,"\n")
        nuevo_nodo.izquierda = nodo_izquierdo
        nuevo_nodo.derecha = nodo_derecho

        # Insertar el nuevo objeto en la cola de prioridad   
        heapq.heappush(cola_prioridad, nuevo_nodo) 
        heapq.heapify(cola_prioridad) 
        
        print("Cola después de heapify:", cola_prioridad,"\n")
        
    # El último objeto es la raíz del árbol
    return cola_prioridad[0]

def asignar_codigos_huffman(nodo, codigo_actual="", codigos={}):
    print(nodo)
    if nodo.simbolo is not None:
        # Si es una hoja, asignar el código actual
        codigos[nodo.simbolo] = codigo_actual
        print(codigo_actual,codigos)
    else:
        # Recorrer el árbol de forma recursiva
        asignar_codigos_huffman(nodo.derecha, codigo_actual + "0", codigos)
        asignar_codigos_huffman(nodo.izquierda, codigo_actual + "1", codigos)
        
    return codigos

# Función principal que integra todo
def codificacion_huffman(frase):
    # Paso 1: Calcular probabilidades
    probabilidades = calcular_probabilidades(frase)
    
    # Paso 2: Crear el árbol de Huffman
    arbol_huffman = crear_arbol_huffman(probabilidades)
    
    # Paso 3: Asignar códigos de Huffman
    codigos_huffman = asignar_codigos_huffman(arbol_huffman)
    
    # Codificar la frase
    frase_codificada = ''.join([codigos_huffman[letra] for letra in frase.replace(" ", "").lower()])
    
    return codigos_huffman, frase_codificada

def intercalar_vectores (vector1, vector2):
    contador = 0
    modulacion = []
    for v1, v2 in zip(vector1, vector2):
        modulacion.extend([v1, v2])
        contador += 2  # Incrementar el contador en 2 por cada iteración 
    #Transformar vector en diccionario
    diccionario = {modulacion[i]: modulacion[i+1] for i in range(0, len(modulacion), 2)}
    contador = 0
    return diccionario 

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