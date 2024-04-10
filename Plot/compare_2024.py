import sys, os
#from line_routines import *
#import recomb_sub as sub
#import matplotlib.pyplot as plt
#from tardis.io import config_reader
#from tardis import model, simulation
from read_output import *
import numpy as np
import logging
import warnings
from numpy import exp
from pylab import *
from astropy import units
from pretty import *
import astropy.io.ascii as io



def run_tardis(yml_file="basic.yml"):
	'''
	runs a tardis model and returns a class instance of Radial1dModel type
	'''
	#read the config file and create a model
	tardis_config = config_reader.TARDISConfiguration.from_yaml(yml_file)
	radial1d = model.Radial1DModel(tardis_config)
	simulation.run_radial1d(radial1d)

	return radial1d


# if you want to rerun model, uncomment this
#mod = run_tardis(yml_file="tardis_python.yaml")
#mod.spectrum.to_ascii("tardis_python_spectrum.dat", mode="flux")

w, f = np.loadtxt("tardis_python_spectrum.dat", unpack=True)


# we have to correct fluxes to same distance by r**2 law
PY2TAR = (100.0 ** 2) / (0.1e6 **2)



s = read_spec_file("1d_sn")
s2 = io.read("1d_sn_87.spec")
s3 = io.read("1d_sn_87_2.spec")


figure(figsize=(10,6))
#suptitle("Python v Tardis comparison with fix to #117")

# make new plot

#subplot(411)
set_pretty()
long_ticks()
big_tick_labels(16)

#frame1=fig1.add_axes((.1,.3,.8,.6))
plot(w, f / PY2TAR, label= "Tardis", c="k")
plot(s2["Lambda"], s2["A45P0.50"], label= "Python 2024", linewidth=2, alpha=0.8)
plot(s.wavelength, s.spec[0], label= "Python Thesis", linewidth=2, alpha=0.8)
plot(s3["Lambda"], s3["A45P0.50"], label= "Python 2024 Aniso", linewidth=2, alpha=0.8)
ylabel ("Flux at 100pc (erg~s$^{-1}$~cm$^{-2}$~\AA$^{-1}$)", fontsize=20)
float_legend()
xlim(1000,11000)
#gca().set_xticklabels([])

subplots_adjust(right=0.97)
# frame2=fig1.add_axes((.1,.1,.8,.2))
# plot()
# plot(w, f / PY2TAR, label= "Tardis", c="k")


# subplot(413)
# plot(s.wavelength, s.spec[0], label= "Python dev 141006", c="b")
# plot(s2.wavelength, s2.spec[0], label= "Python 76b", c="g")
# ylabel ("Flux at 100pc")
# legend()


# subplot(414)
# plot(s.wavelength, s.emitted, label= "Python dev 141006 emitted", c="b")
# plot(s2.wavelength, s2.emitted, label= "Python 76b emitted", c="g")
# ylabel ("Flux at 100pc")
# legend()


xlabel("Wavelength (\AA)", fontsize=20)


#show()
savefig("tardispython_2024.png", dpi=300)



