from serial import*
from matplotlib import*
import matplotlib.pyplot as plt 
import matplotlib.animation as animation 
from matplotlib.lines import Line2D
import numpy as np


#py -m pip install pyserial

#serial=Serial('/dev/ttyACM0',9600)
serial=Serial('COM9',9600)
cadena=list
cadena=serial.readline().decode('utf-8')

AnchoGrafica = 100 #ancho de la grafica
#Graficas
fig=plt.figure()

ax1=fig.add_subplot(211) #(horizontal,vertical,posicion)
ax2=fig.add_subplot(212)

x=np.linspace(0,1,1)

#vectores para guardar datos del sensor

v1=[]
v2=[]


x=[]

y1=[]
y2=[]

#Codigo de lectura
while True:
    def animacion(i):
        cadena=serial.readline().decode('utf-8')
        
        cadena=np.array(cadena.split(','))

        presion = cadena[0]      
        temperatura = cadena[1]
        
        s1=np.array(presion.split(':'))[-1]
        s2=np.array(temperatura.split(':'))[-1]


        s1=float(s1)
        s2=float(s2)

        v1.insert(0,s1)
        v2.insert(0,s2)

        x.insert(0,i)

        y1.insert(0,s1)
        y2.insert(0,s2)

        print(y1,'\n',y2,'\n')


        if (len(y1)>AnchoGrafica):
            y1.pop()
            y2.pop()
            x.pop()

        ax1.clear()

        ax1.plot(x[0:AnchoGrafica],y1[0:AnchoGrafica],'Red')

        ax2.clear()
        ax2.plot(x[0:AnchoGrafica],y2[0:AnchoGrafica],'Blue')

        ax1.title.set_text('Sensor de Presion')
        ax1.set_xlabel("Tiempo")
        ax1.set_ylabel("Presion")

        ax2.title.set_text('Sensor de Temperatura')
        ax2.set_xlabel("Tiempo")
        ax2.set_ylabel("Temperatura")
        
    anim=animation.FuncAnimation(fig,animacion, interval=1000)    
    plt.show()