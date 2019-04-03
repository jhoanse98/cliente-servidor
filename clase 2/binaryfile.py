import os

"""import os
with open ("creditos.mp3", 'rb') as archivomp3:
	data= archivomp3.read()
	print(data)

with open("archivito.mp3", 'w+') as archivotxtmp3:
	datos = archivotxtmp3.write(str(data))
	print(datos)"""


curFile = 'creditos.mp3'
size = os.stat(curFile).st_size
print ('File size:', size)
