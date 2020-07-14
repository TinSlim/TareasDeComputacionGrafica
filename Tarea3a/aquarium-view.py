import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import random

import Modulo.transformations as tr
import Modulo.easy_shaders as es
import Modulo.basic_shapes as bs
import Modulo.basic_shapes as bs
import Modulo.readobj as robj

import json

def reader(json_file):
    with open(json_file) as f:
        data = json.load(f)
        return data

try:
    archivo_json=str(sys.argv[1])
except:
    archivo_json="view-setup.json"

archivo_json=reader(archivo_json)

# Variables del JSON
filename = archivo_json["filename"]



t_a = archivo_json["t_a"]
t_b = archivo_json["t_b"]
t_c = archivo_json["t_c"]

n_a = archivo_json["t_a"]
n_b = archivo_json["t_a"]
n_c = archivo_json["t_a"]


def createColorCubeAleta(i, j, k, X, Y, Z,c):
    l_x = X[i, j, k]
    r_x = X[i+1, j, k]
    b_y = Y[i, j, k]
    f_y = Y[i, j+1, k]
    b_z = Z[i, j, k]
    t_z = Z[i, j, k+1]

    altura = abs(t_z-b_z)
    ancho = abs(f_y-b_y)
    largo = abs(l_x-r_x)
    
    #c = np.random.rand
    #   positions    colors
    vertices = [
    # Z+: number 1
        l_x-largo/2, b_y+ancho/3,  t_z-altura/3+altura/2, c,0,1-c,
         r_x-largo, b_y+ancho/3,  t_z-altura/3, c,0,1-c,
         r_x-largo,  f_y-ancho/3,  t_z-altura/3, c,0,1-c,
        l_x-largo/2,  f_y-ancho/3,  t_z-altura/3+altura/2, c,0,1-c,
    # Z-: number 6
        l_x-largo/2, b_y+ancho/3, b_z+altura/3-altura/2, c,0,1-c,
         r_x-largo, b_y+ancho/3, b_z+altura/3, c,0,1-c,
         r_x-largo,  f_y-ancho/3, b_z+altura/3, c,0,1-c,
        l_x-largo/2,  f_y-ancho/3, b_z+altura/3-altura/2, c,0,1-c,
        ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7]

    return (bs.Shape(vertices, indices),l_x, b_y+ancho/2, t_z-altura/2) #LX -0.05


def createColorCube(i, j, k, X, Y, Z,c):
    l_x = X[i, j, k]
    r_x = X[i+1, j, k]
    b_y = Y[i, j, k]
    f_y = Y[i, j+1, k]
    b_z = Z[i, j, k]
    t_z = Z[i, j, k+1]
    #c = np.random.rand
    #   positions    colors
    vertices = [
    # Z+: number 1
        l_x, b_y,  t_z, c,0,1-c,
         r_x, b_y,  t_z, c,0,1-c,
         r_x,  f_y,  t_z, c,0,1-c,
        l_x,  f_y,  t_z, c,0,1-c,
    # Z-: number 6
        l_x, b_y, b_z, c,0,1-c,
         r_x, b_y, b_z, c,0,1-c,
         r_x,  f_y, b_z, c,0,1-c,
        l_x,  f_y, b_z, c,0,1-c,
    # X+: number 5
         r_x, b_y, b_z, c,0,1-c,
         r_x,  f_y, b_z, c,0,1-c,
         r_x,  f_y,  t_z, c,0,1-c,
         r_x, b_y,  t_z, c,0,1-c,
    # X-: number 2
        l_x, b_y, b_z, c,0,1-c,
        l_x,  f_y, b_z, c,0,1-c,
        l_x,  f_y,  t_z, c,0,1-c,
        l_x, b_y,  t_z, c,0,1-c,
    # Y+: number 4
        l_x,  f_y, b_z, c,0,1-c,
        r_x,  f_y, b_z, c,0,1-c,
        r_x,  f_y, t_z, c,0,1-c,
        l_x,  f_y, t_z, c,0,1-c,
    # Y-: number 3
        l_x, b_y, b_z, c,0,1-c,
        r_x, b_y, b_z, c,0,1-c,
        r_x, b_y, t_z, c,0,1-c,
        l_x, b_y, t_z, c,0,1-c,
        ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7]

    return bs.Shape(vertices, indices)


