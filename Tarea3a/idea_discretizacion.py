import numpy as np


W = 4  #X
L =7    #Y
H = 107   #Z
h = 0.1

nw = int(W/h) -1
nl = int(L/h) -1
nh = int(H/h) -1


def getK(x,y,z):
    return x+nw*y+z*nh*nw

def getIJK(k):
    z = k//(nh*nw)
    y = (k%(nh*nw))//nw
    x = (k%(nh*nw))%nw
    return (x,y,z)


for z in range(nh):
    for y in range(nl):
        for x in range(nw):
            k = getK(x,y,z)
            
            k_x = getK(x+1,y,z)
            k_-x = getK(x-1,y,z)
            k_y = getK(x,y+1,z)
            k_-y = getK(x,y-1,z)
            k_z = getK(x,y,z+1)
            k_-z = getK(x,y,z-1)
            
            #centro
            if (1<=x and x<=nw -2) and (1<=y and y<=nl-2) and (1<=z and z<=nh-2):
                A[k, k_x] = 1
                A[k, k_-x] = 1
                A[k, k_y] = 1
                A[k, k_-y] = 1
                A[k, k_z] = 1
                A[k, k_-z] = 1
                A[k,k] = -4
                b[k] = 0

            ##########################
            #+x
            elif (x==nw-1) and (1<=y and y<=nl-2) and (1<=z and z<=nh-2):
                A[k, k_x] = 0
                A[k, k_-x] = 2 
                A[k, k_y] = 1
                A[k, k_-y] = 1
                A[k, k_z] = 1
                A[k, k_-z] = 1
                A[k,k] = -4
                b[k] = -2*h*B

            #-x
            elif (x==0) and (1<=y and y<=nl-2) and (1<=z and z<=nh-2):
                A[k, k_x] =2
                A[k, k_-x] = 0
                A[k, k_y] = 1
                A[k, k_-y] = 1
                A[k, k_z] = 1
                A[k, k_-z] = 1
                A[k,k] = -4
                b[k] = -2*h*B

            #+y
            elif (1<=x and x<=nw -2) and (y==nl-1) and (1<=z and z<=nh-2):
                A[k, k_x] = 1
                A[k, k_-x] = 1 
                A[k, k_y] = 0
                A[k, k_-y] = 2
                A[k, k_z] = 1
                A[k, k_-z] = 1
                A[k,k] = -4
                b[k] = -2*h*B

            #-y
            elif (1<=x and x<=nw -2) and (y==0) and (1<=z and z<=nh-2):
                A[k, k_x] = 1
                A[k, k_-x] = 1 
                A[k, k_y] = 2
                A[k, k_-y] = 0
                A[k, k_z] = 1
                A[k, k_-z] = 1
                A[k,k] = -4
                b[k] = -2*h*B

            #+z arreglar
            elif (1<=x and x<=nw -2) and (1<=y and y<=nl-2) and (z==nh-1):
                A[k, k_x] = 1
                A[k, k_-x] = 1 
                A[k, k_y] = 1
                A[k, k_-y] = 1
                A[k, k_z] = 0
                A[k, k_-z] = 2
                A[k,k] = -4
                b[k] = 0

            #-z Agregar heater
            elif (1<=x and x<=nw -2) and (1<=y and y<=nl-2) and (z==0):
                A[k, k_x] = 1
                A[k, k_-x] = 1 
                A[k, k_y] = 1
                A[k, k_-y] = 1
                A[k, k_z] = 2
                A[k, k_-z] = 0
                A[k,k] = -4
                b[k] = 0

            ##2 paredes##
            
            elif (1<=x and x<=nw -2) and (y==nl-1) and (z==nh-1):
                A[k, k_x] = 1
                A[k, k_-x] = 1 
                A[k, k_y] = 1
                A[k, k_-y] = 2
                A[k, k_z] = 0
                A[k, k_-z] = 1
                A[k,k] = -4
                b[k] = -B -2*h*b
            
            elif (1<=x and x<=nw -2) and (y==0) and (z==nh-1):
                A[k, k_x] = 1
                A[k, k_-x] = 1 
                A[k, k_y] = 2
                A[k, k_-y] = 0
                A[k, k_z] = 0
                A[k, k_-z] = 1
                A[k,k] = -4
                b[k] = -B-2*h*b


            elif (1<=x and x<=nw -2) and (y==nl-1) and (z==0):
                A[k, k_x] = 1
                A[k, k_-x] = 1 
                A[k, k_y] = 0
                A[k, k_-y] = 2
                A[k, k_z] = 1
                A[k, k_-z] = 0
                A[k,k] = -4
                b[k] = -B -2*h*b
            
            elif (1<=x and x<=nw -2) and (y==0) and (z==0):
                A[k, k_x] = 1
                A[k, k_-x] = 1 
                A[k, k_y] = 2
                A[k, k_-y] = 0
                A[k, k_z] = 1
                A[k, k_-z] = 0
                A[k,k] = -4
                b[k] = -B -2*h*b

