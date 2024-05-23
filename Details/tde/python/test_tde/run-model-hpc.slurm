#!/bin/bash
#SBATCH --nodes=
#SBATCH --ntasks=120
#SBATCH --ntasks-per-node=
#SBATCH --time=15:00:00
#SBATCH --partition=
#SBATCH --exclusive
#SBATCH --open-mode=append
#SBATCH --output=output.log
#SBATCH --error=error.log

# Load MPI module Python was built with
module load openmpi/5.0.0

# Set envrionment variables 
export PYTHON=$HOME/codes/python
export PYVERSION=88
export PYEXE=$PYTHON/bin/py$PYVERSION
export PYFLAGS="-p 2 --rseed"
export ROOT_NAME="tde_standard"

# Setup data symbolic link
$PYTHON/bin/Setup_Py_Dir

# Run Python
mpiexec -np $SLURM_NTASKS $PYEXE $PYFLAGS $ROOT_NAME

