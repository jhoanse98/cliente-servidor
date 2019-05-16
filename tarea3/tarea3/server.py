import zmq
import sys

MAX_BUFFER=1024*1024*1

if __name__ == "__main__":
    context = zmq.Context()
    socketProxy = context.socket(zmq.REQ)
    socketProxy.connect("tcp://localhost:5555")


    port = sys.argv[1]
    socketRecv = context.socket(zmq.REP)
    socketRecv.bind('tcp://*:{}'.format(port))

    address = 'localhost:{}'.format(port).encode('ascii')
    numPetitions = sys.argv[2].encode('ascii')
    socketProxy.send_multipart([b'server',address,numPetitions])
    response = socketProxy.recv_multipart()

    print(response)

    while True:
        responseClient = socketRecv.recv_multipart()
        print(responseClient[0])
        if responseClient[0] == b'sending':
            namefile= responseClient[1].decode()
            print("Vamos a subir un archivo")
            with open(namefile,'ab') as f:
                        #print(message[0])
                        f.write(responseClient[2])
            socketRecv.send_multipart([b'ok'])
        if responseClient[0] == b'downloading':
            print('bajando un archivo')
            with open(responseClient[1].decode(),'rb') as download:
                data=download.read(MAX_BUFFER)
                socketRecv.send_multipart([b'downloading', data])
                print('se esta bajando un archivito')


                        
