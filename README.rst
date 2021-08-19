#### Re-running the project

To re-run the project with conda, first install the required packages in a new conda environment:
```
conda env create -f envtest.yml
```
You then need to activate the environment to use in your IDE. The command for this is ```conda activate envtest```. Note that, to try to ensure compatibility with all operating systems, the environment file is simplified. It only specifies the version of Python, conda is trusted to resolve dependencies and pick the right versions of other required packages.

There are a couple of ways to run the python files. The first is to run them from the command line, from the root directory. For example:
``python -m src.download_raw_data``
To run all of them at once, use 
``python -m src.master``
Or, from within an IDE, run the contents of src/master.py (but run it as if from the root folder).
