#!/usr/bin/python -u 

import numpy 

def countbond(bondfile):
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
            if v < 1.27: CC3.append(k)
            if 1.27 <= v < 1.4: CC2.append(k) 
            if v >= 1.4: CC1.append(k)
        if k[0] < 145 and k[1] > 144:
            if v < 1.225: CN3.append(k)
            if 1.225 <= v < 1.34: CN2.append(k)
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
            Csp.append(x[0])
        if (len(x)-1) / 2 == 3:
            Csp2.append(x[0])
        if (len(x)-1) / 2 == 4:
            Csp3.append(x[0])

    for x in buff[144:]:
        if (len(x)-1) / 2 == 1: 
            Nsp.append(x[0])
        if (len(x)-1) / 2 == 2:
            Nsp.append(x[0])
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





if __name__ == '__main__':
    countbond('cnbond')