import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import json

# Parámetros de la señal
frecuencia = 5       # Frecuencia de la señal en Hz
duracion = 0.5         # Duración de la señal en segundos
fs = 100             # Frecuencia de muestreo (samples/segundo)

valor_primer_byte = 11111111

bits_por_muestra = 5 # Resolución en bits

# -----------------------------------------------------------
# ----------- Generar la señal de onda sinusoidal ----------- 
# -----------------------------------------------------------

# t genera un array de tiempo desde 0.0 con un aumento de 0.01 hasta 1

t = np.linspace(0, duracion + 1/(int(fs * duracion)), int(fs * duracion), endpoint=False)  #inicio, final, Numero de muestras (no debe ser negativo), endpoint = True (se coloca cuando la ultima muestra es el STOP)
señal_original_sinusoidal = np.sin(2 * np.pi * frecuencia * t) #Ecuacion de la señal, se puede agregar un offset para no tener que normalizar la grafica
# Normalización para que los valores estén entre 0 y 1 (lo que facilita la cuantización), es como agregarle un offset
señal_sinusoidal = (señal_original_sinusoidal - señal_original_sinusoidal.min()) / (señal_original_sinusoidal.max() - señal_original_sinusoidal.min()) #Se agrega un offset para la señal de muestreo

# -----------------------------------------------------------
# ----------- Generar la señal de onda triangular ----------- 
# -----------------------------------------------------------

t = np.linspace(0, duracion, int(fs * duracion), endpoint=False)
señal_original_triangular = signal.sawtooth(2 * np.pi * frecuencia * t, width=0.5)  # Señal triangular
# Normalización para que los valores estén entre 0 y 1 (lo que facilita la cuantización)
señal_triangular = (señal_original_triangular - señal_original_triangular.min()) / (señal_original_triangular.max() - señal_original_triangular.min())

# -----------------------------------------------------------
# ----------- Generar la señal de onda cuadrada ------------- 
# -----------------------------------------------------------

t = np.linspace(0, duracion, int(fs * duracion), endpoint=False)
señal_original_cuadrada = signal.square(2 * np.pi * frecuencia * t)  # Señal cuadrada
# Normalización para que los valores estén entre 0 y 1 (lo que facilita la cuantización)
señal_cuadrada = (señal_original_cuadrada - señal_original_cuadrada.min()) / (señal_original_cuadrada.max() - señal_original_cuadrada.min())

# -----------------------------------------------------------------------
# ----------- Cuantización de la señal, discretizar la señal  ----------- 
# -----------------------------------------------------------------------

ADC = 2 ** bits_por_muestra  # Número de niveles de cuantización, ** es potencia, ADC = 2 ** 5 = 32

# Convertir los valores cuantizados a formato binario (PCM)
def decimal_a_binario(numero, bit):
    return format(int(numero), f'0{8}b') #Se muestran 8 bits

def señal_cuantizada_normalizada(señal):
    señal_normalizada = np.round(señal * (ADC - 1)) #Se resta 1 para que sean 31 bits y evitar desbordamiento
    señal_cuantizada  = [decimal_a_binario(valor, bits_por_muestra) for valor in señal_normalizada]
    return señal_cuantizada , señal_normalizada

def intercalar_vectores (primer_byte,vector1, vector2, vector3):
    modulacion = [primer_byte]
    contador = 0
    limite_maximo = len(t)
    for v1, v2, v3 in zip(vector1, vector2, vector3):
        if contador < limite_maximo: # Verificar si aún no se ha alcanzado el límite
            modulacion.extend([v1, v2, v3])
            contador += 3  # Incrementar el contador en 3 por cada iteración
    # Cortar la lista al límite máximo si excede
    modulacion = modulacion[:limite_maximo]  # +1 para incluir el valor inicial
    return modulacion 
   
señal_cuantizada_sinusoidal , señal_normalizada_sinusoidal  = señal_cuantizada_normalizada(señal_sinusoidal)
señal_cuantizada_triangular , señal_normalizada_triangular  = señal_cuantizada_normalizada(señal_triangular)
señal_cuantizada_cuadrada   , señal_normalizada_cuadrada    = señal_cuantizada_normalizada(señal_cuadrada)

bytes_modulados = intercalar_vectores(valor_primer_byte,señal_cuantizada_sinusoidal,señal_cuantizada_triangular,señal_cuantizada_cuadrada)
señal_modulada = intercalar_vectores('',señal_normalizada_sinusoidal.astype(str),señal_normalizada_triangular.astype(str),señal_normalizada_cuadrada.astype(str))



# Especificar el nombre del archivo JSON
nombre_archivo = 'modulacion_PCM.json'

# Generar el archivo JSON
with open(nombre_archivo, 'w') as archivo_json:
    json.dump(bytes_modulados, archivo_json)

# Graficar la señal original y cuantizada

plt.figure(figsize=(10, 8))

#Grafica señal sinusoidal
plt.subplot(4, 2, 1)
plt.plot(t, señal_original_sinusoidal)
plt.title('Señal Original (Onda Sinusoidal)')
plt.grid(True)

plt.subplot(4, 2, 2)
plt.stem(t, señal_normalizada_sinusoidal, basefmt=' ',markerfmt='g' ,linefmt='g')
plt.title(f'Señal Cuantizada con {bits_por_muestra} bits')
plt.ylim(0,35)
plt.grid(True)

#Grafica señal triangular
plt.subplot(4, 2, 3)
plt.plot(t, señal_original_triangular)
plt.title('Señal Original (Onda Triangular)')
plt.grid(True)

plt.subplot(4, 2, 4)
plt.stem(t, señal_normalizada_triangular, basefmt=' ',markerfmt='m' ,linefmt='m')
plt.title(f'Señal Cuantizada con {bits_por_muestra} bits')
plt.ylim(0,35)
plt.grid(True)

#Grafica señal cuadrada
plt.subplot(4, 2, 5)
plt.plot(t, señal_original_cuadrada)
plt.title('Señal Original (Onda Cuadrada)')
plt.grid(True)

plt.subplot(4, 2, 6)
plt.stem(t, señal_normalizada_cuadrada, basefmt=' ',markerfmt='r' ,linefmt='r')
plt.title(f'Señal Cuantizada con {bits_por_muestra} bits')
plt.ylim(0,35)
plt.grid(True)

plt.subplot(4, 1, 4)
plt.stem(t, señal_modulada, basefmt=' ',markerfmt='r' ,linefmt='r')
plt.title(f'Señal Cuantizada con {bits_por_muestra} bits')
plt.grid(True)

plt.tight_layout()
plt.show()
