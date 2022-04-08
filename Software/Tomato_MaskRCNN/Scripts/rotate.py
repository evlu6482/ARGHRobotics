def rotateaboutX(X,Y,Z):
    import numpy as np
    import math as m
    theta=-21 *np.pi/180 
    c,s= m.cos(theta), m.sin(theta)
    a= np.array([[1,0,0],
                 [0,c,s],
                 [0,-s,c]])
    V=np.array([X,Y,Z])
    nx,ny,nz=a.dot(V)
    # nx=(nx+0.024)
    # ny=(ny+0.1995)
    # nz=(-nz+0.065)
    return nx, ny, nz
#     Location of Calibrated Center Point In Camera Frame:
# cX:  0.030763614966848193 cY:  -0.03466931447254483 cZ:  0.43800002336502075
# desired location x=5.6 y=59.75 z=24.6 [cm]

X=0.03076
Y=-0.034669
Z=0.438

# nx,ny,nz=eng.Rotate(X,Y,Z,nargout=3)
# print(nx)
# print(ny)
# print(nz)

nx1,nz1,ny1=rotateaboutX(X,Y,Z)
print("desired location x=0.056 y=0.5975 z=0.2596 [m]")
print(nx1+0.024)
print(ny1+0.1995)
print(-nz1+0.065)

#31 ,31.5