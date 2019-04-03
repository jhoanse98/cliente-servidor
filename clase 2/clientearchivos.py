import zmq
import time
import os
import sys
from math import ceil

#10.253.4.31

if __name__ == "__main__":

	parametros = sys.argv
	archivo = parametros[2]
	print(archivo)
	context = zmq.Context()
	#  Socket to talk to server
	print("Connecting to hello world server...")
	socket = context.socket(zmq.REQ) #me indica como van a interactuar cliente y servidor (REQ-> request)
	socket.connect("tcp://10.253.4.31:5555")
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
			for i in range(0,ceil(os.path.getsize(archivo)/1024)):
				archivoenviado.seek(i*1024)
				t=archivoenviado.read(1024)
				socket.send(t)
				message = socket.recv()


	if message == b"bajararchivos":
		send(b"estan bajando un archivo")
		tamaño = socket.recv()
		for i in range (0,ceil(int(tamaño)/1024)):
			socket.send(b"ready")
			archivito = socket.recv()
			print(archivito.decode())
			with open(archivo, 'ab') as archivobajado:
				archivobajado.write(archivito)
					
