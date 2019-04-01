
import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response

#socket.send(b"Jhoan") #send solo envia una linea de texto (cadena)

socket.send_multipart([b"resta", b"7", b"5"])


    #  Get the reply.
message = socket.recv()
print("Received reply  [ %s ]" % (message))


	