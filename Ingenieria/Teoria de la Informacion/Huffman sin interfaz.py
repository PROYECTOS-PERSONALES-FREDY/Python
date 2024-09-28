import heapq
from collections import Counter
import math

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
    entropia = sum(p * math.log2(1/p) for p in probabilidades.values())
    return entropia

# Paso 4: Calcular el largo medio
def calcular_largo_medio(probabilidades, longitudes_codigos):
    largo_medio = sum(probabilidades[s] * longitudes_codigos[s] for s in probabilidades)
    return largo_medio

# Paso 5: Calcular la eficiencia
def calcular_eficiencia(entropia, largo_medio):
    if largo_medio > 0:
        eficiencia = entropia / largo_medio
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


def main():
    #frase = ("AAAAABCDDE")
    #frase = input("Introduce una frase: ")
    frase = ("mi_mama_me_mima")
    ''' m   1
        _   01
        A   000
        I   0010
        E   0011
    '''
    # Calcular probabilidades
    probabilidades = calcular_probabilidades(frase)
    # Codigo Huffman
    codigos_huffman, frase_codificada = codificacion_huffman(frase)
    # Calcular entropía
    entropia = calcular_entropia(probabilidades)
    
    '''# Calcular largo medio
    largo_medio = calcular_largo_medio(probabilidades, longitudes_codigos)
    # Calcular eficiencia
    eficiencia = calcular_eficiencia(entropia)'''

    print("\nProbabilidades de cada letra: ")
    for letra, prob in probabilidades.items():
        print(f"{letra}: {prob:.4f}")

    print("\nCódigos de Huffman para cada letra: ")
    for letra, codigo in codigos_huffman.items():
        print(f"{letra}: {codigo}")

    print("\nFrase codificada usando Huffman: ")
    print(frase_codificada)
    
    print("\nEntropía: ")
    print(entropia)
    
    '''
    print("\nLargo medio: ")
    #print(largo_medio)
    
    print("\nEficiencia: ")
    print(eficiencia)
    '''
    
if __name__ == "__main__":
    main()