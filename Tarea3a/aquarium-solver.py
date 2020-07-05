import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import Modulo.transformations as tr
import Modulo.easy_shaders as es
import Modulo.basic_shapes as bs
import Modulo.basic_shapes as bs


def createColorCube(i, j, k, X, Y, Z,c):
    c=(c/40)**3
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
        l_x, b_y,  t_z, c,0,0.01,
         r_x, b_y,  t_z, c,0,0.01,
         r_x,  f_y,  t_z, c,0,0.01,
        l_x,  f_y,  t_z, c,0,0.01,
    # Z-: number 6
        l_x, b_y, b_z, c,0,0.01,
         r_x, b_y, b_z, c,0,0.01,
         r_x,  f_y, b_z, c,0,0.01,
        l_x,  f_y, b_z, c,0,0.01,
    # X+: number 5
         r_x, b_y, b_z, c,0,0.01,
         r_x,  f_y, b_z, c,0,0.01,
         r_x,  f_y,  t_z, c,0,0.01,
         r_x, b_y,  t_z, c,0,0.01,
    # X-: number 2
        l_x, b_y, b_z, c,0,0.01,
        l_x,  f_y, b_z, c,0,0.01,
        l_x,  f_y,  t_z, c,0,0.01,
        l_x, b_y,  t_z, c,0,0.01,
    # Y+: number 4
        l_x,  f_y, b_z, c,0,0.01,
        r_x,  f_y, b_z, c,0,0.01,
        r_x,  f_y, t_z, c,0,0.01,
        l_x,  f_y, t_z, c,0,0.01,
    # Y-: number 3
        l_x, b_y, b_z, c,0,0.01,
        r_x, b_y, b_z, c,0,0.01,
        r_x, b_y, t_z, c,0,0.01,
        l_x, b_y, t_z, c,0,0.01,
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
        self.projection = PROJECTION_ORTHOGRAPHIC


# We will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

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
    load_voxels = np.load('solution.npy')
    #X, Y, Z = np.mgrid[-2:2:20j, -2:2:20j, -2:2:20j]
    #X, Y, Z = np.mgrid[0:2:8j, 0:2.5:10j, 0:1.5:6j]


    #X, Y, Z = np.mgrid[0:2:20j, 0:2.5:25j, 0:1.5:15j]
    #matriz_resuelta = matrix(4,3,5,1,25,0.1,25,30,"solution")
    #X, Y, Z = np.mgrid[0:2:8, 0:2:8j, 0:2:8j]
    #X, Y, Z = np.mgrid[0:4:20j, 0:5:25j, 0:3:15j]
    ###################4     3       5
    ###3,6,4
    X, Y, Z = np.mgrid[-1.5:1.5:12j, -3:3:24j, -2:2:16j]
    #X, Y, Z = np.mgrid[0:2:8j, 0:2.5:10j, 0:1.5:6j]
    print(load_voxels.shape)
    print(range(X.shape[0]-1),range(X.shape[1]-1),range(X.shape[2]-1))

    isosurface = bs.Shape([], [])
    
    # Now let's draw voxels!
    for k in range(X.shape[2]-1):
        for j in range(X.shape[1]-1):
            for i in range(X.shape[0]-1):
                print(load_voxels[i,j,k])
                if load_voxels[i,j,k]:
                    temp_shape = createColorCube(i,j,k, X,Y, Z,load_voxels[i,j,k])
                    merge(destinationShape=isosurface, strideSize=6, sourceShape=temp_shape)


    gpu_surface = es.toGPUShape(isosurface)


    t0 = glfw.get_time()
    camera_theta = np.pi/4
    camera_theta2 = 0

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS):
            camera_theta -= 2 * dt

        if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS):
            camera_theta += 2* dt

        if (glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS):
            camera_theta2 += 2*dt

        if (glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS):
            camera_theta2 -= 2*dt

        # Setting up the view transform

        camX = 10 * np.sin(camera_theta) * np.sin(camera_theta2)
        camY = 10 * np.cos(camera_theta) * np.sin(camera_theta2)
        camZ = 10 * np.cos(camera_theta2)


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
        pipeline.drawShape(gpuAxis, GL_LINES)
        pipeline.drawShape(gpu_surface)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
