import heapq
from collections import defaultdict, Counter

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
        return self.probabilidad < otro.probabilidad

def crear_arbol_huffman(probabilidades):
    # Crear una cola de prioridad con nodos
    cola_prioridad = [Nodo(simbolo, probabilidad) for simbolo, probabilidad in probabilidades.items()]
    heapq.heapify(cola_prioridad)
    
    # Crear el árbol de Huffman
    while len(cola_prioridad) > 1:
        # Extraer los dos nodos con menor probabilidad
        nodo_izquierdo = heapq.heappop(cola_prioridad)
        nodo_derecho = heapq.heappop(cola_prioridad)
        
        # Crear un nuevo nodo con la suma de sus probabilidades
        nuevo_nodo = Nodo(None, nodo_izquierdo.probabilidad + nodo_derecho.probabilidad)
        nuevo_nodo.izquierda = nodo_izquierdo
        nuevo_nodo.derecha = nodo_derecho
        
        # Insertar el nuevo nodo en la cola de prioridad
        heapq.heappush(cola_prioridad, nuevo_nodo)
    
    # El último nodo es la raíz del árbol
    return cola_prioridad[0]

def asignar_codigos_huffman(nodo, codigo_actual="", codigos={}):
    if nodo.simbolo is not None:
        # Si es una hoja, asignar el código actual
        codigos[nodo.simbolo] = codigo_actual
    else:
        # Recorrer el árbol de forma recursiva
        asignar_codigos_huffman(nodo.izquierda, codigo_actual + "0", codigos)
        asignar_codigos_huffman(nodo.derecha, codigo_actual + "1", codigos)
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

# Ejemplo de uso
#frase = input("Introduce una frase: ")
frase = ("AAAABBC")
probabilidades = calcular_probabilidades(frase)
codigos_huffman, frase_codificada = codificacion_huffman(frase)

print("\nProbabilidades de cada letra:")
for letra, prob in probabilidades.items():
    print(f"{letra}: {prob:.4f}")

print("\nCódigos de Huffman para cada letra:")
for letra, codigo in codigos_huffman.items():
    print(f"{letra}: {codigo}")

print("\nFrase codificada usando Huffman:")
print(frase_codificada)