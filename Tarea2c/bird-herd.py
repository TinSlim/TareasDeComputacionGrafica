"""Cristóbal Torres Gutiérrez"""


##Bibliotecas
import glfw
from glfw.GLFW import *

from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

##Módulos
import Modulo.transformations as tr
import Modulo.basic_shapes as bs
import Modulo.scene_graph as sg
import Modulo.easy_shaders as es
import Modulo.readobj as rbj
import Modulo.lighting_shaders as ls

import Modulo.csvtolist_nuevo as cv
import Modulo.curvas as crv


##Recibe entrada del usuario, en caso de no haber usa un camino predeterminado
try:
    archivo_csv=str(sys.argv[1])
except:
    archivo_csv="path.csv"



##Se trabajan los puntos del archivo csv
a=cv.parsear_archivo(archivo_csv)
lista=[]
lista_pequenia=[]
lista.append(a[len(a)-1])
for punto in a:
    lista.append(punto)
lista.append(a[0])
lista.append(a[1])

lista2=[]
for punto in lista:
    for coordenada in punto:
        lista_pequenia.append(int(coordenada))
    lista2.append(lista_pequenia)
    lista_pequenia=[]

b=crv.curvas_pajaros(lista2)

##Curva final con todos los puntos concatenados
c=crv.concatenacion(b)


##Clase controller para guardas variables
class controller():
    angulo=-0.1
    rotation_y=0.1

    angulo1=0.4
    rotation_y1=-1.0

    angulo2=1.2
    rotation_y2=-2.6

    angulo3=0.5
    rotation_y3=-1.1
    
    angulo4=0.9
    rotation_y4=-1.9

    rotacion_alas=0
    rotation_x=-1.6#0
    derivada=0

    alas_subiendo = True
    alas_bajando = False
    alas_subiendo1 = True
    alas_bajando1 = False
    alas_subiendo2 = True
    alas_bajando2 = False
    alas_subiendo3 = True
    alas_bajando3 = False
    alas_subiendo4 = True
    alas_bajando4 = False


    angulo_pajaro=0

    alasSubiendo=True

    Fondo1 = True

##Se instancia un control
control=controller()

##Botones, barra espaciadora permite cambiar la escena, Esc permite salir del programa
def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    if key == glfw.KEY_SPACE:
        control.Fondo1 = not control.Fondo1

    elif key == glfw.KEY_ESCAPE:
        sys.exit()

##Fondo 1
def fondo():
    GpuSuelo = es.toGPUShape(bs.createTextureQuad("Texturas/campo.jpg"),GL_REPEAT,GL_LINEAR)
    GpuPared = es.toGPUShape(bs.createTextureQuad("Texturas/Fondo2.png"),GL_REPEAT,GL_LINEAR)
    GpuPared2 = es.toGPUShape(bs.createTextureQuad("Texturas/Fondo2Nubes.png"),GL_REPEAT,GL_LINEAR)

    suelo = sg.SceneGraphNode("Suelo")
    suelo.childs+=[GpuSuelo]
    suelo.transform = tr.matmul([tr.uniformScale(55),tr.translate(0,0,0)])

    pared1 = sg.SceneGraphNode("pared1")
    pared1.childs+=[GpuPared2]
    pared1.transform = tr.matmul([tr.translate(0,55,15),tr.scale(125,1,45),tr.rotationX(np.pi/2)])

    pared2 = sg.SceneGraphNode("pared2")
    pared2.childs+=[GpuPared]
    pared2.transform = tr.matmul([tr.translate(0,-55,15),tr.scale(125,1,45),tr.rotationX(np.pi/2)])

    pared3 = sg.SceneGraphNode("pared3")
    pared3.childs+=[GpuPared]
    pared3.transform = tr.matmul([tr.translate(50,0,15),tr.scale(1,125,45),tr.rotationX(np.pi/2),tr.rotationY(np.pi/2)])

    pared4 = sg.SceneGraphNode("pared4")
    pared4.childs+=[GpuPared2]
    pared4.transform = tr.matmul([tr.translate(-55,0,15),tr.scale(1,125,45),tr.rotationX(np.pi/2),tr.rotationY(np.pi/2)])

    Fondo = sg.SceneGraphNode("Fondo")
    Fondo.transform = tr.translate(0,0,-1)
    Fondo.childs+= [suelo]
    Fondo.childs+= [pared1]
    Fondo.childs+= [pared2] 
    Fondo.childs+= [pared3]
    Fondo.childs+= [pared4]

    return Fondo


