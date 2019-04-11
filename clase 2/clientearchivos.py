import zmq
import time
import os
import sys
from math import ceil

import hashlib

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

#10.253.4.31

if __name__ == "__main__":

	parametros = sys.argv
	archivo = parametros[2]
	print(archivo)
	context = zmq.Context()
	envio=1024*1024*10
	#  Socket to talk to server
	print("Connecting to hello world server...\n\n")
	socket = context.socket(zmq.REQ) #me indica como van a interactuar cliente y servidor (REQ-> request)
	socket.connect("tcp://localhost:5555")
	socket.send_multipart([parametros[1].encode(), archivo.encode()])


	    #  Get the reply.
	message = socket.recv()



	if message == b"subearchivo":
		print("Received reply  [ %s ]" % (message))
		size= os.path.getsize(archivo)
		
		socket.send(str(size).encode())
		message = socket.recv()
		print(message.decode())
		with open (archivo, 'rb') as archivoenviado:
			for i in range(0,ceil(os.path.getsize(archivo)/envio)):
				archivoenviado.seek(i*envio)
				t=archivoenviado.read(envio)
				socket.send(t)
				message = socket.recv()
		socket.send(b"todo correcto")
		message=socket.recv()
		print(message.decode())


	if message == b"bajararchivos":
		socket.send(b"estan bajando un archivo")
		tamaño = socket.recv()
		print(tamaño.decode())
		for i in range (0,ceil(int(tamaño)/envio)):
			socket.send(b"ready")
			archivito = socket.recv()
			#print(archivito.decode())
			with open(archivo, 'ab') as archivobajado:
				archivobajado.write(archivito)


	if message== b"listar":
		socket.send(b"enlistando archivos")
		print ("Los archivos que hay en el servidor son: \n\n")
		while True:
			archivo= socket.recv()
			if(archivo.decode()):
				print(archivo.decode())
				socket.send(b"Esperando mas archivos")
			else:
				break

	#calcular ram disponible
	#suponiendo que el tramo es de 1 gb en las mejores condiciones puede tardar 1 sg
	#segmentar sirve para generar un balanceo de cargas roound 
	#mi archivo pasa de mi computador a el servidor
	
					
