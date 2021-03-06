#Romel Aldair Vázquez Molina A01700519
#Carolina Gómez Manzano A01632229
#David Sánchez Magaña A01720476
#Jose A. Kaun Sada A01720829


#Implementación de agentes en Python
#Avance 3

#Descripción general:
#En este avance el agente carro ya está al 90% de sus funcionalidades
#El agente semaforo está al 50% de sus funcionalidades

#Interacciones implementadas al momento:
#El agente carro evita colisiones con otros agentes carro
#El agente semaforo prende y apaga sus luces verdes y rojas
#El agente carro puede ver el semaforo y avanza si la luz es verde, de otra forma se detiene
#Al finalizar el recorrido, el agente se reposiciona en nuevas coordenadas para hacer un nuevo recorrido

#SE PUEDE MODIFICAR DE LOS PARAMETROS
#steps
#agentsCarro

#LIMITES
#No poner más de 20 agentes carro
#No modificar el tamaño de la malla, ese es fijo
#No modificar la cantidad de agentes semaforo

#Output
#se imprime la posición de cada agente a en cada agente
#Se imprime cuando un agente finaliza un recorrido

#VARIABLES GLOBALES
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
SEIS=6
NUEVE=9

# Model design
import random
import agentpy as ap
import numpy as np

# Visualization
import matplotlib.pyplot as plt 
import IPython
from random import choice
from IPython.display import HTML

def funcionVacia():
    return True

def SemaforoSeisSeis(inicioX, inicioZ):
    global SEIS
    if(inicioX==SEIS and inicioZ==SEIS):
        return True
    else:
        return False

def SemaforoSeisNueve(inicioX, inicioZ):
    global SEIS, NUEVE
    if(inicioX==SEIS and inicioZ==NUEVE):
        return True
    else:
        return False
    
def SemaforoNueveNueve(inicioX, inicioZ):
    global NUEVE
    if(inicioX==NUEVE and inicioZ==NUEVE):
        return True
    else:
        return False
    
