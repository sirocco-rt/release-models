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
import util 



def make_figure(fnames=['cv_standard','cv_hhe','cv_hhe_short', 'cv_cno'],xdir="{}/Demos/cv/".format(util.g_DataDir)):

    util.set_cmap_cycler("viridis", N=4)
    #util.set_ui_cycler("british")
    plt.rcParams["lines.linewidth"] = 1.5

    if os.path.isdir(xdir)==False:
        print('Cannot find %s' % xdir)
        return

    labels = [util.BASIC_MODE, 'Macro(H,He)', 'Macro(H,He), ${\cal N}_\gamma=10^7$', 'Macro(H,He,C,N,O)']
    colors = ["C0","C1","C1", "C2"]
    lstyle = ["-o", "-o", "--o", "-o"]
    plt.figure(1,(6,5))
    for i,root in enumerate(fnames):
        fname='{}/{}.convergence.txt'.format(xdir,root)

        try:
            s=ascii.read(fname)
        except:
            print('Error: could not read {}'.format(fname))
            return


        s.info()

        plt.plot(s['Ncycle']+1,s['Converged'],lstyle[i],label=labels[i], lw=3, c=colors[i])
        # if i == 1:
        #     plt.plot(s['Ncycle']+1,s['hc_converged'],'o-',label=labels[i]+": $T_e$ convergence", lw=3, ls="--", c="C{}".format(str(i)))

    plt.ylim(0,1.05)
    plt.xticks(range(0,20,2))
    plt.xlim(0,20)
    plt.legend(frameon=False, fontsize=16)
    plt.xlabel('Ionization Cycle',size=util.onepanel_labelsize)
    plt.ylabel('Converged Fraction',size=util.onepanel_labelsize)
    plt.tight_layout(pad=0.07)
    util.save_paper_figure('cv_converge.pdf')
    


# Next lines permit one to run the routine from the command line
if __name__ == "__main__":
    util.set_plot_defaults()
    make_figure()



