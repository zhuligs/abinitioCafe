#!/usr/bin/python -u 

import numpy as np
from scipy.optimize import curve_fit


def bm3(x, V0, K, KK):
    t1 = 1.5 * K 
    t2 = (V0/x)**(7./3.) - (V0/x)**(5./3.)
    t3 = (V0/x)**(2./3.) - 1.
    t4 = 1 + 0.75 * (KK - 4.) * t3
    return t1 * t2 * t4


# def fit():
#     data = np.loadtxt('test2.txt')
#     y = data[:, 0]
#     x = data[:, 1]
#     print x 
#     print y


def fitt(datafile):
    data = np.loadtxt(datafile)
    y = data[:, 0]
    n = len(data[0])
    for i in range(1, n):
        x = data[:, i]
        V0, K, KK = fit(x, y)
        xx = np.linspace(x[0], x[-1], 200)
        yy = bm3(xx, V0, K, KK)
        f = open(datafile + '_' + str(i), 'w')
        for i in range(200):
            f.write("%9.3f %9.3f\n" % (yy[i], xx[i]))
        f.close()


def fit(x, y):
    init_vals = [x[0], 100., 20.]
    # print init_vals
    best_vals, covar = curve_fit(bm3, x, y, p0=init_vals, maxfev=10000)
    return best_vals


if __name__ == '__main__':
    fitt('test.txt')



    
    
