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


##Botones, barra espaciadora permite cambiar la escena, Esc permite salir del programa
def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    if key == glfw.KEY_SPACE:
        control.Fondo1 = not control.Fondo1

    elif key == glfw.KEY_ESCAPE:
        sys.exit()



if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    ##Tamaño ventana
    width = 600
    height = 600
    
    window = glfw.create_window(width, height, "Aquarium", None, None)
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

    #Variables iniciales
    rotacion_pajaro=0

    t0 = glfw.get_time()
    camera_theta = -3*np.pi/4
    camera_theta2 = 0

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1


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

        

        # Drawing shapes
        glUseProgram(mvpTPipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(mvpTPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(mvpTPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(mvpTPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        #sg.drawSceneGraphNode(Fondo, mvpTPipeline, "model")
        
        
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
        #sg.drawSceneGraphNode(pajarito, pipeline, "model")
        

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()