def createColorCubeBorde(i, j, k, X, Y, Z,c):
    l_x = X[i, j, k]
    r_x = X[i+1, j, k]
    b_y = Y[i, j, k]
    f_y = Y[i, j+1, k]
    b_z = Z[i, j, k]
    t_z = Z[i, j, k+1]
    #c = np.random.rand
    #   positions    colors
    vertices = [
    # Z+: number 1
        l_x, b_y,  t_z, 0,c,0,
         r_x, b_y,  t_z, 0,c,0,
         r_x,  f_y,  t_z, 0,c,0,
        l_x,  f_y,  t_z, 0,c,0,
    # Z-: number 6
        l_x, b_y, b_z, 0,c,0,
         r_x, b_y, b_z, 0,c,0,
         r_x,  f_y, b_z, 0,c,0,
        l_x,  f_y, b_z, 0,c,0,
    # X+: number 5
         r_x, b_y, b_z, 0,c,0,
         r_x,  f_y, b_z, 0,c,0,
         r_x,  f_y,  t_z, 0,c,0,
         r_x, b_y,  t_z, 0,c,0,
    # X-: number 2
        l_x, b_y, b_z, 0,c,0,
        l_x,  f_y, b_z, 0,c,0,
        l_x,  f_y,  t_z, 0,c,0,
        l_x, b_y,  t_z, 0,c,0,
    # Y+: number 4
        l_x,  f_y, b_z, 0,c,0,
        r_x,  f_y, b_z, 0,c,0,
        r_x,  f_y, t_z, 0,c,0,
        l_x,  f_y, t_z, 0,c,0,
    # Y-: number 3
        l_x, b_y, b_z, 0,c,0,
        r_x, b_y, b_z, 0,c,0,
        r_x, b_y, t_z, 0,c,0,
        l_x, b_y, t_z, 0,c,0,
        ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7]

    return bs.Shape(vertices, indices)