##Pájaro
def pajaro():
    gpuCabeza = es.toGPUShape(rbj.readOBJ("Model/cabeza.obj", (0,0.5,0.8)))
    gpuTorso = es.toGPUShape(rbj.readOBJ("Model/torso.obj", (1,1,0.3)))
    gpuAlaSupDer = es.toGPUShape(rbj.readOBJ("Model/alasupder.obj", (0,0.5,0.9)))
    gpuAlaInfDer = es.toGPUShape(rbj.readOBJ("Model/alainfder.obj", (0,0.5,1)))
    gpuAlaSupIzq = es.toGPUShape(rbj.readOBJ("Model/alasupizq.obj", (0,0.5,0.9)))
    gpuAlaInfIzq = es.toGPUShape(rbj.readOBJ("Model/alainfizq.obj", (0,0.5,1)))
    a=bs.createColorQuad(0, 0, 0)
    gpuBlackQuad =  es.toGPUShape(a)

    

    #################Ala Derecha
    #Ala inf derecha
    AlaInfDerecha = sg.SceneGraphNode("AlaInfDerecha")
    AlaInfDerecha.transform = tr.translate(0,0,0)  #Ajustar bn
    AlaInfDerecha.childs+=[gpuAlaInfDer]

    #Rotación ala inf derecha
    RotacionAlaInfDerecha = sg.SceneGraphNode("RotacionAlaInfDerecha")
    RotacionAlaInfDerecha.transform = tr.matmul([tr.translate(-1.5,-2,-2),tr.rotationY(np.pi/3),tr.translate(1,2,2)])
    RotacionAlaInfDerecha.childs+= [AlaInfDerecha]

    #Ala sup derecha
    AlaSupDerecha = sg.SceneGraphNode("AlaSupDerecha")
    AlaSupDerecha.childs+=[gpuAlaSupDer]
   
    #Ala derecha
    AlaDerecha = sg.SceneGraphNode("AlaDerecha")
    AlaDerecha.childs+=[AlaSupDerecha]
    AlaDerecha.childs+=[RotacionAlaInfDerecha]
    #AlaDerecha.transform = tr.matmul([tr.translate(-1,-2.5,0),tr.rotationY(np.pi),tr.rotationX(np.pi),tr.translate(1,2.5,0)])  #AlaDerecha.transform = tr.matmul([tr.translate(0,-2,0),tr.rotationX(np.pi*(2/3)),tr.translate(0,2,0.5)])#

    #############        tr.rotationX(np.pi)
    #Ala inf derecha
    AlaInfIzquierda = sg.SceneGraphNode("AlaInfIzquierda")
    #AlaInfIzquierda.transform = tr.translate(0,0,0)  #Ajustar bn
    AlaInfIzquierda.childs+=[gpuAlaInfIzq]

    #Rotación ala inf izquierda
    RotacionAlaInfIzquierda = sg.SceneGraphNode("RotacionAlaInfIzquierda") 
    RotacionAlaInfIzquierda.transform = tr.matmul([tr.translate(1.5,-2,-2),tr.rotationY(-np.pi/3),tr.translate(-1,2,2)])
    RotacionAlaInfIzquierda.childs+= [AlaInfIzquierda]

    #Ala sup derecha
    AlaSupIzquierda = sg.SceneGraphNode("AlaSupIzquierda")
    AlaSupIzquierda.childs+=[gpuAlaSupIzq]

    #Ala derecha
    AlaIzquierda = sg.SceneGraphNode("AlaIzquierda")
    AlaIzquierda.childs+=[AlaSupIzquierda]
    AlaIzquierda.childs+=[RotacionAlaInfIzquierda]
    
    #Alas
    Alas = sg.SceneGraphNode("Alas")
    Alas.childs+=[AlaDerecha]
    Alas.childs+=[AlaIzquierda]

    #Torso
    Torso = sg.SceneGraphNode("Torso")
    Torso.childs+= [gpuTorso]
    #Torso.transform=tr.matmul([tr.rotationX(np.pi/2),tr.uniformScale(1)])
    #Torso.transform=tr.matmul([tr.rotationZ(90),tr.translate(0,0,0)])

    #Cabeza
    Cabeza = sg.SceneGraphNode("Cabeza")
    Cabeza.childs+= [gpuCabeza]
    #Cabeza.transform=tr.rotationX(np.pi/2)

    #Cuerpo
    Cuerpo = sg.SceneGraphNode("Cuerpo")
    Cuerpo.childs+= [Torso]
    Cuerpo.childs+= [Cabeza]


    #Pajaro Total1
    Pajaro1 = sg.SceneGraphNode("Pajaro1")
    Pajaro1.childs+=[Alas]
    Pajaro1.childs+=[Cuerpo]
    Pajaro1.transform=tr.matmul([tr.uniformScale(0.1),tr.rotationX(np.pi*(1/2))])

    #Pajaro
    Pajaro = sg.SceneGraphNode("Pajaro")
    Pajaro.childs+=[Pajaro1]

    return Pajaro

