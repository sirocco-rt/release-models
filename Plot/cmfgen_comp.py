from astropy.table import Table
import matplotlib.pyplot as plt
import numpy as np
import util


def make_figure(path="{}/Tests/cmfgen/".format(util.g_DataDir), root="cmfgen_try", **savefig_kwargs):
    """Make CMFGEN ionization comparison

    Args:
        path (_type_, optional): path to folder. Defaults to "{}/Tests/cmfgen/".format(util.g_DataDir).
        root (str, optional): root file name to plot. Defaults to "a3_hhe".
    """

    h_frac = Table.read("{}/{}.H.frac.txt".format(path, root), format='ascii')
    he_frac = Table.read(
        "{}/{}.He.frac.txt".format(path, root), format='ascii')
    c_frac = Table.read("{}/{}.C.frac.txt".format(path, root), format='ascii')
    py_data = Table.read("{}/{}.master.txt".format(path, root), format='ascii')

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5, 5))

    r2, he2 = np.genfromtxt("{}/cmfgen_he2.txt".format(path), unpack=True)
    r3, he3 = np.genfromtxt("{}/cmfgen_he3.txt".format(path), unpack=True)

    ax.plot(r2, he2, linestyle='-', c="C0", alpha=0.7,
            lw=4, label=r"He~\textsc{ii}, \textsc{cmfgen}")
    ax.plot(r3, he3, linestyle='-', c="C1", alpha=0.7,
            lw=4, label=r"He~\textsc{ii}, \textsc{cmfgen}")
    ax.plot(he_frac["r"]/1.4e12, he_frac["i02"], "-o", c="C0",
            label=r"He~\textsc{{iii}}, {}".format(util.CODE_NAME))
    ax.plot(he_frac["r"]/1.4e12, he_frac["i03"], "-o", c="C1",
            label=r"He~\textsc{{iii}}, {}".format(util.CODE_NAME))
    ax.loglog()
    ax.set_ylim(1e-3, 1.5)
    ax.set_xlim(1, 50)
    ax.set_xlabel("$R/R_*$")
    ax.set_ylabel("Ion fraction")

    ax.legend(loc='lower left')
    fig.tight_layout(pad=0.1)
    util.save_paper_figure("cmfgen_ions.pdf", fig=fig, **savefig_kwargs)


if __name__ == "__main__":
    util.set_plot_defaults()
    util.set_ui_cycler("deep")
    make_figure(root="cmfgen_try")
