import zmq
import os
import sys
from math import ceil

if __name__ == "__main__":

    parametros = sys.argv
    archivo = parametros[1]
    filename, file_extension = os.path.splitext(archivo)
    print (filename, file_extension)
    size= os.path.getsize(parametros[1])
    print(ceil(size/1024))

    #Socket
    context = zmq.Context()
    print("Connecting to server...")
    socket = context.socket(zmq.REQ) 
    socket.connect("tcp://localhost:5555")

    socket.send_multipart([b'start',file_extension.encode()])
    message = socket.recv()
    print('Sending File')
    socket.send_multipart([b'',b'sending'])
    
    message = socket.recv()
    print("Server Say: {}".format(message.decode()))
    if message.decode() == 'get':
        print("Processing")
        with open(archivo,'rb') as f:
            for i in range(0,ceil(size/1024)):
                f.seek(i*1024)
                t=f.read(1024)
                socket.send_multipart([t])
                message = socket.recv()