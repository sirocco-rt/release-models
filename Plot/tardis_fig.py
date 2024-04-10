import sys, os
import numpy as np
import logging
import warnings
from numpy import exp
from astropy import units
import astropy.io.ascii as io
import matplotlib.pyplot as plt 
import util 

util.set_plot_defaults()


def make_figure(path="../Data/Tests/tardis/"):
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

	w, f = np.loadtxt("{}/tardis_python_spectrum.dat".format(path), unpack=True)

	# we have to correct fluxes to same distance by r**2 law
	PY2TAR = (100.0 ** 2) / (0.1e6 **2) 
	norm = 1000.0 # arbitrary normalisation factor 

	s = io.read("{}/1d_sn_87.spec".format(path))

	plt.figure(figsize=(6,4))
	# make new plot
	plt.plot(w, f / PY2TAR * norm, label= "Tardis", c="k")
	plt.plot(s["Lambda"], norm  * s["A45P0.50"], label= "{}".format(util.CODE_NAME), linewidth=2.5, alpha=1)
	plt.ylabel(r"$F_\lambda$ (Arb.)", fontsize=20)
	plt.legend(frameon=False, fontsize=20)
	plt.xlim(1000,11000)


	plt.xlabel(r"Wavelength (\AA)", fontsize=20)
	plt.tight_layout(pad=0.1)
	plt.savefig("Figures/tardis_comparison.pdf")


if __name__ == "__main__":
	make_figure()
