#!/usr/bin/python -u


import numpy as np
from scipy.integrate import quad


def expz(z, n):
    return z**n / ((np.exp(z) - 1) * (1 - np.exp(-1 * z)))


def expzint(n, theta, T):
    return quad(expz, 0, theta / T, args=(n))[0]


def rho(T, dv, n, theta):
    return dv * (T / theta)**n * expzint(n, theta, T)


def rhobgsta(T, dv, n, theta, rhosat):
    return 1. / (1. / rho(T, dv, n, theta) + 1. / rhosat)


def readexpdata():
    buff = []
    with open('expd.dat') as f:
        for line in f:
            buff.append(line.split())
    return np.array(buff, float)


def fitdata(theta, dv, n):
    expdata = readexpdata()
    xx = []
    for i in range(180, 220):
        xfit = float(i)
        error = 0.
        for x in expdata:
            calx = rhobgsta(x[0], dv, n, theta, xfit)
            error += (x[1] - calx)**2
        xx.append([i, error])

    # for x in xx:
    #     print x[0], x[1]

    sortx = sorted(xx, key=lambda x: x[1])
    return sortx[0][0]


if __name__ == '__main__':
    # theta = 636.
    # n = 4.9
    # # print expzint(n, theta)
    # dv = 67.5
    # rhosat = 200.
    # for k in range(10, 2500):
    #     T = float(k)
    #     print k, rho(T, dv, n, theta), rhobgsta(T, dv, n, theta, rhosat)
    theta = 636.
    dv = 67.5
    n = 4.9
    rho_sat = fitdata(theta, dv, n)
    print 'Best rho_sat', rho_sat
    f = open('cal.dat', 'w')
    for k in range(10, 2500):
        T = float(k)
        y1 = rho(T, dv, n, theta)
        y2 = rhobgsta(T, dv, n, theta, rho_sat)
        f.write("%7.2f %7.2f %7.2f\n" % (T, y1, y2))
    f.close()