def SemaforoNueveSeis(inicioX, inicioZ):
    global NUEVE, SEIS
    if(inicioX==NUEVE and inicioZ==SEIS):
        return True
    else:
        return False
    


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
        
    def setupParameters(self, coordenada, tiempoEspera, tiempoActivo, luzVerde, luzRojo):
        self.posX=coordenada[0] #int
        self.posZ=coordenada[1] #int
        self.tiempoEspera=tiempoEspera #int (segundos) 
        self.tiempoActivo=tiempoActivo #int (segundos)
        self.luzVerde=luzVerde #bool
        self.luzRojo=luzRojo#bool
        self.contar=False
        self.actualizar=False
        #self.semaforos[]=semaforos #array de semaforos, para comunicarse con otros agentes
        
    #def actualizarTiempoEspera(self):
        #total=0
        #for i in self.semaforos:
            #total= total + self.semaforos[i].tiempoActivo
        #tiempoEspera=total
        
    #def actualizarTiempoActivo(self, cantidadDeVehiculos):
        #self.tiempoActivo=cantidadDeVehiculos*5
        
    #def actualizarTiempos(cantidadDeVehiculos):
        #self.actualizarTiempoActivo(cantidadDeVehiculos)
        #self.actualizarTiempoEspera()
        
    #def encenderLuzVerde():
        
    #def encenderLuzAmarilla():
    
    #def encenderLuzRoja():
            
    def actualizarLuces(self):
        condicion=True
        if(self.luzRojo):
            if(self.tiempoEspera>=0):
                if(self.tiempoEspera==0):
                    agentes=self.grid.neighbors(self, distance=5)
                    for i in agentes:
                        if(isinstance(i,agenteSemaforo)):
                            if(i.luzVerde):
                                condicion=False
                    if(condicion):
                    #self.tiempoActivo=5
                        self.luzVerde=True
                        self.luzRojo=False
                else:
                    self.tiempoEspera=self.tiempoEspera-1
                    
            
        elif(self.luzVerde):
            if(self.tiempoActivo>=0):
                if(self.tiempoActivo==0):
                    self.tiempoEspera=self.tiempoEspera+2
                    self.luzVerde=False
                    self.luzRojo=True
                    agentes=self.grid.neighbors(self, distance=5)
                    for i in agentes:
                        if(isinstance(i,agenteSemaforo)):
                            if(SemaforoSeisSeis(i.posX, i.posZ) and SemaforoNueveNueve(self.posX, self.posZ)): 
                                i.contar=True
                                i.actualizar=True
                        
                   
                            elif(SemaforoNueveSeis(i.posX, i.posZ) and SemaforoSeisNueve(self.posX, self.posZ)): 
                                i.contar=True
                                i.actualizar=True
                        
                  
                            elif(SemaforoSeisNueve(i.posX, i.posZ) and SemaforoSeisSeis(self.posX, self.posZ)): 
                                i.contar=True
                                i.actualizar=True
                        
                   
                            elif(SemaforoNueveNueve(i.posX, i.posZ) and SemaforoNueveSeis(self.posX, self.posZ)): 
                                i.contar=True
                                i.actualizar=True
                else:
                    self.tiempoActivo=self.tiempoActivo-1
            
        #self.actualizarTiempos(cantidadDeVehiculos)
        #self.encenderLuzVerde()
        #self.encenderLuzAmarilla()
        #self.encenderLuzRoja()
        
        #def contarcarros
            #para cada vecino a 5 vecino a 5 metros
               #que sea un vehiculo
                    #que la distancia en Y o X sea 0
                        #contador++
    def contarCarros(self):
        if (self.contar==True):
            self.contar=False
            agentes=self.grid.neighbors(self, distance=5)
            for i in agentes:
                if(isinstance(i,agenteVehiculo)):
                    if(carroIzquierda(i.posXInicial, i.posZInicial, i.posX) and SemaforoNueveNueve(self.posX, self.posZ)): #ej self(11,6) i(10,6)
                        if(i.posX in range (9, 14)):
                            self.tiempoActivo=self.tiempoActivo+1
                        
                    #ir hacia abajo
                    elif(carroAbajo(i.posXInicial, i.posZInicial, i.posZ) and SemaforoSeisNueve(self.posX, self.posZ)): #eje self (0,1) i(0,0)
                        if(i.posZ in range (9, 14)):
                            self.tiempoActivo=self.tiempoActivo+1
                        
                    #ir a la derecha 
                    elif(carroDerecha(i.posXInicial, i.posZInicial, i.posX) and SemaforoSeisSeis(self.posX, self.posZ)): #ej self(0,0) i(1,0)
                        if(i.posX in range (2, 7)):
                            self.tiempoActivo=self.tiempoActivo+1
                        
                    #ir hacia arriba
                    elif(carroArriba(i.posXInicial, i.posZInicial, i.posZ) and SemaforoNueveSeis(self.posX, self.posZ)): #
                        if(i.posZ in range (2, 7)):
                            self.tiempoActivo=self.tiempoActivo+1
                
    def actualizarTiempos(self):
        if(self.actualizar==True):
            self.actualizar=False
            agentes=self.grid.neighbors(self, distance=4)
            for i in agentes:
                if(isinstance(i,agenteSemaforo)):
                    i.tiempoEspera=i.tiempoEspera+self.tiempoActivo
            #para cada vecino a 4 metros
                #que sea un semaforo
                    #tiempo de espera en nuevo semaforo=ese tiempo + contador del semaforo self
        
