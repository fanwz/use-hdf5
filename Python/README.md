# Introduction

This sample test convert Chinese A share's Level2 data in csv format to HDF5 file.

The final generated file structure is as follows:

![hdf5-sreenshot](https://github.com/fanwz/use-hdf5/blob/master/Python/hdf5-sreenshot.png)

And use the following Python packages,you can choose the one that suits you.
## pytables

- It can be used in Python2 or Python3 in Windows|Linux|Mac OS

## h5py

- It can be used in Python2 or Python3 in Linux.
- In Windows,I encounter a error(Miss DLL) with native Python environment,but in the conda's Python environment it will be OK.


# Test log
One day of Chinese A share's Level2 data,there are about 9000000 rows,and more than 9000 stocks.So it must be created more than 9000 datasets in a hdf5 file.

It takes a long time to convert this stock's data to hdf5.

I add some print timestamp to the code,and the log show that as below:

- The size of original data file(csv) is about 2.6GB,and all loaded by pandas's read_csv method will occupy more than 5GB memory.

- It takes about 60mins to convert all data to a hdf5 file, the hdf5 file size is about 355MB.

- About 3 stocks' data can be convert(create dataset and write data) to hdf5 in one second.

- If processed by filtered stock list,such as filtering out about 1800 stocks,It takes about 10mins and hdf5 file size is about 280MB.

So I think switching in dataset and write a little data one by one may take most of time of converting all stock data,and if (create dataset)write data as more as possible in one time will be save much more time.

# Note:
Because I use the stock's code(like 000001) for the dataset name in Python.When run the test,there will be warning message like below.
> NaturalNameWarning: object name is not a valid Python identifier: '000865'; it does not match the pattern ``^[a-zA-Z_][a-zA-Z0-9_]*$``; you will not be able to use natural naming to access this object; using ``getattr()`` will still work, though
  NaturalNameWarning)

You can customize the dateset's name start with English letter to avoid this warning.
