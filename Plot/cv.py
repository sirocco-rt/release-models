#!/usr/bin/env python
# coding: utf-8


'''
                    Space Telescope Science Institute

Synopsis:

Plot routines for making figures associated with CV models


Command line usage (if any):

    usage: PlotCV.py 

Description:

    A simple command line script to make a figure for the
    CV spectra

Primary routines:

    doit

Notes:

    This version is hardowired to be have the data in the Data
    folder

History:

240506 ksl Coding begun

'''
# # Figure to compare various CV models
import matplotlib.pyplot as plt
from astropy.io import ascii
import util


def make_figure(simple='cv_standard', hhe='cv_hhe', cno='cv_cno', xdir="{}/Demos/cv/".format(util.g_DataDir), **savefig_kwargs):
    '''
    Plot the UV and visible spectra of various CV models
    '''
    util.set_cmap_cycler("viridis", N=4)
    util.set_ui_cycler("canada")
    plt.rcParams["lines.linewidth"] = 2
    uv_simple = f'{xdir}/{simple}.spec'
    uv_hhe = f'{xdir}/{hhe}.spec'
    uv_cno = f'{xdir}/{cno}.spec'

    xsimple = ascii.read(uv_simple)
    xhhe = ascii.read(uv_hhe)
    xcno = ascii.read(uv_cno)

    vis_simple = uv_simple.replace('cv_', 'vis_')
    vis_hhe = uv_hhe.replace('cv_', 'vis_')
    vis_cno = uv_cno.replace('cv_', 'vis_')

    vsimple = ascii.read(vis_simple)
    vhhe = ascii.read(vis_hhe)
    vcno = ascii.read(vis_cno)

    wmin = 850
    wmax = 1800
    ang = 'A62P0.50'

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))  # 3 rows, 2 columns
    ax_to_use = [axs[0], axs[0], axs[0]]

    # Plot for the first row
    offset = 1e-11
    ax_to_use[0].plot(xsimple['Lambda'], (2*offset) +
                      util.smooth(xsimple[ang]), label=util.BASIC_MODE, c="C0")
    ax_to_use[0].text(0.05, 0.04, r'$i=62.5^\circ$', fontsize=20,
                      ha='left', va='center', transform=ax_to_use[0].transAxes)
    ax_to_use[0].set_xlim(wmin, wmax)
    ax_to_use[0].legend()

    ax_to_use[1].plot(xhhe['Lambda'], offset +
                      util.smooth(xhhe[ang]), label='Macro(H,He)', c="C2")
    ax_to_use[1].set_xlim(wmin, wmax)
    # ax_to_use[1].legend()

    # Plot for the third row
    ax_to_use[2].plot(xcno['Lambda'], util.smooth(
        xcno[ang]), label='Macro(H,He,C,N,O)', c="C3")
    ax_to_use[2].set_xlim(wmin, wmax)
    ax_to_use[2].legend()
    ax_to_use[2].set_xlabel(util.wavelength_label,
                            fontsize=util.onepanel_labelsize)
    ax_to_use[2].set_ylabel(r"$F_\lambda$~(Arb.)",
                            fontsize=util.onepanel_labelsize)

    wmin = 3500
    wmax = 6800
    ang = 'A80P0.50'
    ymin = 0
    ymax = 1e-12

    ax_to_use = [axs[1], axs[1], axs[1]]

    # Plot for the second row
    offset = 3e-13
    ax_to_use[0].plot(vsimple['Lambda'], (2*offset) +
                      util.smooth(vsimple[ang]), label=util.BASIC_MODE, c="C0")
    ax_to_use[0].text(0.05, 0.04, r'$i=80^\circ$', fontsize=20,
                      ha='left', va='center', transform=ax_to_use[0].transAxes)
    ax_to_use[0].set_xlim(wmin, wmax)
    ax_to_use[0].set_ylim(ymin, ymax)

    ax_to_use[1].plot(vhhe['Lambda'], offset +
                      util.smooth(vhhe[ang]), label='Macro(H,He)', c="C2")
    ax_to_use[1].set_xlim(wmin, wmax)
    ax_to_use[1].set_ylim(ymin, ymax)

    # Plot for the third row
    ax_to_use[2].plot(vcno['Lambda'], util.smooth(
        vcno[ang]), label='Macro(H,He,C,N,O)', c="C3")
    ax_to_use[2].set_xlim(wmin, wmax)
    ax_to_use[2].set_ylim(ymin, ymax)

    # Add axis labels
    ax_to_use[2].set_xlabel(util.wavelength_label,
                            fontsize=util.onepanel_labelsize)

    plt.tight_layout(pad=0.05)

    util.save_paper_figure('cv_spec.pdf', **savefig_kwargs)


# Next lines permit one to run the routine from the command line
if __name__ == "__main__":
    util.set_plot_defaults()
    make_figure(xdir="{}/Demos/cv/".format(util.g_DataDir))
