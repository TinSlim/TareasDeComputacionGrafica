import csv

#Entrega en formato lista 
#Ejemplo [['0','4'],.....]
def parsear_archivo(archivo):
    lectura=open(archivo, newline='')
    reader = csv.reader(lectura)
    data = list(reader)
    return data


#Devuelve arreglo con coordenadas donde hay 'x'
#Ej:  [['x1','2'],['2','6']]-->[  [1,2] ]
def encontrar_x(parseado):
    listado_de_x=[]
    for coordenada in parseado:
        if 'x' in coordenada[0]:
            listado_de_x.append( [int( coordenada[0].replace('x','') ),int(coordenada[1])])
    return listado_de_x

def quitar_x_coord(a):
    if 'x' in a:
       a=a.replace('x','')
    return int(a)

#Quita las x y transforma a entero
def quitar_x(parseado):
    l = []
    for lista in parse:
        l.append(list(map(quitar_x_coord, lista)))   
   # print(parse)
    return l 
   
def maximo_y(parseado_sin_x):
    max=parseado_sin_x[0][1]
    for coordenada in parseado_sin_x:
        if coordenada[1]>max:
            max=coordenada[1]
    return max

def ponderar_parseado_numpy_y(lista,numero):
    tamanio_lista=len(lista)
    n=0
    while n<tamanio_lista:
        lista[n][1]=(lista[n][1])/numero
        n+=1
    return lista 

parse=parsear_archivo("datos.csv")
print(encontrar_x(parse))

print(quitar_x(parse))
