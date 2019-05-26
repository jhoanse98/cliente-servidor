import zmq
import time


if __name__ == "__main__":
    context= zmq.Context()
    socket=context.socket(zmq.ROUTER)
    socket.bind("tcp://*:9999")

    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    

    while True:
        socks = dict(poller.poll(1024))
        if socket in socks:
            print("llego algo")
            t=time.localtime()
            who, *message = socket.recv_multipart() 
            print(time.strftime("%c"),message)
            
