Running the project

1) Create enviroment
To re-run the project with conda, first install the required packages in a new conda environment.
Using anaconda command line in root folder run:

'''conda env create -f environment.yml'''


You then need to activate the environment.
For that, use console command line.

'''conda activate conda-env'''


2) Run python files
There are a couple of ways to run the python files.
The first is to run them from the command line, from the root directory. For example:

'''python -m src.download_raw_data'''

To run all of them at once, use 

'''python -m src.master'''


Or, from within an IDE, run the contents of src/master.py (but run it as if from the root folder).

Finally, continue with Noteebooks.
