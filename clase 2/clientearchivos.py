"""import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.REQ) #me indica como van a interactuar cliente y servidor (REQ-> request)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response

#socket.send(b"Jhoan") #send solo envia una linea de texto (cadena)

socket.send_multipart([b"subirarchivo", b"creditos2.mp3"])


    #  Get the reply.
message = socket.recv()
print("Received reply  [ %s ]" % (message))


#implementar un servidor de archivos subir archivos, bajar archivos, compartir archivos. Nota: los archivos no seran solo texto... archivos 
#ejemplo compartir una pelicula (subir la pelicula, bajar la pelicula)
#para la subida o bajar archivos no es aconsejable para el caso de la pelicula hacerlo con json

#lunes miercoles y viernes despues de las 11 y antes de las 2"""




##############################################################################################################3
###############################################################################################################
###############################################################################################################


import zmq
import time
import os
import sys
from math import ceil



if __name__ == "__main__":

	parametros = sys.argv
	archivo = parametros[2]
	print(archivo)
	context = zmq.Context()
	#  Socket to talk to server
	print("Connecting to hello world server...")
	socket = context.socket(zmq.REQ) #me indica como van a interactuar cliente y servidor (REQ-> request)
	socket.connect("tcp://localhost:5555")
	socket.send_multipart([parametros[1].encode(), archivo.encode()])


	    #  Get the reply.
	message = socket.recv()



	if message == b"subearchivo":
		print("Received reply  [ %s ]" % (message))
		with open (archivo, 'rb') as archivoenviado:
			for i in range(0,ceil(os.path.getsize(archivo)/1024)):
				archivoenviado.seek(i*1024)
				t=archivoenviado.read(1024)
				socket.send(t)
				message = socket.recv()


	if message == b"bajararchivos":
		print("if de bajar archivos")
		for i in range (0,ceil(os.path.getsize(archivo)/1024)):
			socket.send(b"ready")
			archivito = socket.recv()
			print(archivito.decode())
			with open(archivo, 'ab') as archivobajado:
				archivobajado.write(archivito)
					
