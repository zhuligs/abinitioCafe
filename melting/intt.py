#!/usr/bin/python


import scipy.optimize as opt
import numpy as np
import pylab as plt
from mpl_toolkits.mplot3d import Axes3D
from copy import deepcopy as cp


# def foa(T1, T2, T3):

def twoD_Gaussian( x, y, amplitude, xo, yo, sigma_x, sigma_y, ):
    # print 'ssx,', sigma_x
    theta = 0.0
    offset = 0.0
    xo = float(xo)
    yo = float(yo)    
    a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
    b = -(np.sin(2*theta))/(4*sigma_x**2) + (np.sin(2*theta))/(4*sigma_y**2)
    c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)
    g = offset + amplitude*np.exp( - (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo) 
                            + c*((y-yo)**2)))
    return g.ravel()


def get_sigma(T1, T2, T3):
    difft = []
    for i in range(1, 10000):
        sx = i * 0.01
        dt = twoD_Gaussian(12.5, 0, T1, 0, 0, sx, 10)
        ddt = abs(dt[0] - T2)
        difft.append([ddt, sx])
    sdiff = sorted(difft, key=lambda x:x[0])
    sigma_x = sdiff[0][1]

    difft = []
    for i in range(1, 10000):
        sy = i * 0.01
        dt = twoD_Gaussian(0, 12.5, T1, 0, 0, 10, sy)
        ddt = abs(dt[0] - T3)
        difft.append([ddt, sy])
    sdiff = sorted(difft, key=lambda x:x[0])
    sigma_y = sdiff[0][1]
    return (sigma_x, sigma_y)


def linT(T1, T4, d):
    return (T4-T1)*d/5.0 + T1


def getT(T1, T2, T3, T4, sigma_x, sigma_y):

    x = np.arange(-12.5, 12.5, 0.1)
    y = np.arange(-12.5, 12.5, 0.1)
    x, y = np.meshgrid(x, y)
    X = x
    Y = y
    
    datas = []
    n = 100
    dt = 5.0 / n
    for i in range(n+1):
        d = i * dt
        amp = linT(T1, T4, d)
        # print amp
        data = twoD_Gaussian(x, y, amp, 0, 0, sigma_x, sigma_y)
        datas.append(cp(data))

    dt = 0
    for x in datas:
        dxx = sum(x)/len(x)
        dt += dxx
        # print dxx
    return dt/(n+1)


def rplot(T1, T2, T3, T4, sigma_x, sigma_y):
    x = np.arange(-12.5, 12.5, 0.1)
    y = np.arange(-12.5, 12.5, 0.1)
    x, y = np.meshgrid(x, y)
    X = x
    Y = y
    
    datas = []
    for i in range(6):
        d = i * 1.0
        amp = linT(T1, T4, d)
        # print amp
        data = twoD_Gaussian(x, y, amp, 0, 0, sigma_x, sigma_y)
        datas.append(cp(data))

    norm = plt.cm.colors.Normalize(vmax=3000, vmin=1500)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i in range(6):
        data = datas[i]
        minx = min(data)
        maxx = max(data)
        nn = 32
        delt = (maxx - minx) / nn
        levs = []
        for j in range(nn+1):
            levs.append(minx + j * delt)
        Z = data.reshape(250, 250)
        ofs = 5 - i
        cset = ax.contourf(X, Y, Z, zdir='z', levels=levs, offset=ofs, 
                           norm=norm, cmap=plt.cm.jet)
    ax.set_zlim3d(0, 5)
    surf = ax.plot_surface(X, Y, Z, norm=norm, cmap=plt.cm.jet, shade=False)
    fig.colorbar(surf)
    plt.show()


if __name__ == '__main__':
    T1 = 3000
    T2 = 2500
    T3 = 2720
    T4 = 1800
    sigma_x, sigma_y = get_sigma(T1, T2, T3)
    print 'Average T:', getT(T1, T2, T3, T4, sigma_x, sigma_y)
    rplot(T1, T2, T3, T4, sigma_x, sigma_y)

