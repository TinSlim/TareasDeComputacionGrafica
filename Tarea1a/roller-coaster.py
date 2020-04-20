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
import Modulo.csvtolist_nuevo as ctl
import Modulo.curvas as crv

#Se recoge entrada
try:
    archivo_csv=str(sys.argv[1])
except:
    archivo_csv="datos.csv"

#Parsear el csv
parse=ctl.parsear_archivo(archivo_csv)
lista_de_x=ctl.encontrar_x(parse)
parse_sin_x=ctl.quitar_x(parse)

parse_sin_x2=[]
parse_sin_x2.append([-1,2])
n=0
while n<len(parse_sin_x):
    parse_sin_x2.append(parse_sin_x[n])
    n+=1
parse_sin_x2.append([n,1])
ultima_coordenada=parse_sin_x2[len(parse_sin_x2)-2]

#Factor que pondera (max altura)
maximo=ctl.maximo_y(parse_sin_x2)

#Armar curvas
separadas=crv.separador_de_curvas(parse_sin_x2,lista_de_x)
curvas_y_rectas=crv.curvas_rectas(separadas)
camino_final=crv.concatenacion(curvas_y_rectas)
numero=0

camino_final=ctl.ponderar_parseado_numpy_y(camino_final,maximo)




def createBackground():                    
    textura = es.toGPUShape(bs.createTextureQuad("Imagenes/fondo_vigas.jpg", nx=1, ny=1),GL_REPEAT,GL_LINEAR)
    background = sg.SceneGraphNode("background")
    background.transform=tr.scale(1,2,1)
    background.childs += [textura]
    return background

def createPistaShape(lista,R,G,B):
    # Defining the location and colors of each vertex  of the shape
    
    vertices=[]
    for punto in lista:

        vertices.append((punto[0]))
        vertices.append((2))   ###########
        vertices.append((punto[2]))
        vertices.append(R)
        vertices.append(G)
        vertices.append(B)

        vertices.append((punto[0]))
        vertices.append((punto[1]))
        vertices.append((punto[2]))
        vertices.append(R)
        vertices.append(G)
        vertices.append(B) 
 
    indices=[]
    puntos=len(vertices)/6
    n=0
    while n<puntos-2:
       indices.append(n)
       indices.append(n+1)
       indices.append(n+2)
       n+=1
    

    return bs.Shape(vertices, indices)

def createCar():
    gpuTorso = es.toGPUShape(bs.createTextureQuad("Imagenes/monito.png", nx=1, ny=1),GL_REPEAT,GL_LINEAR)
    gpuHombro = es.toGPUShape(bs.createTextureQuad("Imagenes/hombro.png", nx=1, ny=1),GL_REPEAT,GL_LINEAR)
    gpuAntebrazo = es.toGPUShape(bs.createTextureQuad("Imagenes/antebrazo.png", nx=1, ny=1),GL_REPEAT,GL_LINEAR)

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
    gpuRedQuad = es.toGPUShape(bs.createTextureQuad("Imagenes/carrito.png", nx=1, ny=1),GL_REPEAT,GL_LINEAR)

    # Creating a single wheel
    wheel = sg.SceneGraphNode("wheel")
    wheel.transform = tr.uniformScale(0.2)
    #wheel.childs += [gpuBlackQuad]

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
    traslatedCar.transform = tr.matmul([tr.translate(0,0.3,0),tr.uniformScale(0.2)])
    traslatedCar.childs += [car,humano]

    return traslatedCar

def createPista():
    cuboGPU2=es.toGPUShape(createPistaShape(camino_final,0,0,0))
    cuboGPU1=es.toGPUShape(createPistaShape(camino_final,0.5254,0.8196,0.98030))#############
    pista1=sg.SceneGraphNode("pista1")
    pista1.transform=tr.translate(0,0.01,0)
    pista2=sg.SceneGraphNode("pista2")
    pista1.childs+=[cuboGPU1]
    pista2.childs+=[cuboGPU2]
    pista = sg.SceneGraphNode("pista")
    pista.transform=tr.identity()
    pista.childs+=[pista2]
    pista.childs+=[pista1]
    return pista

def create_big_quad():
    quadGPU=es.toGPUShape(bs.createColorQuad(0.5254,0.8196,0.98030))
    quad=sg.SceneGraphNode("Cuadrado")
    quad.childs+=[quadGPU]
    return quad

def sol():
    solGPU=es.toGPUShape(bs.createTextureQuad("Imagenes/sol.png"),GL_REPEAT,GL_LINEAR)
    sun=sg.SceneGraphNode("Cuadrado")
    sun.childs+=[solGPU]
    return sun


