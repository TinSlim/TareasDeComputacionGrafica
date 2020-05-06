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

#######################glfw.set_input_mode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)
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

#print(c)

class controller():
    angulo=-0.1
    rotacion_alas=0
    rotation_y=0.1
    rotation_x=-1.6#0

    alasSubiendo=True

control=controller()

def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return
    
    elif key == glfw.KEY_SPACE:
        control.angulo+=0.1

    elif key == glfw.KEY_Q:
        control.angulo-=0.1

    elif key == glfw.KEY_F:
        control.rotacion_alas-=0.1

    elif key == glfw.KEY_G:
        control.rotacion_alas-=0.1


    elif key == glfw.KEY_M:
        control.rotation_y+=0.1

    elif key == glfw.KEY_N:
        control.rotation_y-=0.1

    elif key == glfw.KEY_ESCAPE:
        sys.exit()





def pajaro():
    gpuCabeza = es.toGPUShape(rbj.readOBJ("Model/cabeza.obj", (0,1,1)))
    gpuTorso = es.toGPUShape(rbj.readOBJ("Model/torso.obj", (0,1,1)))
    gpuAlaSupDer = es.toGPUShape(rbj.readOBJ("Model/alasupder.obj", (0,1,1)))
    gpuAlaInfDer = es.toGPUShape(rbj.readOBJ("Model/alainfder.obj", (0,1,1)))
    gpuAlaSupIzq = es.toGPUShape(rbj.readOBJ("Model/alasupizq.obj", (0,1,1)))
    gpuAlaInfIzq = es.toGPUShape(rbj.readOBJ("Model/alainfizq.obj", (0,1,1)))

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
    AlaDerecha.transform = tr.matmul([tr.translate(-1,-2.5,0),tr.rotationY(np.pi),tr.rotationX(np.pi),tr.translate(1,2.5,0)])  #AlaDerecha.transform = tr.matmul([tr.translate(0,-2,0),tr.rotationX(np.pi*(2/3)),tr.translate(0,2,0.5)])#

    #############        tr.rotationX(np.pi)
    #Ala inf derecha
    AlaInfIzquierda = sg.SceneGraphNode("AlaInfIzquierda")
    AlaInfIzquierda.transform = tr.translate(0,0,0)  #Ajustar bn
    AlaInfIzquierda.childs+=[gpuAlaInfIzq]

    #Rotación ala inf derecha
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

    #Pajaro
    Pajaro = sg.SceneGraphNode("Pajaro")
    Pajaro.childs+=[Alas]
    Pajaro.childs+=[Cuerpo]
    Pajaro.transform=tr.rotationX(np.pi*(1/2))

    return Pajaro



if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Reading a *.obj file", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)


    # Defining shader programs
    #pipeline = ls.SimpleFlatShaderProgram()
    pipeline = ls.SimplePhongShaderProgram()
    #pipeline = ls.SimplePhongShaderProgram()
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    gpuAxis = es.toGPUShape(bs.createAxis(7))
    #gpuSuzanne = es.toGPUShape(shape = readOBJ('suzanne.obj', (0.9,0.6,0.2)))
    gpuSuzanne = es.toGPUShape(shape = rbj.readOBJ('Model/alasupder.obj', (0.9,0.6,0.2)))
    pajarito=pajaro()
    #gpuCarrot = es.toGPUShape(shape = readOBJ('carrot.obj', (0.6,0.9,0.5)))

    
    Ala_Inf_Izquierda=sg.findNode(pajarito, "RotacionAlaInfIzquierda")
    Ala_Inf_Derecha=sg.findNode(pajarito, "RotacionAlaInfDerecha")
    
    Ala_Derecha = sg.findNode(pajarito, "AlaDerecha")
    Ala_Izquierda = sg.findNode(pajarito, "AlaIzquierda")
    Pajaro1 = sg.findNode(pajarito, "Pajaro")
    
    #Config inicial
    Ala_Inf_Izquierda.transform = tr.matmul([tr.translate(1.5,-2,-2),tr.rotationY(-(control.angulo)),tr.translate(-1.5,2,2)])
    Ala_Inf_Derecha.transform = tr.matmul([tr.translate(-1.5,-2,-2),tr.rotationY(control.angulo),tr.translate(1.5,2,2)])

    Ala_Derecha.transform = tr.matmul([tr.translate(-1,-2.5,0),tr.rotationZ(control.rotation_y),tr.rotationX(control.rotation_x),tr.translate(1,2.5,0)])###
    Ala_Izquierda.transform = tr.matmul([tr.translate(1,-2.5,0),tr.rotationZ(-1*(control.rotation_y)),tr.rotationX(control.rotation_x),tr.translate(-1,2.5,0)])


    t0 = glfw.get_time()
    camera_theta = -3*np.pi/4
    
    ###
    counter=0

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        
        glfw.poll_events()
        cursor_at = glfw.get_cursor_pos(window)

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS):
            camera_theta -= 2 * dt

        if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS):
            camera_theta += 2* dt



        ######################################
        if cursor_at[1]<600 and cursor_at[1]>0:
            Ala_Inf_Izquierda.transform = tr.matmul([tr.translate(1.5,-2,-2),tr.rotationY(-(control.angulo+0.00215*cursor_at[1])),tr.translate(-1.5,2,2)])
            Ala_Inf_Derecha.transform = tr.matmul([tr.translate(-1.5,-2,-2),tr.rotationY(control.angulo+0.00215*cursor_at[1]),tr.translate(1.5,2,2)])

            Ala_Derecha.transform = tr.matmul([tr.translate(-1,-2.5,0),tr.rotationZ(control.rotation_y-0.0045*cursor_at[1]),tr.rotationX(control.rotation_x),tr.translate(1,2.5,0)])###
            Ala_Izquierda.transform = tr.matmul([tr.translate(1,-2.5,0),tr.rotationZ(-1*(control.rotation_y-0.0045*cursor_at[1])),tr.rotationX(control.rotation_x),tr.translate(-1,2.5,0)])
        

        camaraX=c[counter][0]
        camaraY=c[counter][1]
        camaraZ=c[counter][2]
        Pajaro1.transform=tr.translate(camaraX,camaraY,camaraZ)
        #print(control.angulo,control.rotation_y)
        #print(cursor_at)

        
        #-0.1   0.1
        #1.2     -2.6
        #---------
        # 1.3     2.7
        #0.00216         0.004500
        R = 12
        camX = R * np.sin(camera_theta)
        camY = R * np.cos(camera_theta)

        if counter==len(c)-4:
            counter=0
        counter+=1

        #viewPos = np.array([camaraX, camaraY, camaraZ])
        viewPos = np.array([camX, camY, 7])
        view = tr.lookAt(
            viewPos,
            np.array([0,0,1]),
            np.array([0,0,1])
        )

        # Setting up the projection transform
        projection = tr.perspective(60, float(width)/float(height), 0.1, 100)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        #if (controller.fillPolygon):
        #    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        #else:
        #    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Drawing shapes
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


        ###
        sg.drawSceneGraphNode(pajarito, pipeline, "model")
        #pipeline.drawShape(gpuSuzanne)

            ##
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE,
            tr.matmul([
                tr.uniformScale(3),
                tr.rotationX(np.pi/2),
                tr.translate(1.5,-0.25,0)])
        )
        #pipeline.drawShape(gpuCarrot)
        
        glUseProgram(mvpPipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        mvpPipeline.drawShape(gpuAxis, GL_LINES)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()

