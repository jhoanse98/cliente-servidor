"""
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP) # REP -> Reply
socket.bind("tcp://*:5555")

#ip 192.168.9.61


def subirarchivo(nombrearchivo):
    with open (nombrearchivo, 'rb') as archivo:
        data = archivo.read()
        print(data)

    #with open ("archivonuevo.txt" , 'w+') as archivosubido:
     #   archivo = archivosubido.write(data.decode())
      #  print (archivo)

    with open ("archivonuevosss.mp3" , 'w+', errors="ignore") as archivosubido:
        archivo = archivosubido.write(data.decode())
        print (archivo)

#subirarchivo("archivo.txt")


while True:
    #  Wait for next request from client
    #message = socket.recv()
    a1, a2 = socket.recv_multipart()  #operacion bloqueante. bloquea la ejecucion del programa
                                        #existen dos posibilidades . que al socket le llega informacion o no hay nada. Se queda esperando hasta que llegue algo. en caso de recibir algo la operacion sigue. 
    

    if a1 == b'subirarchivo':
        subirarchivo(a2)
        socket.send("Archivo Subido".encode())"""





##############################################################################################################3
###############################################################################################################
###############################################################################################################




'''always listening'''

import zmq
import os
import time
import sys
from math import ceil

context = zmq.Context()
socket = context.socket(zmq.REP) # REP -> Reply
socket.bind("tcp://*:5555")


def subirarchivos(nombrearchivo):
    socket.send(b"subearchivo")
    tamañoarchivo = socket.recv()
    socket.send(b"procediendo a subir archivo")
    for i in range (0,ceil(int(tamañoarchivo)/1024)):
        archivito = socket.recv()
        with open("archivosubido"+file_extension, 'ab') as archivo:
            archivo.write(archivito)
            socket.send(b"ready")


def bajararchivos(nombrearchivobajar):
    filename, file_extension = os.path.splitext(nombrearchivobajar)
    size= os.path.getsize(nombrearchivobajar)
    print(ceil(size/1024))

    socket.send(b"bajararchivos")

    with open (nombrearchivobajar, 'rb') as archivoenviado:
        for i in range(0,ceil(size/1024)): 
            message = socket.recv()
            archivoenviado.seek(i*1024)
            t=archivoenviado.read(1024)
            print("hola server")
            socket.send(t)
            



if __name__ == "__main__":

    while True:
        funcion, archivo= socket.recv_multipart()
        print("hola")
        print(archivo)

        if funcion == b"subirarchivos":
            subirarchivos(archivo.decode())

        if funcion == b"bajararchivos":
            bajararchivos(archivo.decode())



"""

"""





