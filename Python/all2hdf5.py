#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/13 17:49
# @Author  : AMR
# @File    : all2hdf5.py
# @Software: PyCharm

import pandas as pd
from tables import *
import os
import numpy as np
import sys
import time

H5PY_EN = False
# only in anacond python2,other has bug.
if sys.version_info[0] == 2:
    import h5py
    H5PY_EN = True
else:
    pass


ZN2EN_DICT = {
    '时间': 'Time',
    '代码': 'Code',
    '最新价': 'Price',
    '最高价': 'HighestPrice',
    '最低价': 'LowestPrice',
    '总量': 'Volume',
    '总金额': 'Turnover',
    '挂买价1': 'BidPrice1', '挂买量1': 'BidVol1',
    '挂买价2': 'BidPrice2', '挂买量2': 'BidVol2',
    '挂买价3': 'BidPrice3', '挂买量3': 'BidVol3',
    '挂买价4': 'BidPrice4', '挂买量4': 'BidVol4',
    '挂买价5': 'BidPrice5', '挂买量5': 'BidVol5',
    '挂买价6': 'BidPrice6', '挂买量6': 'BidVol6',
    '挂买价7': 'BidPrice7', '挂买量7': 'BidVol7',
    '挂买价8': 'BidPrice8', '挂买量8': 'BidVol8',
    '挂买价9': 'BidPrice9', '挂买量9': 'BidVol9',
    '挂买价10': 'BidPrice10', '挂买量10': 'BidVol10',
    '挂卖价1': 'AskPrice1', '挂卖量1': 'AskVol1',
    '挂卖价2': 'AskPrice2', '挂卖量2': 'AskVol2',
    '挂卖价3': 'AskPrice3', '挂卖量3': 'AskVol3',
    '挂卖价4': 'AskPrice4', '挂卖量4': 'AskVol4',
    '挂卖价5': 'AskPrice5', '挂卖量5': 'AskVol5',
    '挂卖价6': 'AskPrice6', '挂卖量6': 'AskVol6',
    '挂卖价7': 'AskPrice7', '挂卖量7': 'AskVol7',
    '挂卖价8': 'AskPrice8', '挂卖量8': 'AskVol8',
    '挂卖价9': 'AskPrice9', '挂卖量9': 'AskVol9',
    '挂卖价10': 'AskPrice10', '挂卖量10': 'AskVol10',
    '总成交笔数': 'Amount'
}

stock_quote = [
               {'Time': 'str32'},
               {'Code': 'str16'},
               {'Price': 'float'},
               {'HighestPrice': 'float'},
               {'LowestPrice': 'float'},
               {'Volume': 'int64'},
               {'Turnover': 'float'},
               {'BidPrice1': 'float'}, {'BidVol1': 'int'},
               {'BidPrice2': 'float'}, {'BidVol2': 'int'},
               {'BidPrice3': 'float'}, {'BidVol3': 'int'},
               {'BidPrice4': 'float'}, {'BidVol4': 'int'},
               {'BidPrice5': 'float'}, {'BidVol5': 'int'},
               {'BidPrice6': 'float'}, {'BidVol6': 'int'},
               {'BidPrice7': 'float'}, {'BidVol7': 'int'},
               {'BidPrice8': 'float'}, {'BidVol8': 'int'},
               {'BidPrice9': 'float'}, {'BidVol9': 'int'},
               {'BidPrice10': 'float'}, {'BidVol10': 'int'},
               {'AskPrice1': 'float'}, {'AskVol1': 'int'},
               {'AskPrice2': 'float'}, {'AskVol2': 'int'},
               {'AskPrice3': 'float'}, {'AskVol3': 'int'},
               {'AskPrice4': 'float'}, {'AskVol4': 'int'},
               {'AskPrice5': 'float'}, {'AskVol5': 'int'},
               {'AskPrice6': 'float'}, {'AskVol6': 'int'},
               {'AskPrice7': 'float'}, {'AskVol7': 'int'},
               {'AskPrice8': 'float'}, {'AskVol8': 'int'},
               {'AskPrice9': 'float'}, {'AskVol9': 'int'},
               {'AskPrice10': 'float'}, {'AskVol10': 'int'},
               {'Amount': 'int'}, {'IOPV': 'float'}
               ]


def str2TbType(str, pos=None):
    tpdict = dict(str16=StringCol(16, pos=pos),
                  str32=StringCol(32, pos=pos),
                  float=Float64Col(pos=pos),
                  int=Int32Col(pos=pos),
                  int64=Int64Col(pos=pos))
    return tpdict[str]


def gen_npdtype(quote):
    # [('foo', 'i4'), ('bar', 'f4'), ('baz', 'S10')]
    dtypedict = dict(str16='S16',
                     str32='S32',
                     float='f8',
                     int='i4',
                     int64='i8')
    dtype = [(list(x.keys())[0], dtypedict[x[list(x.keys())[0]]]) for x in quote]
    # print(dtype)
    return dtype

