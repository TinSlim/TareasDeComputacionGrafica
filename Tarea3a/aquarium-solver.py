import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve

import json

def reader(json_file):
    with open(json_file) as f:
        data = json.load(f)
        return data

try:
    archivo_json=str(sys.argv[1])
except:
    archivo_json="problem-setup.json"

archivo_json=reader(archivo_json)

# Variables del JSON
W = archivo_json["width"]
L = archivo_json["lenght"]
H = archivo_json["height"]

h_a = archivo_json["heater_a"]
h_b = archivo_json["heater_b"]
win_loss = archivo_json["window_loss"]
amb_temp = archivo_json["ambient_temperature"]
filename = archivo_json["filename"]

# Espaciado
h = 0.2


#c = 1  #contstat
#B = 0

#nw = int(W/h) -1
#nl = int(L/h) -1
#nh = int(H/h) -1


# Entrega indexación a partir de X,Y,Z; Tamaño Acuario y espaciado

#//
def getK(x,y,z,W,L,H,h):
    nw = int(W//h) -1
    nl = int(L//h) -1
    nh = int(H//h) -1
    return x+nw*y+z*nl*nw

def getIJK(k,W,L,H,h):
    nw = int(W//h) -1
    nl = int(L//h) -1
    nh = int(H//h) -1
    z = k//(nl*nw)
    y = (k%(nl*nw))//nw
    x = (k%(nl*nw))%nw
    return (x,y,z)


def solveMatrix(A,b):
    return np.linalg.solve(A,b)


def matrix(W,L,H,h,C,B,header_a,header_b,nombre_final):
    nw = int(W//h) -1 #x
    print(nw,'nw')
    nl = int(L//h) -1    #y
    print(nl,'nl')
    nh = int(H//h) -1  #z
    print(nh,'nh')
    print('ns',nw,nl,nh,(nw)*(nl)*(nh))

    N = (nw)*(nl)*(nh)

    A = csc_matrix((N,N))

    #A = np.zeros(((nw)*(nl)*(nh),(nw)*(nl)*(nh)))
    b = np.zeros(nw*nl*nh)
    #b = np.zeros ((nw+1)*(nl+1)*(nw+1))
    #print( len(A),len(b),'lens')

    for z in range(nh):
        print(str(z*100//(nh-1))+'% Completado de Discretización')
        for y in range(nl):
            for x in range(nw):

                k = getK(x,y,z,W,L,H,h)
                
                k_x = getK(x+1,y,z,W,L,H,h)
                k__x = getK(x-1,y,z,W,L,H,h)
                k_y = getK(x,y+1,z,W,L,H,h)
                k__y = getK(x,y-1,z,W,L,H,h)
                k_z = getK(x,y,z+1,W,L,H,h)
                k__z = getK(x,y,z-1,W,L,H,h)
                #centro
                if (1<=x and x<=nw -2) and (1<=y and y<=nl-2) and (1<=z and z<=nh-2):
                    A[k, k_x] = 1
                    A[k, k__x] = 1
                    A[k, k_y] = 1
                    A[k, k__y] = 1
                    A[k, k_z] = 1
                    A[k, k__z] = 1
                    A[k,k] = -6
                    b[k] = 0

                ##########################
                #+x
                elif (x==nw-1) and (1<=y and y<=nl-2) and (1<=z and z<=nh-2):
                    #A[k, k_x] = 0
                    A[k, k__x] = 2 
                    A[k, k_y] = 1
                    A[k, k__y] = 1
                    A[k, k_z] = 1
                    A[k, k__z] = 1
                    A[k,k] = -6
                    b[k] = -2*h*B

                #_x
                elif (x==0) and (1<=y and y<=nl-2) and (1<=z and z<=nh-2):
                    A[k, k_x] =2
                    #A[k, k__x] = 0
                    A[k, k_y] = 1
                    A[k, k__y] = 1
                    A[k, k_z] = 1
                    A[k, k__z] = 1
                    A[k,k] = -6
                    b[k] = -2*h*B

                #+y
                elif (1<=x and x<=nw -2) and (y==nl-1) and (1<=z and z<=nh-2):
                    A[k, k_x] = 1
                    A[k, k__x] = 1 
                    #A[k, k_y] = 0
                    A[k, k__y] = 2
                    A[k, k_z] = 1
                    A[k, k__z] = 1
                    A[k,k] = -6
                    b[k] = -2*h*B

                #_y
                elif (1<=x and x<=nw -2) and (y==0) and (1<=z and z<=nh-2):
                    A[k, k_x] = 1
                    A[k, k__x] = 1 
                    A[k, k_y] = 2
                    #A[k, k__y] = 0
                    A[k, k_z] = 1
                    A[k, k__z] = 1
                    A[k,k] = -6
                    b[k] = -2*h*B

                #+z arreglar
                elif (1<=x and x<=nw -2) and (1<=y and y<=nl-2) and (z==nh-1):
                    A[k, k_x] = 1
                    A[k, k__x] = 1 
                    A[k, k_y] = 1
                    A[k, k__y] = 1
                    #A[k, k_z] = 0
                    A[k, k__z] = 1
                    A[k,k] = -6
                    b[k] = - C

                #_z Agregar heater#####
                elif (1<=x and x<=nw -2) and (1<=y and y<=nl-2) and (z==0):
                    l_quinto = (nl)/5
                    w_tercio = (nw)/3
                    #if (l_quinto<x and x< l_quinto * 2) and (w_tercio<y and y<w_tercio*2):
                    #    b[k] = -header_a
                    #elif (l_quinto*3<x and x< l_quinto * 4) and (w_tercio<y and y<w_tercio*2):
                    #    b[k] = -header_b
                   # else:
                    #    b[k] = 0
                    if  (l_quinto<=y and y<= l_quinto * 2) and (w_tercio<=x and x<=w_tercio*2):
                        b[k] = -header_a
                        A[k, k_z] = 1

                    elif (l_quinto*3<=y and y<= l_quinto * 4) and (w_tercio<=x and x<=w_tercio*2):
                        b[k] = -header_b
                        A[k, k_z] = 1
                    
                    else:
                        b[k] = 0
                        A[k,k_z] = 2

                    A[k, k_x] = 1
                    A[k, k__x] = 1 
                    A[k, k_y] = 1
                    A[k, k__y] = 1
                    A[k,k] = -6
                ## if x or y 000 blabal
                        
                #3 paredes ##
                elif (x==0) and (y==0) and (z==0):
                    A[k, k_x] =2
                    #A[k, k__x] = 0 
                    A[k, k_y] = 2
                    #A[k, k__y] = 0
                    A[k, k_z] = 2
                    #A[k, k__z] = 0
                    A[k,k] = -6
                    b[k] = -4*h*B  

                elif (x==0) and (y==0) and (z==nh-1):
                    A[k, k_x] =2
                    #A[k, k__x] = 0 
                    A[k, k_y] = 2
                    #A[k, k__y] = 0
                    #A[k, k_z] = 0
                    A[k, k__z] = 1
                    A[k,k] = -6
                    b[k] = -4*h*B - C

                elif (x==0) and (y==nl-1) and (z==0):
                    A[k, k_x] =2
                    #A[k, k__x] = 0 
                    #A[k, k_y] = 0
                    A[k, k__y] = 2
                    A[k, k_z] = 2
                    #A[k, k__z] = 0
                    A[k,k] = -6
                    b[k] = -4*h*B  

                elif (x==0) and (y==nl-1) and (z==nh-1):
                    A[k, k_x] =2
                    #A[k, k__x] = 0 
                    #A[k, k_y] = 0
                    A[k, k__y] = 2
                    #A[k, k_z] = 0
                    A[k, k__z] = 1
                    A[k,k] = -6
                    b[k] = -4*h*B - C  
             
                elif (x==nw -1) and (y==0) and (z==0):
                    #A[k, k_x] =0
                    A[k, k__x] = 2 
                    A[k, k_y] = 2
                    #A[k, k__y] = 0
                    A[k, k_z] = 2
                    #A[k, k__z] = 0
                    A[k,k] = -6
                    b[k] = -4*h*B

                elif (x==nw -1) and (y==0) and (z==nh-1):
                    #A[k, k_x] =0
                    A[k, k__x] = 2 
                    A[k, k_y] = 2
                    #A[k, k__y] = 0
                    #A[k, k_z] = 0
                    A[k, k__z] = 1
                    A[k,k] = -6
                    b[k] = -4*h*B - C  

                elif (x==nw -1) and (y==nl-1) and (z==0):
                    #A[k, k_x] =0
                    A[k, k__x] = 2 
                    #A[k, k_y] = 0
                    A[k, k__y] = 2
                    A[k, k_z] = 2
                    #A[k, k__z] = 0
                    A[k,k] = -6
                    b[k] = -4*h*B

                elif (x==nw -1) and (y==nl-1) and (z==nh-1):
                    #A[k, k_x] =0
                    A[k, k__x] = 2 
                    #A[k, k_y] = 0
                    A[k, k__y] = 2
                    #A[k, k_z] = 0
                    A[k, k__z] = 1
                    A[k,k] = -6
                    b[k] = -4*h*B - C  



                ##2 paredes##
                
                elif (1<=x and x<=nw -2) and (y==nl-1) and (z==nh-1):
                    A[k, k_x] = 1
                    A[k, k__x] = 1 
                    #A[k, k_y] = 0
                    A[k, k__y] = 2
                    #A[k, k_z] = 0
                    A[k, k__z] = 1
                    A[k,k] = -6
                    b[k] = -C -2*h*B
                
                elif (1<=x and x<=nw -2) and (y==0) and (z==nh-1):
                    A[k, k_x] = 1
                    A[k, k__x] = 1 
                    A[k, k_y] = 2
                    #A[k, k__y] = 0
                    #A[k, k_z] = 0
                    A[k, k__z] = 1
                    A[k,k] = -6
                    b[k] = -C-2*h*B

                elif (1<=x and x<=nw -2) and (y==nl-1) and (z==0):
                    A[k, k_x] = 1
                    A[k, k__x] = 1 
                    #A[k, k_y] = 0
                    A[k, k__y] = 2
                    A[k, k_z] = 2
                    #A[k, k__z] = 0
                    A[k,k] = -6
                    b[k] = -2*h*B
                
                elif (1<=x and x<=nw -2) and (y==0) and (z==0):
                    A[k, k_x] = 1
                    A[k, k__x] = 1 
                    A[k, k_y] = 2
                    #A[k, k__y] = 0
                    A[k, k_z] = 2
                    #A[k, k__z] = 0
                    A[k,k] = -6
                    b[k] = -2*h*B

                ###########################
                elif (x==nw -1) and (1<=y and y<=nl-2) and (z==nh-1):
                    #A[k, k_x] = 0
                    A[k, k__x] = 2 
                    A[k, k_y] = 1
                    A[k, k__y] = 1
                    #A[k, k_z] = 0
                    A[k, k__z] = 1
                    A[k,k] = -6
                    b[k] = -2*h*B -C
                
                elif (x==0) and (1<=y and y<=nl-2) and (z==nh-1):
                    A[k, k_x] = 2
                    #A[k, k__x] = 0 
                    A[k, k_y] = 1
                    A[k, k__y] = 1
                    #A[k, k_z] = 0
                    A[k, k__z] = 1
                    A[k,k] = -6
                    b[k] = -2*h*B -C          


                elif (x==nw -1) and (1<=y and y<=nl-2) and (z==0):
                    #A[k, k_x] = 0
                    A[k, k__x] = 2 
                    A[k, k_y] = 1
                    A[k, k__y] = 1
                    A[k, k_z] = 2
                    #A[k, k__z] = 0
                    A[k,k] = -6
                    b[k] = -2*h*B 
                
                elif (x==0) and (1<=y and y<=nl-2) and (z==0):
                    A[k, k_x] = 2
                    #A[k, k__x] = 0 
                    A[k, k_y] = 1
                    A[k, k__y] = 1
                    A[k, k_z] = 2
                    #A[k, k__z] = 0
                    A[k,k] = -6
                    b[k] = -2*h*B
                ##############################

                elif (x==nw -1) and (y==nl-1) and (1<=z and z<=nh-2):
                    #A[k, k_x] =0
                    A[k, k__x] = 2 
                    #A[k, k_y] = 0
                    A[k, k__y] = 2
                    A[k, k_z] = 1
                    A[k, k__z] = 1
                    A[k,k] = -6
                    b[k] = -4*h*B

                elif (x==nw -1) and (y==0) and (1<=z and z<=nh-2):
                    #A[k, k_x] =0
                    A[k, k__x] = 2 
                    A[k, k_y] = 2
                    #A[k, k__y] = 0
                    A[k, k_z] = 1
                    A[k, k__z] = 1
                    A[k,k] = -6
                    b[k] = -4*h*B 

                elif (x==0) and (y==nl-1) and (1<=z and z<=nh-2):
                    A[k, k_x] =2
                    #A[k, k__x] = 0 
                    #A[k, k_y] = 0
                    A[k, k__y] = 2
                    A[k, k_z] = 1
                    A[k, k__z] = 1
                    A[k,k] = -6
                    b[k] = -4*h*B

                elif (x==0) and (y==0) and (1<=z and z<=nh-2):
                    A[k, k_x] =2
                    #A[k, k__x] = 0 
                    A[k, k_y] = 2
                    #A[k, k__y] = 0
                    A[k, k_z] = 1
                    A[k, k__z] = 1
                    A[k,k] = -6
                    b[k] = -4*h*B 

    

    print('Espere Resolución de la Matriz')
    vector_resuelto = spsolve(A, b)


    tamanio = getIJK(len(vector_resuelto)-1,W,L,H,h)
    Matriz_ultima = np.zeros( (tamanio[0] +1,tamanio[1] +1 ,tamanio[2]+1) )
    indice = 0
    for numero in vector_resuelto:
        coordenada = getIJK(indice,W,L,H,h)
        Matriz_ultima[coordenada] = numero
        indice+=1
    
    np.save(nombre_final, Matriz_ultima)
    print('Discretización completada con éxito, ',nombre_final)
    return Matriz_ultima



#ub[1:nw + 1, 1:nl + 1, 1:nh + 1] = u[:, :, :]
#ub[0:nw + 2, 0:nl + 2, nh + 1] = AMBIENT_TEMPERATURE

# Se ejecuta discretización
matriz_resuelta = matrix(W,L,H,0.2,amb_temp,win_loss,h_a,h_b,filename)

#ub = np.zeros((nw + 2, nl + 2, nh + 2))
#ub[1:nw + 1, 1:nl + 1, 1:nh + 1] = u[:, :, :]
#ub[0:nw + 2, 0:nl + 2, nh + 1] = AMBIENT_TEMPERATURE
# We will write the equation associated with row m
            #m = getM(i, j, k)
            # We obtain indices of the other coefficients
            #m_up = getM(i, j + 1, k)
            #m_down = getM(i, j - 1, k)
            #m_left = getM(i - 1, j, k)
            #m_right = getM(i + 1, j, k)
            #m_near = getM(i, j, k + 1)
            #m_far = getM(i, j, k - 1)

# Solving our system
#x = scipy.sparse.linalg.spsolve(A, b)

# Now we return our solution to the 3D discrete domain
# In this matrix we will store the solution in the 3D domain
#u = np.zeros((nw, nl, nh))

#for m in range(N):
#    i, j, k = getIJK(m)
#    u[i, j, k] = x[m]