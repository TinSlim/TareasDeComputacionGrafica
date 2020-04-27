import csv
import numpy as np

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
       # print(a)
        a=a.replace('x','')
        #print(a)
    return int(a)

def parseado_coordenada(parse):
    l = []
    for lista in parse:
        l.append(list(map(borrado_x, lista)))   
   # print(parse)
    return l 

def agregar_coord_z(lista):
    for curva in lista:
        for coordenada in curva:
            coordenada.append(0)
    return lista

def agregar_coord_z2(lista):
    total=[]
    curve=[]
    coor=[]
    for curva in lista:
        for coordenada in curva:
            curve.append(np.array([[coordenada[0],coordenada[1],0]]).T)
        total.append(curve)
        curve=[]
    return total            



###Primero parseado, luego parseado_coordenada

def list_to_numpy(lista):
    return np.array(lista)    


def crater(lista,lista_x):
    salida=[]
    actual=[]
    crateres=0
    for t in lista:
        for x in lista_x:
            if t[0]==x[0] and t[1]==x[1]:
                actual.append([t[0]-0.3,t[1]])
                actual.append([t[0]+0.3,t[1]])

                salida.append(actual)
                actual=[[t[0]-0.3,t[1]],[t[0]+0.3,t[1]]]
            else:
                actual.append([t[0],t[1]])
    if not (actual==[]):
        salida.append(actual)
    return salida                


#a=parsear("datos.csv")

#b=parseado_coordenada(a)
#caidas=ubicacion_caidas(a)

#hoyos=crater(b,caidas)
#print(hoyos)
#c=agregar_coord_z(hoyos)

#print(c)