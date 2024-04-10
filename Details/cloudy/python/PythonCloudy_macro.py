#!/usr/bin/env python 

'''
                    Space Telescope Science Institute

Synopsis:  

Run a grid of thin shell models for comparions with Cloudy


Command line usage (if any):

    usage: PythonCloudy_macro.py -h -log_ipmin -5 -log_ipmax 5 -npoints 100  -cno -icycles 1 -nproc 8 py88a

    where all of the variables are optinal except the python version

    -h will print this brief documentation and then quith
    -log_ipmin -5 sets the minimum ionizaiton parameter to 10**-5
    -log_ipmax 5  sets the maxium ionization paramver to 10**5
    -npoints 100  sets the number of models that wil be cacluated
    -cno switches to an atomic data file that has cno, as well as H and He as the atomic datasset 
    -icycles  1 sets the number of ioncycles, 1 is the values needed for a fixed temperature model
    -nproc 8  sets the number of threads

Description:  

    The routine executes a number of python runs of a thin shell model for comparison with
    similar models created with Cloudy.  As it goes, it uses windsave2table to get the ion
    fractions for each ion.  Finally, it reads the windsave2table outputs to create a summary
    table for each ion.

Primary routines:


Notes:
                                       
History:

240331 ksl Coding begun.  Adapted from an ipynb file on this date

'''




import os

import subprocess
import numpy as np
import shutil
from glob import glob
from astropy.io import ascii
from astropy.table import Table, join,vstack,hstack
from glob import glob
import numpy as np
import matplotlib.pyplot as plt




base='''System_type(star,cv,bh,agn,previous)                   bh

### Parameters for the Central Object
Central_object.mass(msol)                  0.8
Central_object.radius(cm)                  1e10
Binary.mass_sec(msol)                           0.4
Binary.period(hr)                             1000

### Parameters for the Disk (if there is one)
Disk.type(none,flat,vertically.extended,rmin>central.obj.rad)                 none

### Parameters for Boundary Layer or the compact object in an X-ray Binary or AGN
Central_object.radiation(yes,no)                  yes
Central_object.rad_type_to_make_wind(bb,models,power,cloudy,brems,mono)               cloudy
Central_object.luminosity(ergs/s)          %.3e
Central_object.power_law_index             -0.9
Central_object.geometry_for_source(sphere,lamp_post,bubble)               sphere
Central_object.cloudy.low_energy_break(ev)                .136
Central_object.cloudy.high_energy_break(ev)               20000

### Parameters describing the various winds or coronae in the system
Wind.number_of_components                  1
Wind.type(SV,star,hydro,corona,kwd,homologous,shell,imported)                shell

### Parameters associated with photon number, cycles,ionization and radiative transfer options
Photons_per_cycle                          10000000
Ionization_cycles                          %d
Spectrum_cycles                            0
Wind.ionization(on.the.spot,ML93,LTE_tr,LTE_te,fixed,matrix_bb,matrix_pow,matrix_est)           matrix_pow
Line_transfer(pure_abs,pure_scat,sing_scat,escape_prob,thermal_trapping,macro_atoms_escape_prob,macro_atoms_thermal_trapping)     macro_atoms_thermal_trapping
Matom_transition_mode(mc_jumps,matrix)             mc_jumps
Wind.radiation(yes,no)                           no
Atomic_data                                %s
# Atomic_data                                data/h10_hetop_standard80.dat
# Atomic_data                                zdata/master_cno.dat
Surface.reflection.or.absorption(reflect,absorb,thermalized.rerad)              reflect
Wind_heating.extra_processes(none,adiabatic,nonthermal,both)                 none

### Parameters for Domain 0
Shell.wind_mdot(msol/yr)                   4.7e-20
Shell.wind.radmin(cm)                      1e11
Shell.wind.radmax(cm)                      1.00000000001e11
Shell.wind_v_at_rmin(cm)                   1
Shell.wind.v_at_rmax(cm)                   1.000010
Shell.wind.acceleration_exponent           1
Wind.t.init                                10000
Wind.filling_factor(1=smooth,<1=clumped)   1

### Parameters for Reverberation Modeling (if needed)
Reverb.type(none,photon,wind,matom)                 none

### Other parameters
Photon_sampling.approach(T_star,cv,yso,AGN,tde_bb,min_max_freq,user_bands,cloudy_test,wide,logarithmic)          cloudy_test
Photon_sampling.low_energy_limit(eV)            0.13
Photon_sampling.high_energy_limit(eV)                 1e8
'''