class QuotesData(IsDescription):
    pass


class HDF5File(object):
    def __init__(self, filepath):
        self.h5file = open_file(filepath)

    def read_test(self):
        table = self.h5file.root.quote["000854"]
        for row in table.iterrows():
            print(row['Time'])


class Csv2Hdf5(object):
    def __init__(self, csvfile):
        self.csvfile = csvfile
        self.filename = os.path.split(csvfile)[-1].split('.')[0]
        self.stocklist = []
        self.csvdf = pd.DataFrame()
        self.__gen_data_struct()
        self.__readcsv()

    def __gen_data_struct(self):
        for idx, v in enumerate(stock_quote):
            key = list(v.keys())[0]
            QuotesData.columns[key] = str2TbType(v[key], pos=idx)


    def __readcsv(self):
        df = pd.read_csv(self.csvfile)
        # print(df)
        df.rename(columns=ZN2EN_DICT, inplace=True)

        # make stock code to 6 digit str.
        df['Code'] = df['Code'].apply(lambda x:str(x).zfill(6))

        self.stocklist = df['Code'].unique()
        self.csvdf = df

    def write_hdf5_by_row(self, savefile=None, mode='w'):
        if savefile is None:
            savefile = self.filename + ".h5"

        hdf5 = open_file(savefile, mode)
        if "quote" not in hdf5.root:
            quote = hdf5.create_group("/", "quote", "Stock quote")
        else:
            quote = hdf5.root.quote

        for stock in self.stocklist:
            if stock not in quote:
                filters = Filters(complevel=5, complib='zlib', fletcher32=True)
                datatable = hdf5.create_table(quote, stock, QuotesData, "mytest stock info", filters=filters)
            else:
                datatable = quote[stock]

            write_row = datatable.row

            for index, row in self.csvdf[self.csvdf['Code'] == stock].iterrows():
                for i in range(0, len(stock_quote)):
                    key = list(stock_quote[i])[0]
                    write_row[key] = row[key]
                write_row.append()
            datatable.flush()

        hdf5.close()

    # write hdf5 table by numpy data. fast than by row
    def write_hdf5_by_np(self, savefile=None, mode='w'):
        if savefile is None:
            savefile = self.filename + ".h5"

        col_list = [list(x.keys())[0] for x in stock_quote]
        dtype = gen_npdtype(stock_quote)

        hdf5 = open_file(savefile, mode)
        if "quote" not in hdf5.root:
            quote = hdf5.create_group("/", "quote", "Stock quote")
        else:
            quote = hdf5.root.quote

        for stock in self.stocklist:
            tg_df = self.csvdf[self.csvdf['Code'] == stock][col_list]
            npar = tg_df.to_records(index=False)
            npar = np.array(npar, dtype=dtype)

            if stock not in quote:
                filters = Filters(complevel=5, complib='zlib', fletcher32=True)
                datatable = hdf5.create_table(quote, stock, npar, "mytest stock info", filters=filters)
            else:
                datatable = quote[stock]
                datatable.append(npar)

        hdf5.close()


    def write_hdf5_h5py(self):
        if not H5PY_EN:
            print("h5py can not use in this python version!")
            return

        print(self.csvdf.info())
        col_list = [x.keys()[0] for x in stock_quote]

        dtype = gen_npdtype(stock_quote)
        print(dtype)

        hdf5 = h5py.File(self.filename + "z_array.h5", 'a')

        if "quote" not in hdf5:
            quote = hdf5.create_group("quote", "Stock quote")
        else:
            quote = hdf5['quote']

        for stock in self.stocklist:
            tg_df = self.csvdf[self.csvdf['Code'] == stock][col_list]
            npar = tg_df.to_records(index=False)
            # print(npar)
            npar = np.array(npar, dtype=dtype)
            print(stock)
            print(len(npar))

            if stock not in quote:
                quote.create_dataset(stock, data=npar, maxshape=(None,), compression="gzip")
            else:
                quote[stock].resize(quote[stock].shape[0] + len(npar), axis=0)
                quote[stock][-len(npar):] = npar

    @staticmethod
    def read_hdf5(filepath):
        h5file = open_file(filepath)
        table = h5file.root.quote["000854"]
        table1 = h5file.root.quote["000001"]
        table2 = h5file.root.quote["000002"]
        table3 = h5file.root.quote["000003"]
        # for row in table.iterrows():
        #     print(row['Time'])
        # by cols method
        print(table.cols.Time[1:5])

        # in-kernel selection
        sd = [row['HighestPrice'] for row in table.where("""(HighestPrice > 0)""")]
        print(sd)
        while True:
            pass


