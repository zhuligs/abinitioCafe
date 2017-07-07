#!/usr/bin/python -u 

import numpy as np
from itdbase import Cell
import itin

def countbond(bondfile):

    xcell = set_cell_from_vasp('POSCAR')
    pos = xcell.get_cart_positions()
    buff = []
    with open(bondfile) as f:
        for line in f:
            buff.append(line.split())

    binfo = {}
    j = 0
    for item in buff:
        # print 'item', item
        for i in range(0, len(item)-2, 2):
            # print i, i+1, i+2
            yz = tuple(sorted([int(item[0]), int(item[i+1])]))
            binfo[yz] = float(item[i+2])
            j += 1
            # binfo.append([yz, float(item[i+2])])
    # print binfo
    # print len(binfo)
    # print k

    CC1 = []
    CC2 = []
    CC3 = []
    CN1 = []
    CN2 = []
    CN3 = []
    NN1 = []
    NN2 = []
    NN3 = []

    for k, v in binfo.items():
        if k[0] < 145 and k[1] < 145:
            if v < 1.3: CC3.append(k)
            if 1.3 <= v < 1.4: CC2.append(k) 
            if v >= 1.4: CC1.append(k)
        if k[0] < 145 and k[1] > 144:
            if v < 1.180: CN3.append(k)
            if 1.180 <= v < 1.34: CN2.append(k)
            if v >= 1.34: CN1.append(k)
        if k[0] > 144 and k[1] > 144:
            print 'NN', v
            if v < 1.175: NN3.append(k)
            if 1.175 <= v < 1.3: NN2.append(k)
            if v >= 1.3: NN1.append(k)


    print 'C-C', len(CC1)
    print 'C=C', len(CC2)
    print 'C#C', len(CC3)
    print 'C-N', len(CN1)
    print 'C=N', len(CN2)
    print 'C#N', len(CN3)
    print 'N-N', len(NN1)
    print 'N=N', len(NN2)
    print 'N#N', len(NN3)

    Csp = []
    Csp2 = []
    Csp3 = []
    Nsp = []
    Nsp2 = []
    Nsp3 = []

    for x in buff[:144]:
        if (len(x)-1) / 2 == 1: 
            Csp.append(x[0])
        if (len(x)-1) / 2 == 2:
            n0 = int(x[0]) - 1 
            n1 = int(x[1]) - 1
            n2 = int(x[3]) - 1
            if jiaodu(pos[n0], pos[n1], pos[n2]):
                Csp.append(x[0])
            else:
                Csp2.append(x[0])
        if (len(x)-1) / 2 == 3:
            Csp2.append(x[0])
        if (len(x)-1) / 2 == 4:
            Csp3.append(x[0])

    for x in buff[144:]:
        if (len(x)-1) / 2 == 1: 
            Nsp.append(x[0])
        if (len(x)-1) / 2 == 2:
            n0 = int(x[0]) - 1 
            n1 = int(x[1]) - 1
            n2 = int(x[3]) - 1
            if jiaodu(pos[n0], pos[n1], pos[n2]):
                Nsp.append(x[0])
            else:
                Nsp2.append(x[0])
        if (len(x)-1) / 2 == 3:
            Nsp2.append(x[0])
        if (len(x)-1) / 2 == 4:
            Nsp3.append(x[0])
    print 'Csp', len(Csp)
    print 'Csp2', len(Csp2)
    print 'Csp3', len(Csp3)
    print 'Nsp', len(Nsp)
    print 'Nsp2', len(Nsp2)
    print 'Nsp3', len(Nsp3)

    print Csp
    print Nsp

    nco = 0
    for x in buff:
        nco = nco + (len(x)-1) / 2
    print 'ave coor', nco/216.
    nco = 0
    for x in buff[:144]:
        nco = nco + (len(x)-1) / 2
    print 'c coor', nco/144.
    nco = 0
    for x in buff[144:]:
        nco = nco + (len(x)-1) / 2
    print 'n coor', nco/72.




def jiaodu(p0, p1, p2):
    a = p1 - p0
    b = p2 - p0

    cosa = np.dot(a, b) / np.sqrt(np.dot(a,a) * np.dot(b, b))

    du = np.arccos(cosa)/np.pi * 180.
    if du > 170:
        return True
    else:
        return False


def set_cell_from_vasp(pcar):
    xcell = Cell()
    buff = []
    with open(pcar) as f:
        for line in f:
            buff.append(line.split())

    lat = np.array(buff[2:5], float)
    try:
        typt = np.array(buff[5], int)
    except:
        del(buff[5])
        typt = np.array(buff[5], int)
    pos = np.array(buff[7:7+itin.nat], float)
    xcell.set_name(itin.sname)
    xcell.set_lattice(lat)
    if buff[6][0].strip()[0] == 'D':
        xcell.set_positions(pos)
    else:
        xcell.set_cart_positions(pos)
    xcell.set_typt(typt)
    xcell.set_znucl(itin.znucl)
    xcell.set_types()
    xcell.cal_fp(itin.fpcut, itin.lmax)
    return xcell





if __name__ == '__main__':
    countbond('cnbond')
    # xcell = set_cell_from_vasp('POSCAR')
    # pos = xcell.get_cart_positions()

    # jiaodu(pos[215], pos[143], pos[69])
    # jiaodu(pos[27], pos[16], pos[99])