def createColorPez(i, j, k, X, Y, Z,c):
    l_x = X[i, j, k]
    r_x = X[i+1, j, k]
    b_y = Y[i, j, k]
    f_y = Y[i, j+1, k]
    b_z = Z[i, j, k]
    t_z = Z[i, j, k+1]
    altura = abs(t_z-b_z)
    ancho = abs(f_y-b_y)
    largo = abs(l_x-r_x)
    #c = np.random.rand
    #   positions    colors
    vertices = [
    # Z+: number 1
        l_x, b_y+ancho/5,  t_z-altura/6, c,0,1-c,
         r_x, b_y+ancho/5, t_z-altura/6, c,0,1-c,
         r_x,  f_y-ancho/5,  t_z-altura/6, c,0,1-c,
        l_x,  f_y-ancho/5,  t_z-altura/6, c,0,1-c,
    # Z-: number 6
        l_x, b_y+ancho/5, b_z+altura/6, c,0,1-c,
         r_x, b_y+ancho/5, b_z+altura/6, c,0,1-c,
         r_x,  f_y-ancho/5, b_z+altura/6, c,0,1-c,
        l_x,  f_y-ancho/5, b_z+altura/6, c,0,1-c,
        
        ######f_y-ancho/5*2
        l_x+largo, b_y+ancho/5,  t_z-altura/6, c,0,1-c,
         r_x+largo/3, b_y+ancho/5, t_z-altura/4, c,0,1-c,
         r_x+largo/3,  f_y-ancho/5,  t_z-altura/4, c,0,1-c,
        l_x+largo/3,  f_y-ancho/5,  t_z-altura/6, c,0,1-c,
    # Z-: number 6
        l_x+largo/3, b_y+ancho/5, b_z+altura/6, c,0,1-c,
         r_x+largo/3, b_y+ancho/5, b_z+altura/4, c,0,1-c,
         r_x+largo/3,  f_y-ancho/5, b_z+altura/4, c,0,1-c,
        l_x+largo/3,  f_y-ancho/5, b_z+altura/6, c,0,1-c,
        
        
        
        l_x+largo/3, b_y,  t_z-altura/3, c,0,1-c,
         r_x, b_y, t_z-altura/3, c,0,1-c,
         r_x,  f_y,  t_z-altura/3, c,0,1-c,
        l_x+largo/3,  f_y,  t_z-altura/3, c,0,1-c,
    # Z-: number 6
        l_x+largo/3, b_y, b_z+altura/3, c,0,1-c,
         r_x, b_y, b_z+altura/3, c,0,1-c,
         r_x,  f_y, b_z+altura/3, c,0,1-c,
        l_x+largo/3,  f_y, b_z+altura/3, c,0,1-c]





    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7,
        
        8, 9, 10, 10, 11, 8,
        12, 13, 14, 14, 15, 12,
        12, 13, 8, 8, 9, 12,
        14, 15, 11, 11, 10, 14,
        13, 14, 10, 10, 9, 13,
        15, 12, 8, 8, 11, 15,
        
        16,17,18,18,19,16,
        20,21,22,22,23,20,
        20,21,16,16,17,20,
        22,23,19,19,18,22,
        21,22,18,18,17,21,
        23,20,16,16,19,23]

    return bs.Shape(vertices, indices),[l_x+(largo/2),b_y+(ancho/2),b_z+(altura/2)]   #


def createColorPez1(i, j, k, X, Y, Z,c):
    l_x = X[i, j, k]
    r_x = X[i+1, j, k]
    b_y = Y[i, j, k]
    f_y = Y[i, j+1, k]
    b_z = Z[i, j, k]
    t_z = Z[i, j, k+1]
    altura = abs(t_z-b_z)
    ancho = abs(f_y-b_y)
    largo = abs(l_x-r_x)
    #c = np.random.rand
    #   positions    colors
    vertices = [
    # Z+: number 1
        l_x, b_y+ancho/3,  t_z, c,0,1-c,
         r_x, b_y+ancho/3, t_z, c,0,1-c,
         r_x,  f_y-ancho/3,  t_z, c,0,1-c,
        l_x,  f_y-ancho/3,  t_z, c,0,1-c,
    # Z-: number 6
        l_x, b_y+ancho/3, b_z, c,0,1-c,
         r_x, b_y+ancho/3, b_z, c,0,1-c,
         r_x,  f_y-ancho/3, b_z, c,0,1-c,
        l_x,  f_y-ancho/3, b_z, c,0,1-c,
        
        ######f_y-ancho/5*2
        l_x+largo, b_y+ancho/3,  t_z-altura/6, c,0,1-c,
         r_x+largo/3, b_y+ancho/3, t_z-altura/4, c,0,1-c,
         r_x+largo/3,  f_y-ancho/3,  t_z-altura/4, c,0,1-c,
        l_x+largo/3,  f_y-ancho/3,  t_z-altura/6, c,0,1-c,
    # Z-: number 6
        l_x+largo/3, b_y+ancho/3, b_z+altura/6, c,0,1-c,
         r_x+largo/3, b_y+ancho/3, b_z+altura/4, c,0,1-c,
         r_x+largo/3,  f_y-ancho/3, b_z+altura/4, c,0,1-c,
        l_x+largo/3,  f_y-ancho/3, b_z+altura/6, c,0,1-c,
        
        
        
        l_x+largo/3, b_y+ancho/4,  t_z-altura/3, c,0,1-c,
         r_x, b_y+ancho/4, t_z-altura/3, c,0,1-c,
         r_x,  f_y-ancho/4,  t_z-altura/3, c,0,1-c,
        l_x+largo/3,  f_y-ancho/4,  t_z-altura/3, c,0,1-c,
    # Z-: number 6
        l_x+largo/3, b_y+ancho/4, b_z+altura/3, c,0,1-c,
         r_x, b_y+ancho/4, b_z+altura/3, c,0,1-c,
         r_x,  f_y-ancho/4, b_z+altura/3, c,0,1-c,
        l_x+largo/3,  f_y-ancho/4, b_z+altura/3, c,0,1-c]





    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7,
        
        8, 9, 10, 10, 11, 8,
        12, 13, 14, 14, 15, 12,
        12, 13, 8, 8, 9, 12,
        14, 15, 11, 11, 10, 14,
        13, 14, 10, 10, 9, 13,
        15, 12, 8, 8, 11, 15,
        
        16,17,18,18,19,16,
        20,21,22,22,23,20,
        20,21,16,16,17,20,
        22,23,19,19,18,22,
        21,22,18,18,17,21,
        23,20,16,16,19,23]

    return bs.Shape(vertices, indices)


