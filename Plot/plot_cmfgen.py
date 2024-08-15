import sys, os
import numpy as np
import logging
import warnings
from numpy import exp
from astropy import units, constants
import astropy.io.ascii as io
import matplotlib.pyplot as plt 
import util 
from scipy.signal import boxcar
from scipy.signal import convolve

def singlet(ax, name=r'Ly$\alpha',wavelength=1216,bot=0.8,top=0.9):
    limits=ax.get_xlim()
    ylim = ax.get_ylim()
    # print(limits)
    if limits[0]<wavelength and wavelength<limits[1]:
        ylim = ax.get_ylim()
        dy=ylim[1]-ylim[0]
        xbot=ylim[0]+bot*dy
        xtop=ylim[0]+top*dy
        ax.plot([wavelength,wavelength],[xbot,xtop],'k')
        # print(xbot,xtop)
        ax.text(wavelength,xtop,name,va='bottom',ha='center')
        
def doublet(ax, name='PV',w1=1118,w2=1128,bot=0.8,top=0.9):
    limits=ax.get_xlim()
    ylim = ax.get_ylim()
    # print(limits)
    if limits[0]<w1 and w2<limits[1]:
        dy=ylim[1]-ylim[0]
        xbot=ylim[0]+bot*dy
        xtop=ylim[0]+top*dy
        ax.plot([w1,w1],[xbot,xtop],'k')
        ax.plot([w2,w2],[xbot,xtop],'k')
        # print(xbot,xtop)
        ax.text(0.5*(w1+w2),xtop,name,va='bottom',ha='center')
        
def add_lines(ax):
    singlet(ax=ax, name=r'Ly$\alpha$',wavelength=1215.33,bot=0.8,top=0.9)
    singlet(ax=ax, name=r'Ly$\beta$',wavelength=1025.4,bot=0.8,top=0.9)
    singlet(ax=ax, name=r'Ly$\gamma$',wavelength=972.27,bot=0.8,top=0.85)
    singlet(ax=ax, name=r'Ly$\delta$',wavelength=949.48,bot=0.8,top=0.9)
    singlet(ax=ax, name=r'CIV',wavelength=1549,bot=0.8,top=0.9)
    singlet(ax=ax, name=r'CIII',wavelength=977.02008,bot=0.8,top=0.9)
    singlet(ax=ax, name=r'NIII',wavelength=989.7990118,bot=0.8,top=0.95)
    singlet(ax=ax, name=r'CIII$^{*}$',wavelength=1175,bot=0.8,top=0.9)
    singlet(ax=ax, name=r'NIV$^{*}$',wavelength=1718,bot=0.8,top=0.9)
    singlet(ax=ax, name=r'HeII',wavelength=1640,bot=0.8,top=0.9)
    singlet(ax=ax, name=r'NIV$^{*}$',wavelength=923,bot=0.8,top=0.9)
    singlet(ax=ax, name=r'OV$^{*}$',wavelength=1371.3,bot=0.8,top=0.9)
    singlet(ax=ax, name=r'NIV$^{*}$',wavelength=955.334,bot=0.7,top=0.75)
    
    
    doublet(ax = ax, name='PV',w1=1118,w2=1128,bot=0.8,top=0.9)
    doublet(ax = ax, name='NV',w1=1238.8,w2=1242.8,bot=0.8,top=0.9)
    doublet(ax = ax, name='SiIV',w1=1393.7,w2=1402.7,bot=0.8,top=0.9)
    doublet(ax = ax, name='SVI',w1=933.38,w2=945.55,bot=0.8,top=.85)
    doublet(ax = ax, name='OVI',w1=1031.9,w2=1037.6,bot=0.8,top=.85)
    doublet(ax = ax, name='SIV',w1=1062.6,w2=1076,bot=0.8,top=.85)


def make_figure(path="{}/Tests/cmfgen/".format(util.g_DataDir), root="a3_hhe"):
    """
    Generate a comparison figure between Tardis and Python spectra.

    Parameters:
    -----------
    path : str, optional
        Path to the directory containing the data files. Defaults to "../Data/Tests/tardis/".

    Returns:
    --------
    None

    Notes:
    ------
    This function loads data files for Tardis and Python spectra, corrects fluxes to the same distance 
    using the inverse square law, and creates a comparison plot. It plots Tardis spectrum and Python 
    spectrum (assuming the data files are named "tardis_python_spectrum.dat", "1d_sn_87.spec", and 
    "1d_sn_87_2.spec" respectively). The plot is saved as "Figures/tardis_comparison.pdf".

    """

    cmfgen=io.read('{}/a3.spec.txt'.format(path))
    #a3.info()
    #smooth=201
    cmfgen['smooth']=util.smooth(cmfgen['nuFnu'], width=201)

    star=io.read("{}/{}.spec".format(path, root))
    star['nuFnu']=star['Lambda']*star['A45P0.50']
    star_nufnu=util.smooth(star['nuFnu'], width=21)
    py_zorder = 5

    xlims = ((875,1199), (1150,1499), (1450,1799))
    #cmfzorder = 1

    fig, axes = plt.subplots(figsize=(7,10), nrows=3, ncols=1)
    norm = 1e4

    for i, ax in enumerate(axes):
        ax.plot(star['Lambda'],norm*star_nufnu,label=util.CODE_NAME, zorder=py_zorder, c="C0", lw=2.5)
        ax.plot(cmfgen['Wave'],norm*cmfgen['smooth'],label='CMFGen', c="k", lw=3, alpha=0.8)
        ax.set_xlim(xlims[i][0], xlims[i][1])
        add_lines(ax)
        ax.set_ylabel(r'$\nu F_{\nu}$ ($10^{-4}$~erg~cm$^{-2}$~s$^{-1}$)',size=16)



    ax.legend(loc='best')
    ax.set_xlabel(util.wavelength_label, fontsize=util.onepanel_labelsize)
    fig.tight_layout(pad=0.1)
    util.save_paper_figure("cmfgen_comparison.pdf", fig=fig)




if __name__ == "__main__":
    util.set_plot_defaults()
    make_figure()
