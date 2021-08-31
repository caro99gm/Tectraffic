

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
    contador=0
    origenes=[(0,5),(6,0),(5,11),(11,6)]
    tupla=[]
    while(contador!=cCarros):
        tupla.append(random.choice(origenes))
        contador=contador+1
    return tupla


class agenteSemaforo(ap.Agent):
    def setup (self):
        self.grid = self.model.grid
        self.random = self.model.random
        
    def setupParameters(self, posX, posY, tiempoEspera, tiempoActivo, tiempoAmarillo, luzVerde, luzAmarillo, luzRojo):
        self.posX=posX #int
        self.posY=posY #int
        self.tiempoEspera=tiempoEspera #int (segundos) 
        self.tiempoActivo=tiempoActivo #int (segundos)
        self.tiempoAmarillo=tiempoAmarillo #int (segundos)
        self.luzVerde=luzVerde #bool
        self.luzAmarillo=luzAmarillo #bool
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
        self.posXInicial=coordenada[0]
        self.posZInicial=coordenada[1]
        

    def modificarVelocidad(self, velocidad):
        #acelerar o frenar, depende el caso
        self.velocidad=velocidad
    
    def actualizarPosicion(self):
        #Ir a la izquierda
        if(self.posXInicial==11 and self.posZInicial==6 and self.posX!=0):
            self.posX=self.posX-1
            self.grid.move_by(self, (-1,0))
        
        #ir hacia abajo
        elif(self.posXInicial==5 and self.posZInicial==11 and self.posZ!=0):
            self.posZ=self.posZ-1
            self.grid.move_by(self, (0,-1))
        
        #ir a la derecha 
        elif(self.posXInicial==0 and self.posZInicial==5 and self.posX!=11):
            self.posX=self.posX+1
            self.grid.move_by(self, (1,0))
        
        #ir hacia arriba
        elif(self.posXInicial==6 and self.posZInicial==0 and self.posZ!=11):
            self.posZ=self.posZ+1
            self.grid.move_by(self, (0,1))
        
        
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
        self.grid.add_agents(self.semaforos, positions=[(4,4),(4,7),(7,4),(7,7)])
    

    def step(self):
        # Called at every simulation step
        #self.agents.leerSemaforo(agenteSemaforo)
        #self.agents.detectarVehiculos(agenteVehiculo)
        if(self.vehiculos.select((self.vehiculos.posX < s) or (self.vehiculos.posZ < s))): #HACER QUE SE MUEVAN HASTA QUE LLEGAN A (9,9)
            nueva_velocidad=random.randrange(10)
            self.vehiculos.modificarVelocidad(nueva_velocidad)
            self.vehiculos.actualizarPosicion()
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
    'size':12,
    'velocidad':0,
    'posX':0,
    'posZ':0,
    'agentsCarro':20,
    'agentsSemaforo':4,
    'steps':13,
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