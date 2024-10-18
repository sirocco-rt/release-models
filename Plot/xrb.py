"""Create the XRB figure for the release paper."""

from io import StringIO
from astropy.io import ascii as io 
from matplotlib import gridspec
from matplotlib import pyplot as plt
import util
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
import numpy as np 
import roman
from mendeleev import element


line_data = """12 12.0 8.4246 1.4718820341618593 1 0
12 12.0 8.4192 1.4728260862077154 2 0
14 14.0 6.1858 2.0045939708687635 1 0
14 14.0 6.1804 2.006345444469613  2 0
26 25.0 1.8504 6.701263178231733  2 0
26 25.0 1.5732 7.882034951055174   1 1
26 26.0 1.7835 6.9526309980375665  2 0 
26 26.0 1.778 6.974138011811023  2  0
16 16.0 4.7328 2.620017195951656  1 0
16 16.0 4.7274 2.623009981173583  2 0
10 10.0 12.1375 1.0216286208032956 1 0
10 10.0 12.1321 1.022083347895253  2 0
26 24.0 10.663 1.1629013771921595  1 1
26 24.0 10.619 1.1677198780487803  2 1
14 14.0 5.218 2.3763927529704865  1 0
14 14.0 5.2168 2.3769393852553287  2 0
12 12.0 7.1069 1.7447856850384835  1 0
12 12.0 7.1058 1.7450557833037799  2 0"""

def make_figure(quasar_path = "{}/Demos/xrb/".format(util.g_DataDir)):
    
    #util.set_cmap_cycler(cmap_name="RdYlBu_r", N=6)
    util.set_ui_cycler("canada")
    PARSEC_TO_CM = 3.086e18
    HEV = 4.13620e-15

    spectrum_file = io.read("{}/XRB_fe.log_spec".format(quasar_path))

    # Create the overall figure, using gridspec to make the subplots
    fig = plt.figure(figsize=util.onespec_size)
    gs = gridspec.GridSpec(1, 1)

    # UV spectra
    ax1 = plt.subplot(gs[0])
    colors = ["C0", "C3", "C6"]
    conv = spectrum_file["Lambda"]/spectrum_file["Freq."]
    #print (spectrum_file.keys)
    for ii, i in enumerate((70,80)):
        x, y = HEV * spectrum_file["Freq."] / 1e3, 1e22*spectrum_file["Freq."]*conv*spectrum_file[f"A{i}P0.50"]
        
        ax1.plot(
            x,
            y,
            label=r"$i = {}^\circ$".format(i),
            lw = 2.5,
            c=colors[ii]
        )
    ax1.set_yscale("log")
    ax1.set_xscale("log")
    ax1.legend(loc="upper right", frameon=True, fontsize=16)
    ax1.set_xlim(0.97,9)
    ax1.set_ylim(1e-3,4)
    ticks = [1,2,3,4,5,6,7,8,9]
    ax1.set_xticks(ticks)
    ax1.set_xticklabels([str(t) for t in ticks])
    #ax1.set_ylim(1e-1,200)
    ax1.set_ylabel(r"$E~F_E$ (Arb.)", fontsize=util.onepanel_labelsize)
    ax1.set_xlabel(r"$E$ (keV)", fontsize=util.onepanel_labelsize, labelpad=-0.1)

    
    z,ion,w,e_line, id, offset = np.genfromtxt(StringIO(line_data), unpack=True)
    ax1.vlines(e_line, 6.1e-3,4, color="k", lw=1, ls="--", zorder=1, alpha=0.6)
    bbox = dict(facecolor='w', edgecolor="k", boxstyle='round,pad=0.12')
    for i in range(len(e_line)):
        #if e_line[i] > 0:
        ax1.axvline(e_line[i], color="k", lw=1, ls="--", zorder=1, alpha=0.4)
        if id[i] == 1:
            elem = element(int(z[i])).symbol
            ion_roman = roman.toRoman(int(ion[i])).lower()
            #print (elem, ion_roman)
            label = r"{}\textsc{{ {} }}".format(str(elem), ion_roman)
            ax1.text(e_line[i], 1.2e-3, label, rotation=90, fontsize=12, ha="center", va="bottom", bbox=bbox)
    ax1.text(6.8, 1.2e-3, r"Fe \textsc{xxv},\textsc{xxvi}", rotation=90, fontsize=12, ha="center", va="bottom", bbox=bbox)
    #ax1.vlines(e_line, 5e-3,3, ls="--", color="k", lw=1)

    # Add inset figure
    inset_ax = inset_axes(ax1, width="35%", height="30%", loc="lower left", borderpad=4)
    for ii, i in enumerate((70,80)):
        x, y = HEV * spectrum_file["Freq."] / 1e3, 1e22*spectrum_file["Freq."]*conv*spectrum_file[f"A{i}P0.50"]
        inset_ax.plot(
            x,
            y,
            lw = 2,
            c=colors[ii]
        )
    inset_ax.xaxis.tick_top()   
    inset_ax.set_yscale("log")
    inset_ax.set_xscale("log")
    inset_ax.set_xlim(6.6,7.1)
    inset_ax.set_ylim(0.02,0.1)
    inset_ax.set_xticks([], minor=True)
    inset_ax.set_xticks([6.6,6.8, 7])
    #inset_ax.set_yticks([0.01,0.02])
    inset_ax.set_yticklabels([])
    inset_ax.set_xticklabels(["6.6", "6.8", "7"])
    mark_inset(ax1, inset_ax, loc1=2, loc2=3, fc="none", ec="0.7")
    inset_ax.set_yticklabels([])
    #inset_ax.set_xticklabels(["6.5", "7"])

    # Clean up the figure
    #fig.tight_layout(pad=0.05)
    inset_ax.set_yticks([], minor=True)
    inset_ax.set_yticklabels([])
    plt.subplots_adjust(top=0.99, right=0.98, left=0.14, bottom=0.15)
    util.save_paper_figure("xrb_demo_model.pdf", fig=fig, dpi=300)

if __name__ == "__main__":
    util.set_plot_defaults()
    make_figure()
