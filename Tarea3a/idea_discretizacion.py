


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
