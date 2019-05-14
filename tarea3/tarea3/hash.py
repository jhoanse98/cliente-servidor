    
import os
import hashlib
from math import ceil

def hasheador(archivo,size,MAX_BUFFER = 1024*1024*10):
    hasher = hashlib.sha256()
    #size= os.path.getsize('Lession_2.mp4.mp4')
    with open(archivo,'rb') as f:
        for i in range(0,ceil(size/MAX_BUFFER)):
                f.seek(i*MAX_BUFFER)
                data=f.read(MAX_BUFFER)
                hasher.update(data)
        return(hasher.hexdigest())

def hashitos(x):
    hasher = hashlib.sha256()
    hasher.update(x)
    return(hasher.hexdigest())