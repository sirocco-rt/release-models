import sys
import os
import numpy as np
import logging
import warnings
from numpy import exp
from astropy import units
import astropy.io.ascii as io
import astropy.constants as const
import matplotlib.pyplot as plt
import util


HEV = 4.13620e-15


def plot_wind_panels(fig, gs_wind, sp, colours, options_flex, order):

    signs = ((-1, 1), (1, 1), (-1, -1), (1, -1))
    xlims = ((-1, 0), (0, 1), (-1, 0), (0, 1))
    ylims = ((0, 1), (0, 1), (-1, 0), (-1, 0))

    for i in range(4):
        obj = order[i]
        sightline = options_flex[obj]["sightlines"]
        rmax = options_flex[obj]["rmax"]
        rg = const.GM_sun.cgs.value * \
            options_flex[obj]["masses"] / const.c.cgs.value / const.c.cgs.value

        d = io.read(
            "{}/{}.master.txt".format(options_flex[obj]["wind_paths"], options_flex[obj]["roots"]))
        x, z, ne, inwind = util.wind_to_masked(
            d, value_string="ne", return_inwind=True)
        _, _, t_e, inwind = util.wind_to_masked(
            d, value_string="t_e", return_inwind=True)

        ax = fig.add_subplot(gs_wind[sp[i]])
        pcol = ax.pcolormesh(signs[i][0] * x/rg, signs[i][1] *
                             z/rg, np.log10(ne), vmin=8, vmax=12)
        pcol.set_edgecolor('face')
        ax.set_xlim(xlims[i][0] * rmax, xlims[i][1] * rmax)
        ax.set_ylim(ylims[i][0] * rmax, ylims[i][1] * rmax)
        ax.set_yticklabels([])
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xticklabels([])
        # ax.plot([xlims[i][0] * rmax/10.0, xlims[i][1] * rmax/10.0], [0, 0], lw=6)

        # plot the sightline
        for j in (0, 1):
            xx = np.linspace(0, 10.0*rmax, 10)
            theta = np.radians(sightline[j])
            ax.plot(signs[i][0]*xx * np.sin(theta),
                    signs[i][1]*xx * np.cos(theta), c=colours[i], ls=":", lw=3)

        if options_flex[obj]["masses"] > 100:
            mass_label = "10^{:.0f}".format(
                np.log10(options_flex[obj]["masses"]))
        else:
            if options_flex[obj]["masses"] == 10:
                mass_label = "{:.0f}".format(options_flex[obj]["masses"])
            else:
                mass_label = "{:.1f}".format(options_flex[obj]["masses"])

        # rg = util.grav_radius(mass)
        if rmax == 3e5:
            label = r"{}, ${}~M_\odot$, $3\times10^5~r_g$".format(
                options_flex[obj]["wind_label"], mass_label, np.log10(rmax))
        else:
            label = r"{}, ${}~M_\odot$, $10^{:.0f}~r_g$".format(
                options_flex[obj]["wind_label"], mass_label, np.log10(rmax))
        bbox = dict(facecolor='w', edgecolor=colours[i], boxstyle='round')
        if i < 2:
            ax.text(0.5, 0.8, label,
                    c=colours[i], transform=ax.transAxes, fontsize=16, ha="center", bbox=bbox)
        else:
            ax.text(0.5, 0.2, label,
                    c=colours[i], transform=ax.transAxes, fontsize=16, ha="center", bbox=bbox)
    # plt.colorbar()
    return pcol


def plot_spectra(fig, gridspecs, roots, colours, options_flex, order):

    for i in range(len(roots)):
        obj = order[i]
        sightline = options_flex[obj]["sightlines"]

        specfile_suffix = "spec"
        if options_flex[obj]["plot_units"] == "fnu":
            specfile_suffix = "log_spec"
        s = io.read(
            "{}/{}.{}".format(options_flex[obj]["paths"], options_flex[obj]["roots"], specfile_suffix))
        ax = fig.add_subplot(gridspecs[i])
        # plt.subplot(4,2,sp[i]+1)
        if options_flex[obj]["spec_units"] == "fl" and options_flex[obj]["plot_units"] == "fnu":
            conv = s["Lambda"] / s["Freq."] * options_flex[obj]["renorm"]
        else:
            conv = options_flex[obj]["renorm"]

        if options_flex[obj]["plot_units"] == "fnu":
            xconv = HEV
            key = "Freq."
            xlabel = r"$E=h \nu$~(eV)"
            ylabel = r"$F_{\rm E}$"
        elif options_flex[obj]["plot_units"] == "fl":
            xconv = 1.0
            key = "Lambda"
            xlabel = r"$\lambda$~(\AA)"
            ylabel = r"$F_{\rm \lambda}$"

        ax.plot(xconv * s[key],  conv *
                s["A{:d}P0.50".format(sightline[0])], c=colours[i], lw=2)
        ax.plot(xconv * s[key],  conv *
                s["A{:d}P0.50".format(sightline[1])], c=colours[i], alpha=0.8, lw=2)
        if options_flex[obj]["plot_units"] == "fnu":
            ax.set_xscale("log")

        ax.text(options_flex[obj]["ilabel_x"], options_flex[obj]["ilabel_y"]
                [1], r"${}^\circ$".format(sightline[0]), c=colours[i], fontsize=14)
        ax.text(options_flex[obj]["ilabel_x"], options_flex[obj]["ilabel_y"][0], r"${}^\circ$".format(
            sightline[1]), c=colours[i], alpha=0.8, fontsize=14)

        ax.set_yscale("log")
        ax.set_ylabel(ylabel, labelpad=-2)

        if i > 1:
            ax.set_xlabel(xlabel, labelpad=-2)

        if i == 1 or i == 3:
            ax.yaxis.set_label_position("right")
            ax.yaxis.tick_right()
        ax.set_ylim(options_flex[obj]["ylims"][0],
                    options_flex[obj]["ylims"][1])
        ax.set_xlim(options_flex[obj]["wlims"][0],
                    options_flex[obj]["wlims"][1])
        bbox = dict(facecolor='w', edgecolor=colours[i], boxstyle='round')
        ax.text(0.05, 0.07, options_flex[obj]["spec_label"], c=colours[i],
                transform=ax.transAxes, fontsize=14, ha="left", bbox=bbox)


