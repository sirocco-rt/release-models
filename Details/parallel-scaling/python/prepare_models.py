"""Prepare a directory for running scaling tests on Iridis 5.

This script will create directories that will contain the input files required
to run scaling tests on Iridis 5 for a tuple of models.
"""

import math
import shutil
from pathlib import Path

PYTHON_VERSION = "88a"
PYTHON_DIRECTORY = "$HOME/codes/python"
ROOT_NAMES = (
    "agn_macro_matrix",
    "cv_macro_matrix",
)
ESTIMATED_MODEL_TIME_SECONDS = (50000, 50000)
NUM_TASKS = (
    "1",
    "2",
    "4",
    "8",
    "16",
    "32",
    "40",
    "80",
    "120",
    "160",
    "200",
    "240",
    "280",
    "320",
)
CORES_PER_NODE = 40
PARTITION = "batch"

SLURM_TEMPLATE = """#!/bin/bash
#SBATCH --nodes={}
#SBATCH --ntasks={}
#SBATCH --time={:02d}:{:02d}:00
#SBATCH --partition={}

module load openmpi/4.1.1/gcc
export PYTHON={}

$PYTHON/bin/Setup_Py_Dir
mpiexec -np $SLURM_NTASKS $PYTHON/bin/py{} {}
"""

for n in range(len(ROOT_NAMES)):  # pylint: disable=consider-using-enumerate
    root = ROOT_NAMES[n]
    root_pf = Path(f"./{root}.pf.in")
    if not root_pf.exists():
        raise FileNotFoundError(f"{root_pf} does not exist")

    for ntasks in NUM_TASKS:
        directory_name = f"./{root}/{ntasks}"
        new_folder = Path(directory_name)
        if new_folder.exists():
            shutil.rmtree(new_folder)
        new_folder.mkdir(parents=True)
        shutil.copy(root_pf, Path(f"{new_folder}/{root}.pf"))

        num_cores = int(ntasks)
        num_nodes = math.ceil(num_cores / CORES_PER_NODE)
        time_seconds = ESTIMATED_MODEL_TIME_SECONDS[n] / num_cores
        time_hours = math.floor(time_seconds / 3600)
        time_minutes = math.ceil((time_seconds % 3600) / 60)

        print(f"{time_hours}:{time_minutes}")

        with open(
            f"{directory_name}/{root}_ntasks-{ntasks}.slurm",
            "w",
            encoding="utf-8",
        ) as file_out:
            file_out.writelines(
                SLURM_TEMPLATE.format(
                    num_nodes,
                    num_cores,
                    time_hours,
                    time_minutes,
                    PARTITION,
                    PYTHON_DIRECTORY,
                    PYTHON_VERSION,
                    root_pf.stem,
                )
            )
