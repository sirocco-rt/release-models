Model outputs, parameter files, and plotting scripts for the Sirocco release paper. 

[![release_plots](https://github.com/agnwinds/release-models/actions/workflows/test_figures.yml/badge.svg)](https://github.com/agnwinds/release-models/actions/workflows/test_figures.yml)

### TO make figures

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

* Details/ -- folders for each comparisons including being able to run them in detail, more intended for a developer. 
* Plot/ -- scripts for making plots. There are python scripts for each figure, and a script MakeAllFigures.py which...makes all figures. util.py contains utility functions and code name definition as util.CODE_NAME.
	* Figures/ -- folder containing the figures that will go in the actual paper. 

* Data/ -- contains just the data needed for the figures + parameter files. The structure is:
	* Tests/
		* tardis.
		* cloudy/
		* cmfgen/
	* Demo/
		* tde/
		* quasar/
		* cv/
		* xrb/
    		* rad-hydro
