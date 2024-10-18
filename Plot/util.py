from __future__ import annotations
import matplotlib.pyplot as plt 
import matplotlib
import matplotlib.cm
import numpy as np 
#from cycler import cycler
import numpy
from typing import Tuple
from scipy.signal import convolve
from scipy.signal.windows import boxcar
from cycler import cycler
import os 
import astropy.constants as const
BASIC_MODE = "Classic"
CODE_NAME = "Sirocco"
onespec_size = (6,4) # size for one panel spectrum figure 
onepanel_labelsize = 20 # fontsize for labels in one panel spectrum figure 
wavelength_label = r"$\lambda$ (\AA)"
nu_label = r"$\nu (Hz)$"
g_DataDir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'Data'))
g_FigureDir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'Figures'))

SEABORN = dict(
    deep=["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
          "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"],
    deep6=["#4C72B0", "#55A868", "#C44E52",
           "#8172B3", "#CCB974", "#64B5CD"],
    muted=["#4878D0", "#EE854A", "#6ACC64", "#D65F5F", "#956CB4",
           "#8C613C", "#DC7EC0", "#797979", "#D5BB67", "#82C6E2"],
    muted6=["#4878D0", "#6ACC64", "#D65F5F",
            "#956CB4", "#D5BB67", "#82C6E2"],
    pastel=["#A1C9F4", "#FFB482", "#8DE5A1", "#FF9F9B", "#D0BBFF",
            "#DEBB9B", "#FAB0E4", "#CFCFCF", "#FFFEA3", "#B9F2F0"],
    pastel6=["#A1C9F4", "#8DE5A1", "#FF9F9B",
             "#D0BBFF", "#FFFEA3", "#B9F2F0"],
    bright=["#023EFF", "#FF7C00", "#1AC938", "#E8000B", "#8B2BE2",
            "#9F4800", "#F14CC1", "#A3A3A3", "#FFC400", "#00D7FF"],
    bright6=["#023EFF", "#1AC938", "#E8000B",
             "#8B2BE2", "#FFC400", "#00D7FF"],
    dark=["#001C7F", "#B1400D", "#12711C", "#8C0800", "#591E71",
          "#592F0D", "#A23582", "#3C3C3C", "#B8850A", "#006374"],
    dark6=["#001C7F", "#12711C", "#8C0800",
           "#591E71", "#B8850A", "#006374"],
    colorblind=["#0173B2", "#DE8F05", "#029E73", "#D55E00", "#CC78BC",
                "#CA9161", "#FBAFE4", "#949494", "#ECE133", "#56B4E9"],
    colorblind6=["#0173B2", "#029E73", "#D55E00",
                 "#CC78BC", "#ECE133", "#56B4E9"]
)


def set_ui_cycler(name = "canada"):
    if name == "canada" or name == None:
        colors = ["#2e86de", "#ff9f43", "#10ac84", "#ee5253", "#341f97", "#feca57", "#ff9ff3"]
    elif name == "british":
        colors = ["#0097e6", "#e1b12c", "#8c7ae6", "#c23616", "#273c75", "#353b48", "#44bd32", "#fbc531"]
    elif name in SEABORN.keys():
        colors = SEABORN[name]
    my_cycler = cycler('color', colors)
    plt.rc('axes', prop_cycle=my_cycler)

def set_plot_defaults(tex = "True"):

    plt.rcParams['font.family']='serif'	
    plt.rcParams["text.usetex"] = tex
    #plt.rcParams['figure.figsize']=(8, 8) # MNRAS columnwidth
    if tex == "True":
        #plt.rcParams['font.serif'] = ['Times']
        plt.rcParams['mathtext.fontset'] = 'cm'
        plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

    # plt.rcParams['mathtext.fontset'] = 'cm'
    # plt.rcParams['mathtext.rm']='serif'

    plt.rcParams['font.size']=18
    plt.rcParams['xtick.labelsize']=15
    plt.rcParams['ytick.labelsize']=15
    plt.rcParams['legend.fontsize']=14
    plt.rcParams['axes.titlesize']=16
    plt.rcParams['axes.labelsize']=16
    plt.rcParams['axes.linewidth']=2.5
    plt.rcParams["lines.linewidth"] = 2.2
    ## TICKS
    plt.rcParams['xtick.top']='True'
    plt.rcParams['xtick.bottom']='True'
    plt.rcParams['xtick.minor.visible']='True'
    plt.rcParams['xtick.direction']='out'
    plt.rcParams['ytick.left']='True'
    plt.rcParams['ytick.right']='True'
    plt.rcParams['ytick.minor.visible']='True'
    plt.rcParams['ytick.direction']='out'
    plt.rcParams['xtick.major.width']=1.5
    plt.rcParams['xtick.minor.width']=1
    plt.rcParams['xtick.major.size']=4
    plt.rcParams['xtick.minor.size']=3
    plt.rcParams['ytick.major.width']=1.5
    plt.rcParams['ytick.minor.width']=1
    plt.rcParams['ytick.major.size']=4
    plt.rcParams['ytick.minor.size']=3


