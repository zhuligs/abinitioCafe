#!/usr/bin/python


import scipy.optimize as opt
import numpy as np
import pylab as plt


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


x = np.arange(-12.5, 12.5, 0.1)
y = np.arange(-12.5, 12.5, 0.1)
x, y = np.meshgrid(x, y)


t = 0
sx = 20.7
sy = 28.2


# for i in range(1, 1000):
#     sy = i*0.1
#     print sy, twoD_Gaussian( (0, 12.5), 3000, 0, 0, sx, sy, t, 0)

print twoD_Gaussian( (12.5, 0), 3000, 0, 0, sx, sy, t, 0)
print twoD_Gaussian( (0, 12.5), 3000, 0, 0, sx, sy, t, 0)
print twoD_Gaussian( (5, 5), 3000, 0, 0, sx, sy, t, 0)

data = twoD_Gaussian((x, y), 3000, 0, 0, sx, sy, 0, 0)*0.6
plt.figure()
plt.imshow(data.reshape(250, 250))
plt.colorbar()
# plt.contour(x, y, data.reshape(250, 250), 8, colors='w')
plt.show()

# # print data

