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
CODE_NAME = "Python"
onespec_size = (6,4) # size for one panel spectrum figure 
onepanel_labelsize = 20 # fontsize for labels in one panel spectrum figure 
wavelength_label = r"$\lambda$ (\AA)"
nu_label = r"$\nu (Hz)$"
g_DataDir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'Data'))
g_FigureDir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'Figures'))

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