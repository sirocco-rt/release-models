[![release_plots](https://github.com/agnwinds/release-models/actions/workflows/test_figures.yml/badge.svg)](https://github.com/agnwinds/release-models/actions/workflows/test_figures.yml)
[![DOI](https://zenodo.org/badge/335235472.svg)](https://doi.org/10.5281/zenodo.13993033)
[![arXiv](https://img.shields.io/badge/arXiv-2410.19908-b31b1b.svg)](https://arxiv.org/abs/2410.19908)

# Sirocco Release Models

This repository contains model outputs, parameter files, and plotting scripts for the Sirocco release paper. 

### Making Figures
To make the figures, run 
```
cd Plot
python MakeAllFigures.py 
```
You may need to run this first: 
```
pip -r requirements.txt
```

### Directory Structure 

The structure of this repository is 

* **Details:** folders for each comparisons including being able to run them in detail, more intended for a developer. 
* **Plot:** scripts for making plots. There are python scripts for each figure, and a script MakeAllFigures.py which...makes all figures. util.py contains utility functions and code name definition as util.CODE_NAME.
	* Figures/ -- folder containing the figures that will go in the actual paper. 

* **Data:** contains just the data needed for the figures + parameter files. The structure is:
	* **Tests:**
		* tardis.
		* cloudy/
		* cmfgen/
	* **Demo:**
		* tde/
		* quasar/
		* cv/
		* xrb/
    		* rad-hydro