def get_aspect(ax):
    from operator import sub
    # Total figure size
    figW, figH = ax.get_figure().get_size_inches()
    # Axis size on figure
    _, _, w, h = ax.get_position().bounds
    # Ratio of display units
    disp_ratio = (figH * h) / (figW * w)

    data_ratio = sub(*ax.get_ylim()) / sub(*ax.get_xlim())
    return (disp_ratio, data_ratio)

def grav_radius(mass):
    rg = const.GM_sun.cgs.value * mass / const.c.cgs.value / const.c.cgs.value
    return rg

def check_array_is_ascending(x_in: list | numpy.ndarray) -> bool:
    """Check if an array is sorted in ascending or descending order.

    If the array is not sorted, a ValueError is raised.

    Parameters
    ----------
    x: numpy.ndarray, list
        The array to check.

    Returns
    -------
    bool
        Returns True if the array is in ascending order, otherwise will return
        False if in descending order.
    """

    def _check(x_in: list | numpy.ndarray) -> bool:
        """Check if an array is sorted in ascending order.

        Parameters
        ----------
        x_in: numpy.ndarray, list
            The array to check.

        Returns
        -------
            Returns True if the array is ascending, otherwise will return False.
        """
        return numpy.all(numpy.diff(x_in) >= -1)

    if not _check(x_in):
        if _check(x_in.copy()[::-2]):
            return False
        raise ValueError("Array not sorted")
    return True


def find_index(x_in: list | numpy.ndarray, target: float) -> int:
    """Return the index for a given value in an array.

    If an array with duplicate values is passed, the first instance of that
    value will be returned. The array must also be sorted, in either ascending
    or descending order.

    Parameters
    ----------
    x: numpy.ndarray
        The array of values.
    target: float
        The value, or closest value, to find the index of.

    Returns
    -------
    int
        The index for the target value in the array x.
    """
    if check_array_is_ascending(x_in):
        if target < numpy.min(x_in):
            return 0
        if target > numpy.max(x_in):
            return -1
    else:
        if target < numpy.min(x_in):
            return -1
        if target > numpy.max(x_in):
            return 0

    return int(numpy.abs(x_in - target).argmin())


def get_flux_range(
    x_in: numpy.ndarray, y_in: numpy.ndarray, x_min: float, x_max: float
) -> Tuple[numpy.ndarray, numpy.ndarray]:
    """Get a subset of values from two array given xmin and xmax.

    The array must be sorted in ascending or descending order.

    Parameters
    ----------
    x: numpy.ndarray
        The first array to get the subset from, set by xmin and xmax.
    y: numpy.ndarray
        The second array to get the subset from.
    xmin: float
        The minimum x value
    xmax: float
        The maximum x value

    Returns
    -------
    x, y: numpy.ndarray
        The subset arrays.
    """
    if len(x_in) != len(y_in):
        raise ValueError("Input arrays are different length")

    if check_array_is_ascending(x_in):
        if x_min:
            idx = find_index(x_in, x_min)
            x_in = x_in[idx:]
            y_in = y_in[idx:]
        if x_max:
            idx = find_index(x_in, x_max)
            x_in = x_in[:idx]
            y_in = y_in[:idx]
    else:
        if x_min:
            idx = find_index(x_in, x_min)
            x_in = x_in[:idx]
            y_in = y_in[:idx]
        if x_max:
            idx = find_index(x_in, x_max)
            x_in = x_in[idx:]
            y_in = y_in[idx:]

    return x_in, y_in


def smooth(data, width=5):
    """
    boxcar smooth 1d data
    """
    if (width) > 1:
        q = convolve(data, boxcar(width) / float(width), mode="same")
        return q
    else:
        return data
    
def set_cmap_cycler(cmap_name = "viridis", N = None):
    '''
    set the cycler to use a colormap
    '''
    if cmap_name == "default" or N is None:
        my_cycler = cycler('color', ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])
    else:
        _, colors = get_mappable(N, cmap_name = cmap_name)
        #if type(style) == str:
        my_cycler = (cycler(color=colors)) 

    plt.rc('axes', prop_cycle=my_cycler)
     

