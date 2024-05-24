"""Create the TDE figure for the release paper."""

import math

from astropy.io import ascii
from matplotlib import gridspec
from matplotlib import pyplot as plt
from util import get_flux_range, smooth

PARSEC_TO_CM = 3.086e18

# A10P0.50   A35P0.50   A60P0.50   A75P0.50   A85P0.50
spectrum_file = ascii.read("python/Results/tde_standard.log_spec")
optical_depth_spectrum = ascii.read("python/Results/tde_standard.spec_tau")

# Convert from flux to luminosity
for col in ("Created", "Emitted", "A10P0.50", "A60P0.50", "A75P0.50"):
    spectrum_file[col] *= 4 * math.pi * (100 * PARSEC_TO_CM) ** 2
    spectrum_file[col] = spectrum_file[col] * spectrum_file["Lambda"]

# Create the overall figure, using gridspec to make the subplots
fig = plt.figure(figsize=(12, 6))
gs = gridspec.GridSpec(2, 2, width_ratios=[1, 1], height_ratios=[1, 1])

# UV spectra
ax1 = plt.subplot(gs[0, 0])
ax1.set_xlim(900, 3100)
for i in (10, 60, 75):
    x, y = get_flux_range(
        spectrum_file["Lambda"], smooth(spectrum_file[f"A{i}P0.50"]), 1000, 3000
    )
    ax1.plot(
        x,
        y,
        label=f"$i = {i}^\circ$",
    )
ax1.set_yscale("log")
ax1.legend(loc="upper right")
ax1.set_ylabel(r"$\nu~L_\nu$ [erg s$^{-1}$]")

# Optical spectra
ax2 = plt.subplot(gs[1, 0])
ax2.set_xlim(3900, 8100)
for i in (10, 60, 75):
    x, y = get_flux_range(
        spectrum_file["Lambda"], smooth(spectrum_file[f"A{i}P0.50"]), 4000, 8000
    )
    ax2.plot(
        x,
        y,
    )
ax2.set_yscale("log")
ax2.set_ylabel(r"$\nu~L_\nu$ [erg s$^{-1}$]")
ax2.set_xlabel("Restframe Wavelength [$\AA$]")

# Reprocessing
ax3 = plt.subplot(gs[:, 1])
ax3_twin = ax3.twinx()
# emitted vs. created
ax3.plot(spectrum_file["Freq."], smooth(spectrum_file["Emitted"]), label="Emergent")
ax3.plot(spectrum_file["Freq."], smooth(spectrum_file["Created"]), label="Disk")
# optical depth
for col, i in enumerate((35, 60, 75, 85)):
    ax3_twin.plot(
        optical_depth_spectrum["Freq."],
        optical_depth_spectrum[f"A{i}P0.50"],
        label=f"$i = {i}^\circ$",
        color=f"C{col + 2}",
    )
ax3.set_ylabel(r"$\nu~L_\nu$ [erg s$^{-1}$]")
ax3.set_xlabel("Restframe Frequency [Hz]")
ax3.set_xscale("log")
ax3.set_yscale("log")
ax3_twin.set_yscale("log")
ax3_twin.legend(loc="upper left")
ax3_twin.set_ylabel("Continuum optical depth $\tau$")

# Clean up the figure
fig.tight_layout()
fig.savefig("tde_standard.png", dpi=300)
plt.show()
