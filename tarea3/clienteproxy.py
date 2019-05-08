import zmq
import hashlib
import hash  as hasher
from math import ceil
import os
import json

MAX_BUFFER = 1024*1024*10



if __name__ == "__main__":
    context=zmq.Context()
    socketproxy=context.socket(zmq.REQ)
    MAX_BUFFER=1024*1024

    socketproxy.connect("tcp://192.168.1.245:5555")
    print("enviamos a proxy")
    hashcomplete=(hasher.hasheador())
    print(type(hashcomplete))
    size= os.path.getsize('Lession_2.mp4.mp4')
    rango = ceil(size/MAX_BUFFER)
    
    
    hashlist=[b'client',hashcomplete.encode()]
    with open('Lession_2.mp4.mp4','rb') as archivo:
        for i in range(0, rango):
            archivo.seek(i*MAX_BUFFER)
            data=archivo.read(MAX_BUFFER)
            hashi=hasher.hashitos(data)
            hashlist.append(hashi.encode())
    
    

    
    print(hashlist)
    socketproxy.send_multipart(hashlist)

    while True:
        
        socketproxy.recv_multipart() 

    

        
    

        
        








