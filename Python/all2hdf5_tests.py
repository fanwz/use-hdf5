#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/14 17:55
# @Author  : AMR
# @File    : all2hdf5_tests.py
# @Software: PyCharm

from all2hdf5 import *
import pandas as pd

df = pd.read_csv("test_df2.csv")
wr = DataFrame2Hdf5(df)
wr.write_hdf5_by_np()
# wr = Csv2Hdf5("test_df2.csv")
# wr.write_hdf5_by_np("aaaa.h5")