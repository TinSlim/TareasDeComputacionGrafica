# coding=utf-8
"""
Daniel Calderon, CC3501, 2019-2
Drawing many cars in 2D using scene_graph2
"""

"""Módulos"""
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

"""Módulos del Profe"""
import Modulo.transformations as tr
import Modulo.basic_shapes as bs
import Modulo.scene_graph as sg
import Modulo.easy_shaders as es
import Modulo.ex_curves as curves

"""Módulos mios"""
import Modulo.csvtolist2 as ctl


#Using datos.csv file to make a list        TODO  BORRAR TRY EXCEPT
try:
    archivo_csv=print(sys.argv[1])
except:
    archivo_csv="datos.csv"

csv_list=ctl.parsear(archivo_csv)
coordenadas=ctl.parseado_coordenada(csv_list)
caidas=ctl.ubicacion_caidas(csv_list)

lista_incluyendo_caidas=ctl.crater(coordenadas,caidas)
trayectoria=ctl.agregar_coord_z2(lista_incluyendo_caidas)

curvas_int=[]
curvas_totales=[]

derivadas_int=[]
derivadas_totales=[]

conteo_curvas=0
n=0
tamanio=0
for curva in trayectoria:
    tamanio=len(curva)
    tamanio=tamanio-3
    while n<tamanio:
        #curvas_int.append( curves.Catmull(curva[n],curva[n+1],curva[n+2],curva[n+3]) )
        curvas_int.append(curves.evalCurve(curves.Catmull(curva[n],curva[n+1],curva[n+2],curva[n+3]),1000))
        derivadas_int.append(curves.evalCurve_prima(curves.Catmull(curva[n],curva[n+1],curva[n+2],curva[n+3]),1000))
        n+=1
    curvas_totales.append(curvas_int)
    derivadas_totales.append(derivadas_int)
    curvas_int=[]
    derivadas_int=[]
    n=0

curvas_finales=[]
counter=1
primera=True
for curva in curvas_totales:
    tamanio=len(curva)
    curva_total=curva[0]
    while counter<tamanio:
        curva_total=np.concatenate((curva_total,curva[counter]))
        counter+=1
    curvas_finales.append(curva_total)    
    counter=0

derivadas_finales=[]
counter=1
primera=True
for curva in derivadas_totales:
    tamanio=len(curva)
    derivada_total=curva[0]
    while counter<tamanio:
        derivada_total=np.concatenate((derivada_total,curva[counter]))
        counter+=1
    derivadas_finales.append(derivada_total)    
    counter=0

print(derivadas_finales)

#TODO   Funciones de prueba para el carril, son rectas

def funcion_funcion(array,x_actual):
    y=0
    for ubicacion in range(len(array)):
        if x_actual>array[ubicacion][0]:
            y=(  (array[ubicacion+1][1]-array[ubicacion][1])/(array[ubicacion+1][0]-array[ubicacion][0]))*(x_actual-array[ubicacion][0])+array[ubicacion][1]
    return y

def derivada_funcion(array,x_actual):
    variable=0
    for ubicacion in range(len(array)):
        if x_actual>array[ubicacion][0]:
            variable=(  (array[ubicacion+1][1]-array[ubicacion][1])/(array[ubicacion+1][0]-array[ubicacion][0]))
    return variable


class Controller():
    salto=False
    saltando=False
    derivada=0
    x=0
    y=0
    vy=0
    g=9

    posicion_inicial=0

control=Controller()

def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    if key == glfw.KEY_SPACE and control.saltando==False:
        control.salto=True
        return
    
    elif key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print('Unknown key')