###########################
            elif (x==nw -1) and (1<=y and y<=nl-2) and (z==nh-1):
                A[k, k_x] = 0
                A[k, k_-x] = 2 
                A[k, k_y] = 1
                A[k, k_-y] = 1
                A[k, k_z] = 0
                A[k, k_-z] = 1
                A[k,k] = -4
                b[k] = 0
            
            elif (x==0) and (1<=y and y<=nl-2) and (z==nh-1):
                A[k, k_x] = 2
                A[k, k_-x] = 0 
                A[k, k_y] = 1
                A[k, k_-y] = 1
                A[k, k_z] = 0
                A[k, k_-z] = 1
                A[k,k] = -4
                b[k] = 0          


            elif (x==nw -1) and (1<=y and y<=nl-2) and (z==0):
                A[k, k_x] = 0
                A[k, k_-x] = 2 
                A[k, k_y] = 1
                A[k, k_-y] = 1
                A[k, k_z] = 1
                A[k, k_-z] = 0
                A[k,k] = -4
                b[k] = 0
            
            elif (x==0) and (1<=y and y<=nl-2) and (z==0):
                A[k, k_x] = 2
                A[k, k_-x] = 0 
                A[k, k_y] = 1
                A[k, k_-y] = 1
                A[k, k_z] = 1
                A[k, k_-z] = 0
                A[k,k] = -4
                b[k] = 0

            ##############################

            elif (x==nw -1) and (y==nl-1) and (1<=z and z<=nh-2):
                A[k, k_x] =0
                A[k, k_-x] = 2 
                A[k, k_y] = 0
                A[k, k_-y] = 2
                A[k, k_z] = 1
                A[k, k_-z] = 1
                A[k,k] = -4
                b[k] = 0  

            elif (x==nw -1) and (y==0) and (1<=z and z<=nh-2):
                A[k, k_x] =0
                A[k, k_-x] = 2 
                A[k, k_y] = 2
                A[k, k_-y] = 0
                A[k, k_z] = 1
                A[k, k_-z] = 1
                A[k,k] = -4
                b[k] = 0  

            elif (x==0) and (y==nl-1) and (1<=z and z<=nh-2):
                A[k, k_x] =2
                A[k, k_-x] = 0 
                A[k, k_y] = 0
                A[k, k_-y] = 2
                A[k, k_z] = 1
                A[k, k_-z] = 1
                A[k,k] = -4
                b[k] = 0  

            elif (x==0) and (y==0) and (1<=z and z<=nh-2):
                A[k, k_x] =2
                A[k, k_-x] = 0 
                A[k, k_y] = 2
                A[k, k_-y] = 0
                A[k, k_z] = 1
                A[k, k_-z] = 1
                A[k,k] = -4
                b[k] = 0  
            




            #3 paredes ##
            if (x==0) and (y==0) and (z==0):
                A[k, k_x] =2
                A[k, k_-x] = 0 
                A[k, k_y] = 2
                A[k, k_-y] = 0
                A[k, k_z] = 1
                A[k, k_-z] = 0
                A[k,k] = -4
                b[k] = 0  

            if (x==0) and (y==0) and (z==nh-1):
                A[k, k_x] =2
                A[k, k_-x] = 0 
                A[k, k_y] = 2
                A[k, k_-y] = 0
                A[k, k_z] = 0
                A[k, k_-z] = 1
                A[k,k] = -4
                b[k] = 0  


            if (x==0) and (y==nl-1) and (z==0):
                A[k, k_x] =2
                A[k, k_-x] = 0 
                A[k, k_y] = 0
                A[k, k_-y] = 2
                A[k, k_z] = 1
                A[k, k_-z] = 0
                A[k,k] = -4
                b[k] = 0  

            if (x==0) and (y==nl-1) and (z==nh-1):
                A[k, k_x] =2
                A[k, k_-x] = 0 
                A[k, k_y] = 0
                A[k, k_-y] = 2
                A[k, k_z] = 0
                A[k, k_-z] = 1
                A[k,k] = -4
                b[k] = 0  

            
            
            if (x==nw -1) and (y==0) and (z==0):
                A[k, k_x] =0
                A[k, k_-x] = 2 
                A[k, k_y] = 2
                A[k, k_-y] = 0
                A[k, k_z] = 1
                A[k, k_-z] = 0
                A[k,k] = -4
                b[k] = 0  

            if (x==nw -1) and (y==0) and (z==nh-1):
                A[k, k_x] =0
                A[k, k_-x] = 2 
                A[k, k_y] = 2
                A[k, k_-y] = 0
                A[k, k_z] = 0
                A[k, k_-z] = 1
                A[k,k] = -4
                b[k] = 0  


            if (x==nw -1) and (y==nl-1) and (z==0):
                A[k, k_x] =0
                A[k, k_-x] = 2 
                A[k, k_y] = 0
                A[k, k_-y] = 2
                A[k, k_z] = 1
                A[k, k_-z] = 0
                A[k,k] = -4
                b[k] = 0  



            if (x==nw -1) and (y==nl-1) and (z==nh-1):
                A[k, k_x] =0
                A[k, k_-x] = 2 
                A[k, k_y] = 0
                A[k, k_-y] = 2
                A[k, k_z] = 0
                A[k, k_-z] = 1
                A[k,k] = -4
                b[k] = 0  
