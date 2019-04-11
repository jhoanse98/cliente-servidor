import zmq
import os
import time
import sys
from math import ceil
from os import listdir
import hashlib

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


context = zmq.Context()
socket = context.socket(zmq.REP) # REP -> Reply
socket.bind("tcp://*:5555")
envio=1024*1024*10
contador=0


def subirarchivos(nombrearchivo):   
    global contador
    contador=contador+1
    print(contador)
    filename, file_extension = os.path.splitext(nombrearchivo)
    socket.send(b"subearchivo")
    tamañoarchivo = socket.recv().decode()
    filenameencriptado= encrypt_string(filename+tamañoarchivo+str(contador))
    socket.send(b"procediendo a subir archivo")
    for i in range (0,ceil(int(tamañoarchivo)/envio)):
        archivito = socket.recv()
        with open(filenameencriptado+file_extension, 'ab') as archivo:
            archivo.write(archivito)
            socket.send(b"ready")
    socket.recv()
    socket.send(b"El nombre para descargar el archivo "+filename.encode()+file_extension.encode()+ b" es "+filenameencriptado.encode()+file_extension.encode())



def bajararchivos(nombrearchivobajar):
    filename, file_extension = os.path.splitext(nombrearchivobajar)
    size= os.path.getsize(nombrearchivobajar)
    print(ceil(size/envio))

    socket.send(b"bajararchivos")
    message=socket.recv()
    print(message.decode())
    socket.send(str(size).encode())

    with open (nombrearchivobajar, 'rb') as archivoenviado:
        for i in range(0,ceil(size/envio)): 
            message = socket.recv()
            archivoenviado.seek(i*envio)
            t=archivoenviado.read(envio)
            print("hola server")
            socket.send(t)
            

def archivosservidor(ruta = '.'):
    socket.send(b"listar")
    socket.recv()
    archivos=listdir(ruta)
    for archivitos in archivos:
        socket.send(archivitos.encode())
        socket.recv()
    socket.send(b"")


if __name__ == "__main__":

    while True:
        funcion, archivo= socket.recv_multipart()
        if funcion == b"subirarchivos":
            subirarchivos(archivo.decode())

        if funcion == b"bajararchivos":
            bajararchivos(archivo.decode())

        if funcion == b"listar":
            archivosservidor()

"""

"""