class DataFrame2Hdf5(object):
    def __init__(self, df):
        self.filename = str(time.time())
        self.stocklist = []
        self.csvdf = pd.DataFrame()
        self.__readdf(df)

    def __readdf(self, tgdf):
        df = tgdf

        # convert Chinese cols to English
        df.rename(columns=ZN2EN_DICT, inplace=True)

        # make stock code to 6 digit str.
        df['Code'] = df['Code'].apply(lambda x:str(x).zfill(6))

        # get all stocks code in dataframe
        self.stocklist = df['Code'].unique()
        self.csvdf = df

    # write hdf5 table by numpy data. fast than by row
    def write_hdf5_by_np(self, savefile=None, mode='w'):
        if savefile is None:
            savefile = self.filename + '.h5'

        col_list = [list(x.keys())[0] for x in stock_quote]
        dtype = gen_npdtype(stock_quote)

        hdf5 = open_file(savefile, mode)
        if "quote" not in hdf5.root:
            quote = hdf5.create_group("/", "quote", "Stock quote")
        else:
            quote = hdf5.root.quote

        for stock in self.stocklist:
            tg_df = self.csvdf[self.csvdf['Code'] == stock][col_list]
            npar = tg_df.to_records(index=False)
            npar = np.array(npar, dtype=dtype)

            if stock not in quote:
                filters = Filters(complevel=5, complib='zlib', fletcher32=True)
                datatable = hdf5.create_table(quote, stock, npar, "mytest stock info", filters=filters)
            else:
                datatable = quote[stock]
                datatable.append(npar)

        hdf5.close()


    def write_hdf5_h5py(self):
        if not H5PY_EN:
            print("h5py can not use in this python version!")
            return

        print(self.csvdf.info())
        col_list = [x.keys()[0] for x in stock_quote]

        dtype = gen_npdtype(stock_quote)
        print(dtype)

        hdf5 = h5py.File(self.filename + "z_array.h5", 'a')

        if "quote" not in hdf5:
            quote = hdf5.create_group("quote", "Stock quote")
        else:
            quote = hdf5['quote']

        for stock in self.stocklist:
            tg_df = self.csvdf[self.csvdf['Code'] == stock][col_list]
            npar = tg_df.to_records(index=False)
            # print(npar)
            npar = np.array(npar, dtype=dtype)
            print(stock)
            print(len(npar))

            if stock not in quote:
                quote.create_dataset(stock, data=npar, maxshape=(None,), compression="gzip")
            else:
                quote[stock].resize(quote[stock].shape[0] + len(npar), axis=0)
                quote[stock][-len(npar):] = npar

    @staticmethod
    def read_hdf5(filepath):
        h5file = open_file(filepath)
        table = h5file.root.quote["000854"]
        table1 = h5file.root.quote["000001"]
        table2 = h5file.root.quote["000002"]
        table3 = h5file.root.quote["000003"]
        # for row in table.iterrows():
        #     print(row['Time'])
        # by cols method
        print(table.cols.Time[1:5])

        # in-kernel selection
        sd = [row['HighestPrice'] for row in table.where("""(HighestPrice > 0)""")]
        print(sd)
        while True:
            pass


# write hdf5 use pandas package
# it easy to use but make hdf5 file big than csv.
class Csv2Hdf5Pd(object):
    def __init__(self, csvfile):
        self.csvfile = csvfile
        self.filename = os.path.split(csvfile)[-1].split('.')[0]
        print(self.filename)
        self.stocklist = []
        self.csvdf = pd.DataFrame()
        self.__gen_data_struct()
        self.__readcsv()

    def __gen_data_struct(self):
        for idx, v in enumerate(stock_quote):
            key = list(v.keys())[0]
            QuotesData.columns[key] = str2TbType(v[key], pos=idx)

    def __readcsv(self):
        df = pd.read_csv(self.csvfile)
        # print(df)
        df.rename(columns=ZN2EN_DICT, inplace=True)
        # print(df)

        # make stock code to 6 digit str.
        df['Code'] = df['Code'].apply(lambda x:str(x).zfill(6))

        self.stocklist = df['Code'].unique()
        self.csvdf = df

    def write_hdf5(self):
        print(self.csvdf.info())
        hdf5_db = pd.io.pytables.HDFStore(self.filename + "_pd_lg.h5", complevel=9, complib='bzip2')
        for stock in self.stocklist:
            hdf5_db["quote/"+stock] = self.csvdf[self.csvdf['Code'] == stock]

    @staticmethod
    def read_hdf5(h5file):
        hdf5_db = pd.io.pytables.HDFStore(h5file)
        # print(hdf5_db.info())
        print(hdf5_db["quote/000823"].info())


if __name__ == "__main__":
    pass