#!/usr/bin/env python
# coding: utf-8


'''
                    Space Telescope Science Institute

Synopsis:

Plot routines for making figures associated with CV models


Command line usage (if any):

    usage: PlotCV.py filename

Description:

Primary routines:

    doit

Notes:

History:

240506 ksl Coding begun

'''
# # Figure to compare various CV models

import os
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import ascii

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

def fig_compare(simple='cv_standard', hhe='cv_hhe', cno='cv_cno', xdir='python/Results'):
    '''
    Plot the UV and visible spectra of various CV models
    '''

    uv_simple = f'{xdir}/{simple}.spec'
    uv_hhe = f'{xdir}/{hhe}.spec'
    uv_cno = f'{xdir}/{cno}.spec'

    xsimple = ascii.read(uv_simple)
    xhhe = ascii.read(uv_hhe)
    xcno = ascii.read(uv_cno)

    vis_simple = uv_simple.replace('cv_', 'vis_')
    vis_hhe = uv_hhe.replace('cv_', 'vis_')
    vis_cno = uv_cno.replace('cv_', 'vis_')

    print(vis_simple,vis_hhe,vis_cno)

    vsimple = ascii.read(vis_simple)
    vhhe = ascii.read(vis_hhe)
    vcno = ascii.read(vis_cno)

    wmin = 850
    wmax = 1800
    ang = 'A62P0.50'

    fig, axs = plt.subplots(3, 2, figsize=(12, 12))  # 3 rows, 2 columns

    # Plot for the first row
    axs[0, 0].plot(xsimple['Lambda'], xsmooth(xsimple[ang]), label='Simple')
    axs[0, 0].text(0.3, 0.85, r'i=62 deg', fontsize=12, ha='center', va='center', transform=axs[0, 0].transAxes)
    axs[0, 0].set_xlim(wmin, wmax)
    axs[0, 0].legend()

    axs[1, 0].plot(xhhe['Lambda'], xsmooth(xhhe[ang]), label='Macro(H,He)')
    axs[1, 0].set_xlim(wmin, wmax)
    axs[1, 0].legend()

    # Plot for the third row
    axs[2, 0].plot(xcno['Lambda'], xsmooth(xcno[ang]), label='Macro(H,He,C,N,O)')
    axs[2, 0].set_xlim(wmin, wmax)
    axs[2, 0].legend()

    wmin=3500
    wmax=6800
    ang = 'A80P0.50'
    ymin=0
    ymax=4e-13

    # Plot for the second row
    axs[0, 1].plot(vsimple['Lambda'], xsmooth(vsimple[ang]), label='Simple')
    axs[0, 1].text(0.3, 0.85, r'i=80 deg', fontsize=12, ha='center', va='center', transform=axs[0,1].transAxes)
    axs[0, 1].set_xlim(wmin, wmax)
    axs[0, 1].set_ylim(ymin,ymax)
    axs[0, 1].legend()

    axs[1, 1].plot(vhhe['Lambda'], xsmooth(vhhe[ang]), label='Macro(H,He)')
    axs[1, 1].set_xlim(wmin, wmax)
    axs[1,1].set_ylim(ymin,ymax)
    axs[1, 1].legend()

    # Plot for the third row
    axs[2, 1].plot(vcno['Lambda'], xsmooth(vcno[ang]), label='Macro(H,He,C,N,O)')
    axs[2, 1].set_xlim(wmin, wmax)
    axs[2, 1].set_ylim(ymin,ymax)
    axs[2, 1 ].legend()


    # Add axis labels
    fig.text(0.5, -0.02, r'Wavelength ($\AA$)', ha='center', va='center', fontsize=14)
    fig.text(-0.02, 0.5, r'Flux (ergs cm$^{-2}$ s$^{-1} \AA^{-1}$)', ha='center', va='center', rotation='vertical', fontsize=14)

    plt.tight_layout()

    plt.savefig('cv_spec.png')


def doit(xdir='../Data/Demos/cv/'):
    '''
    This is a hardired routine to produce figurets
    for CV models
    '''



    print('Making CV figure')
    fig_compare(xdir=xdir)


# Next lines permit one to run the routine from the command line
if __name__ == "__main__":
    import sys
    print('hello world')
    print(sys.argv)
    doit()


