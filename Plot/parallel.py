"""Create a figure showing the parallel scaling of Python.

The data used is for the M16 AGN model, using the matrix transition mode for
macro atoms.
"""

import matplotlib.pyplot as plt
import numpy
import util

# This is a dictionary containing the run time for the (same) ionisation cycle
# for a given number of MPI tasks. The keys of the dictionary are the number of
# MPI tasks, and the values are the run time in seconds.
agn_ntask_sec = {
    "1": 6734.799999999999,
    "2": 3363.3,
    "4": 1692.1999999999998,
    "8": 849.0,
    "16": 448.0,
    "32": 191.39999999999998,
    "40": 158.10000000000002,
    "80": 84.29999999999995,
    "120": 58.19999999999999,
    "160": 46.69999999999999,
    "200": 39.0,
    "240": 34.30000000000001,
    "280": 30.80000000000001,
    "320": 27.5,
}


def make_figure(**savefig_kwargs):
    """Plot the parallel scaling for a set of models.

    Parameters
    ----------
    models : list
        A list of list of models.
    labels:
        A list containing the names of each model list.
    """
    fig, ax = plt.subplots(figsize=(5, 4))

    ntasks = numpy.array([int(k) for k in agn_ntask_sec.keys()])
    time = numpy.array([v for v in agn_ntask_sec.values()])

    ax.plot(ntasks, ntasks, "-", label="Ideal", zorder=0)
    ax.plot(ntasks, agn_ntask_sec["1"] / time, "o-", label="Actual")

    ax.set_xlabel(r"$N_{p}$")
    ax.set_ylabel(r"$T_{1}~/~T_{N_{p}}$")
    ax.legend()
    fig.tight_layout()
    util.save_paper_figure("m16_agn_scaling.pdf",
                           fig=fig, dpi=300, **savefig_kwargs)


if __name__ == "__main__":
    util.set_plot_defaults()
    make_figure()
