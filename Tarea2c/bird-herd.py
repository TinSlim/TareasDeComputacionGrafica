import glfw
from glfw.GLFW import *

from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import Modulo.transformations as tr
import Modulo.basic_shapes as bs
import Modulo.scene_graph as sg
import Modulo.easy_shaders as es
import Modulo.readobj as rbj
import Modulo.lighting_shaders as ls

import Modulo.csvtolist_nuevo as cv
import Modulo.curvas as crv

a=cv.parsear_archivo("path.csv")
lista=[]
lista_pequenia=[]
lista.append(a[len(a)-1])
for punto in a:
    lista.append(punto)
lista.append(a[0])

lista2=[]
for punto in lista:
    for coordenada in punto:
        lista_pequenia.append(int(coordenada))
    lista2.append(lista_pequenia)
    lista_pequenia=[]
print(lista2)

b=crv.curvas_pajaros(lista2)

c=crv.concatenacion(b)

print(c)


#glfw.set_input_mode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)