class Controller():
    salto=False
    saltando=False
    derivada=0
    cayendo=False
    x=0
    y=0
    vy=0
    g=9

    accidente=False
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
    auto=createCar()
    pista=createPista()
    cuadrado=create_big_quad()
    cuadrado2=create_big_quad()

    sun=sol()

    fondo=createBackground()        
    fondo1=createBackground()
    fondo2=createBackground()
    fondo3=createBackground()
    fondo4=createBackground()
    
    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

     #Enable transparency
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    #Contadores iniciales; posición pista, desplazamiento pista
    x_pista=0
    espacios_salto=0

    #Contador puntero lista coordenadas de la montaña rusa, ubicación inicial.
    contador_posicion_x=0
    posicion_actual=camino_final[0][0]
    control.x=posicion_actual


    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        #Caso de terminar el camino
        try:
            camino_final[contador_posicion_x+1][0]-camino_final[contador_posicion_x][0]
        except:
            print("Ganaste")
            sys.exit()

        #:::::::::::::::::::::::::::::::::::::::::::::::::::::::.Manejo de la rotación del carrito::::::::::::
        #Por si queda un número dividido en 0, como en los agujeros
        if camino_final[contador_posicion_x+1][0]-camino_final[contador_posicion_x][0]==0  :
            derivada=0
        else:
            derivada=(  camino_final[contador_posicion_x+1][1]-camino_final[contador_posicion_x][1]  )/   (camino_final[contador_posicion_x+1][0]-camino_final[contador_posicion_x][0]  )
        
        
        #Variacion derivada
        if control.derivada <derivada:
            control.derivada+=0.0000000000000000000000000000000000000000000000000000001
        elif control.derivada>derivada:
            derivada-=0.0000000000000000000000000000000000000000000000000000001
        control.derivada=derivada
        angulo=np.arctan(derivada)


            

        #:::::::::::::::::::Condiciones según posición o estados del control:::::::::::::::::
        #Caso Accidente
        if (control.y)-(0.34)-0.5<-3:
            control.accidente=True
            print("NOT SAFE")
        
        if control.accidente:
            sys.exit()
        


        #Manejo del salto y restricciones
        if control.salto:
            if not control.saltando and not control.cayendo:
                control.posicion_inicial=control.y
                control.vy=0.005
                control.saltando=True
            control.salto=False
        
    
        elif control.saltando:
                control.vy=0.005
                if (control.y-control.posicion_inicial)>0.5:
                    control.saltando=False
                    control.cayendo=True
                    control.vy=-0.005

        elif control.cayendo and not control.saltando:
            control.vy=-0.005
            if abs(control.y-camino_final[contador_posicion_x][1])<0.02:
                control.vy=0
                control.y=camino_final[contador_posicion_x][1]
                control.cayendo=False


        elif control.y-camino_final[contador_posicion_x+1][1]>0.3:
            control.cayendo=True

        #Si no paso ninguno de los anteriores, está en el camino
        else:
            control.y=camino_final[contador_posicion_x][1]

        #Renovar posición Y
        control.y=control.y+control.vy

        #Avanzar posición X
        contador_posicion_x+=1

        #Lo que desplaza la montaña rusa cada fotograma y actualización de su posición
        espacios_salto=camino_final[contador_posicion_x][0]-camino_final[contador_posicion_x-1][0]
        x_pista-=espacios_salto

        #:::::::::::::::::Transformaciones:::::::::::::::::
        pista.transform=tr.translate(x_pista,-0.4-0.5,0)

        auto.transform=tr.matmul([tr.translate(0,(control.y)-(0.34)-0.5,0),tr.uniformScale(0.2),tr.rotationZ(angulo)])
        
        fondo.transform=tr.matmul([tr.translate(x_pista%1+0.5,0,0),tr.scale(1,2,1)])
        fondo1.transform=tr.matmul([tr.translate(x_pista%1,0,0),tr.scale(1,2,1)])
        fondo2.transform=tr.matmul([tr.translate(x_pista%1-0.5,0,0),tr.scale(1,2,1)])
        fondo3.transform=tr.matmul([tr.translate(x_pista%1-1,0,0),tr.scale(1,2,1)])
        fondo4.transform=tr.matmul([tr.translate(x_pista%1-1.5,0,0),tr.scale(1,2,1)])

        sun.transform=tr.matmul([tr.translate(1,1,0),tr.uniformScale(1.3)])


        cuadrado.transform=tr.matmul([tr.translate(x_pista-1,0,0),tr.scale(2,2,1),tr.identity()])
        cuadrado2.transform=tr.matmul([tr.translate(x_pista+1+ultima_coordenada[0],0,0),tr.scale(2,2,1),tr.identity()])

        

        #::::::::::::::::::Dibujado::::::::::::::::::::
        glUseProgram(pipeline2.shaderProgram)
        sg.drawSceneGraphNode(fondo, pipeline2, "transform")
        sg.drawSceneGraphNode(fondo1, pipeline2, "transform")
        sg.drawSceneGraphNode(fondo2, pipeline2, "transform")
        sg.drawSceneGraphNode(fondo3, pipeline2, "transform")
        sg.drawSceneGraphNode(fondo4, pipeline2, "transform")
        

        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(pista, pipeline, "transform")
        sg.drawSceneGraphNode(cuadrado, pipeline, "transform")
        sg.drawSceneGraphNode(cuadrado2, pipeline, "transform")

        

        glUseProgram(pipeline2.shaderProgram)
        sg.drawSceneGraphNode(sun,pipeline2,"transform")
        sg.drawSceneGraphNode(auto, pipeline2, "transform")
        



        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    
    glfw.terminate()