def make_figure(**savefig_kwargs):
    roots = ["run128", "cv_hhe", "XRB_fe", "tde_standard"]

    colours = ["C0", "C1", "C6", "C3"]

    #  initialise options -- probably should be doing this with **kwargs or something
    options = dict()
    options["sightlines"] = ((10, 55), (45, 80), (70, 80), (35, 75))
    options["signs"] = ((-1, 1), (1, 1), (-1, -1), (1, -1))
    options["rmax"] = (1e4, 1e6, 3e5, 1e4)
    options["masses"] = np.array([1e9, 0.8, 10.0, 1e6])
    # add spectra
    options["spec_units"] = ("fl", "fl", "fnu", "fl")
    options["plot_units"] = ("fl", "fl", "fnu", "fnu")
    options["wlims"] = ((1000, 6900), (1000, 1799), (800, 1e4), (1.5, 120))
    options["ylims"] = ((1e-2, 80), (1e-2, 10), (0.4, 40), (1e-2, 20))

    options["object"] = ("quasar", "cv", "xrb", "tde")
    options["wind_label"] = (r"Quasar", r"CV", r"XRB", r"TDE")
    options["spec_label"] = (r"Quasar, Optical-UV (§8.2)", r"CV, Optical-UV (§8.1)",
                             r"XRB, X-ray (§8.3)", r"TDE, Broad-band (§8.4)")
    options["ilabel_x"] = (5500, 1690, 1000, 2)
    options["ilabel_y"] = ((0.2, 2), (0.1, 1.5), (5, 23), (0.4, 4))
    options["paths"] = ["{}/Demos/quasar/".format(util.g_DataDir), "{}/Demos/cv/".format(
        util.g_DataDir), "{}/Demos/xrb/".format(util.g_DataDir), "{}/Demos/tde/".format(util.g_DataDir)]
    options["wind_paths"] = ["{}/Demos/quasar/".format(util.g_DataDir), "{}/Demos/cv/".format(
        util.g_DataDir), "{}/Demos/xrb/".format(util.g_DataDir), "{}/Demos/tde/".format(util.g_DataDir)]
    options["renorm"] = (1, 1e11, 1e24, 1e15)
    options["roots"] = roots

    # create a more flexible dictionary with all these options
    options_flex = dict()
    for i, obj in enumerate(options["object"]):
        options_flex[obj] = dict()
        for key in options.keys():
            if key != "object":
                options_flex[obj][key] = options[key][i]

    # set up figure and gridspec objects
    fig = plt.figure(figsize=(12, 6))
    gs_wind = plt.GridSpec(2, 4, hspace=0, top=0.99, wspace=0,
                           right=0.93, left=0.07, bottom=0.1)

    order = ("quasar", "xrb", "cv", "tde")
    # make the middle part of the figure
    pcol = plot_wind_panels(fig, gs_wind, (1, 2, 5, 6),
                            colours, options_flex, order=order)
    cax = plt.axes([0.285, 0.05, 0.25, 0.04])
    cbar = plt.colorbar(
        mappable=pcol, orientation="horizontal", cax=cax, extend="both")
    plt.text(
        0.55, 0.05, r"$\log [n_e~({\rm cm}^{-3})]$", transform=plt.gcf().transFigure)

    # add spectra
    options["spec_units"] = ("fl", "fnu", "fl", "fl")
    gs_spec = plt.GridSpec(2, 4, top=0.99, right=0.94, left=0.06,
                           bottom=0.1, wspace=0.1, hspace=0.14)

    gridspecs = (gs_spec[0], gs_spec[3], gs_spec[4], gs_spec[7])
    plot_spectra(fig, gridspecs, roots, colours, options_flex, order=order)

    # plt.subplots_adjust(wspace=0.1, right=0.95, left=0.05, top=0.99)
    util.save_paper_figure("demo.pdf", fig=fig,  **savefig_kwargs)


if __name__ == "__main__":
    util.set_plot_defaults()
    make_figure()