def createCar():
    gpuTorso = es.toGPUShape(bs.createTextureQuad("monito.png", nx=1, ny=1),GL_REPEAT,GL_LINEAR)
    gpuHombro = es.toGPUShape(bs.createTextureQuad("hombro.png", nx=1, ny=1),GL_REPEAT,GL_LINEAR)
    gpuAntebrazo = es.toGPUShape(bs.createTextureQuad("antebrazo.png", nx=1, ny=1),GL_REPEAT,GL_LINEAR)

    antebrazo = sg.SceneGraphNode("antebrazo")
    antebrazo.transform=tr.matmul([tr.translate(0.65,-0.25,0),tr.rotationZ(1.3),tr.scale(0.45,0.86,1)])
    antebrazo.childs+=[gpuAntebrazo]

    hombro = sg.SceneGraphNode("hombro")
    hombro.transform=tr.matmul([tr.rotationZ(1),tr.scale(0.5,1,1)])
    hombro.childs+=[gpuHombro]

    torso = sg.SceneGraphNode("torso")
    torso.transform=tr.scale(0.7,1,1)
    torso.childs+=[gpuTorso]


    brazo= sg.SceneGraphNode("brazo")
    brazo.transform=tr.matmul([tr.translate(0,-0.2,0),tr.uniformScale(0.4)])
    brazo.childs+=[hombro]
    brazo.childs+=[antebrazo]

    brazo_rotacion=sg.SceneGraphNode("brazo_rotacion")
    brazo_rotacion.childs+=[brazo]

    cuerpo=sg.SceneGraphNode("cuerpo")
    cuerpo.transform=tr.matmul([tr.translate(0.05,0.25,0),tr.uniformScale(0.5)])
    cuerpo.childs+=[torso]
    cuerpo.childs+=[brazo_rotacion]
    

    humano=sg.SceneGraphNode("humano")
    humano.transform=tr.scale(1,1.5,1)
    humano.childs+=[cuerpo]


    ######################
    gpuBlackQuad = es.toGPUShape(bs.createTextureQuad("rueda.png", nx=1, ny=1),GL_REPEAT,GL_LINEAR)
    gpuRedQuad = es.toGPUShape(bs.createTextureQuad("carrito.png", nx=1, ny=1),GL_REPEAT,GL_LINEAR)

    # Creating a single wheel
    wheel = sg.SceneGraphNode("wheel")
    wheel.transform = tr.uniformScale(0.2)
    wheel.childs += [gpuBlackQuad]

    wheelRotation = sg.SceneGraphNode("wheelRotation")
    wheelRotation.childs += [wheel]

    # Instanciating 2 wheels, for the front and back parts
    frontWheel = sg.SceneGraphNode("frontWheel")
    frontWheel.transform = tr.translate(0.3,-0.3,0)
    frontWheel.childs += [wheelRotation]

    backWheel = sg.SceneGraphNode("backWheel")
    backWheel.transform = tr.translate(-0.3,-0.3,0)
    backWheel.childs += [wheelRotation]
    
    # Creating the chasis of the car
    chasis = sg.SceneGraphNode("chasis")
    chasis.transform = tr.scale(1,0.5,1)
    chasis.childs += [gpuRedQuad]

    car = sg.SceneGraphNode("car")
    car.childs += [chasis]
    car.childs += [frontWheel]
    car.childs += [backWheel]

    traslatedCar = sg.SceneGraphNode("traslatedCar")
    traslatedCar.transform = tr.translate(0,0.3,0)
    traslatedCar.childs += [car,humano]

    return traslatedCar

def createCars(N):

    # First we scale a car
    scaledCar = sg.SceneGraphNode("traslatedCar")
    scaledCar.transform = tr.uniformScale(0.15)
    scaledCar.childs += [createCar()] # Re-using the previous function

    cars = sg.SceneGraphNode("cars")

    baseName = "scaledCar"
    for i in range(N):
        # A new node is only locating a scaledCar in the scene depending on index i
        newNode = sg.SceneGraphNode(baseName + str(i))
        newNode.transform = tr.translate(0.4 * i - 0.9, 0.9 - 0.4 * i, 0)
        newNode.childs += [scaledCar]

        # Now this car is added to the 'cars' scene graph
        cars.childs += [newNode]

    return cars

def createBackground():                    
    textura = es.toGPUShape(bs.createTextureQuad("fondo.jpg", nx=1, ny=1),GL_REPEAT,GL_LINEAR)
    background = sg.SceneGraphNode("background")
    background.transform=tr.uniformScale(2)
    background.childs += [textura]
    return background


if __name__ == "__main__":

    
    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 700
    height = 700

    window = glfw.create_window(width, height, "Roller Coaster of Death", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleTransformShaderProgram()
    pipeline2=es.SimpleTextureTransformShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # Creating shapes on GPU memory
    textura_marselo=createBackground()
    car = createCar()

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

     #Enable transparency
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    

    control.x=curvas_finales[0][1][0]
    control.y=curvas_finales[0][1][1]
    control.derivada=derivadas_finales[0][1][0]
    

    numero_arreglo=0

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Modifying only a specific node in the scene graph
        wheelRotationNode = sg.findNode(car, "wheelRotation")
        theta = -10 * glfw.get_time()
        wheelRotationNode.transform = tr.rotationZ(theta)

        brazo_rotacion=sg.findNode(car,"brazo_rotacion")


        #Using controller
        if control.salto==True:                                                                 #Salto
            print('salto')
            control.posicion_inicial=control.y
            control.vy=0.04
            control.salto=False
            control.saltando=True



        #Updating horizontal position X axis
        
        control.x=curvas_finales[0][numero_arreglo][0]
        control.y=curvas_finales[0][numero_arreglo][1]
        control.derivada=derivadas_finales[0][numero_arreglo][1]

        numero_arreglo+=1

        angulo=np.arctan(control.derivada)


        # Modifying only car 3
        car.transform = tr.matmul([tr.scale(0.3,0.3,0.3),   tr.translate(0,(control.y)/2, 0),tr.rotationZ(angulo)])



        #Drawing Background  
        glUseProgram(pipeline2.shaderProgram)
        sg.drawSceneGraphNode(textura_marselo,pipeline2,"transform")

        # Drawing the Car
        glUseProgram(pipeline2.shaderProgram)
        sg.drawSceneGraphNode(car, pipeline2, "transform")

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    
    glfw.terminate()