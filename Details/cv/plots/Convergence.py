#!/usr/bin/env python
# coding: utf-8


'''
                    Space Telescope Science Institute

Synopsis:  

A routine to produce a figure that illustrates
how rapidly (CV) models converge)


Command line usage (if any):

    usage: Convergence.py filename

Description:  

Primary routines:

    doit

Notes:
                                       
History:

240524 ksl Coding begun

'''

import sys
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import ascii
import os




def doit(standard='cv_standard',hhe='cv_hhe',cno='cv_cno',xdir='../python//Results/'):

    if os.path.isdir(xdir)==False:
        print('Cannot find %s' % xdir)
        return

    sfile='%s/%s.convergence.txt' % (xdir,standard)
    hfile='%s/%s.convergence.txt' % (xdir,hhe)
    cfile='%s/%s.convergence.txt' % (xdir,cno)


    try:
        s=ascii.read(sfile)
    except:
        print('Error: could not read %s' % sfile)
        return

    try:
        h=ascii.read(hfile)
    except:
        print('Error: could not read %s' % hfile)
        return

    try:
        c=ascii.read(cfile)
    except:
        print('Error: could not read %s' % cfile)
        return

    c.info()

    plt.figure(1,(6,6))

    plt.plot(s['Ncycle'],s['Converged'],'o-',label='Standard')
    plt.plot(h['Ncycle'],h['Converged'],'o-',label='Macro(H,He)')
    plt.plot(c['Ncycle'],c['Converged'],'o-',label='Macro(H,He.C.N,O)')
    plt.xlim(0.1,10)
    plt.ylim(0,1.1)
    plt.legend()
    plt.xlabel('Cycle',size=16)
    plt.ylabel('Converged Fraction',size=16)
    plt.tight_layout()
    plt.savefig('cv_converge.png')
    


# Next lines permit one to run the routine from the command line
if __name__ == "__main__":
    import sys
    if len(sys.argv)==1:
        doit()
    elif len(sys.argv)==2:
        doit(sys.argv[1])
    else:
        print (__doc__)




