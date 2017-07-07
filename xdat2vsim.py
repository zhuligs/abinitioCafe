#!/usr/bin/python -u

import numpy as np
import math
from optparse import OptionParser


def xdat2vsim(npt, l, ascii, vasp):
    xbuff = []
    with open('XDATCAR') as f:
        for line in f:
            xbuff.append(line.split())

    symb = xbuff[5]
    typt = np.array(xbuff[6], int)
    nat = sum(typt)

    symbs = []
    for i in range(len(symb)):
        symbs += symb[i] * typt[i]

    nconf = 0
    for xx in xbuff:
        if 'Direct' in xx:
            nconf += 1

    if npt:
        for i in range(nconf):
            k = i * (8 + nat)
            lat = np.array(xbuff[k + 2: k + 5], float)
            dlat = get_dlat(lat)
            pos = np.array(xbuff[k + 8: k + 8 + nat], float)
            xyz = np.dot(pos, dlat)
            if i % l == 0:
                nsr = str('%8.8d' % i)
                if ascii:
                    f = open('xdat.' + nsr + '.ascii', 'w')
                    f.write(str(nat) + '\n')
                    f.write("%15.9f    %15.9f    %15.9f\n" %
                            (dlat[0][0], dlat[1][0], dlat[1][1]))
                    f.write("%15.9f    %15.9f    %15.9f\n" %
                            (dlat[2][0], dlat[2][1], dlat[2][2]))
                    for ip in range(len(xyz)):
                        f.write("%15.9f %15.9f %15.9f  %2s  %4d\n" %
                                (xyz[ip][0], xyz[ip][1], xyz[ip][2], symbs[ip], ip))
                    f.close()
                if vasp:
                    f = open('xdat.' + nsr + '.vasp', 'w')
                    f.write('xdat.' + nsr + '\n')
                    f.write('1.0\n')
                    for x in dlat:
                        f.write("%15.9f %15.9f %15.9f\n" % tuple(x))
                    for x in symb:
                        f.write(x + '  ')
                    f.write('\n')
                    for x in typt:
                        f.write(str(x) + '  ')
                    f.write('\n')
                    f.write('D\n')
                    for x in pos:
                        f.write("%15.9f %15.9f %15.9f\n" % tuple(x))
                    f.close()

    else:
        lat = np.array(xbuff[2: 5], float)
        dlat = get_dlat(lat)
        for i in range(nconf):
            k = 7 + i * (1 + nat)
            pos = np.array(xbuff[k + 1: k + 1 + nat], float)
            xyz = np.dot(pos, dlat)
            if i % l == 0:
                nsr = str('%8.8d' % i)
                if ascii:
                    f = open('xdat.' + str + '.ascii', 'w')
                    f.write(str(nat) + '\n')
                    f.write("%15.9f    %15.9f    %15.9f\n" %
                            (dlat[0][0], dlat[1][0], dlat[1][1]))
                    f.write("%15.9f    %15.9f    %15.9f\n" %
                            (dlat[2][0], dlat[2][1], dlat[2][2]))
                    for ip in range(len(xyz)):
                        f.write("%15.9f %15.9f %15.9f  %2s  %4d\n" %
                                (xyz[ip][0], xyz[ip][1], xyz[ip][2], symbs[ip], ip))
                    f.close()
                if vasp:
                    f = open('xdat.' + nsr + '.vasp', 'w')
                    f.write('xdat.' + nsr + '\n')
                    f.write('1.0\n')
                    for x in dlat:
                        f.write("%15.9f %15.9f %15.9f\n" % tuple(x))
                    for x in symb:
                        f.write(x + '  ')
                    f.write('\n')
                    for x in typt:
                        f.write(str(x) + '  ')
                    f.write('\n')
                    f.write('D\n')
                    for x in pos:
                        f.write("%15.9f %15.9f %15.9f\n" % tuple(x))
                    f.close()


def get_dlat(lat):
    cons = lat2lcons(lat)
    dlat = lcons2lat(cons)
    return np.array(dlat, float)


def lat2lcons(lat):
    ra = math.sqrt(lat[0][0]**2 + lat[0][1]**2 + lat[0][2]**2)
    rb = math.sqrt(lat[1][0]**2 + lat[1][1]**2 + lat[1][2]**2)
    rc = math.sqrt(lat[2][0]**2 + lat[2][1]**2 + lat[2][2]**2)

    cosa = (lat[1][0] * lat[2][0] + lat[1][1] * lat[2][1] +
            lat[1][2] * lat[2][2]) / rb / rc
    cosb = (lat[0][0] * lat[2][0] + lat[0][1] * lat[2][1] +
            lat[0][2] * lat[2][2]) / ra / rc
    cosc = (lat[0][0] * lat[1][0] + lat[0][1] * lat[1][1] +
            lat[0][2] * lat[1][2]) / rb / ra

    alpha = math.acos(cosa)
    beta = math.acos(cosb)
    gamma = math.acos(cosc)

    return np.array([ra, rb, rc, alpha, beta, gamma], float)


def lcons2lat(cons):
    (a, b, c, alpha, beta, gamma) = cons

    bc2 = b**2 + c**2 - 2 * b * c * math.cos(alpha)

    h1 = a
    h2 = b * math.cos(gamma)
    h3 = b * math.sin(gamma)
    h4 = c * math.cos(beta)
    h5 = ((h2 - h4)**2 + h3**2 + c**2 - h4**2 - bc2) / (2 * h3)
    h6 = math.sqrt(c**2 - h4**2 - h5**2)

    lattice = [[h1, 0., 0.], [h2, h3, 0.], [h4, h5, h6]]
    return lattice


if __name__ == "__main__":
    parser = OptionParser()
    parser.set_defaults(is_npt=False, l=1, is_ascii=False, is_vasp=False)
    parser.add_option("-p", dest="is_npt", action="store_true")
    parser.add_option("-a", dest="is_ascii", action="store_true")
    parser.add_option("-v", dest="is_vasp", action="store_true")
    parser.add_option("-l", dest="l", type="int")

    (options, args) = parser.parse_args()
    xdat2vsim(options.is_npt, options.l, options.is_ascii, options.is_vasp)
