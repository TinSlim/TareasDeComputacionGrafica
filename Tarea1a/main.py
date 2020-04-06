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

"""Módulos mios"""
import Modulo.csvtolist as ctl


#Using datos.csv file to make a list        TODO  BORRAR TRY EXCEPT
try:
    archivo_csv=print(sys.argv[1])
except:
    archivo_csv="datos.csv"

lista_parseada=ctl.parsear(archivo_csv)
print(lista_parseada)
lista_coordenada=ctl.parseado_coordenada(lista_parseada)
print(lista_coordenada)

#TODO   Funciones de prueba para el carril, son rectas

def funcion_funcion(array,x_actual):
    y=0
    for ubicacion in range(len(array)):
        if x_actual>array[ubicacion][0]:
            y=(  (array[ubicacion+1][1]-array[ubicacion][1])/(array[ubicacion+1][0]-array[ubicacion][0]))*(x_actual-array[ubicacion][0])+array[ubicacion][1]
    print(x_actual)
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
    gpuTorso = es.toGPUShape(bs.createColorQuad(0,1,0))
    gpuHombro = es.toGPUShape(bs.createColorQuad(1,0.764,0.67))
    gpuAntebrazo = es.toGPUShape(bs.createColorQuad(1,0.764,0.67))

    antebrazo = sg.SceneGraphNode("antebrazo")
    antebrazo.transform=tr.matmul([tr.translate(0.65,-0.2,0),tr.rotationZ(30),tr.scale(0.45,0.86,1)])
    antebrazo.childs+=[gpuAntebrazo]

    hombro = sg.SceneGraphNode("hombro")
    hombro.transform=tr.matmul([tr.rotationZ(1),tr.scale(0.5,1,1)])
    hombro.childs+=[gpuHombro]

    torso = sg.SceneGraphNode("torso")
    torso.transform=tr.scale(0.7,1,1)
    torso.childs+=[gpuTorso]


    brazo= sg.SceneGraphNode("brazo")
    brazo.transform=tr.matmul([tr.translate(0.5,0,0),tr.uniformScale(0.7)])
    brazo.childs+=[hombro]
    brazo.childs+=[antebrazo]

    brazo_rotacion=sg.SceneGraphNode("brazo_rotacion")
    brazo_rotacion.childs+=[brazo]

    cuerpo=sg.SceneGraphNode("cuerpo")
    cuerpo.transform=tr.matmul([tr.translate(-0.2,0.5,0),tr.uniformScale(0.5)])
    cuerpo.childs+=[torso]
    cuerpo.childs+=[brazo_rotacion]
    

    humano=sg.SceneGraphNode("humano")
    humano.childs+=[cuerpo]




###########################
    gpuBlackQuad = es.toGPUShape(bs.createColorQuad(0,0,0))
    gpuRedQuad = es.toGPUShape(bs.createColorQuad(1,0,0))

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


    #Angulo inicial
    derivada=derivada_funcion(lista_coordenada,control.x)
    angulo=np.arctan(derivada)
    rotacion=0
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
            control.vy=0.08
            control.salto=False
            control.saltando=True

        
        #Rotación, ángulo se puede calcular a partir del arctan de la derivada:
        if derivada <derivada_funcion(lista_coordenada,control.x):
            derivada+=0.01
        elif derivada>derivada_funcion(lista_coordenada,control.x):
            derivada-=0.01
        angulo=np.arctan(derivada)


        if derivada>0:
            if rotacion >0:
                rotacion-=0.01
                brazo_rotacion.transform=tr.rotationZ(rotacion)
        else:
             if rotacion<1:
                rotacion+=0.01
                brazo_rotacion.transform=tr.rotationZ(rotacion)

        #Updating vertical position Y axis
        control.y=control.y+control.vy

        if control.y<funcion_funcion(lista_coordenada,control.x):           #Si cae en camino, sigue el camino      TODO
            control.vy=0
            control.saltando=False
            control.y=funcion_funcion(lista_coordenada,control.x)

        if control.saltando and (control.y-control.posicion_inicial>3):    #Caída
            control.vy=-0.06

        if not control.saltando and not control.salto:                              #Si no salta ni cae, sigue el camino
            control.y=funcion_funcion(lista_coordenada,control.x)


        #Updating horizontal position X axis
        control.x+=0.001



        # Modifying only car 3
        car.transform = tr.matmul([tr.scale(0.3,0.3,0.3),   tr.translate(0,control.y/3, 0),tr.rotationZ(angulo)])

        # Uncomment to see the position of scaledCar_3, it will fill your terminal
        #print("car3Position =", sg.findPosition(cars, "scaledCar3"))

        #Drawing Background  
        glUseProgram(pipeline2.shaderProgram)
        sg.drawSceneGraphNode(textura_marselo,pipeline2,"transform")

        # Drawing the Car
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(car, pipeline, "transform")

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    
    glfw.terminate()