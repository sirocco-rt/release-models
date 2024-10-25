import sys
import os
import numpy as np
import logging
import warnings
from numpy import exp
from astropy import units, constants
import astropy.io.ascii as io
import matplotlib.pyplot as plt
import util


def make_figure(path="{}/Tests/tardis/".format(util.g_DataDir), **savefig_kwargs):
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
    util.set_cmap_cycler("default")
    w, f = np.loadtxt(
        "{}/tardis_python_spectrum.dat".format(path), unpack=True)
    # tardis_data = io.read("{}/tardis_snr.txt".format(path))
    # w = constants.c.cgs.value / tardis_data["nu"] * 1e8
    # f = tardis_data["nuLnu"] / w / (4.0 * np.pi * 0.1e6 * 0.1e6 * constants.pc.cgs.value * constants.pc.cgs.value)

    # we have to correct fluxes to same distance by r**2 law
    PY2TAR = (100.0 ** 2) / (0.1e6 ** 2)
    norm = 1000.0  # arbitrary normalisation factor

    s = io.read("{}/1d_sn_87.spec".format(path))

    plt.figure(figsize=util.onespec_size)
    # make new plot
    plt.plot(w, f / PY2TAR * norm, label="Tardis", c="k")
    plt.plot(s["Lambda"], norm * s["A45P0.50"],
             label="{}".format(util.CODE_NAME), linewidth=2.5, alpha=1)
    plt.ylabel(r"$F_\lambda$ (Arb.)", fontsize=util.onepanel_labelsize)
    plt.legend(frameon=False, fontsize=util.onepanel_labelsize)
    plt.xlim(1000, 11000)

    plt.xlabel(util.wavelength_label, fontsize=util.onepanel_labelsize)
    plt.tight_layout(pad=0.1)
    util.save_paper_figure("tardis_comparison.pdf", **savefig_kwargs)


if __name__ == "__main__":
    util.set_plot_defaults()
    make_figure()
