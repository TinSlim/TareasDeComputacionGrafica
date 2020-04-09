import numpy as np

def generateT(t):
    return np.array([[1, t, t**2, t**3]]).T

def evalCurve(M, N):
    # The parameter t should move between 0 and 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(N, 3), dtype=float)
    
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(M, T).T
        
    return curve

def Catmull(P1, P2, P3, P4):
    
    # Generate a matrix concatenating the columns
    G = np.concatenate((P1, P2, P3, P4), axis=1)
    
    # Hermite base matrix is a constant
    Mh = np.array([[0, -0.5, 1, -0.5], [1, 0, -2.5, 1.5], [0, 0.5, 2, -1.5], [0, 0, -0.5, 0.5]])    
    
    return np.matmul(G, Mh)


def separador_de_curvas(lista_puntos,lista_x):
    curvas=[]
    curva_actual=[]
    n=0
    while n<len(lista_puntos):
        agujero=False
        for x in lista_x:
            if lista_puntos[n][0]==x[0] and lista_puntos[n][1]==x[1]:
                ##
                curva_actual.append( [lista_puntos[n][0]-0.1 , lista_puntos[n][1]] )####
                ##
                curva_actual.append(lista_puntos[n+1])
                curvas.append(curva_actual)
                curva_actual=[ [lista_puntos[n][0]-0.1,lista_puntos[n][1]] ,[ lista_puntos[n][0]+0.1,lista_puntos[n][1]] ]####2
                curvas.append(curva_actual)
                curva_actual=[lista_puntos[n-1]]
                curva_actual.append( [lista_puntos[n][0]+0.1, lista_puntos[n][1]] )###
                agujero=True
        if not agujero: 
            curva_actual.append(lista_puntos[n])
            if n+1==len(lista_puntos):
                curvas.append(curva_actual)
        n+=1
    return curvas


def curvas_rectas(curvas_separadas):
    Mh = np.array([[0, -0.5, 1, -0.5], [1, 0, -2.5, 1.5], [0, 0.5, 2, -1.5], [0, 0, -0.5, 0.5]])

    curvas_puntos=[]
    cantidad_de_curvas=len(curvas_separadas)
    n=0
    m=0
    G=0
    while n<cantidad_de_curvas:
        if n%2==0:
            while m<len(curvas_separadas[n])-3:
                G = Catmull(np.array( [[ curvas_separadas[n][m][0],curvas_separadas[n][m][1],0]]).T  ,  np.array( [[ curvas_separadas[n][m+1][0],curvas_separadas[n][m+1][1],0]]).T,np.array( [[ curvas_separadas[n][m+2][0],curvas_separadas[n][m+2][1],0]]).T,np.array( [[ curvas_separadas[n][m+3][0],curvas_separadas[n][m+3][1],0]]).T )
                curvas_puntos.append(evalCurve(G,1000))####10 implica velocidad
                m+=1
            m=0
        else:
            ts = np.linspace(curvas_separadas[n][0][0],curvas_separadas[n][1][0], 70)   #tambien implica velocidad
            arreglo=[]
            for x in ts:
                arreglo.append([x,-10,0])
            arreglo=np.array(arreglo)
            curvas_puntos.append(arreglo)
        n+=1
    return curvas_puntos

def concatenacion(curvas_rectas):
    curvas_final=[]
    for curva in curvas_rectas:
        for coordenada in curva:
            curvas_final.append(coordenada)
    return curvas_final

lista_x=[[5, 1]]
lista=[[0, 4], [1, 2], [2, 6], [3, 3], [4, 7], [5, 1], [6, 1], [7, 1], [8, 1], [9, 3], [10, 4]]
separadas=separador_de_curvas(lista,lista_x)
#print(separadas)
curvas_y_rectas=curvas_rectas(separadas)
#print(concatenacion(curvas_y_rectas))
# P1 = np.array([[0, 0, 1]]).T