def run_one(log_ip=-8,version='',adata='data/h10_hetop_standard80.dat',ncycles=1,nproc=8):

    if log_ip<0:
        pfname='%s_m%03.2f' % (version,-log_ip)
    else:
        pfname='%s_p%03.2f' % (version,log_ip)
    

    f=open(pfname+'.pf','w')
    
    xlum=1e21 * 10**(log_ip+8.0)


    
    f.write(base % (xlum,ncycles,adata))
    f.close()

    py=version
  

    if nproc>1:
        # xcommand='mpirun -np %d  %s -p %s > %s.out.txt' % (nproc,py,pfname,pfname)
        xcommand='mpirun -np %d  %s %s > %s.out.txt' % (nproc,py,pfname,pfname)
    else:
        # xcommand='%s -p %s > %s.out.txt' % (py,pfname,pfname)
        xcommand='%s %s > %s.out.txt' % (py,pfname,pfname)

    print(xcommand)
    try:
        subprocess.run(xcommand,shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Error occurred:", e)
        print("Failed command:", e.cmd)
        # Print out the return code
        print("Return code:", e.returncode)
        # Print out any output from the process
        print("Output:", e.output)
        # Continue the script
        pass

    try:
        signame= '%s.sig' % pfname
        f=open(signame)
    except:
        print('Error: Could not open %s ' % signame)
        return 1
        

    lines=f.readlines()
    last_line=lines[-1]
    print(last_line)
    if last_line.count('COMPLETE'):
        windsave2table = version.replace('py','windsave2table')
        xcommand='%s %s >> %s.out.txt' % (windsave2table,pfname,pfname)
        # print(xcommand)
        subprocess.run(xcommand,shell=True, check=True)
        return 0
    return 1
              


def do_many(log_ipmin=-5,log_ipmax=8,npts=10,version='',adata='data/h10_hetop_standard80.dat',ncycles=1,nproc=8):
    log_ip=np.linspace(log_ipmin,log_ipmax,npts)
    # print(log_ip)
    i=1
    for one in log_ip:
        if one<0:
            pfname='%s_m%03.2f' % (version,-one)
        else:
            pfname='%s_p%03.2f' % (version,one)
        ival=run_one(one,version,adata,ncycles,nproc)
        if ival==0:
            # os.remove(pfname+'.wind_save')
            shutil.rmtree('diag_%s' % pfname)
            files = glob('%s*spec*' % pfname)
            # print(files)
            for one_file in files:
                os.remove(one_file)
            print('Finished %s successfully (%d/%d)' % (pfname,i,len(log_ip)))
        else:
            print('Failed on %s  (%d/%d)' % (pfname,i,len(log_ip)))
        i+=1
                  
        

def get_roots(version):
    prefix=x= version
    xfiles=glob('%s*master.txt' % prefix)
    xorder=[]
    xroot=[]
    for one in xfiles:
        foo=one.replace('.master.txt','')
        xroot.append(foo)
        foo=foo.replace('%s_' % prefix,'')
        foo=foo.replace('p','+')
        foo=foo.replace('m','-')
        xorder.append(eval(foo))
    xtab=Table([xroot,xorder],names=['Root','IP'])
    xtab['IP'].format='.2f'
    xtab.sort('IP')
    return xtab
    



def get_frac(root,element='H'):
    filename='%s.%s.frac.txt' % (root,element)
    try:
        xtab=ascii.read(filename)
        
    except:
        print('Error: could not read %s',filename)
        return None

    colnames=xtab.colnames
    xtab.remove_column('r')
    xtab.remove_column('inwind')
    return xtab



def make_summary_table(roots, element='H',version=''):


    record=[]
    for one in roots:
        try:
            xtab=ascii.read(one['Root']+'.master.txt')
        except:
            print('Error: make_summary_table: Could not read %s' % (one['Root']+'.master.txt'))
        ytab=xtab['i','converge','t_e','t_r','ip','xi']
        ztab=ytab[ytab['i']==1]
        # print(ztab)
        htab=get_frac(one['Root'],element)
        zztab=join(ztab,htab,join_type='left')
        # hetab=get_frac(one,'He')
        # zztab=join(zztab,hetab,join_type='left')
        # # print(zztab)
        record.append(zztab)

    xxx=vstack(record)

    

    xxx['ip'].format='.3e'
    xxx['xi'].format='.3e'
    xxx['t_e'].format='.3e'
    xxx['t_r'].format='.3e'
    

    xxx.write('Sum_%s_%s_pl.txt' % (version,element),format='ascii.fixed_width_two_line',overwrite=True)
    return xxx



def steer(argv):
    '''
    This portion of the code allows the routines
    to be run from the command line

    PythonCloudy_macro.py -h -log_ipmin -5 -log_ipmax 5 -npoints 100  -cno -ncycles 1 py88a
    '''


    version=''
    npoints=100
    log_ipmin=-5
    log_ipmax=5
    i=1
    nproc=8
    icycles=1
    atomic_data='data/h10_hetop_standard80.dat'
    cno_data='zdata/master_cno.dat'
    cno=False

    while i<len(argv):
        if argv[i][0:2]=='-h':
            print(__doc__)
            return
        elif argv[i]=='-npoints':
            i+=1
            points=int(argv[i])
        elif argv[i]=='-nproc':
            i+=1
            nproc=int(argv[i])
        elif argv[i][0:4]=='-icy':
            i+=1
            icycles=int(argv[i])
        elif argv[i]=='-cno':
            cno=True
        elif argv[i]=='-log_ipmin':
            i+=1
            log_ipmin=eval(arv[i])
        elif argv[i]=='-log_ipmax':
            i+=1
            log_ipmax=eval(arv[i])

        elif argv[i][0]=='-':
            print('Error: Unknown switch :', argv)
        elif version=='':
            version=argv[i]
        else:
            print('Error: Ill-formed command line:',argv)
            return


        i+=1


    xversion=version
    if cno==True:
        atomic_data=cno_data
        xversion='%s_%s' % (xversion,'cno')
    if icycles>1:
        xversion='%s_%s' % (xversion,'conv')

    print('Beginning a run using %s`with %d processors' % (version,nproc))
    print('Running %d ionization cycles with this atomic data file %s' % (icycles,atomic_data))
    print('Log ip min %.1f log ip_max %.1f with %d models\n\n' % (log_ipmin,log_ipmax,npoints))


    do_many(npts=npoints,version=version,adata=atomic_data,ncycles=icycles,nproc=nproc)
    roots=get_roots(version)
    make_summary_table(roots, element='H',version=xversion)
    make_summary_table(roots, element='He',version=xversion)
    make_summary_table(roots, element='C',version=xversion)
    make_summary_table(roots, element='N',version=xversion)
    make_summary_table(roots, element='O',version=xversion)
    make_summary_table(roots, element='Si',version=xversion)
    make_summary_table(roots, element='Fe',version=xversion)

    print('The program is now complete')
    



# Next lines permit one to run the routine from the command line
if __name__ == "__main__":
    import sys
    if len(sys.argv)>1:
        steer(sys.argv) 
    else:
        print (__doc__)
