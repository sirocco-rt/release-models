To be able to run scaling tests, you first need to run `prepare_models.py` to
generate the directories and files needed to submit tests to your HPC cluster.
If you are not using Iridis 5, you will need to update some of the variables
at the top of `prepare_models.py` to match your HPC cluster. If your cluster
doesn't use SLURM, then you are on your own.

After running `prepare_models.py`, you will have a directory structure like
this:

```bash
$ ls
agn_macro_matrix/ cv_macro_matrix/ prepare_models.py
```

You will need to upload the `agn_macro_matrix` and `cv_macro_matrix` directories
to your HPC cluster. Then you can submit each job to the cluster.