def createColorPez2(i, j, k, X, Y, Z,c):
    l_x = X[i, j, k]
    r_x = X[i+1, j, k]
    b_y = Y[i, j, k]
    f_y = Y[i, j+1, k]
    b_z = Z[i, j, k]
    t_z = Z[i, j, k+1]
    altura = abs(t_z-b_z)
    ancho = abs(f_y-b_y)
    largo = abs(l_x-r_x)
    #c = np.random.rand
    #   positions    colors
    vertices = [
    # Z+: number 1
        l_x, b_y+ancho/7,  t_z-altura/2.5, c,0,1-c,
         r_x, b_y+ancho/7, t_z-altura/2.5, c,0,1-c,
         r_x,  f_y-ancho/7,  t_z-altura/2.5, c,0,1-c,
        l_x,  f_y-ancho/7,  t_z-altura/2.5, c,0,1-c,
    # Z-: number 6
        l_x, b_y+ancho/7, b_z+altura/2.5, c,0,1-c,
         r_x, b_y+ancho/7, b_z+altura/2.5, c,0,1-c,
         r_x,  f_y-ancho/7, b_z+altura/2.5, c,0,1-c,
        l_x,  f_y-ancho/7, b_z+altura/2.5, c,0,1-c,
        
        ######f_y-ancho/5*2
        l_x+largo, b_y+ancho/5,  t_z-altura/2.5, c,0,1-c,
         r_x+largo/3, b_y+ancho/5, t_z-altura/2.5, c,0,1-c,
         r_x+largo/3,  f_y-ancho/5,  t_z-altura/2.5, c,0,1-c,
        l_x+largo/3,  f_y-ancho/5,  t_z-altura/2.5, c,0,1-c,
    # Z-: number 6
        l_x+largo/3, b_y+ancho/5, b_z+altura/2.5, c,0,1-c,
         r_x+largo/3, b_y+ancho/5, b_z+altura/2.5, c,0,1-c,
         r_x+largo/3,  f_y-ancho/5, b_z+altura/2.5, c,0,1-c,
        l_x+largo/3,  f_y-ancho/5, b_z+altura/2.5, c,0,1-c,
        
        
        
        l_x+largo/3, b_y,  t_z-altura/3, c,0,1-c,
         r_x, b_y, t_z-altura/3, c,0,1-c,
         r_x,  f_y,  t_z-altura/3, c,0,1-c,
        l_x+largo/3,  f_y,  t_z-altura/3, c,0,1-c,
    # Z-: number 6
        l_x+largo/3, b_y, b_z+altura/3, c,0,1-c,
         r_x, b_y, b_z+altura/3, c,0,1-c,
         r_x,  f_y, b_z+altura/3, c,0,1-c,
        l_x+largo/3,  f_y, b_z+altura/3, c,0,1-c]





    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7,
        
        8, 9, 10, 10, 11, 8,
        12, 13, 14, 14, 15, 12,
        12, 13, 8, 8, 9, 12,
        14, 15, 11, 11, 10, 14,
        13, 14, 10, 10, 9, 13,
        15, 12, 8, 8, 11, 15,
        
        16,17,18,18,19,16,
        20,21,22,22,23,20,
        20,21,16,16,17,20,
        22,23,19,19,18,22,
        21,22,18,18,17,21,
        23,20,16,16,19,23]

    return bs.Shape(vertices, indices)




