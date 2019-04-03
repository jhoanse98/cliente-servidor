import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


if __name__ == "__main__":
    print("Server Alive")
    fileExt = ''
    while True:
        message = socket.recv_multipart()
        
        if len(message) == 2:
            print("Message: {}".format(message[0]))
            if message[1].decode() == 'sending':
                socket.send(b'get')
            else:
                fileExt = message[1].decode()
                socket.send(b'extSaved')
        else:
            fileName = 'test2'+fileExt
            with open(fileName,'ab') as f:
                #print(message[0])
                f.write(message[0])
                socket.send(b'nothing')