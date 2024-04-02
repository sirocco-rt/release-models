#!/usr/bin/env python
# coding: utf-8

'''
                    Space Telescope Science Institute

Synopsis:  

This is a routine to plot comparisons between 
ionization calculated with different Cloudy
and Python models, most if not all of which 
are assoociated with optically thin plasmas


Command line usage (if any):

    usage: CloudyCompare2024.py -h -conv -cno py88a

Description:  

    This is a specialized routine to make standardized
    plots of cloudy/Python comparions, where

    There is only one required command line variable an
    that is the python variable.

    -h prints this help and exits
    -conv looks for converged models for both
        cloudy and Python
    -cno looks for models where not just H and He are
        macro atoms, but so are CNO


Primary routines:

    doit

Notes:
 The Ferland definition of ionization parameter is in the variable ip.
                                       
History:

240402 ksl Coding begun

'''

import sys
from astropy.io import ascii
import numpy as np
import matplotlib.pyplot as plt
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


def plot_one(cloudy='cl_helium_PL.dat',python='py_he',element='He',imin=0,imax=0,ipmin=-8,ipmax=4,outname=''):
    print('Comparing: ',cloudy,python)
    pfile='%s' % (python)
    try:
        xp=ascii.read(pfile)
    except:
        print('Error: Could not read %s' % pfile)
        return None


    
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
        plt.semilogy(xc['ip'],xc[colname[i]],':',color=color_cycle[color_index])
        plt.semilogy(np.log10(xp['ip']),xp[colname[i]],color=color_cycle[color_index],label=xlabel)
        i+=1
        color_index+=1
        if color_index==len(color_cycle):
            color_index=0
    plt.legend()
    plt.xlabel('log (Ionization Parameter)')
    plt.ylabel('Fractional Abundnce')
    plt.ylim(1e-4,1.2)
    if ipmin!=0 or ipmax!=0:
        plt.xlim(ipmin,ipmax)
    plt.tight_layout()


def do_fe(cloudy='cl_iron_PL.dat',python='py_fe'):
    plt.figure(1,(8,8))
    plt.clf()
    plt.subplot(3,1,1)
    plot_one(cloudy,python,element='Fe',imax=9,ipmin=-8,ipmax=2)
    plt.subplot(3,1,2)
    plot_one(cloudy,python,element='Fe',imin=10,imax=18,ipmin=-2,ipmax=3)
    plt.subplot(3,1,3)
    plot_one(cloudy,python,element='Fe',imin=19,imax=27,ipmin=0,ipmax=8)



def doit(python_dir,cloudy_dir,version,cno=False, converge=False):

    #Now define the file names

    print('hello ',converge)


    cl_he='%s/cl_helium_PL.dat' % (cloudy_dir)
    cl_c='%s/cl_carbon_PL.dat' % (cloudy_dir)
    cl_n='%s/cl_nitrogen_PL.dat' % (cloudy_dir)
    cl_o='%s/cl_oxygen_PL.dat' % (cloudy_dir)
    cl_fe='%s/cl_iron_PL.dat' % (cloudy_dir)


    py_he='%s/Sum_%s_He_pl.txt' % (python_dir,version)
    py_c='%s/Sum_%s_C_pl.txt' % (python_dir,version)
    py_n='%s/Sum_%s_N_pl.txt' % (python_dir,version)
    py_o='%s/Sum_%s_O_pl.txt' % (python_dir,version)
    py_fe='%s/Sum_%s_Fe_pl.txt' % (python_dir,version)

    print('choices',cno,converge)

    if converge:
        print ('OK cowboy')
        py_he=py_he.replace(version,'%s_%s' % (version,'conv'))
        py_c=py_c.replace(version,'%s_%s' % (version,'conv'))
        py_n=py_n.replace(version,'%s_%s' % (version,'conv'))
        py_o=py_o.replace(version,'%s_%s' % (version,'conv'))
        py_fe=py_fe.replace(version,'%s_%s' % (version,'conv'))

    if cno:
        print ('OK cowgirl')
        py_he=py_he.replace(version,'%s_%s' % (version,'cno'))
        py_c=py_c.replace(version,'%s_%s' % (version,'cno'))
        py_n=py_n.replace(version,'%s_%s' % (version,'cno'))
        py_o=py_o.replace(version,'%s_%s' % (version,'cno'))
        py_fe=py_fe.replace(version,'%s_%s' % (version,'cno'))

    xstart='Sum_%s' % version
    if converge:
        xstart='%s_conv' % xstart
    if cno:
        xstart='%s_cno' % xstart

    # Now do the plots
    plot_one(cloudy=cl_he,python=py_he,element='He',imin=0,imax=0,ipmin=-8,ipmax=4)
    plt.savefig('%s_%s.png' % (xstart,'He'))

    plt.clf()
    plot_one(cloudy=cl_c,python=py_c,element='C',ipmin=-8,ipmax=4)
    plt.savefig('%s_%s.png' % (xstart,'C'))

    plt.clf()
    plot_one(cloudy=cl_n,python=py_n,element='N',ipmin=-8,ipmax=4)
    plt.savefig('%s_%s.png' % (xstart,'N'))

    plt.clf()
    plot_one(cloudy=cl_o,python=py_o,element='O',ipmin=-8,ipmax=4)
    plt.savefig('%s_%s.png' % (xstart,'O'))

    plt.clf()
    plot_one(cloudy=cl_fe,python=py_fe,element='Fe',imax=9,ipmin=-8,ipmax=2)
    plt.savefig('%s_%s.png' % (xstart,'Fe_1_9'))

    plt.clf()
    plot_one(cloudy=cl_fe,python=py_fe,element='Fe',imin=10,imax=18,ipmin=-2,ipmax=3)
    plt.savefig('%s_%s.png' % (xstart,'Fe_10_18'))

    plt.clf()
    plot_one(cloudy=cl_fe,python=py_fe,element='Fe',imin=14,imax=27,ipmin=-2,ipmax=8)
    plt.savefig('%s_%s.png' % (xstart,'Fe_14_27'))

    plt.clf()
    plot_one(cloudy=cl_fe,python=py_fe,element='Fe',imin=19,imax=27,ipmin=0,ipmax=8)
    plt.savefig('%s_%s.png' % (xstart,'Fe_19_27'))
    plt.clf()
    # do_fe()



def steer(argv):

    cloudy_dir='../cloudy'
    python_dir='../python'
    converge=False
    cno=False
    version=''

    i=1
    while i<len(argv):
        if argv[i][0:2]=='-h':
            print(__doc__)
            return
        elif argv[i]=='-conv':
            converge=True
        elif argv[i]=='-cno':
            cno=True
        elif argv[i][0]=='-':
            print('Error: Unknown switch in command line',argv)
        elif version=='':
            version=argv[i]
        i+=1

    if converge:
        cloudy_dir='../cloudy_converge'

    doit(python_dir,cloudy_dir,version,cno,converge)


# Next lines permit one to run the routine from the command line
if __name__ == "__main__":
    import sys
    if len(sys.argv)>1:
        steer(sys.argv)
    else:
        print (__doc__)