##Para crear un cubo con una textura en un orden específico
def createTextureCube(image_filename):

    # Defining locations and texture coordinates for each vertex of the shape  
    vertices = [
    #   positions         texture coordinates
    # Z+
        -5, -5,  5, 0, 0.3,     #x,y-->| abajo
         5, -5,  5, 0.5, 0.3,
         5,  5,  5, 0.5, 0,
        -5,  5,  5, 0, 0,

    # Z-
        -5, -5, -5, 0.5, 0.3,
         5, -5, -5, 1, 0.3,
         5,  5, -5, 1, 0,
        -5,  5, -5, 0.5, 0,
        
    # X+
         5, -5, -5, 0, 0.6,
         5,  5, -5, 0.5, 0.6,
         5,  5,  5, 0.5, 0.3,
         5, -5,  5, 0, 0.3
,
 
    # X-
        -5, -5, -5, 0.5, 0.6,
        -5,  5, -5, 1, 0.6,
        -5,  5,  5, 1, 0.3,
        -5, -5,  5, 0.5, 0.3,

    # Y+
        -5,  5, -5, 0, 0.9,
         5,  5, -5, 0.5, 0.9,
         5,  5,  5, 0.5, 0.6,
        -5,  5,  5, 0, 0.6,

    # Y-
        -5, -5, -5, 0.5, 0.9,
         5, -5, -5, 1, 0.9,
         5, -5,  5, 1, 0.6,
        -5, -5,  5, 0.5, 0.6
        ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
          0, 1, 2, 2, 3, 0, # Z+
          7, 6, 5, 5, 4, 7, # Z-
          8, 9,10,10,11, 8, # X+
         15,14,13,13,12,15, # X-
         19,18,17,17,16,19, # Y+
         20,21,22,22,23,20] # Y-

    return bs.Shape(vertices, indices, image_filename)


##Fondo2, a partir de un cubo
def createWall():
    Gpu1 = es.toGPUShape(createTextureCube("Texturas/espacio.png"),GL_REPEAT,GL_LINEAR)
    Gpu2 = es.toGPUShape(bs.createTextureQuad("Texturas/sol.jpg"),GL_REPEAT,GL_LINEAR)
    Gpu3 = es.toGPUShape(bs.createTextureQuad("Texturas/satelite.png"),GL_CLAMP_TO_EDGE,GL_LINEAR)

    Satelite = sg.SceneGraphNode("Satelite")
    Satelite.childs += [Gpu3]
    Satelite.transform = tr.matmul([tr.uniformScale(0.7),tr.rotationZ(10),tr.rotationY(np.pi/2),])

    Sol = sg.SceneGraphNode("Sol")
    Sol.childs += [Gpu2]
    Sol.transform = tr.matmul([tr.translate(-3, 0, 3),tr.rotationZ(1),tr.rotationY(np.pi/2),])

    Fondo1 = sg.SceneGraphNode("Fondo1")
    Fondo1.childs += [Gpu1]
    Fondo1.transform = tr.uniformScale(22)

    Fondos = sg.SceneGraphNode("Fondos")
    Fondos.childs+=[Fondo1]
    Fondos.childs+=[Sol]
    Fondos.childs+=[Satelite]
    

    return Fondos



