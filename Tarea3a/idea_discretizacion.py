import numpy as np


W = 4  #X
L =7    #Y
H = 107   #Z
h = 0.1

c = 1  #contstat
B = 0

nw = int(W/h) -1
nl = int(L/h) -1
nh = int(H/h) -1


def getK(x,y,z):
    W=3
    L=3
    H = 3
    h = 1
    nw = int(W/h) -1
    nl = int(L/h) -1
    nh = int(H/h) -1
    return x+nw*y+z*nl*nw

def getIJK(k):
    W=3
    L=3
    H = 3
    h = 1
    nw = int(W/h) -1
    nl = int(L/h) -1
    nh = int(H/h) -1
    z = k//(nh*nw)
    y = (k%(nh*nw))//nw
    x = (k%(nh*nw))%nw
    return (x,y,z)

def matrix(W,L,H,h,C,B,header_a,header_b):
    nw = int(W/h) -1 #x
    nl = int(L/h) -1    #y
    nh = int(H/h) -1  #z

    A = np.zeros(((nw)*(nl)*(nw),(nw)*(nl)*(nw)))
    #A = np.zeros(((nw+1)*(nl+1)*(nw+1),(nw+1)*(nl+1)*(nw+1)))
    b = np.zeros (nw*nl*nw)
    print( len(A),len(b))

    for z in range(nh):
        for y in range(nl):
            for x in range(nw):

                k = getK(x,y,z)
                
                k_x = getK(x+1,y,z)
                k__x = getK(x-1,y,z)
                k_y = getK(x,y+1,z)
                k__y = getK(x,y-1,z)
                k_z = getK(x,y,z+1)
                k__z = getK(x,y,z-1)
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
                    l_quinto = L/5
                    w_tercio = W/3
                    if (l_quinto<x and x< l_quinto * 2) and (w_tercio<y and y<w_tercio*2):
                        b[k] = -header_a
                    elif (l_quinto*3<x and x< l_quinto * 4) and (w_tercio<y and y<w_tercio*2):
                        b[k] = -header_b
                    else:
                        b[k] = 0

                    A[k, k_x] = 1
                    A[k, k__x] = 1 
                    A[k, k_y] = 1
                    A[k, k__y] = 1
                    A[k, k_z] = 1
                    #A[k, k__z] = 0
                    A[k,k] = -6
                ## if x or y 000 blabal
                        
                #3 paredes ##
                elif (x==0) and (y==0) and (z==0):
                    A[k, k_x] =2
                    #A[k, k__x] = 0 
                    A[k, k_y] = 2
                    #A[k, k__y] = 0
                    A[k, k_z] = 1
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
                    A[k, k_z] = 1
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
                    A[k, k_z] = 1
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
                    A[k, k_z] = 1
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
                    A[k, k_z] = 1
                    #A[k, k__z] = 0
                    A[k,k] = -6
                    b[k] = -2*h*B
                
                elif (1<=x and x<=nw -2) and (y==0) and (z==0):
                    A[k, k_x] = 1
                    A[k, k__x] = 1 
                    A[k, k_y] = 2
                    #A[k, k__y] = 0
                    A[k, k_z] = 1
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
                    A[k, k_z] = 1
                    #A[k, k__z] = 0
                    A[k,k] = -6
                    b[k] = -2*h*B 
                
                elif (x==0) and (1<=y and y<=nl-2) and (z==0):
                    A[k, k_x] = 2
                    #A[k, k__x] = 0 
                    A[k, k_y] = 1
                    A[k, k__y] = 1
                    A[k, k_z] = 1
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

    return (A,b)            
                

def solveMatrix(A,b):
    return np.linalg.solve(A,b)

matriz_resuelta = matrix(3,3,3,1,1,2,20,20)
vector_resuelto = solveMatrix(matriz_resuelta[0],matriz_resuelta[1])
print(vector_resuelto)

Matriz_ultima = np.zeros( (getIJK(len(vector_resuelto)-1)[0] +1,getIJK(len(vector_resuelto)-1)[1] +1 ,getIJK(len(vector_resuelto)-1)[2] +1 ) )
print(Matriz_ultima)

indice = 0
for numero in vector_resuelto:
    coordenada = getIJK(indice)
    Matriz_ultima[coordenada] = numero
    indice+=1
print(Matriz_ultima)