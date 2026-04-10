import numpy as np

def angulo(a,b,c):

    a=np.array(a)
    b=np.array(b)
    c=np.array(c)

    ba=a-b
    bc=c-b

    cosang=np.dot(ba,bc)/(np.linalg.norm(ba)*np.linalg.norm(bc))
    cosang=np.clip(cosang,-1,1)

    ang=np.degrees(np.arccos(cosang))

    return ang