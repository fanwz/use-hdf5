# Introduction

This sample test convert Chinese A share's Level2 data in csv format to HDF5 file.

The final generated file structure is as follows:


And use the following Python packages,you can choose the one that suits you.
## pytables

- It can be used in Python2 or Python3 in Windows|Linux|Mac OS

## h5py

- It can be used in Python2 or Python3 in Linux.
- In Windows,I encounter a error(Miss DLL) with native Python environment,but in the conda's Python environment it will be OK.




# Note:
Because I use the stock's code(like 000001) for the dataset name in Python.When run the test,there will be warning message like below.
> NaturalNameWarning: object name is not a valid Python identifier: '000865'; it does not match the pattern ``^[a-zA-Z_][a-zA-Z0-9_]*$``; you will not be able to use natural naming to access this object; using ``getattr()`` will still work, though
  NaturalNameWarning)

You can customize the dateset's name start with English letter to avoid this warning.
