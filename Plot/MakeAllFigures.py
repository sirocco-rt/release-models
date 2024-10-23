import util
import sys
import importlib
import numpy as np

np.seterr(divide='ignore')

print("Making all figures for SIROCCO release paper.")

tex = "True"
if len(sys.argv) > 1:
    if sys.argv[1] == "--notex":
        tex = "False"

print("Using tex?", tex)
util.set_plot_defaults(tex=tex)


list_of_modules = ["demo", "cloudy", "tardis", "cmfgen", "parallel", "cv",
                   "quasar", "converge", "xrb", "tde", "radhydro", "cmfgen_comp"]

for mod_name in list_of_modules:
    print("importing and running {}...".format(mod_name), end="")
    module = importlib.import_module(mod_name)
    module.make_figure(transparent=False)
    print("Done.")
