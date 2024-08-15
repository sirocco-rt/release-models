"""Create the TDE figure for the release paper."""

import math

from astropy.io import ascii
from matplotlib import gridspec
from matplotlib import pyplot as plt
import util 

def make_figure(tde_path = "{}/Demos/tde".format(util.g_DataDir)):
    
    util.set_ui_cycler("colorblind")
    PARSEC_TO_CM = 3.086e18

    # A10P0.50   A35P0.50   A60P0.50   A75P0.50   A85P0.50
    spectrum_file = ascii.read("{}/tde_standard.log_spec".format(tde_path))
    optical_depth_spectrum = ascii.read("{}/tde_standard.spec_tau".format(tde_path))

    # Convert from flux to luminosity
    for col in ("Created", "Emitted", "A10P0.50", "A60P0.50", "A75P0.50"):
        spectrum_file[col] *= 4 * math.pi * (100 * PARSEC_TO_CM) ** 2
        spectrum_file[col] = spectrum_file[col] * spectrum_file["Lambda"]

    # Create the overall figure, using gridspec to make the subplots
    fig = plt.figure(figsize=(12, 6))
    gs = gridspec.GridSpec(2, 2, width_ratios=[1, 1], height_ratios=[1, 1])

    # UV spectra
    ax1 = plt.subplot(gs[0, 0])
    ax1.set_xlim(1000, 2999)
    for i in (10, 60, 75):
        x, y = util.get_flux_range(
            spectrum_file["Lambda"], util.smooth(spectrum_file[f"A{i}P0.50"]), 1000, 3000
        )
        ax1.plot(
            x,
            y,
            label=f"$i = {i}^\circ$",
            lw=2.5,
        )
    ax1.set_yscale("log")
    ax1.legend(loc="upper right")
    ax1.set_ylabel(r"$\nu~L_\nu$ [erg s$^{-1}$]", fontsize=util.onepanel_labelsize)
    ax1.text(0.05, 0.1, "UV", transform=ax1.transAxes, fontsize=16, ha="left")

    # Optical spectra
    ax2 = plt.subplot(gs[1, 0])
    ax2.set_xlim(4000, 7999)
    for i in (10, 60, 75):
        x, y = util.get_flux_range(
            spectrum_file["Lambda"], util.smooth(spectrum_file[f"A{i}P0.50"]), 4000, 8000
        )
        ax2.plot(
            x,
            y,
            lw=2.5
        )
    ax2.set_yscale("log")
    ax2.set_ylabel(r"$\nu~L_\nu$ [erg s$^{-1}$]", fontsize=util.onepanel_labelsize)
    ax2.set_xlabel(util.wavelength_label, fontsize=util.onepanel_labelsize)
    ax2.text(0.05, 0.1, "Optical", transform=ax2.transAxes, fontsize=16, ha="left")
    # Reprocessing
    ax3 = plt.subplot(gs[:, 1])
    ax3_twin = ax3.twinx()
    # emitted vs. created
    ax3.plot(spectrum_file["Freq."], util.smooth(spectrum_file["Emitted"]), label="Emergent", lw=2.5)
    ax3.plot(spectrum_file["Freq."], util.smooth(spectrum_file["Created"]), label="Disc Input", lw=2.5)
    # optical depth
    for col, i in enumerate((35, 60, 75, 85)):
        ax3_twin.plot(
            optical_depth_spectrum["Freq."],
            optical_depth_spectrum[f"A{i}P0.50"],
            label=f"$i = {i}^\circ$",
            color=f"C{col + 2}",
            lw=2.5
        )
    ax3.set_ylabel(r"$\nu L_\nu$ [erg s$^{-1}$]", fontsize=util.onepanel_labelsize)
    ax3.set_xlabel(util.nu_label, fontsize=util.onepanel_labelsize)
    ax3.set_xscale("log")
    ax3.set_yscale("log")
    ax3.set_xlim(3e14,3e16)
    ax3_twin.set_yscale("log")
    ax3_twin.legend(loc="lower right")
    ax3.legend()
    ax3_twin.set_ylabel(r"Continuum optical depth $\tau$", fontsize=util.onepanel_labelsize)
    ax3.text(0.05, 0.1, "Global Reprocessing", transform=ax3.transAxes, fontsize=16, ha="left")
    # Clean up the figure
    fig.tight_layout(pad=0.05)
    util.save_paper_figure("tde_demo_model.pdf", fig=fig, dpi=300)
    #plt.show()

if __name__ == "__main__":
    util.set_plot_defaults()
    make_figure()