class agenteVehiculo(ap.Agent):

    def setup(self):
        self.grid = self.model.grid
        self.random = self.model.random
        # Inicializar un agente con parametros

        
    def setupParameters(self, coordenada):
        self.posX=coordenada[0] #int
        self.posY=0 #int
        self.posZ=coordenada[1] #int
        self.posXInicial=coordenada[0] #int nunca cambia
        self.posZInicial=coordenada[1] #int nunca cambia
        self.primerSemaforo=True
        self.vueltas=0
        #if(primerCarro(self.posXInicial, self.posZInicial, self.posX)):
            #self.actualizarPosicion()
    
    
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
            if(isinstance(i,agenteVehiculo)):
                #Ir a la izquierda
                if(carroIzquierda(self.posXInicial, self.posZInicial, self.posX)): #ej self(11,6) i(10,6)
                    if(self.posX-i.posX==1 and self.posZ-i.posZ==0):
                        return True
                    
                #ir hacia abajo
                elif(carroAbajo(self.posXInicial, self.posZInicial, self.posZ)): #eje self (0,1) i(0,0)
                    if(self.posZ-i.posZ==1 and self.posX-i.posX==0):
                        
                        return True
                    
                #ir a la derecha 
                elif(carroDerecha(self.posXInicial, self.posZInicial, self.posX)): #ej self(0,0) i(1,0)
                    #print(i.posX-self.posX)
                    if(self.posX-i.posX==-1 and self.posZ-i.posZ==0):
                        
                        return True
                    
                #ir hacia arriba
                elif(carroArriba(self.posXInicial, self.posZInicial, self.posZ)): #
                    if(self.posZ-i.posZ==-1 and self.posX-i.posX==0):
                        return True
        return False
    
    def verSemaforo(self):
        if(self.primerSemaforo):
            agentes=self.grid.neighbors(self, distance=1)
            for i in agentes:
                if(isinstance(i,agenteSemaforo)):
                    #print(i, i.luzRojo)
                    if(i.luzRojo):
                        
                        return True
                        
        
        return False
    def end(self):
        global QUINCE, OCHO, SIETE, CERO
        origenes=[(CERO,SIETE),(OCHO,CERO),(SIETE,QUINCE),(QUINCE,OCHO)]
        nuevaPos=random.choice(origenes)
        if(carroIzquierda(self.posXInicial, self.posZInicial, 1)): #ej self(11,6) i(10,6)
            if(self.posX==CERO):
                self.posX=nuevaPos[0]
                self.posZ=nuevaPos[1]
                self.posXInicial=nuevaPos[0]
                self.posZInicial=nuevaPos[1]
                self.grid.move_to(self, (self.posX,self.posZ))
                self.vueltas=self.vueltas+1
                self.primerSemaforo=True
                return True
                    
                #ir hacia abajo
        elif(carroAbajo(self.posXInicial, self.posZInicial, 1)): #eje self (0,1) i(0,0)
            if(self.posZ==CERO):
                self.posX=nuevaPos[0]
                self.posZ=nuevaPos[1]
                self.posXInicial=nuevaPos[0]
                self.posZInicial=nuevaPos[1]
                self.grid.move_to(self, (self.posX,self.posZ))
                self.vueltas=self.vueltas+1
                self.primerSemaforo=True
                return True
                    
                #ir a la derecha 
        elif(carroDerecha(self.posXInicial, self.posZInicial, 1)): #ej self(0,0) i(1,0)
            if(self.posX==QUINCE):
                self.posX=nuevaPos[0]
                self.posZ=nuevaPos[1]
                self.posXInicial=nuevaPos[0]
                self.posZInicial=nuevaPos[1]
                self.grid.move_to(self, (self.posX,self.posZ))
                self.vueltas=self.vueltas+1
                self.primerSemaforo=True
                return True
                    
                #ir hacia arriba
        elif(carroArriba(self.posXInicial, self.posZInicial, 1)): #
            if(self.posZ==QUINCE):
                self.posX=nuevaPos[0]
                self.posZ=nuevaPos[1]
                self.posXInicial=nuevaPos[0]
                self.posZInicial=nuevaPos[1]
                self.grid.move_to(self, (self.posX,self.posZ))
                self.vueltas=self.vueltas+1
                self.primerSemaforo=True
                return True
        return False
    
    def desactivarPrimerSemaforo(self):
        coordenadas=[(SIETE,SIETE),(SIETE,OCHO),(OCHO,SIETE),(OCHO,OCHO)]
        for i in coordenadas:
            if(self.posX==i[0] and self.posZ==i[1]):
                self.primerSemaforo=False
        
        
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
        
    

