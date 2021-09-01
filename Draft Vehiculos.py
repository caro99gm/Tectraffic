
primerIzquierdo=True
primerDerecho=True
primerArriba=True
primerAbajo=True
XSEMAFORO=6
YSEMAFORO=9
CERO=0
QUINCE=15
SIETE=7
OCHO=8

# Model design
import random
import agentpy as ap
import numpy as np

# Visualization
import matplotlib.pyplot as plt 
import IPython
from random import choice
from IPython.display import HTML

def llenarTuplaPosicionesCarros(cCarros):
    global SIETE, OCHO, CERO, QUINCE
    contador=0
    origenes=[(CERO,SIETE),(OCHO,CERO),(SIETE,QUINCE),(QUINCE,OCHO)]
    tupla=[]
    while(contador!=cCarros):
        tupla.append(random.choice(origenes))
        contador=contador+1
    return tupla        
    

def carroIzquierda(inicioX, inicioZ, condicion):
    global OCHO, CERO, QUINCE
    if(inicioX==QUINCE and inicioZ==OCHO and condicion!=CERO):
        return True
    else:
        return False
    
def carroDerecha(inicioX, inicioZ, condicion):
    global SIETE, CERO, QUINCE
    if(inicioX==CERO and inicioZ==SIETE and condicion!=QUINCE):
        return True
    else:
        return False
    
def carroArriba(inicioX, inicioZ, condicion):
    global OCHO, CERO, QUINCE
    if(inicioX==OCHO and inicioZ==CERO and condicion!=QUINCE):
        return True
    else:
        return False
    
def carroAbajo(inicioX, inicioZ, condicion):
    global SIETE, CERO, QUINCE
    if(inicioX==SIETE and inicioZ==QUINCE and condicion!=CERO):
        return True
    else:
        return False
"""   
def primerCarro(x,z,x2):
    global primerIzquierdo, primerDerecho, primerArriba, primerAbajo
    if(carroIzquierda(x,z,x2) and primerIzquierdo):
        primerIzquierdo=False
        return True
    elif(carroDerecha(x,z,x2) and primerDerecho):
        primerDerecho=False
        return True
    elif(carroArriba(x,z,x2) and primerArriba):
        primerArriba=False
        return True
    elif(carroAbajo(x,z,x2) and primerAbajo):
        primerAbajo=False
        return True
    else:
        return False

"""
class agenteSemaforo(ap.Agent):
    def setup (self):
        self.grid = self.model.grid
        self.random = self.model.random
        
    def setupParameters(self, posX, posY, tiempoEspera, tiempoActivo, tiempoAmarillo, luzVerde, luzAmarillo, luzRojo):
        self.posX=posX #int
        self.posY=posY #int
        self.tiempoEspera=tiempoEspera #int (segundos) 
        self.tiempoActivo=tiempoActivo #int (segundos)
        self.luzVerde=luzVerde #bool
        self.luzRojo=luzRojo#bool
        #self.semaforos[]=semaforos #array de semaforos, para comunicarse con otros agentes
        
    def actualizarTiempoEspera(self):
        total=0
        #for i in self.semaforos:
            #total= total + self.semaforos[i].tiempoActivo
        tiempoEspera=total
        
    def actualizarTiempoActivo(self, cantidadDeVehiculos):
        self.tiempoActivo=cantidadDeVehiculos*5
        
    def actualizarTiempos(cantidadDeVehiculos):
        self.actualizarTiempoActivo(cantidadDeVehiculos)
        self.actualizarTiempoEspera()
        
    #def encenderLuzVerde():
        
    #def encenderLuzAmarilla():
    
    #def encenderLuzRoja():
            
    def prenderSemaforo():
        self.actualizarTiempos(cantidadDeVehiculos)
        #self.encenderLuzVerde()
        #self.encenderLuzAmarilla()
        #self.encenderLuzRoja()
        
        
