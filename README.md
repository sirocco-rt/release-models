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

* Details/ -- folders for each comparisons including being able to run them in detail, more intended for a developer
* Plot/ -- scripts for making plots, will eventually contain something like:
	* MakeAllFigures.py
	* fig1.py
	* fig2.py
	* ...
	* util.py: utility functions and code name definition as util.CODE_NAME 
	* Figures/ -- folder containing the figures that will go in the actual paper. 

* Data/ -- just the data needed for the figures + parameter files. Could include scripts for running cloudy and so on here if desired. Please add tests and demo models in the format:
	* Tests/
		* Tardis/
		* Cloudy/
		* CMFGEN/
		* etc...
	* Demo/
		* TDE/
		* Quasar/
		* CV/
		* XRB/

### Instructions

* Please create a folder within the above framework
* Add:  the parameter file, spectrum outputs and any other useful outputs that are not memory intensive (i.e. no .diag files or .wind_save files, but .master.txt files are OK)
* Add any scripts used to make plots, ideally portable to other users
* If required, create a corresponding folder in Details/ that contains further analysis, scripts for running ionization loops, etc. 