def createPez(lista_coord, F, G, H,c,n):
    peces = [ ]
    lista = lista_coord
    random.shuffle(lista)
    pez = n
    aleta_pos = []
    while n >0:
        nuevo = lista.pop()
        aleta = createColorCubeAleta(nuevo[0], nuevo[1], nuevo[2], F, G, H,c)
        aleta_pos.append([aleta[1],aleta[2],aleta[3]])
        
        pececillo = createColorPez(nuevo[0], nuevo[1], nuevo[2], F, G, H,c)
        peces.append([es.toGPUShape(pececillo[0]),pececillo[1]])
        peces.append(es.toGPUShape(aleta[0]))
        n-=1
    return peces,aleta_pos
    

def createPez1(lista_coord, F, G, H,c,n):
    peces = [ ]
    lista = lista_coord
    random.shuffle(lista)
    pez = n
    aleta_pos = []
    while n >0:
        nuevo = lista.pop()
        aleta = createColorCubeAleta(nuevo[0], nuevo[1], nuevo[2], F, G, H,c)
        aleta_pos.append([aleta[1],aleta[2],aleta[3]])
        peces.append(es.toGPUShape(aleta[0]))
        peces.append(es.toGPUShape(createColorPez1(nuevo[0], nuevo[1], nuevo[2], F, G, H,c)))
        n-=1
    return peces,aleta_pos


def createPez2(lista_coord, F, G, H,c,n):
    peces = [ ]
    lista = lista_coord
    random.shuffle(lista)
    pez = n
    aleta_pos = []
    while n >0:
        nuevo = lista.pop()
        aleta = createColorCubeAleta(nuevo[0], nuevo[1], nuevo[2], F, G, H,c)
        aleta_pos.append([aleta[1],aleta[2],aleta[3]])
        peces.append(es.toGPUShape(aleta[0]))
        peces.append(es.toGPUShape(createColorPez2(nuevo[0], nuevo[1], nuevo[2], F, G, H,c)))
        n-=1
    return peces,aleta_pos
    

def merge(destinationShape, strideSize, sourceShape):

    # current vertices are an offset for indices refering to vertices of the new shape
    offset = len(destinationShape.vertices)
    destinationShape.vertices += sourceShape.vertices
    destinationShape.indices += [(offset/strideSize) + index for index in sourceShape.indices]


PROJECTION_ORTHOGRAPHIC = 0
PROJECTION_FRUSTUM = 1
PROJECTION_PERSPECTIVE = 2



# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.projection = PROJECTION_PERSPECTIVE

        self.A = False
        self.B = False
        self.C = False


# We will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon


    elif key == glfw.KEY_A:
        controller.A = not controller.A

    elif key == glfw.KEY_B:
        controller.B = not controller.B

    elif key == glfw.KEY_C:
        controller.C = not controller.C



    elif key == glfw.KEY_1:
        print('Orthographic projection')
        controller.projection = PROJECTION_ORTHOGRAPHIC

    elif key == glfw.KEY_2:
        print('Frustum projection')
        controller.projection = PROJECTION_FRUSTUM

    elif key == glfw.KEY_3:
        print('Perspective projection')
        controller.projection = PROJECTION_PERSPECTIVE

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)



