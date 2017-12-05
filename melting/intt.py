#!/usr/bin/python


import scipy.optimize as opt
import numpy as np
import pylab as plt
from mpl_toolkits.mplot3d import Axes3D


# def foa(T1, T2, T3):

def twoD_Gaussian( (x, y), amplitude, xo, yo, sigma_x, sigma_y, theta, offset ):
    # print 'ssx,', sigma_x
    xo = float(xo)
    yo = float(yo)    
    a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
    b = -(np.sin(2*theta))/(4*sigma_x**2) + (np.sin(2*theta))/(4*sigma_y**2)
    c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)
    g = offset + amplitude*np.exp( - (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo) 
                            + c*((y-yo)**2)))
    return g.ravel()


x = np.arange(-12.5, 12.5, 0.01)
y = np.arange(-12.5, 12.5, 0.01)
x, y = np.meshgrid(x, y)

# X = np.arange(0, 250, 1)
# Y = np.arange(0, 250, 1)
xxx, yyy = np.meshgrid(np.linspace(-12.5,12.5,2500), np.linspace(-12.5,12.5,2500))
X = xxx
Y = yyy
print X
Z = xxx*0.0
# Y = y 
zz = x * 0.0
Zs = []
for i in range(6):
    Zs.append(zz + i*1.0)

t = 0
sx = 20.7
sy = 28.2


# for i in range(1, 1000):
#     sy = i*0.1
#     print sy, twoD_Gaussian( (0, 12.5), 3000, 0, 0, sx, sy, t, 0)

print twoD_Gaussian( (12.5, 0), 3000, 0, 0, sx, sy, t, 0)
print twoD_Gaussian( (0, 12.5), 3000, 0, 0, sx, sy, t, 0)
print twoD_Gaussian( (5, 5), 3000, 0, 0, sx, sy, t, 0)

data0 = twoD_Gaussian((x, y), 3000, 0, 0, sx, sy, 0, 0)
data1 = data0*0.95
# data2 = twoD_Gaussian((x, y), 3000, 0, 0, sx, sy, 0, 0)*0.6
data2 = data0*0.9 
data3 = data0*0.8
data4 = data0*0.7
data5 = data0*0.6
datas= [data0, data1, data2, data3,data4, data5]

# plt.figure()
# plt.imshow(data.reshape(250, 250))
norm = plt.cm.colors.Normalize(vmax=3000, vmin=1500)

fig = plt.figure()

ax0 = fig.add_subplot(121)
ax0.imshow(data0.reshape(2500, 2500), cmap=plt.cm.jet, norm=norm, extent=[-12.5, 12.5, -12.5,12.5])
Z = data0.reshape(2500, 2500)
Z2 = data3.reshape(2500, 2500)
print data0.reshape(2500, 2500)
ax = fig.add_subplot(122, projection='3d')
min1 = min(data0)
min2 = max(data0)
nn = 16

delt = (min2-min1)/nn
levs=[]
for i in range(nn+1):
    levs.append(min1+i*delt)
# ax.plot_surface(X, Y, Z, cmap=plt.cm.jet, norm=norm, shade=False)
cset = ax.contourf(X, Y, Z, zdir='z', levels=levs, offset = 0, norm=norm, cmap=plt.cm.jet)
cset = ax.contourf(X, Y, Z2, zdir='z', offset = 3, norm=norm, cmap=plt.cm.jet)
ax.set_zlim3d(-1,5)
# for i in range(6):
#     Z = Zs[i]
#     data = datas[i]
#     ax.plot_surface(X, Y, Z, facecolors=plt.cm.jet(data0.reshape(250, 250)), shade=False)


# plt.subplot(5,1,1)
# plt.imshow(data1.reshape(250, 250), norm=norm, cmap=plt.cm.jet)

# plt.subplot(5,1,2)
# plt.imshow(data2.reshape(250, 250), norm=norm, cmap=plt.cm.jet)

# plt.subplot(5,1,3)
# plt.imshow(data3.reshape(250, 250), norm=norm, cmap=plt.cm.jet)

# plt.subplot(5,1,4)
# plt.imshow(data4.reshape(250, 250), norm=norm, cmap=plt.cm.jet)

# plt.subplot(5,1,5)
# plt.imshow(data5.reshape(250, 250), norm=norm, cmap=plt.cm.jet)



# plt.colorbar()
# plt.contour(data5.reshape(250, 250), 16)
# plt.imshow(data5.reshape(250, 250), norm=norm, cmap=plt.cm.BuPu_r)
# cax = plt.axes([])

# plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)

# plt.contour(x, y, data.reshape(250, 250), 8, colors='w')
plt.show()

# # print data

