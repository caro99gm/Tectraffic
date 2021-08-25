

# Model design
import random
import agentpy as ap
import numpy as np

# Visualization
import matplotlib.pyplot as plt 
import IPython
from random import choice
from IPython.display import HTML



class agenteVehiculo(ap.Agent):

    def setup(self):
        self.grid = self.model.grid
        self.random = self.model.random
        self.group = self.random.choice(range(self.p.n_groups))
        # Inicializar un agente con parametros

        
    def setup_parameters(self, velocidad, posX, posZ):
        self.velocidad = velocidad #la considero en km/h
        self.posX=posX #la considero como metros
        self.posY=0 #           =
        self.posZ=posZ #           =
        

    def modificarVelocidad(self, velocidad):
        #acelerar o frenar, depende el caso
        self.velocidad=velocidad
    
    def actualizarPosicion(self):
        desplazamiento=self.velocidad*0.2777 #KM/H a M/S
        self.posX=self.posX+desplazamiento
        self.posZ=self.posZ+desplazamiento
    
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
        s= self.p.size
        
        self.grid = ap.Grid(self, (s,s), track_empty=True)
        self.agents = ap.AgentList(self, self.p.agents, agenteVehiculo)
        self.grid.add_agents(self.agents, random=True, empty=True)
        self.agents.setup_parameters(self.p.velocidad,self.p.posX,self.p.posZ)

    def step(self):
        # Called at every simulation step
        #self.agents.leerSemaforo(agenteSemaforo)
        #self.agents.detectarVehiculos(agenteVehiculo)
        nueva_velocidad=random.randrange(10)
        self.agents.modificarVelocidad(nueva_velocidad)
        self.agents.actualizarPosicion()
    
    def update(self):
        self.agents.record('posX', self.agents.posX)  # Record variable
        self.agents.record('posZ', self.agents.posZ)

    def end(self):
        # del agents
        # Called at the end of the simulation
        self.report('Distancia recorrida por los vehiculos en el eje x', self.agents.posX)
        self.report('Distancia recorrida por los vehiculos en el eje z', self.agents.posZ)# Report a simulation result
        
parameters = {
    'size':100,
    'velocidad':0,
    'posX':choice([0,10]),
    'posZ':choice([0,10]),
    'agents':100,
    'steps':1000,
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