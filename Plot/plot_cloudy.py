
import numpy as np
import astropy.io.ascii as ascii
import matplotlib.pyplot as plt 
import util 
import roman

def read_cloudy(filename='cl_helium_PL.dat'):
    xfile='%s' % (filename)
    try:
        x=ascii.read(xfile)
    except:
        print('Error: Could not find %s' % xfile)
        return None
    # x.info()
    names=x.colnames
    x.rename_column('col1','ip')
    j=1
    while j<len(names):
        x.rename_column(names[j],'i%02d' % (j))
        j+=1
    return x

def plot_one(ax=None, cloudy='cl_helium_PL.dat',python='py_he',element='He',imin=0,imax=0,ipmin=-8,ipmax=4,outname=''):
    print('Comparing: ',cloudy,python)
    pfile='%s' % (python)
    try:
        xp=ascii.read(pfile)
    except:
        print('Error: Could not read %s' % pfile)
        return None


    if ax == None:
        fig, ax = plt.subplots()

    xc=read_cloudy(cloudy)
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    colname=xc.colnames
    if imin<=0:
        i=1
    else:
        i=imin

    if imax<=0 or imax+1>len(colname):
        imax=len(colname)
    else:
        imax=imax+1
    color_index=0
    while i<imax:
        xlabel='%s %s' % (element,roman.toRoman(i))
        ax.semilogy(xc['ip'],xc[colname[i]],'-',lw=3, alpha=0.5,color=color_cycle[color_index])
        ax.semilogy(np.log10(xp['ip']),xp[colname[i]],"--",color=color_cycle[color_index],label=xlabel)
        i+=1
        color_index+=1
        if color_index==len(color_cycle):
            color_index=0


    ax.set_ylim(1e-4,1.2)
    if ipmin!=0 or ipmax!=0:
        ax.set_xlim(ipmin,ipmax)
    plt.tight_layout()

def get_chi(ion, python=True, cl = None, python_dir = "./"):
    if python:
        py_fname = '{}/py_{}_pl.txt'.format(python_dir,ion)
        xp=np.genfromtxt(py_fname, unpack=True, skip_header=2) 
        xp2=ascii.read(py_fname) 
        ion_densities = xp[6:]
        #print (ion_densities)
        states = np.arange(1,len(ion_densities)+1,1) 
        xx = (np.sum(states * ion_densities.T, axis=1)-1) / (len(ion_densities)-1)
        return (np.log10(xp2["ip"]),  xx)
    
    else:
        xc=np.genfromtxt(cl[ion], unpack=True, skip_header=2) 
        cion_densities = xc[1:]
        states = np.arange(1,len(cion_densities)+1,1) 
        xcip = xc[0]
        cxx = (np.sum(states * cion_densities.T, axis=1)-1) / (len(cion_densities)-1)
        return (xcip,  cxx)
        

def make_figure(path="{}/Tests/cloudy/".format(util.g_DataDir)):
    """
    Generate a comparison figure between Cloudy and Python ion abundances

    Parameters:
    -----------
    path : str, optional
        Path to the directory containing the data files. Defaults to "../Data/Tests/tardis/".

    Returns:
    --------
    None
    """

    cloudy_dir = "{}/cloudy_ce/".format(path)
    python_dir = "{}/python_basic/".format(path)
    macro_dir = "{}/python_hhe_matom/".format(path)

    cl = dict()
    cl["H"]='%s/cl_hydrogen_PL.dat' % (cloudy_dir)
    cl["He"]='%s/cl_helium_PL.dat' % (cloudy_dir)
    cl["C"]='%s/cl_carbon_PL.dat' % (cloudy_dir)
    cl["N"]='%s/cl_nitrogen_PL.dat' % (cloudy_dir)
    cl["O"]='%s/cl_oxygen_PL.dat' % (cloudy_dir)
    cl["Fe"]='%s/cl_iron_PL.dat' % (cloudy_dir)

    #util.set_cmap_cycler("Dark", N=10)

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(13,7.5))
    for i,ion in enumerate(["H", "He", "C", "O", "Fe"]):
        ax = axes.flatten()[i]
        py_fname = '{}/py_{}_pl.txt'.format(python_dir,ion)
        macro_fname = '{}/py_{}_pl.txt'.format(macro_dir,ion)

        if ion == "Fe":
            plot_one(ax,cloudy=cl[ion],python=py_fname,element=ion,imin=19,imax=27,ipmin=0,ipmax=7)

        else:
            plot_one(ax,cloudy=cl[ion],python=py_fname,element=ion,imin=0,imax=0,ipmin=-6,ipmax=4)

        ax.legend(loc="lower right")
        if i > 2: ax.set_xlabel(r"$\log U$", fontsize=20)
        ax.set_ylabel(r"$N_i/N_{\rm elem}$", fontsize=16)

    imax = (2,3)
    for i,ion in enumerate(["H","He"]):
        macro_fname = '{}/py_{}_pl.txt'.format(macro_dir,ion)
        ax = axes.flatten()[i]
        d = ascii.read(macro_fname)
        colname=d.colnames[6:]
        for j in range(0,imax[i]):
            ax.semilogy(np.log10(d['ip']),d[colname[j]], ls=":")

    ax = axes.flatten()[-1]
    util.set_cmap_cycler("Dark2", N=8)
    for i,ion in enumerate(["H", "He", "C", "N", "O", "Fe"]):
        ip, xx = get_chi(ion, python=True, cl = None, python_dir = python_dir)
        ax.plot(ip,  xx, ls="--", c="C"+str(i))

        xcip,  cxx = get_chi(ion, python=False, cl=cl)
        ax.plot(xcip,  cxx, ls='-', lw=3, alpha=0.5, c="C"+str(i), label=ion)
    ax.set_ylim(0,1.03)
    ax.set_xlim(-6,6)
    ax.set_ylabel(r'$\chi$', fontsize=20)
    ax.set_xlabel(r"$\log U$", fontsize=20)

    fig.tight_layout(pad=0.05)
    util.save_paper_figure("cloudy_comparison.pdf", fig=fig)




if __name__ == "__main__":
    util.set_plot_defaults()
    make_figure()
