# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python server to interact with Unity
# Sergio. Julio 2021
# Actualización Lorena Martínez Agosto 2021

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
# import nuestros agentes
import RetoVehiculos

import numpy as np


# Size of the board:
width = 30
height = 30

# Importa tu lógica de agentes aqui:
parameters = {
    'size':16,
    'agentsCarro':20,
    'agentsSemaforo':4,
    'steps':200,
}

model = RetoVehiculos.modeloVehiculo(parameters)
model.setup()

def updatePositions():
    model.step()
    model.update()
    positions= model.getPosition()
    return positions


#Esta función convierte a json una secuencia
def positionsToJSON(ps):
    posDICT = []
    for p in ps:
        pos = {
            "x" : p[0],
            "z" : p[1],
            "y" : 0.5
        }
        posDICT.append(pos)
    return json.dumps(posDICT)

#El rey del server:
class Server(BaseHTTPRequestHandler):
    
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        #post_data = self.rfile.read(content_length)
        post_data = json.loads(self.rfile.read(content_length))
        #logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     #str(self.path), str(self.headers), post_data.decode('utf-8'))
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), json.dumps(post_data))
        
        # AQUI ACTUALIZA LO QUE SE TENGA QUE ACTUALIZAR
        positions = updatePositions()
        self._set_response()
        #AQUI SE MANDA EL SHOW
        # positions es el json
        # agregar el codigo para hacer el json dentro del step
        resp = "{\"data\":" + positionsToJSON(positions) + "}"
        #print(resp)
        # logging.info("Respuesta: " + resp)
        self.wfile.write(resp.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=Server, port=8585):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n") # HTTPD is HTTP Daemon!
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:   # CTRL+C stops the server
        pass
    httpd.server_close()
    logging.info("Stopping httpd...\n")

if __name__ == '__main__':
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()