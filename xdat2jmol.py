#!/usr/bin/python -u

import numpy as np


def xdat2jmol():
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

    f = open('xdat.xyz', 'w')
    for i in range(nconf):
        k = i * (8 + nat)
        lat = np.array(xbuff[k + 2: k + 5], float)
        pos = np.array(xbuff[k + 8: k + 8 + nat], float)
        xyz = np.dot(pos, lat)
        f.write(str(nat) + '\n')
        f.write('xdat\n')
        for i in range(len(xyz)):
            f.write("%2s %15.9f %15.9f %15.9f\n" % (symbs[i], xyz[i][0], xyz[i][1], xyz[i][2]))

    f.close()


if __name__ == "__main__":
    xdat2jmol()
