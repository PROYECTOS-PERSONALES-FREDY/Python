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
        #self.id = id  # Nuevo atributo para el índice
        self.izquierda = None
        self.derecha = None
    
    def __lt__(self, otro):
        '''# Primero, comparar por valor; si son iguales, comparar por índice
        if self.probabilidad  == otro.probabilidad:
            return self.id > otro.id  # Ordenar más reciente a la derecha'''
        return self.probabilidad < otro.probabilidad #Compara dos objetos, self objeto actual < otro objeto a comparar
    
    # Sobrescribir el método __repr__ para visualizar correctamente
    def __repr__(self):
        return f"Nodo(simbolo={self.simbolo}, probabilidad={self.probabilidad})"

def crear_arbol_huffman(probabilidades):
    aux = []
    i = 0
    # Crear una cola de prioridad con objetos
    cola_prioridad = [Nodo(simbolo, probabilidad*100) for simbolo, probabilidad in probabilidades.items()] #Se hace el diccionario con las letras y la probabilidad
    print("\n Cola antes de heapify:", cola_prioridad)
    heapq.heapify(cola_prioridad) #Organizar de menor a mayor con el constructor __lt__(self, otro):
    print("Cola después de heapify:", cola_prioridad,"\n")
    
    numero_datos = len(cola_prioridad)
    # Crear el árbol de Huffman
    while len(cola_prioridad) > 1:
        
        # Extraer los dos objetos con menor probabilidad nodo
        nodo_izquierdo = heapq.heappop(cola_prioridad)
        nodo_derecho = heapq.heappop(cola_prioridad)
        
        suma_nodo_izquierdo_derecho = nodo_izquierdo.probabilidad + nodo_derecho.probabilidad


        for i in len(cola_prioridad):
            if cola_prioridad[i].probabilidad == suma_nodo_izquierdo_derecho:
                suma_nodo_izquierdo_derecho += 1


        '''while len(cola_prioridad) != 0:
            aux.append(heapq.heappop(cola_prioridad))
            print("vectooor:", aux)
            i +=1'''

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
        asignar_codigos_huffman(nodo.izquierda, codigo_actual + "1", codigos)
        asignar_codigos_huffman(nodo.derecha, codigo_actual + "0", codigos)
        
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
#while(True):
#frase = input("Introduce una frase: ")
contador = 0
frase = ("mi_mama_me_mima")

''' m   1
    A   01
    _   000
    I   0010
    E   0011
'''

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