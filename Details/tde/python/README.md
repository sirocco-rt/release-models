This directory contains the files required to run the standard TDE
model, taken from Parkinson et al. 2022, MNRAS, 510, 4. This model should not
be run in this repository, but should be copied from this directory into
another location.

This model takes ~1000s of CPU hours to finish. Therefore it is advised to run
this model on a HPC cluster, rather than your personal machine.

The model can be run with the `Regress.sh` script. Once the model is finished,
and you are satisfied, you can use `GetResults.sh` to move the results into the
correct directory and plot the results using the Python scripts in the `Plots`
directory.

```bash
$ ./Regress.sh test_tde
$ ./GetResults.sh tde_tde
$ cd Plots
$ python plot_tde.py
```

