
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


#modelo sincrono

#Paso de mensajes sincrono o modelo de paso de mensajes sincrono

#ventajas: facil programar
#desventaja: el cliente queda esperando hasta que el cliente no le de una respuesta
#no es bueno cuando hay un numero alto de cliente 

#los mensajes se deben enviar siempre de forma binaria (b"hello")

#para no depeender de la arquitectura es mejor enviar cadenas por ejemplo al enviar el numero 3 de un pc a una raspberry (arquitecturas diferentes ) 011 e binario pc, tecnologia intel 011 es 6 por eso es mejor enviar cadenas