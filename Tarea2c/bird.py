import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import Modulo.transformations as tr
import Modulo.basic_shapes as bs
import Modulo.scene_graph as sg
#import easy_shaders as es
#import lighting_shaders as ls


def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return
    
    elif key == glfw.KEY_ESCAPE:
        sys.exit()


if __name__ == "__main__":

    if not glfw.init():
        sys.exit()

    width = 700
    height = 700

    window = glfw.create_window(width, height, "A", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    #pipeline = es.SimpleTransformShaderProgram()

    
    # Telling OpenGL to use our shader program
    #glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

     #Enable transparency
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)



    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)




        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    
    glfw.terminate()
