
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")



while True:
    #  Wait for next request from client
    #message = socket.recv()
    op, a1, a2 =socket.recv_multipart()
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

  