class modeloVehiculo(ap.Model):

    def setup(self):
        # Called at the start of the simulation
        global s
        global XSEMAFORO
        global YSEMAFORO
        s= self.p.size
        origenCarros=llenarTuplaPosicionesCarros(self.p.agentsCarro)
        cantidadCarros=self.p.agentsCarro
        
        self.grid = ap.Grid(self, (s,s), track_empty=True)
        
        self.vehiculos = ap.AgentList(self, self.p.agentsCarro, agenteVehiculo)
        self.grid.add_agents(self.vehiculos, positions=origenCarros) #DEFINIR LAS POSICIONES INICIALES DE LOS AGENTES
        
        self.semaforos = ap.AgentList(self, self.p.agentsSemaforo, agenteSemaforo)
        self.grid.add_agents(self.semaforos, positions=[(XSEMAFORO,XSEMAFORO),(XSEMAFORO,YSEMAFORO),(YSEMAFORO,XSEMAFORO),(YSEMAFORO,YSEMAFORO)])
        
        contador=0
        condicion=True
        for i in self.grid.positions:
            if(condicion):
                self.vehiculos[contador].setupParameters(self.grid.positions[i])
                if(contador==cantidadCarros-1):
                    condicion=False
                    contador=-1
            else:
                if(contador==0):
                    self.semaforos[contador].setupParameters(self.grid.positions[i], (contador*3), 3, True, False) #como tiempo de espera es 0, tiene que estar prendida la luz verde
                else:
                    self.semaforos[contador].setupParameters(self.grid.positions[i], (contador*3)+2, 0, False, True)
            contador=contador+1
    

    def step(self):
        # Called at every simulation step
        #self.agents.leerSemaforo(agenteSemaforo)
        #self.agents.detectarVehiculos(agenteVehiculo)
        print(" ")
        
        #para cada semaforo
            #semaforo cuenta vehiculos y actualiza propio tiempo Activo
        
        #para cada semaforo
            #semaforo actualiza tiempo de espera de otros semaforo
            
        for i in self.grid.positions:
            if(isinstance(i,agenteVehiculo)):
                i.desactivarPrimerSemaforo()
                if(i.end()==False):
                #Falta meter un if para cuando el carro llegue a la interseccion y ponga self.primerSemaforo=false
                    if (i.choque() or i.verSemaforo()):
                        funcionVacia()
                    else:
                        i.actualizarPosicion()
                        #print(i, i.posX, i.posZ)
                else:
                    funcionVacia()
                    #print("")
                    #print(i," ","Contador vueltas: ",i.vueltas)
            elif(isinstance(i,agenteSemaforo)):
                i.contarCarros()
                i.actualizarTiempos()
                i.actualizarLuces()
               
        self.posc=self.grid.positions.values()
        
        #IMPRESION DE LAS POSICIONES DE LOS AGENTES
        for i in self.grid.positions:
            if(isinstance(i,agenteVehiculo)):
                funcionVacia()
                #print (i,"coordenadas: ",self.grid.positions[i])
            elif(isinstance(i,agenteSemaforo)):
                funcionVacia()
                #print(i, i.posX, i.posZ,"verde: " ,i.luzVerde)
                #print(i, i.posX, i.posZ,"Rojo: " ,i.luzRojo)
                #print(i,"(",i.posX," ",i.posZ,")"," Activo: ",i.tiempoActivo)
                #print(i," Espera:",i.tiempoEspera)
            #if(str(type(i))=="<class '__main__.agenteSemaforo'>"):
                #print (i.luzVerde)
    
        
    def update(self):
        self.vehiculos.record('vueltas', self.vehiculos.vueltas)
        self.vehiculos.record('posX', self.vehiculos.posX)  # Record variable
        self.vehiculos.record('posZ', self.vehiculos.posZ)
        
    def getPosition(self):
        return self.posc


    def end(self):
        # del agents
        # Called at the end of the simulation
        self.report('Vueltas al circuito', self.vehiculos.vueltas)
        self.report('eje x', self.vehiculos.posX)
        self.report('eje z', self.vehiculos.posZ)# Report a simulation result
        
parameters = {
    'size':16,
    'agentsCarro':10,
    'agentsSemaforo':4,
    'steps':200,
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