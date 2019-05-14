import zmq
import sys

if __name__ == "__main__":
    context = zmq.Context()
    socketProxy = context.socket(zmq.REQ)
    socketProxy.connect("tcp://localhost:5555")


    port = sys.argv[1]
    socketRecv = context.socket(zmq.ROUTER)
    socketRecv.bind('tcp://*:{}'.format(port))

    address = 'localhost:{}'.format(port).encode('ascii')
    numPetitions = sys.argv[2].encode('ascii')
    socketProxy.send_multipart([b'server',address,numPetitions])
    response = socketProxy.recv_multipart()

    print(response)

    while True:
        responseClient = socketRecv.recv_multipart()
        if responseClient[1] == b'sending':
            namefile= responseClient[2].decode()
            print("Vamos a subir un archivo")
            with open(namefile,'ab') as f:
                        #print(message[0])
                        f.write(responseClient[3])
        if responseClient[1] == b'downloading':
            with open(responseClient[2].decode(),'rb') as download:
                data=download.read()
                socketRecv.send_multipart([responseClient[0],b'downloading', data])


                        
