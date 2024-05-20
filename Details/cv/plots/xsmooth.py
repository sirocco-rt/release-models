#!/usr/bin/env python 

'''
                    Space Telescope Science Institute

Synopsis:  

This is just a little utility to 
allow me  to boxcar smoothe thins
without having to call the appropirate
routines from scipy


Command line usage (if any):

    usage: xsmooth filename

Description:  

Primary routines:

    doit

Notes:
                                       
History:

210210 ksl Coding begun

'''

import sys
from astropy.io import ascii
import numpy

from scipy.signal import boxcar
from scipy.signal import convolve

def xsmooth(flux,smooth=21):
    '''
    boxcar smooth the flux
    '''
    if (smooth)>1:
        q=convolve(flux,boxcar(smooth)/float(smooth),mode='same')
        return(q)
    else:
        return(flux)


# Next lines permit one to run the routine from the command line
if __name__ == "__main__":
    import sys
    if len(sys.argv)>1:
        # doit(int(sys.argv[1]))
        doit(sys.argv[1])
    else:
        print ('usage: xsmooth filename')
