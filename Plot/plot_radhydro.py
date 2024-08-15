#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
from astropy.io import ascii as io 
from astropy.table import Table
import util 
import numpy as np 
from lick import lick_box_plot
import util 
from scipy.interpolate import griddata
import cmasher as cma
# Interpolation function
def interpolate_data(data, colname, x_grid, y_grid):
    x = data["x"]
    y = data["y"]
    interp_data = griddata((x, y), data[colname], (x_grid, y_grid))
    return interp_data

def make_figure(cv_model = "00001743.pluto", xdir="{}/Demos/rad-hydro/".format(util.g_DataDir)):
    '''
    Plot the UV and visible spectra of various CV models
    '''
    util.set_cmap_cycler("viridis", N=4)
    plt.rcParams["lines.linewidth"] = 1.5
    data = io.read("{}/{}".format(xdir, cv_model))
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10,5))  # 1 rows, 2 columns

    shape = (np.max(data["ir"])+1,np.max(data["itheta"])+1)
    d = Table()
    for key in data.keys():
        d[key] = np.reshape(data[key], shape)
    theta = np.radians(d["theta"])
    theta2 = np.radians(data["theta"])
    x = d["x"] = d["r"] * np.sin(theta)
    y = d["y"] = d["r"] * np.cos(theta)
    data["x"] = data["r"]* np.sin(theta2)
    data["y"] = data["r"]* np.cos(theta2)
    rmin = np.min(d["r"])

    data_interp = dict()
    data_interp["x"] = np.linspace(x.min(), x.max(), 100)
    data_interp["y"] = np.linspace(y.min(), y.max(), 100)
    data_interp["xx"], data_interp["yy"] = np.meshgrid(data_interp["x"], data_interp["y"])
    data_interp["rr"] = np.sqrt(data_interp["xx"]**2 + data_interp["yy"]**2)
    select_mask = (data_interp["rr"]<rmin)
    for key in d.keys():
        if key not in ["x","y"]:
            data_interp[key] = np.array(interpolate_data(data, key, data_interp["xx"], data_interp["yy"]))
            data_interp[key][select_mask] = 0.0
            data_interp[key][np.isnan(data_interp[key])] = 0.0
    print (data_interp["v_x"])
    c_s = np.sqrt(40) * 10.0 * 1e5
    mach = np.sqrt(d["v_x"]**2 + d["v_y"]**2) / c_s
    print (mach)
    

    #density = 
    
    ax[0].pcolormesh(x, y, np.log10(d["density"]), lw=0, rasterized=True, shading="gouraud", cmap=cma.cosmic)
    ax[0].pcolormesh(-x, -y, np.log10(d["density"]), lw=0, rasterized=True, shading="gouraud", cmap=cma.cosmic)
    ax[0].pcolormesh(-x, y, np.log10(d["density"]), lw=0, rasterized=True, shading="gouraud", cmap=cma.cosmic)
    ax[0].pcolormesh(x, -y, np.log10(d["density"]), lw=0, rasterized=True, shading="gouraud", cmap=cma.cosmic)

    #ax[0].streamplot(x_grid[0], y_grid.T[0],v_x, v_y, color=None)
    #ax[0].streamplot(data_interp["x"], data_interp["y"],data_interp["v_x"], data_interp["v_y"])
    #ax[0].quiver(data_interp["x"], data_interp["y"],data_interp["v_x"], data_interp["v_y"])
    #ax[0].contour(y.T,x.T,mach.T, levels=(1,))

    ax[0].set_xlim(-8.5e9,8.5e9)
    ax[0].set_ylim(-8.5e9,8.5e9)
    ax[0].set_xlabel(r"$r_{\rm cyl}$~(cm)")
    ax[0].set_ylabel("$z$~(cm)")
    ax[0].text(0,6e9,"CV Line-driven wind",ha="center",color="w")

    #ax[1].scatter(x, y)
    #ax[0].pcolormesh(x_grid, y_grid, np.log10(v_x))
    #jm_util.get_aspect()

    field = data_interp["v_x"] ** 2 + data_interp["v_y"] ** 2
    # lick_box_plot(
    #     fig,
    #     ax[1],
    #     data_interp["x"],
    #     data_interp["y"],
    #     data_interp["v_x"],
    #     data_interp["v_y"],
    #     np.log10(data_interp["density"]),
    #     size_interpolated=256,
    #     niter_lic=5,
    #     kernel_length=64,
    #     cmap="viridis",
    #     stream_density=1
    # )

    data_xrb = io.read("{}/soft_higg_xrb.dat".format(xdir))
    shape = (100, 220)
    shape2 = (220,100)
    data_xrb["x"] = data_xrb["r"] * np.sin(data_xrb["theta"])
    data_xrb["z"] = data_xrb["r"] * np.cos(data_xrb["theta"])
    plt.scatter(data_xrb["x"], data_xrb["z"])
    plt.pcolormesh(data_xrb["x"].reshape(shape), data_xrb["z"].reshape(shape), np.log10(data_xrb["rho"].reshape(shape2).T), shading="gouraud", cmap="jet")

    #ax[1].set_xlim(0,8.5e9)
    #ax[1].set_ylim(0,8.5e9)
    ax[1].set_xlabel(r"$r_{\rm cyl}$~(cm)")
    ax[1].text(4e9,7.5e9,"XRB Thermal wind")
    plt.tight_layout(pad=0.05)
    print (util.get_aspect(ax[0]))
    util.save_paper_figure('rad-hydro.pdf')


# Next lines permit one to run the routine from the command line
if __name__ == "__main__":
    util.set_plot_defaults()
    make_figure(xdir="{}/Demos/rad-hydro/".format(util.g_DataDir))


