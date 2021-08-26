

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
        self.agents = ap.AgentList(self, self.p.agents, agenteVehiculo)
        self.grid.add_agents(self.agents, positions=[(0,0),(0,0),(0,0)]) #DEFINIR LAS POSICIONES INICIALES DE LOS AGENTES
        self.agents.setup_parameters(self.p.velocidad,self.p.posX,self.p.posZ)

    def step(self):
        # Called at every simulation step
        #self.agents.leerSemaforo(agenteSemaforo)
        #self.agents.detectarVehiculos(agenteVehiculo)
        if(self.agents.select((self.agents.posX < s) or (self.agents.posZ < s))): #HACER QUE SE MUEVAN HASTA QUE LLEGAN A (9,9)
            nueva_velocidad=random.randrange(10)
            self.agents.modificarVelocidad(nueva_velocidad)
            self.agents.actualizarPosicion()
        #IMPRESION DE LAS POSICIONES DE LOS AGENTES
        for i in self.grid.positions:
            print (self.grid.positions[i])
    
        
    def update(self):
        self.agents.record('posX', self.agents.posX)  # Record variable
        self.agents.record('posZ', self.agents.posZ)

    def end(self):
        # del agents
        # Called at the end of the simulation
        self.report('Distancia recorrida por los vehiculos en el eje x', self.agents.posX)
        self.report('Distancia recorrida por los vehiculos en el eje z', self.agents.posZ)# Report a simulation result
        
parameters = {
    'size':10,
    'velocidad':0,
    'posX':0,
    'posZ':0,
    'agents':3,
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