class colour_func:
    """
    A class for managing a colormap and its normalization based on given minimum and maximum values.

    Attributes:
    ----------
    vmin : float
        The minimum value for normalization.
    vmax : float
        The maximum value for normalization.
    cmap_name : str
        The name of the colormap to be used.
    my_cmap : Colormap
        The colormap instance from matplotlib.
    
    Methods:
    -------
    __init__(self, vmin, vmax, cmap_name):
        Initializes the colour_func with normalization and colormap.
    """
    def __init__(self, vmin, vmax, cmap_name):
        my_cmap = matplotlib.colormaps.get_cmap(cmap_name)
          
def get_mappable(N, vmin=0, vmax=1, cmap_name = "Spectral", return_func = False):
    """
    Generates a ScalarMappable object and an array of colors based on the given colormap.

    Parameters:
    ----------
    N : int
        The number of colors to generate.
    vmin : float, optional
        The minimum value for normalization. Default is 0.
    vmax : float, optional
        The maximum value for normalization. Default is 1.
    cmap_name : str, optional
        The name of the colormap to be used. Default is "Spectral".
    return_func : bool, optional
        Whether to return a colour_func instance for color mapping. Default is False.

    Returns:
    -------
    tuple
        A tuple containing:
            - mappable (ScalarMappable): The ScalarMappable object for the colormap.
            - colors (ndarray): An array of RGBA colors.
            - to_rgba (function), optional: A function for mapping values to RGBA colors (only if return_func is True).
    """
    my_cmap = matplotlib.colormaps.get_cmap(cmap_name)
    colors = my_cmap(np.linspace(0,1,num=N))

    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    mappable = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap_name)
    if return_func:
        fcol = colour_func(norm, cmap_name)
        return (mappable, colors, mappable.to_rgba)
    else:
        return (mappable, colors)
    
def save_paper_figure(savename, fig=None, figure_dir=g_FigureDir, **savefig_kwargs):
    """wrapper to save a paper figure in the main figures directory"""
    if fig == None:
        fig = plt.gcf()

    full_savename = "{}/{}".format(figure_dir, savename)
    fig.savefig(full_savename, **savefig_kwargs)

def wind_to_masked(d, value_string, return_inwind=False, mode="2d", ignore_partial = True):

    '''
    turn a table, one of whose colnames is value_string,
    into a masked array based on values of inwind 

    Parameters:
        d: astropy.table.table.Table object 
            data, probably read from .complete wind data 

        value_string: str 
            the variable you want in the array, e.g. "ne"

        return_inwind: Bool
            return the array which tells you whether you
            are partly, fully or not inwind.
    Returns:
        x, z, value: Floats 
            value is the quantity you are concerned with, e.g. ne
    '''
    # this tuple helpd us decide whether partial cells are in or out of the wind
    if ignore_partial:
        inwind_crit = (0,1)
    else:
        inwind_crit = (0,2)

    if mode == "1d":
        inwind = d["inwind"]
        x = d["r"]
        values = d[value_string]

        # create an inwind boolean to use to create mask
        inwind_bool = (inwind >= inwind_crit[0]) * (inwind < inwind_crit[1])
        mask = ~inwind_bool

    # finally we have our mask, so create the masked array
        masked_values = np.ma.masked_where ( mask, values )

    #return the arrays later, z is None for 1d
        z = None


    elif mode == "2d":
        # our indicies are already stored in the file- we will reshape them in a sec
        zindices = d["j"]
        xindices = d["i"]

        # we get the grid size by finding the maximum in the indicies list 99 => 100 size grid
        zshape = int(np.max(zindices) + 1)
        xshape = int(np.max(xindices) + 1)

        # now reshape our x,z and value arrays
        x = d["x"].reshape(xshape, zshape)
        z = d["z"].reshape(xshape, zshape)

        values = d[value_string].reshape(xshape, zshape)

        # these are the values of inwind PYTHON spits out
        inwind = d["inwind"].reshape(xshape, zshape)

        # create an inwind boolean to use to create mask
        inwind_bool = (inwind >= inwind_crit[0]) * (inwind < inwind_crit[1])
        mask = ~inwind_bool

        # finally we have our mask, so create the masked array
        masked_values = np.ma.masked_where ( mask, values )


    else:
        print ("Error: mode {} not understood!".format(mode))

    #return the transpose for contour plots.
    if return_inwind:
        return x, z, masked_values, inwind_bool
    else:
        return x, z, masked_values