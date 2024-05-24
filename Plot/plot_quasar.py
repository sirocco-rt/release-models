"""Create the TDE figure for the release paper."""

import math

from astropy.io import ascii
from matplotlib import gridspec
from matplotlib import pyplot as plt
import util

def make_figure(quasar_path = "../Data/Demos/quasar"):
    
    util.set_plot_defaults()
    util.set_cmap_cycler(cmap_name="RdYlBu_r", N=6)

    PARSEC_TO_CM = 3.086e18

    spectrum_file = ascii.read("{}/run128.spec".format(quasar_path))

    # Convert from flux to luminosity
    #for col in ("A10P0.50", "A50P0.50", "A55P0.50"):
    #    spectrum_file[col] = spectrum_file[col] * spectrum_file["Lambda"]

    # Create the overall figure, using gridspec to make the subplots
    fig = plt.figure(figsize=util.onespec_size)
    gs = gridspec.GridSpec(1, 1)

    # UV spectra
    ax1 = plt.subplot(gs[0])
    ax1.set_xlim(100, 3000)
    colors = ["C0", "C1", "C5"]
    for ii, i in enumerate((10, 50, 55)):
        x, y = spectrum_file["Lambda"], util.smooth(spectrum_file[f"A{i}P0.50"])
        ax1.plot(
            x,
            y,
            label=f"$i = {i}^\circ$",
            lw = 2.5,
            c=colors[ii]
        )
    ax1.set_yscale("log")
    ax1.legend(loc="upper right", frameon=False, fontsize=16)
    ax1.set_xlim(850,2000)
    ax1.set_ylim(1e-1,200)
    ax1.set_ylabel(r"$F_\lambda$ (Arb.)", fontsize=util.onepanel_labelsize)
    ax1.set_xlabel(r"$\lambda$ (\AA)", fontsize=util.onepanel_labelsize)

    # Broadband spectra (TBC)
    # ax2 = plt.subplot(gs[1])
    # ax2.set_xlim(1e14,1e20)
    # for i in (10, 50, 55): 
    #     x, y = spectrum_file["Freq."], smooth(spectrum_file["Lambda"]*spectrum_file[f"A{i}P0.50"])
    #     ax1.plot(
    #         x,
    #         y,
    #         label=f"$i = {i}^\circ$",
    #     )
    # ax2.set_yscale("log")
    # ax2.set_xscale("log")
    # ax2.set_ylabel(r"$\nu~L_\nu$ [erg s$^{-1}$]")
    # ax2.set_xlabel(r"$\nu$~(Hz)")

    # Clean up the figure
    fig.tight_layout(pad=0.05)
    fig.savefig("Figures/quasar_demo_model.pdf", dpi=300)
    #plt.show()

if __name__ == "__main__":
    make_figure()
