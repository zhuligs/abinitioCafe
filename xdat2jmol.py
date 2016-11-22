#!/usr/bin/python -u

import numpy as np
from optparse import OptionParser


def xdat2jmol(npt, l):
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
    if npt:
        for i in range(nconf):
            k = i * (8 + nat)
            lat = np.array(xbuff[k + 2: k + 5], float)
            pos = np.array(xbuff[k + 8: k + 8 + nat], float)
            xyz = np.dot(pos, lat)
            if i % l == 0:
                f.write(str(nat) + '\n')
                f.write('xdat\n')
                for i in range(len(xyz)):
                    f.write("%2s %15.9f %15.9f %15.9f\n" % (symbs[i], xyz[i][0], xyz[i][1], xyz[i][2]))

        f.close()
    else:
        lat = np.array(xbuff[2: 5], float)
        for i in range(nconf):
            k = 7 + i * (1 + nat)
            pos = np.array(xbuff[k + 1: k + 1 + nat], float)
            xyz = np.dot(pos, lat)
            if i % l == 0:
                f.write(str(nat) + '\n')
                f.write('xdat\n')
                for i in range(len(xyz)):
                    f.write("%2s %15.9f %15.9f %15.9f\n" % (symbs[i], xyz[i][0], xyz[i][1], xyz[i][2]))
        f.close()


if __name__ == "__main__":
    parser = OptionParser()
    parser.set_defaults(is_npt=False,
                        l=1)
    parser.add_option("-p", dest="is_npt", action="store_true")
    parser.add_option("-l", dest="l", type="int")
    (options, args) = parser.parse_args()
    xdat2jmol(options.is_npt, options.l)

