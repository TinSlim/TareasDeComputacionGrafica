import csv

#TODO agregar comentarios

def parsear(archivo):
    lectura=open(archivo, newline='')
    reader = csv.reader(lectura)
    data = list(reader)
    return data

def ubicacion_caidas(data):
    arreglo=[]
    for p in data:
        if 'x' in p[0]:
            p[0]=p[0].replace('x','')
            coordenada=[int(p[0]),int(p[1])]
            arreglo.append(coordenada)
    return arreglo


def borrado_x(a):
    if 'x' in a:
        print(a)
        a=a.replace('x','')
        print(a)
    return int(a)

def parseado_coordenada(parse):
    l = []
    for lista in parse:
        l.append(list(map(borrado_x, lista)))   
    print(parse)
    return l 


