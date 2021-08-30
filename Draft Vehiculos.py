

# Model design
import random
import agentpy as ap
import numpy as np

# Visualization
import matplotlib.pyplot as plt 
import IPython
from random import choice
from IPython.display import HTML

class agenteSemaforo(ap.Agent):
    def setup (self):
        self.grid = self.model.grid
        self.random = self.model.random
        self.group = self.random.choice(range(self.p.n_groups))
        
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
        self.group = self.random.choice(range(self.p.n_groups))
        # Inicializar un agente con parametros

        
    def setupParameters(self, velocidad, posX, posZ):
        self.velocidad = velocidad #bool 
        self.posX=posX #int
        self.posY=0 #int
        self.posZ=posZ #int
        

    def modificarVelocidad(self, velocidad):
        #acelerar o frenar, depende el caso
        self.velocidad=velocidad
    
    def actualizarPosicion(self):
        self.posX=self.posX+1
        self.posZ=self.posZ+1
        #DIFERENCIA ENTRE MOVE TO Y MOVE BY
        #MOVE TO LE DAS LA CORDENADA A DONDE LO QUIERAS MOVER EJ. self.grid.move_by(self, (self.posX,self.posZ)) 
        #MOVE BY DESDE LA CORDENADA DONDE ESTA SE MUEVE EL NUMERO DE ESPACIOS QUE LE DAS EJ. (LO DE ABAJO)
        self.grid.move_by(self, (1,1)) #se mueve uno arriba en x y uno arriba en z
        
    
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
        
        self.grid = ap.Grid(self, (s,s), track_empty=True)
        self.vehiculos = ap.AgentList(self, self.p.agentsCarro, agenteVehiculo)
        self.grid.add_agents(self.vehiculos, positions=[(0,0),(0,0),(0,0)]) #DEFINIR LAS POSICIONES INICIALES DE LOS AGENTES
        self.vehiculos.setupParameters(self.p.velocidad,self.p.posX,self.p.posZ)
        self.semaforos = ap.AgentList(self, self.p.agentsSemaforo, agenteSemaforo)
        self.grid.add_agents(self.semaforos, positions=[(4,4),(6,4),(4,6),(6,6)])
        #self.agents.setupParameters(self.p.velocidad,self.p.posX,self.p.posZ)

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
    'size':10,
    'velocidad':0,
    'posX':0,
    'posZ':0,
    'agentsCarro':3,
    'agentsSemaforo':4,
    'steps':13,
    'n_groups':3
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