if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Projections Demo", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program
    pipeline = es.SimpleModelViewProjectionShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    gpuAxis = es.toGPUShape(bs.createAxis(7))
    
    # Load potentials and grid
    load_voxels = np.load(filename)

  
    largo_x = len(load_voxels)
    largo_y = len(load_voxels[0])
    largo_z = len(load_voxels[0][0])

    division = max(largo_x,largo_y,largo_z)
    #X, Y, Z = np.mgrid[-1.5:1.5:(largo_x*1j), -3:3:(largo_y*1j), -2:2:(largo_z*1j)]
    X, Y, Z = np.mgrid[-(largo_x/division):(largo_x/division):(largo_x*1j), -(largo_y/division):(largo_y/division):(largo_y*1j), -(largo_z/division):(largo_z/division):(largo_z*1j)]



    #print(load_voxels.shape)
    #print(range(X.shape[0]-1),range(X.shape[1]-1),range(X.shape[2]-1))

    isosurfaceA = bs.Shape([], [])
    isosurfaceB = bs.Shape([], [])
    isosurfaceC = bs.Shape([], [])

    isosurfaceBorde = bs.Shape([], [])

    
    # Now let's draw voxels!

    coordenadas_t_a = []
    coordenadas_t_b = []
    coordenadas_t_c = []
    
    

    for k in range(X.shape[2]-1):
        for j in range(X.shape[1]-1):
            for i in range(X.shape[0]-1):
                if load_voxels[i,j,k]:
                    
                    if ( (i==0 or i==X.shape[0]-2) and (j==0 or j==X.shape[1]-2 or k==0 or k==X.shape[2]-2) )  or   ((j==0 or j==X.shape[1]-2) and (i==0 or i==X.shape[0]-2 or k==0 or k==X.shape[2]-2)) or ((j==0 or j==X.shape[1]-2 or i==0 or i==X.shape[0]-2) and (k==0 or k==X.shape[2]-2)):
                        temp_shape = createColorCubeBorde(i,j,k, X,Y, Z,0.1)
                        merge(destinationShape=isosurfaceBorde, strideSize=6, sourceShape=temp_shape)

                    elif abs(load_voxels[i,j,k]-t_a) <=2:
                        temp_shape = createColorCube(i,j,k, X,Y, Z,1)
                        merge(destinationShape=isosurfaceA, strideSize=6, sourceShape=temp_shape)
                        coordenadas_t_a.append([i,j,k])

                    elif abs(load_voxels[i,j,k]-t_b) <=2:
                        temp_shape = createColorCube(i,j,k, X,Y, Z,0.6)
                        merge(destinationShape=isosurfaceB, strideSize=6, sourceShape=temp_shape)
                        coordenadas_t_b.append([i,j,k])

                    elif abs(load_voxels[i,j,k]-t_c) <=2:
                        temp_shape = createColorCube(i,j,k, X,Y, Z,0.3)
                        merge(destinationShape=isosurfaceC, strideSize=6, sourceShape=temp_shape)
                        coordenadas_t_c.append([i,j,k])
                    
                    
    
    shapePezA = createPez(coordenadas_t_a, X, Y, Z,1,n_a)
    shapePezB = createPez(coordenadas_t_b, X, Y, Z,0.6,n_b)
    shapePezC = createPez(coordenadas_t_c, X, Y, Z,0.3,n_c)

    gpu_surfaceA = es.toGPUShape(isosurfaceA)
    gpu_surfaceB = es.toGPUShape(isosurfaceB)
    gpu_surfaceC = es.toGPUShape(isosurfaceC)

    gpu_surfaceBorde = es.toGPUShape(isosurfaceBorde)

    t0 = glfw.get_time()
    camera_theta = np.pi/4
    camera_theta2 = -1

    angulo_aleta = -0.8
    angulo_aleta1 = -0.4
    angulo_aleta2 = 0.4
    angulo_aleta3 = -0.8

    ang_der = True
    ang_der1 = True
    ang_der2 = True
    ang_der3 = True
    radio = 10


    ##Angulos_peces
    angulos_peces = []
    for index in shapePezA[0]:
        angulos_peces.append(random.random()*2)
    for index in shapePezB[0]:
        angulos_peces.append(random.random()*2)
    for index in shapePezC[0]:
        angulos_peces.append(random.random()*2)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1



        if ang_der:
            angulo_aleta+=0.05
            if angulo_aleta>=0.8:
                ang_der = not ang_der
        else:
            angulo_aleta-=0.05
            if angulo_aleta<=-0.8:
                ang_der = not ang_der

        ####

        if ang_der1:
            angulo_aleta1+=0.03
            if angulo_aleta1>=0.8:
                ang_der1 = not ang_der1
        else:
            angulo_aleta1-=0.03
            if angulo_aleta1<=-0.8:
                ang_der1 = not ang_der1
        
        ####

        if ang_der2:
            angulo_aleta2+=0.04
            if angulo_aleta2>=0.8:
                ang_der2 = not ang_der2
        else:
            angulo_aleta2-=0.04
            if angulo_aleta2<=-0.8:
                ang_der2 = not ang_der2

        ###

        if ang_der3:
            angulo_aleta3+=0.05
            if angulo_aleta3>=0.8:
                ang_der3 = not ang_der3
        else:
            angulo_aleta3-=0.05
            if angulo_aleta3<=-0.8:
                ang_der3 = not ang_der3


        
        if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS):
            camera_theta -= 2 * dt

        if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS):
            camera_theta += 2* dt

        if (glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS):
            if camera_theta2<0-2*dt:
                camera_theta2 += 2*dt

        if (glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS):
            if camera_theta2>-3.08:
                camera_theta2 -= 2*dt

        if (glfw.get_key(window, glfw.KEY_P) == glfw.PRESS):
            radio += 0.2
        
        if (glfw.get_key(window, glfw.KEY_O) == glfw.PRESS):
            radio -= 0.2


        # Setting up the view transform

        radio = radio
        camX = radio * np.sin(camera_theta) * np.sin(camera_theta2)
        camY = radio * np.cos(camera_theta) * np.sin(camera_theta2)
        camZ = radio * np.cos(camera_theta2)


        viewPos = np.array([camX, camY, camZ])

        view = tr.lookAt(
            viewPos,
            np.array([0,0,0]),
            np.array([0,0,1])
        )

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        # Setting up the projection transform

        if controller.projection == PROJECTION_ORTHOGRAPHIC:
            projection = tr.ortho(-8, 8, -8, 8, 0.1, 100)

        elif controller.projection == PROJECTION_FRUSTUM:
            projection = tr.frustum(-5, 5, -5, 5, 9, 100)

        elif controller.projection == PROJECTION_PERSPECTIVE:
            projection = tr.perspective(60, float(width)/float(height), 0.1, 100)
        
        else:
            raise Exception()

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)


        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Drawing shapes with different model transformations
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.translate(5,0,0))

        
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.uniformScale(3))
        #pipeline.drawShape(gpuAxis, GL_LINES)





        if not controller.A:
            x=0
            y=-1
            alete = 0
            pos_pez = 0
            index_random = 0
            for p in shapePezA[0]:
                y+=1
                if y ==0:
                    angulo_alete = angulo_aleta
                elif y ==1:
                    angulo_alete = angulo_aleta1
                elif y ==2:
                    angulo_alete = angulo_aleta2
                elif y ==4:
                    angulo_alete = angulo_aleta3
                    y=-1
                if not x%2==0:
                    posicion_ale = [shapePezA[1][x//2][0],shapePezA[1][x//2][1],shapePezA[1][x//2][2]]
                    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE,tr.matmul([ tr.uniformScale(3),tr.translate(pos_pez[0],pos_pez[1],pos_pez[2]),tr.rotationZ(angulos_peces[index_random]),tr.translate(-pos_pez[0],-pos_pez[1],-pos_pez[2]),tr.translate(posicion_ale[0],posicion_ale[1],posicion_ale[2]),tr.rotationZ(angulo_alete),tr.translate(-posicion_ale[0],-posicion_ale[1],-posicion_ale[2])]))
                    pipeline.drawShape(p)
                    index_random+=1
                else:
                    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.uniformScale(3),tr.translate(p[1][0],p[1][1],p[1][2]),tr.rotationZ(angulos_peces[index_random]),tr.translate(-p[1][0],-p[1][1],-p[1][2])]))
                    pos_pez=p[1]
                    pipeline.drawShape(p[0])
                x+=1

        if not controller.B:
            x=0
            y=-1
            alete = 0
            pos_pez = 0
            index_random = len(shapePezA[0])
            for p in shapePezB[0]:
                y+=1
                if y ==0:
                    angulo_alete = angulo_aleta
                elif y ==1:
                    angulo_alete = angulo_aleta1
                elif y ==2:
                    angulo_alete = angulo_aleta2
                elif y ==4:
                    angulo_alete = angulo_aleta3
                    y=-1
                if not x%2==0:
                    posicion_ale = [shapePezB[1][x//2][0],shapePezB[1][x//2][1],shapePezB[1][x//2][2]]
                    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE,tr.matmul([ tr.uniformScale(3),tr.translate(pos_pez[0],pos_pez[1],pos_pez[2]),tr.rotationZ(angulos_peces[index_random]),tr.translate(-pos_pez[0],-pos_pez[1],-pos_pez[2]),tr.translate(posicion_ale[0],posicion_ale[1],posicion_ale[2]),tr.rotationZ(angulo_alete),tr.translate(-posicion_ale[0],-posicion_ale[1],-posicion_ale[2])]))
                    pipeline.drawShape(p)
                    index_random+=1
                else:
                    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.uniformScale(3),tr.translate(p[1][0],p[1][1],p[1][2]),tr.rotationZ(angulos_peces[index_random]),tr.translate(-p[1][0],-p[1][1],-p[1][2])]))
                    pos_pez=p[1]
                    pipeline.drawShape(p[0])
                x+=1

        if not controller.C:
            x=0
            y=-1
            alete = 0
            pos_pez = 0
            index_random = len(shapePezB[0])
            for p in shapePezC[0]:
                y+=1
                if y ==0:
                    angulo_alete = angulo_aleta
                elif y ==1:
                    angulo_alete = angulo_aleta1
                elif y ==2:
                    angulo_alete = angulo_aleta2
                elif y ==4:
                    angulo_alete = angulo_aleta3
                    y=-1
                if not x%2==0:
                    posicion_ale = [shapePezC[1][x//2][0],shapePezC[1][x//2][1],shapePezC[1][x//2][2]]
                    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE,tr.matmul([ tr.uniformScale(3),tr.translate(pos_pez[0],pos_pez[1],pos_pez[2]),tr.rotationZ(angulos_peces[index_random]),tr.translate(-pos_pez[0],-pos_pez[1],-pos_pez[2]),tr.translate(posicion_ale[0],posicion_ale[1],posicion_ale[2]),tr.rotationZ(angulo_alete),tr.translate(-posicion_ale[0],-posicion_ale[1],-posicion_ale[2])]))
                    pipeline.drawShape(p)
                    index_random+=1
                else:
                    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.uniformScale(3),tr.translate(p[1][0],p[1][1],p[1][2]),tr.rotationZ(angulos_peces[index_random]),tr.translate(-p[1][0],-p[1][1],-p[1][2])]))
                    pos_pez=p[1]
                    pipeline.drawShape(p[0])
                x+=1
        x=0
        
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.uniformScale(3))
        
        if controller.A:
            pipeline.drawShape(gpu_surfaceA)

        if controller.B:
            pipeline.drawShape(gpu_surfaceB)

        if controller.C:
            pipeline.drawShape(gpu_surfaceC)

        pipeline.drawShape(gpu_surfaceBorde)


        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
