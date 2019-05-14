import zmq
from collections import OrderedDict
from pymongo import MongoClient


if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    dataBase = MongoClient("mongodb://admin:admin12345@ds044577.mlab.com:44577/cliente_servidor")
    db = dataBase["cliente_servidor"]

    savedFiles = db['tarea3']
    servers = OrderedDict()

    print('Proxy inicializado')
    while True:
        who, *message = socket.recv_multipart()
        if who.decode() == 'server':
            servers[message[0].decode('ascii')] = int(message[1].decode('ascii'))
            socket.send_multipart([b'ok'])
        if who.decode() == 'client':
            op,*other = message
            if op == b'send':
                fileName, fileExt, mainHash, *hashis = other
                if len(servers) == 0:
                    socket.send_multipart([b'error',b'no hay servidores disponibles'])
                else:
                    d = OrderedDict()
                    serverKeys = [key for key in servers.keys()]
                    indice = 0
                    error = False
                    response = [b'ok']
                    total = sum([value for value in servers.values()])
                    if len(hashis) > total:
                        socket.send_multipart([b'error', b'No hay espacio suficiente'])
                    else:
                        for h in hashis:
                            if servers[serverKeys[indice]] > 0:
                                d[h.decode()] = serverKeys[indice]
                                servers[serverKeys[indice]] -=1
                                response.append(serverKeys[indice].encode())
                                total-=1
                                indice+=1
                            elif servers[serverKeys[indice]]==0:
                               indice+=1
                            if total==0:
                                error = True
                                break
                            if indice == len(serverKeys):
                                indice = 0
                        if error:
                            socket.send_multipart([b'error',b'No hay espacio Suficiente'])
                        else:
                            print("Quedan {} fracciones".format(total))
                            guardar = {}
                            guardar['fileName'] = fileName.decode()
                            guardar['fileExt'] = fileExt.decode()
                            guardar['mainHash'] = mainHash.decode()
                            guardar['hashis'] = d
                            new= savedFiles.insert_one(guardar).inserted_id
                            socket.send_multipart(response)
            elif op == b'download':
                finded = savedFiles.find_one({"mainHash" : other[0].decode()})
                fullName = finded["fileName"]+finded["fileExt"]
                if finded:
                    response = [b'ok',fullName.encode()]
                    for key,value in finded['hashis'].items():
                        print(key,value)
                        string = '{};{}'.format(key,value)
                        response.append(string.encode())  
                    socket.send_multipart(response)
                else:
                    socket.send_multipart([b'error',b'No se encontro el archivo'])
                    
