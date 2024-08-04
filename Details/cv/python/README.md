This directory contains models of CVs that are made/being made
for the release paper. The models should not be run in the 
repository, rather one should copy this directory to another
location.  

The models can be run with regression.py (or the Regress
command in this directory).  Once one is satisfied with
the runs, the routine GetResults is intended to allow
one to get the results that are needed for figures.

Of course, if any of the input .pf files changes these
need to be moved separately to test\_cv directory

240804 - There are two sets of models, the only difference
being the number of photons and ion cycles.  The short 
version is more than adequate in most cases.  The
short version .pf files are in test\_cv\_short, and the results 
are in Results\_short.  The long version are in test\_cv and 
Results.  
