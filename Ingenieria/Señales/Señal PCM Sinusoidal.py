import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la señal
frecuencia = 5       # Frecuencia de la señal en Hz
duracion = 1         # Duración de la señal en segundos
fs = 100             # Frecuencia de muestreo (samples/segundo)
bits_por_muestra = 5 # Resolución en bits

#------------ Generar la señal de onda sinusoidal

# t genera un array de tiempo desde 0.0 con un aumento de 0.01 hasta 1

t = np.linspace(0, duracion + 1/(int(fs * duracion)), int(fs * duracion), endpoint=False)  #inicio, final, Numero de muestras (no debe ser negativo), endpoint = True (se coloca cuando la ultima muestra es el STOP)

señal_original = np.sin(2 * np.pi * frecuencia * t) #Ecuacion de la señal, se puede agregar un offset para no tener que normalizar la grafica

'''señal_original = array([ 0.        ,  0.3120033 ,  0.59285682,  0.81452073,  0.95486454,
        0.99987663,  0.94506308,  0.79589635,  0.56726895,  0.28200658,
       -0.03141076, -0.34169211, -0.61785961, -0.83234127, -0.96372368,
       -0.99888987, -0.93432894, -0.77648651, -0.54112125, -0.25173155,
        0.06279052,  0.37104371,  0.64225265,  0.8493404 ,  0.97163173,
        0.99691733,  0.92267274,  0.75631038,  0.51443953,  0.22120809,
       -0.09410831, -0.40002914, -0.66601187, -0.86550133, -0.9785809 ,
       -0.99396096, -0.91010597, -0.73538786, -0.48725013, -0.19046633,
        0.12533323,  0.42861978,  0.68911381,  0.88080811,  0.98456433,
        0.99002366,  0.89664104,  0.7137396 ,  0.45957986,  0.1595366 ,
       -0.15643447, -0.45678743, -0.71153568, -0.89524565, -0.98957612,
       -0.98510933, -0.88229123, -0.69138697, -0.43145605, -0.12844943,
        0.18738131,  0.48450429,  0.73325535,  0.90879968,  0.99361131,
        0.97922281,  0.8670707 ,  0.66835202,  0.40290644,  0.09723549,
       -0.21814324, -0.511743  , -0.75425138, -0.92145684, -0.99666593,
       -0.97236992, -0.85099448, -0.64465749, -0.37395921, -0.0659256 ,
        0.24868989,  0.53847668,  0.77450306,  0.93320463,  0.99873696,
        0.96455742,  0.83407843,  0.62032676,  0.34464292,  0.03455064,
       -0.27899111, -0.56467895, -0.7939904 , -0.94403146, -0.99982235,
       -0.95579301, -0.81633925, -0.59538384, -0.31498652, -0.00314159])'''

# Normalización para que los valores estén entre 0 y 1 (lo que facilita la cuantización), es como agregarle un offset
señal_normalizada = (señal_original - señal_original.min()) / (señal_original.max() - señal_original.min()) #Se agrega un offset para la señal de muestreo

'''señal_normalizada = array([4.99986428e-01, 6.56011559e-01, 7.96459459e-01, 9.07308096e-01,
       9.77490568e-01, 1.00000000e+00, 9.72589096e-01, 8.97994505e-01,
       7.83663598e-01, 6.41010941e-01, 4.84278684e-01, 3.29114656e-01,
       1.91010118e-01, 8.37531448e-02, 1.80520540e-02, 4.66308892e-04,
       3.27516343e-02, 1.11684729e-01, 2.29385074e-01, 3.74101707e-01,
       5.31386414e-01, 6.85536210e-01, 8.21161094e-01, 9.24720554e-01,
       9.85875424e-01, 9.98520128e-01, 9.61392243e-01, 8.78198542e-01,
       7.57244914e-01, 6.10607124e-01, 4.52925188e-01, 2.99941751e-01,
       1.66930367e-01, 6.71706208e-02, 1.06223228e-02, 2.93113962e-03,
       4.48649434e-02, 1.32237148e-01, 2.56324692e-01, 4.04738927e-01,
       5.62662478e-01, 7.14328580e-01, 8.44595198e-01, 9.40456780e-01,
       9.92342699e-01, 9.95072771e-01, 9.48374432e-01, 8.56909949e-01,
       7.29810949e-01, 5.79766737e-01, 4.21757421e-01, 2.71558331e-01,
       1.44165036e-01, 5.22962230e-02, 5.12388807e-03, 7.35762049e-03,
       5.87744090e-02, 1.54240906e-01, 2.84225932e-01, 4.35752045e-01,
       5.93691189e-01, 7.42275040e-01, 8.66669290e-01, 9.54454670e-01,
       9.96866867e-01, 9.89671535e-01, 9.33587039e-01, 8.34212742e-01,
       7.01469971e-01, 5.48611493e-01, 3.90898389e-01, 2.44076411e-01,
       1.22803969e-01, 3.91886540e-02, 1.57844974e-03, 1.37282822e-02,
       7.44251368e-02, 1.77609163e-01, 3.12978679e-01, 4.67018667e-01,
       6.24350089e-01, 7.69265297e-01, 8.87296251e-01, 9.66658982e-01,
       9.99430076e-01, 9.82337735e-01, 9.17088422e-01, 8.10196496e-01,
       6.72333829e-01, 5.17264349e-01, 3.60469877e-01, 2.17604452e-01,
       1.02931469e-01, 2.78996432e-02, 0.00000000e+00, 2.20179827e-02,
       9.17553607e-02, 2.02249696e-01, 3.42469461e-01, 4.98415398e-01])'''

