import util, sys 
import importlib 
sys = importlib.import_module("sys")

tex = "True"
if len(sys.argv) > 1:
    if sys.argv[1] == "--notex":
        tex = "False"

print (tex)
util.set_plot_defaults(tex=tex)


list_of_modules = ["plot_tde", "tardis_fig", "plot_parallel_scaling", "plot_cv", 
                   "plot_quasar", "plot_converge", "plot_xrb", "plot_radhydro2"]

for mod_name in list_of_modules:
    module = importlib.import_module(mod_name)
    module.make_figure()