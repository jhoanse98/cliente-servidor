import zmq
import os
import time
import sys
from math import ceil

context = zmq.Context()
socket = context.socket(zmq.REP) # REP -> Reply
socket.bind("tcp://*:5555")


def subirarchivos(nombrearchivo):
    filename, file_extension = os.path.splitext(nombrearchivo)
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
    message=socket.recv()
    print(message.decode())
    socket.send(str(size).encode())

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
        if funcion == b"subirarchivos":
            subirarchivos(archivo.decode())

        if funcion == b"bajararchivos":
            bajararchivos(archivo.decode())



"""

"""