# Cuantización de la señal, discretizar la señal 
ADC = 2 ** bits_por_muestra  # Número de niveles de cuantización, ** es potencia, ADC = 2 ** 5 = 32
señal_cuantizada = np.round(señal_normalizada * (ADC - 1)) #Se resta 1 para que sean 31 bits y evitar desbordamiento

'''señal_cuantizada = array([15., 20., 25., 28., 30., 31., 30., 28., 24., 20., 15., 10.,  6.,
        3.,  1.,  0.,  1.,  3.,  7., 12., 16., 21., 25., 29., 31., 31.,
       30., 27., 23., 19., 14.,  9.,  5.,  2.,  0.,  0.,  1.,  4.,  8.,
       13., 17., 22., 26., 29., 31., 31., 29., 27., 23., 18., 13.,  8.,
        4.,  2.,  0.,  0.,  2.,  5.,  9., 14., 18., 23., 27., 30., 31.,
       31., 29., 26., 22., 17., 12.,  8.,  4.,  1.,  0.,  0.,  2.,  6.,
       10., 14., 19., 24., 28., 30., 31., 30., 28., 25., 21., 16., 11.,
        7.,  3.,  1.,  0.,  1.,  3.,  6., 11., 15.])
        '''

# Convertir los valores cuantizados a formato binario (PCM)
def decimal_a_binario(numero, bit):
    #return format(int(numero), f'0{bit}b')
    return format(int(numero), f'0{8}b') #Se muestran 8 bits

señal_pcm = [decimal_a_binario(valor, bits_por_muestra) for valor in señal_cuantizada]

'''muestra cuantizada en binario = ['01111', '10100', '11001', '11100', '11110', '11111', '11110', '11100', 
                                    '11000', '10100', '01111', '01010', '00110', '00011', '00001', '00000', 
                                    '00001', '00011', '00111', '01100', '10000', '10101', '11001', '11101', 
                                    '11111', '11111', '11110', '11011', '10111', '10011', '01110', '01001', 
                                    '00101', '00010', '00000', '00000', '00001', '00100', '01000', '01101', 
                                    '10001', '10110', '11010', '11101', '11111', '11111', '11101', '11011', 
                                    '10111', '10010', '01101', '01000', '00100', '00010', '00000', '00000', 
                                    '00010', '00101', '01001', '01110', '10010', '10111', '11011', '11110', 
                                    '11111', '11111', '11101', '11010', '10110', '10001', '01100', '01000', 
                                    '00100', '00001', '00000', '00000', '00010', '00110', '01010', '01110', 
                                    '10011', '11000', '11100', '11110', '11111', '11110', '11100', '11001', 
                                    '10101', '10000', '01011', '00111', '00011', '00001', '00000', '00001', 
                                    '00011', '00110', '01011', '01111']'''

print(señal_pcm)

# Graficar la señal original y cuantizada
plt.figure(figsize=(10, 6))

plt.subplot(3, 1, 1)
plt.plot(t, señal_original, label='Señal Original')
plt.title('Señal Original (Onda Sinusoidal)')
plt.grid(True)
plt.legend()

plt.subplot(3, 1, 2)
#plt.step(t, señal_cuantizada, label='Señal Cuantizada', where='mid')
plt.stem(t, señal_cuantizada, label='Señal Cuantizada')
plt.title(f'Señal Cuantizada con {bits_por_muestra} bits')
plt.grid(True)
plt.legend()

# Mostrar los bits de la señal PCM para un segmento de la señal
plt.subplot(3, 1, 3)
plt.title('Señal PCM (bits)')
for i in range(len(señal_pcm[:10])):
    plt.text(i/fs, 0.5, señal_pcm[i], fontsize=10, ha='center')
plt.xlim(0, 10/fs)
plt.ylim(0, 1)
plt.grid(True)

plt.tight_layout()
plt.show()
