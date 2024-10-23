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


def make_figure(fnames=['cv_standard', 'cv_cno', 'cv_hhe', 'cv_hhe_1e5', 'cv_hhe_1e4'], xdir="{}/Demos/cv/".format(util.g_DataDir), **savefig_kwargs):

    util.set_cmap_cycler("viridis", N=4)
    util.set_ui_cycler("canada")
    plt.rcParams["lines.linewidth"] = 1.5

    if os.path.isdir(xdir) == False:
        print('Cannot find %s' % xdir)
        return

    labels = [r"{}, ${{\cal N}}_\gamma=10^7$".format(util.BASIC_MODE), r'Macro(H,He,C,N,O), ${\cal N}_\gamma=10^7$',
              r'Macro(H,He), ${\cal N}_\gamma=10^7$', r'Macro(H,He), ${\cal N}_\gamma=10^5$', r'Macro(H,He), ${\cal N}_\gamma=10^4$']
    colors = ["C0", "C3", "C2", "C2", "C2"]
    lstyle = ["-o", "-o", "-o", "--o", "--^"]

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))
    for i, root in enumerate(fnames):
        fname = '{}/{}.convergence.txt'.format(xdir, root)

        try:
            s = ascii.read(fname)
        except:
            print('Error: could not read {}'.format(fname))
            return

        # s.info()
        x = np.concatenate((np.array([0]), s['Ncycle']+1))
        y = np.concatenate((np.array([0]), s['Converged']))
        ax.plot(x, y, lstyle[i], label=labels[i], lw=3, c=colors[i])
        # if i == 1:
        #     plt.plot(s['Ncycle']+1,s['hc_converged'],'o-',label=labels[i]+": $T_e$ convergence", lw=3, ls="--", c="C{}".format(str(i)))

    ax.set_ylim(0, 1.05)
    ax.set_xticks(range(0, 20, 2))
    ax.set_xlim(0, 20)
    ax.legend(frameon=False, fontsize=14, loc="lower right")
    ax.set_xlabel('Ionization Cycle', size=util.onepanel_labelsize)
    ax.set_ylabel('Converged Fraction', size=util.onepanel_labelsize)
    fig.tight_layout(pad=0.07)
    util.save_paper_figure('cv_converge.pdf', fig=fig, **savefig_kwargs)


# Next lines permit one to run the routine from the command line
if __name__ == "__main__":
    util.set_plot_defaults()
    make_figure()
