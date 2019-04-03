
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP) # REP -> Reply
socket.bind("tcp://*:5555")

#ip 192.168.9.61


while True:
    #  Wait for next request from client
    #message = socket.recv()
    op, a1, a2 =socket.recv_multipart()  #operacion bloqueante. bloquea la ejecucion del programa
    									#existen dos posibilidades . que al socket le llega informacion o no hay nada. Se queda esperando hasta que llegue algo. en caso de recibir algo la operacion sigue. 
    print("Received request: %s" % op)

    if op == b'suma':
    	result = int(a1) + int(a2)
    	socket.send(str(result).encode())
    elif op==b'resta':
    	result = int(a1) - int(a2)
    	socket.send(str(result).encode())
    elif op==b'multiplicacion':
    	result = int(a1) * int(a2)
    	socket.send(str(result).encode())
    elif op==b'division':
    	result = int(a1) / int(a2)
    	socket.send(str(result).encode())
		

    #  Do some 'work'
    time.sleep(1)




























socket.send(b"subearchivo")
    for i in range (0,ceil(size/1024)):
        archivito = socket.recv()
        with open("archivosubido"+file_extension, 'ab') as archivo:
            archivo.write(archivito)
            socket.send(b"ready")












socket.send(b"bajararchivos")

    with open (nombrearchivobajar, 'rb') as archivoenviado:
        for i in range(0,ceil(size/1024)):
            archivoenviado.seek(i*1024)
            t=archivoenviado.read(1024)
            socket.send(t)
            message = socket.recv()

  

