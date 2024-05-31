import plot_tde, tardis_fig, plot_parallel_scaling
import plot_cv, plot_quasar
import sys 

tex = "True"
if len(sys.argv) > 1:
    if sys.argv[1] == "--notex":
        tex = "False"

util.set_plot_defaults(tex=tex)
tardis_fig.make_figure()
plot_parallel_scaling.make_figure()
plot_cv.make_figure()
plot_quasar.make_figure()
plot_tde.make_figure()