class agenteVehiculo(ap.Agent):

    def setup(self):
        self.grid = self.model.grid
        self.random = self.model.random
        # Inicializar un agente con parametros

        
    def setupParameters(self, velocidad, coordenada):
        self.velocidad = velocidad #bool 
        self.posX=coordenada[0] #int
        self.posY=0 #int
        self.posZ=coordenada[1] #int
        self.posXInicial=coordenada[0] #int nunca cambia
        self.posZInicial=coordenada[1] #int nunca cambia
        #if(primerCarro(self.posXInicial, self.posZInicial, self.posX)):
            #self.actualizarPosicion()
        

    def modificarVelocidad(self, velocidad):
        #acelerar o frenar, depende el caso
        self.velocidad=velocidad
    
    def actualizarPosicion(self):
        #Ir a la izquierda
        if(carroIzquierda(self.posXInicial, self.posZInicial, self.posX)):
            self.posX=self.posX-1
            self.grid.move_by(self, (-1,0))
        
        #ir hacia abajo
        elif(carroAbajo(self.posXInicial, self.posZInicial, self.posZ)):
            self.posZ=self.posZ-1
            self.grid.move_by(self, (0,-1))
        
        #ir a la derecha 
        elif(carroDerecha(self.posXInicial, self.posZInicial, self.posX)):
            self.posX=self.posX+1
            self.grid.move_by(self, (1,0))
        
        #ir hacia arriba
        elif(carroArriba(self.posXInicial, self.posZInicial, self.posZ)):
            self.posZ=self.posZ+1
            self.grid.move_by(self, (0,1))
            
        
    
    def choque(self):
        agentes=self.grid.neighbors(self, distance=1)
        for i in agentes:
            if(str(type(i))=="<class '__main__.agenteVehiculo'>"):
                #Ir a la izquierda
                if(carroIzquierda(self.posXInicial, self.posZInicial, self.posX)): #ej self(11,6) i(10,6)
                    if(self.posX-i.posX==1):
                        return True
                    
                #ir hacia abajo
                elif(carroAbajo(self.posXInicial, self.posZInicial, self.posZ)): #eje self (0,1) i(0,0)
                    if(self.posZ-i.posZ==1):
                        
                        return True
                    
                #ir a la derecha 
                elif(carroDerecha(self.posXInicial, self.posZInicial, self.posX)): #ej self(0,0) i(1,0)
                    #print(i.posX-self.posX)
                    if(self.posX-i.posX==-1):
                        
                        return True
                    
                #ir hacia arriba
                elif(carroArriba(self.posXInicial, self.posZInicial, self.posZ)): #
                    if(self.posZ-i.posZ==-1):
                        return True
        return False
        
        
        #DIFERENCIA ENTRE MOVE TO Y MOVE BY
        #MOVE TO LE DAS LA CORDENADA A DONDE LO QUIERAS MOVER EJ. self.grid.move_by(self, (self.posX,self.posZ)) 
        #MOVE BY DESDE LA CORDENADA DONDE ESTA SE MUEVE EL NUMERO DE ESPACIOS QUE LE DAS EJ. (LO DE ABAJO)
        #self.grid.move_by(self, (1,1)) #se mueve uno arriba en x y uno arriba en z
        
    
    #def leerSemaforo(self, agenteSemaforo):
         # semaforo.light 1 = verde, 2 = rojo, 3 = amarillo
        #if semaforo.light == 1:
           # modificarVelocidad(self,40)
       # elif (semaforo.light == 2 or semaforo.light == 3):
            #modificarVelocidad(self,0)
        
    #quitar la comunicacion
    #def detectarVehiculos(self, agenteVehiculo):
        #definimos la distancia entre dos coches
        #distanciaX=abs(self.posX-agenteVehiculo.posX)
        #distanciaZ=abs(self.posZ-agenteVehiculo.posZ)
        #en el caso de luz 1=on, 0=off
        #if (distanciaX<=10 or luz==1 or distanciaZ<=10):
            #modificarVelocidad(self,0)
    

class modeloVehiculo(ap.Model):

    def setup(self):
        # Called at the start of the simulation
        global s
        global XSEMAFORO
        global YSEMAFORO
        s= self.p.size
        origenCarros=llenarTuplaPosicionesCarros(self.p.agentsCarro)
        
        self.grid = ap.Grid(self, (s,s), track_empty=True)
        
        self.vehiculos = ap.AgentList(self, self.p.agentsCarro, agenteVehiculo)
        self.grid.add_agents(self.vehiculos, positions=origenCarros) #DEFINIR LAS POSICIONES INICIALES DE LOS AGENTES
        
        contador=0
        for i in self.grid.positions:
            self.vehiculos[contador].setupParameters(0,self.grid.positions[i])
            contador=contador+1
        
        self.semaforos = ap.AgentList(self, self.p.agentsSemaforo, agenteSemaforo)
        self.grid.add_agents(self.semaforos, positions=[(XSEMAFORO,XSEMAFORO),(XSEMAFORO,YSEMAFORO),(YSEMAFORO,XSEMAFORO),(YSEMAFORO,YSEMAFORO)])
    

    def step(self):
        # Called at every simulation step
        #self.agents.leerSemaforo(agenteSemaforo)
        #self.agents.detectarVehiculos(agenteVehiculo)
        nueva_velocidad=random.randrange(10)
        self.vehiculos.modificarVelocidad(nueva_velocidad)
        for i in self.grid.positions:
            if(str(type(i))=="<class '__main__.agenteVehiculo'>"):
                if(i.choque()):
                    print("no pasa nada")
                else:
                    i.actualizarPosicion()
        #IMPRESION DE LAS POSICIONES DE LOS AGENTES
        for i in self.grid.positions:
            print (self.grid.positions[i])
    
        
    def update(self):
        self.vehiculos.record('posX', self.vehiculos.posX)  # Record variable
        self.vehiculos.record('posZ', self.vehiculos.posZ)

    def end(self):
        # del agents
        # Called at the end of the simulation
        self.report('Distancia recorrida por los vehiculos en el eje x', self.vehiculos.posX)
        self.report('Distancia recorrida por los vehiculos en el eje z', self.vehiculos.posZ)# Report a simulation result
        
parameters = {
    'size':16,
    'velocidad':0,
    'posX':0,
    'posZ':0,
    'agentsCarro':20,
    'agentsSemaforo':4,
    'steps':10,
}


model = modeloVehiculo(parameters)
#animation = ap.animate(ModeloVehiculo, fig, ax, my_plot)

results = model.run()

#results = exp.run()
print("Impresion de la info del tipo de dato result")
print(results)
print("Impresion de la info del reporte en result")
print(results.reporters)
print("Impresion de la información de la simulación")
print(results.info)
#sample = ap.Sample(parameters, n=5)
#exp = ap.Experiment(modeloVehiculo, sample, iterations=2, record=True)

#HTML(animation.to_jshtml())