if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    ##Tamaño ventana
    width = 600
    height = 600
    
    window = glfw.create_window(width, height, "Bird-Herd", None, None)
    glfw.set_input_mode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    #Transparency
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Defining shader programs
    pipeline = ls.SimplePhongShaderProgram()
    mvpTPipeline = es.SimpleTextureModelViewProjectionShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    #glClearColor(0.85, 0.85, 0.85, 1.0)
    glClearColor(19/255, 175/255, 1, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    gpuAxis = es.toGPUShape(bs.createAxis(7))

    Fondo1 = createWall()
    Fondo2 = fondo()
    Satelite_nodo = sg.findNode(Fondo1,"Satelite")

    #####################################################
    ##Se crean 5 pájaros y se guardan los nodos que se usarán despues##
    #####################################################
    pajarito = pajaro()

    Ala_Inf_Izquierda=sg.findNode(pajarito, "RotacionAlaInfIzquierda")
    Ala_Inf_Derecha=sg.findNode(pajarito, "RotacionAlaInfDerecha")
    
    Ala_Derecha = sg.findNode(pajarito, "AlaDerecha")
    Ala_Izquierda = sg.findNode(pajarito, "AlaIzquierda")
    Pajaro1 = sg.findNode(pajarito, "Pajaro")
    Pajaro2 = sg.findNode(pajarito, "Pajaro1")
    ###############
    pajarito2 = pajaro()
    
    Ala_Inf_Izquierda2=sg.findNode(pajarito2, "RotacionAlaInfIzquierda")
    Ala_Inf_Derecha2=sg.findNode(pajarito2, "RotacionAlaInfDerecha")
    
    Ala_Derecha2 = sg.findNode(pajarito2, "AlaDerecha")
    Ala_Izquierda2 = sg.findNode(pajarito2, "AlaIzquierda")
    Pajaro12 = sg.findNode(pajarito2, "Pajaro")
    Pajaro22 = sg.findNode(pajarito2, "Pajaro1")
    ###############
    pajarito3 = pajaro()

    Ala_Inf_Izquierda3=sg.findNode(pajarito3, "RotacionAlaInfIzquierda")
    Ala_Inf_Derecha3=sg.findNode(pajarito3, "RotacionAlaInfDerecha")
    
    Ala_Derecha3 = sg.findNode(pajarito3, "AlaDerecha")
    Ala_Izquierda3 = sg.findNode(pajarito3, "AlaIzquierda")
    Pajaro13 = sg.findNode(pajarito3, "Pajaro")
    Pajaro23 = sg.findNode(pajarito3, "Pajaro1")
    ###############
    pajarito4 = pajaro()

    Ala_Inf_Izquierda4=sg.findNode(pajarito4, "RotacionAlaInfIzquierda")
    Ala_Inf_Derecha4=sg.findNode(pajarito4, "RotacionAlaInfDerecha")
    
    Ala_Derecha4 = sg.findNode(pajarito4, "AlaDerecha")
    Ala_Izquierda4 = sg.findNode(pajarito4, "AlaIzquierda")
    Pajaro14 = sg.findNode(pajarito4, "Pajaro")
    Pajaro24 = sg.findNode(pajarito4, "Pajaro1")
    ###############
    pajarito5 = pajaro()

    Ala_Inf_Izquierda5=sg.findNode(pajarito5, "RotacionAlaInfIzquierda")
    Ala_Inf_Derecha5=sg.findNode(pajarito5, "RotacionAlaInfDerecha")
    
    Ala_Derecha5 = sg.findNode(pajarito5, "AlaDerecha")
    Ala_Izquierda5 = sg.findNode(pajarito5, "AlaIzquierda")
    Pajaro15 = sg.findNode(pajarito5, "Pajaro")
    Pajaro25 = sg.findNode(pajarito5, "Pajaro1")
    ###############

    ##############################################
    ##Configuración incial nodos anteriores para los 5 pájaros##
    ##############################################
    Ala_Inf_Izquierda.transform = tr.matmul([tr.translate(1.5,-2,-2),tr.rotationY(-(control.angulo)),tr.translate(-1.5,2,2)])
    Ala_Inf_Derecha.transform = tr.matmul([tr.translate(-1.5,-2,-2),tr.rotationY(control.angulo),tr.translate(1.5,2,2)])

    Ala_Derecha.transform = tr.matmul([tr.translate(-1,-2.5,0),tr.rotationZ(control.rotation_y),tr.rotationX(control.rotation_x),tr.translate(1,2.5,0)])###
    Ala_Izquierda.transform = tr.matmul([tr.translate(1,-2.5,0),tr.rotationZ(-1*(control.rotation_y)),tr.rotationX(control.rotation_x),tr.translate(-1,2.5,0)])
    ##########
    Ala_Inf_Izquierda2.transform = tr.matmul([tr.translate(1.5,-2,-2),tr.rotationY(-(control.angulo)),tr.translate(-1.5,2,2)])
    Ala_Inf_Derecha2.transform = tr.matmul([tr.translate(-1.5,-2,-2),tr.rotationY(control.angulo),tr.translate(1.5,2,2)])

    Ala_Derecha2.transform = tr.matmul([tr.translate(-1,-2.5,0),tr.rotationZ(control.rotation_y),tr.rotationX(control.rotation_x),tr.translate(1,2.5,0)])###
    Ala_Izquierda2.transform = tr.matmul([tr.translate(1,-2.5,0),tr.rotationZ(-1*(control.rotation_y)),tr.rotationX(control.rotation_x),tr.translate(-1,2.5,0)])
    ##########
    Ala_Inf_Izquierda3.transform = tr.matmul([tr.translate(1.5,-2,-2),tr.rotationY(-(control.angulo)),tr.translate(-1.5,2,2)])
    Ala_Inf_Derecha3.transform = tr.matmul([tr.translate(-1.5,-2,-2),tr.rotationY(control.angulo),tr.translate(1.5,2,2)])

    Ala_Derecha3.transform = tr.matmul([tr.translate(-1,-2.5,0),tr.rotationZ(control.rotation_y),tr.rotationX(control.rotation_x),tr.translate(1,2.5,0)])###
    Ala_Izquierda3.transform = tr.matmul([tr.translate(1,-2.5,0),tr.rotationZ(-1*(control.rotation_y)),tr.rotationX(control.rotation_x),tr.translate(-1,2.5,0)])
    ##########
    Ala_Inf_Izquierda4.transform = tr.matmul([tr.translate(1.5,-2,-2),tr.rotationY(-(control.angulo)),tr.translate(-1.5,2,2)])
    Ala_Inf_Derecha4.transform = tr.matmul([tr.translate(-1.5,-2,-2),tr.rotationY(control.angulo),tr.translate(1.5,2,2)])

    Ala_Derecha4.transform = tr.matmul([tr.translate(-1,-2.5,0),tr.rotationZ(control.rotation_y),tr.rotationX(control.rotation_x),tr.translate(1,2.5,0)])###
    Ala_Izquierda4.transform = tr.matmul([tr.translate(1,-2.5,0),tr.rotationZ(-1*(control.rotation_y)),tr.rotationX(control.rotation_x),tr.translate(-1,2.5,0)])
    ##########
    Ala_Inf_Izquierda5.transform = tr.matmul([tr.translate(1.5,-2,-2),tr.rotationY(-(control.angulo)),tr.translate(-1.5,2,2)])
    Ala_Inf_Derecha5.transform = tr.matmul([tr.translate(-1.5,-2,-2),tr.rotationY(control.angulo),tr.translate(1.5,2,2)])

    Ala_Derecha5.transform = tr.matmul([tr.translate(-1,-2.5,0),tr.rotationZ(control.rotation_y),tr.rotationX(control.rotation_x),tr.translate(1,2.5,0)])###
    Ala_Izquierda5.transform = tr.matmul([tr.translate(1,-2.5,0),tr.rotationZ(-1*(control.rotation_y)),tr.rotationX(control.rotation_x),tr.translate(-1,2.5,0)])
    #########

    #Variables iniciales
    rotacion_pajaro=0

    t0 = glfw.get_time()
    camera_theta = -3*np.pi/4
    camera_theta2 = 0
    
    counter=0

    cursor_at = glfw.get_cursor_pos(window)
    cursor_actual=cursor_at

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        ##Ubicación del cursor
        cursor_at = glfw.get_cursor_pos(window)
        

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        ##Acciones del cursor
        if cursor_actual[0]<cursor_at[0]:        #Si se mueve a la derecha
            if cursor_actual[1]<cursor_at[1] :      #Si se mueve hacia abajo
                camera_theta2 -= 2*(cursor_at[1]-cursor_actual[1])/500
                camera_theta += 2* (cursor_at[0]-cursor_actual[0])/500
            if cursor_actual[1]>cursor_at[1]:        #Si se mueve havia arriba
                camera_theta2 += 2* (cursor_actual[1]-cursor_at[1])/500
                camera_theta += 2* (cursor_at[0]-cursor_actual[0])/500
            

        elif cursor_actual[0]>cursor_at[0]:      #Si se mueve a la izquierda  
            if cursor_actual[1]<cursor_at[1]:        #Si se mueve hacia abajo
                camera_theta2 -= 2* (cursor_at[1]-cursor_actual[1])/500  
                camera_theta -= 2* (cursor_actual[0]-cursor_at[0])/500
            if cursor_actual[1]>cursor_at[1]:         #Si se mueve hacia arriba
                camera_theta2 += 2* (cursor_actual[1]-cursor_at[1])/500
                camera_theta -= 2* (cursor_actual[0]-cursor_at[0])/500

        #Se actualiza el cursor para su comparación en el cilo siguiente
        cursor_actual = cursor_at 
        

        ############################
        ##Movimiento de Alas automático##
        ############################
        if control.alas_subiendo:
            if control.angulo>1.2 or control.rotation_y<-2.6:
                control.alas_subiendo = not control.alas_subiendo
                control.alas_bajando = not control.alas_bajando
            else:
                control.angulo+=0.02
                control.rotation_y-=0.04
        elif control.alas_bajando:
            if control.angulo<-0.1 or control.rotation_y>0.1:
                control.alas_subiendo = not control.alas_subiendo
                control.alas_bajando = not control.alas_bajando
            else:
                control.angulo-=0.02
                control.rotation_y+=0.04

        if control.alas_subiendo1:
            if control.angulo1>1.2 or control.rotation_y1<-2.6:
                control.alas_subiendo1 = not control.alas_subiendo1
                control.alas_bajando1 = not control.alas_bajando1
            else:
                control.angulo1+=0.02
                control.rotation_y1-=0.04
        elif control.alas_bajando1:
            if control.angulo1<-0.1 or control.rotation_y1>0.1:
                control.alas_subiendo1 = not control.alas_subiendo1
                control.alas_bajando1 = not control.alas_bajando1
            else:
                control.angulo1-=0.02
                control.rotation_y1+=0.04

        if control.alas_subiendo2:
            if control.angulo2>1.2 or control.rotation_y2<-2.6:
                control.alas_subiendo2 = not control.alas_subiendo2
                control.alas_bajando2 = not control.alas_bajando2
            else:
                control.angulo2+=0.02
                control.rotation_y2-=0.04
        elif control.alas_bajando2:
            if control.angulo2<-0.1 or control.rotation_y2>0.1:
                control.alas_subiendo2 = not control.alas_subiendo2
                control.alas_bajando2 = not control.alas_bajando2
            else:
                control.angulo2-=0.02
                control.rotation_y2+=0.04

        if control.alas_subiendo3:
            if control.angulo3>1.2 or control.rotation_y3<-2.6:
                control.alas_subiendo3 = not control.alas_subiendo3
                control.alas_bajando3 = not control.alas_bajando3
            else:
                control.angulo3+=0.02
                control.rotation_y3-=0.04
        elif control.alas_bajando3:
            if control.angulo3<-0.1 or control.rotation_y3>0.1:
                control.alas_subiendo3 = not control.alas_subiendo3
                control.alas_bajando3 = not control.alas_bajando3
            else:
                control.angulo3-=0.02
                control.rotation_y3+=0.04

        if control.alas_subiendo4:
            if control.angulo4>1.2 or control.rotation_y4<-2.6:
                control.alas_subiendo4 = not control.alas_subiendo4
                control.alas_bajando4 = not control.alas_bajando4
            else:
                control.angulo4+=0.02
                control.rotation_y4-=0.04
        elif control.alas_bajando4:
            if control.angulo4<-0.1 or control.rotation_y4>0.1:
                control.alas_subiendo4 = not control.alas_subiendo4
                control.alas_bajando4 = not control.alas_bajando4
            else:
                control.angulo4-=0.02
                control.rotation_y4+=0.04
        
        ##############################
        ##Actualización Alas para cada pajaro##
        ##############################
        Ala_Inf_Izquierda.transform = tr.matmul([tr.translate(1.5,-2,-2),tr.rotationY(-(control.angulo)),tr.translate(-1.5,2,2)])
        Ala_Inf_Derecha.transform = tr.matmul([tr.translate(-1.5,-2,-2),tr.rotationY(control.angulo),tr.translate(1.5,2,2)])

        Ala_Derecha.transform = tr.matmul([tr.translate(-1,-2.5,0),tr.rotationZ(control.rotation_y),tr.rotationX(control.rotation_x),tr.translate(1,2.5,0)])###
        Ala_Izquierda.transform = tr.matmul([tr.translate(1,-2.5,0),tr.rotationZ(-1*(control.rotation_y)),tr.rotationX(control.rotation_x),tr.translate(-1,2.5,0)])
        ###############
        Ala_Inf_Izquierda2.transform = tr.matmul([tr.translate(1.5,-2,-2),tr.rotationY(-(control.angulo1)),tr.translate(-1.5,2,2)])
        Ala_Inf_Derecha2.transform = tr.matmul([tr.translate(-1.5,-2,-2),tr.rotationY(control.angulo1),tr.translate(1.5,2,2)])

        Ala_Derecha2.transform = tr.matmul([tr.translate(-1,-2.5,0),tr.rotationZ(control.rotation_y1),tr.rotationX(control.rotation_x),tr.translate(1,2.5,0)])###
        Ala_Izquierda2.transform = tr.matmul([tr.translate(1,-2.5,0),tr.rotationZ(-1*(control.rotation_y1)),tr.rotationX(control.rotation_x),tr.translate(-1,2.5,0)])
        ###############
        Ala_Inf_Izquierda3.transform = tr.matmul([tr.translate(1.5,-2,-2),tr.rotationY(-(control.angulo2)),tr.translate(-1.5,2,2)])
        Ala_Inf_Derecha3.transform = tr.matmul([tr.translate(-1.5,-2,-2),tr.rotationY(control.angulo2),tr.translate(1.5,2,2)])

        Ala_Derecha3.transform = tr.matmul([tr.translate(-1,-2.5,0),tr.rotationZ(control.rotation_y2),tr.rotationX(control.rotation_x),tr.translate(1,2.5,0)])###
        Ala_Izquierda3.transform = tr.matmul([tr.translate(1,-2.5,0),tr.rotationZ(-1*(control.rotation_y2)),tr.rotationX(control.rotation_x),tr.translate(-1,2.5,0)])
        ###############
        Ala_Inf_Izquierda4.transform = tr.matmul([tr.translate(1.5,-2,-2),tr.rotationY(-(control.angulo3)),tr.translate(-1.5,2,2)])
        Ala_Inf_Derecha4.transform = tr.matmul([tr.translate(-1.5,-2,-2),tr.rotationY(control.angulo3),tr.translate(1.5,2,2)])

        Ala_Derecha4.transform = tr.matmul([tr.translate(-1,-2.5,0),tr.rotationZ(control.rotation_y3),tr.rotationX(control.rotation_x),tr.translate(1,2.5,0)])###
        Ala_Izquierda4.transform = tr.matmul([tr.translate(1,-2.5,0),tr.rotationZ(-1*(control.rotation_y3)),tr.rotationX(control.rotation_x),tr.translate(-1,2.5,0)])
        ################
        Ala_Inf_Izquierda5.transform = tr.matmul([tr.translate(1.5,-2,-2),tr.rotationY(-(control.angulo4)),tr.translate(-1.5,2,2)])
        Ala_Inf_Derecha5.transform = tr.matmul([tr.translate(-1.5,-2,-2),tr.rotationY(control.angulo4),tr.translate(1.5,2,2)])

        Ala_Derecha5.transform = tr.matmul([tr.translate(-1,-2.5,0),tr.rotationZ(control.rotation_y4),tr.rotationX(control.rotation_x),tr.translate(1,2.5,0)])###
        Ala_Izquierda5.transform = tr.matmul([tr.translate(1,-2.5,0),tr.rotationZ(-1*(control.rotation_y4)),tr.rotationX(control.rotation_x),tr.translate(-1,2.5,0)])
   

        ##Posición de los pájaros (x,y,z) según coordenadas de la curva del inicio
        camaraX=c[counter][0]
        camaraY=c[counter][1]
        camaraZ=c[counter][2]


        ##Posición siguiente de los pájaros (x,y,z) según coordenadas de la curva del inicio
        posicion_siguienteX = c[counter+1][0]
        posicion_siguienteY = c[counter+1][1]
        posicion_siguienteZ = c[counter+1][2]
        
        ##Obtención derivada entre ambos puntos
        if (posicion_siguienteX-camaraX)!=0:
            derivada = (posicion_siguienteY-camaraY) / (posicion_siguienteX-camaraX)
            if derivada>control.derivada:
                control.derivada+=0.01
            elif derivada<control.derivada:
                control.derivada-=0.01

        ##Obtención del ángulo con arctan de la derivada
        if camaraX>posicion_siguienteX and camaraY<posicion_siguienteY:
            angulo_pajaro=np.arctan(control.derivada) - np.pi/2#no cambiar
        elif camaraX>posicion_siguienteX and camaraY > posicion_siguienteY:
            angulo_pajaro=np.arctan(control.derivada) - np.pi/2#no cambiar
        elif camaraX<posicion_siguienteX and camaraY > posicion_siguienteY:
            angulo_pajaro=-np.arctan(control.derivada) +np.pi + np.pi/2 #arreglar
        else:
            angulo_pajaro=np.arctan(control.derivada)+np.pi -np.pi/2

        ##Traslación de los pájaros por los puntos de la curva
        Pajaro1.transform = tr.translate(camaraX,camaraY,camaraZ)
        Pajaro12.transform = tr.translate(camaraX+1,camaraY+1,camaraZ+1)
        Pajaro13.transform = tr.translate(camaraX+2,camaraY+2,camaraZ+2)
        Pajaro14.transform = tr.translate(camaraX+1,camaraY-1,camaraZ+1)
        Pajaro15.transform = tr.translate(camaraX+2,camaraY-2,camaraZ+2)
       

        #################
        ##Rotación pájaros##
        #################

        ##Rotacion respecto a su eje
        if angulo_pajaro>control.angulo_pajaro:
            control.angulo_pajaro+=0.01
        elif angulo_pajaro<control.angulo_pajaro:
            control.angulo_pajaro-=0.01

        ##Aplicar Rotaciones
        Pajaro2.transform = tr.matmul([tr.uniformScale(0.1),tr.rotationX(np.pi*(1/2)),tr.rotationY(control.angulo_pajaro)])
        Pajaro22.transform = tr.matmul([tr.uniformScale(0.1),tr.rotationX(np.pi*(1/2)),tr.rotationY(control.angulo_pajaro)])
        Pajaro23.transform = tr.matmul([tr.uniformScale(0.1),tr.rotationX(np.pi*(1/2)),tr.rotationY(control.angulo_pajaro)])
        Pajaro24.transform = tr.matmul([tr.uniformScale(0.1),tr.rotationX(np.pi*(1/2)),tr.rotationY(control.angulo_pajaro)])
        Pajaro25.transform = tr.matmul([tr.uniformScale(0.1),tr.rotationX(np.pi*(1/2)),tr.rotationY(control.angulo_pajaro)])


        ####################
        ##Vectores de la cámara##
        ####################
        ##Radio
        R = 12

        #Coordenadas esféricas
        camX = R * np.sin(camera_theta+3) * np.sin(camera_theta2-2)
        camY = R * np.cos(camera_theta+3) * np.sin(camera_theta2-2)
        camZ = R * np.cos(camera_theta2-2)

        ##Vector up varía según dónde se observe
        headX = R * np.sin(camera_theta+3) * np.sin(camera_theta2-2+np.pi/2)
        headY = R * np.cos(camera_theta+3) * np.sin(camera_theta2-2+np.pi/2)
        headZ = R * np.cos(camera_theta2-2+np.pi/2)
        
        
        ##Si se van a acabar los puntos, empezar de nuevo
        if counter==len(c)-4:      
            counter=0
        counter+=1

        ##Actualizar vectores de cámara
        viewPos2 = np.array([5, 5, 5])          #Posición cámara
        viewPos = np.array([camX+5, camY+5, camZ])   #Eye cámara

        view = tr.lookAt(
            viewPos2,
            viewPos,
            np.array([ headX,headY,headZ])
        )


        # Setting up the projection transform
        projection = tr.perspective(60, float(width)/float(height), 0.001, 500)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #Se elige el fondo
        if control.Fondo1:
            Fondo = Fondo1
        else:
            Fondo = Fondo2


        # Drawing shapes
        glUseProgram(mvpTPipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(mvpTPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(mvpTPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(mvpTPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        sg.drawSceneGraphNode(Fondo, mvpTPipeline, "model")
        
        
        glUseProgram(pipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), -3, 0, 3)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 100)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.1)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.uniformScale(3))


        #Dibujado de los 5 pájaros
        sg.drawSceneGraphNode(pajarito, pipeline, "model")
        sg.drawSceneGraphNode(pajarito2, pipeline, "model")
        sg.drawSceneGraphNode(pajarito3, pipeline, "model")
        sg.drawSceneGraphNode(pajarito4, pipeline, "model")
        sg.drawSceneGraphNode(pajarito5, pipeline, "model")

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()

