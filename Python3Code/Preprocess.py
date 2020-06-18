from Load import *

from Chapter2.CreateDataset_new import CreateDataset
from util.VisualizeDataset import VisualizeDataset
from util import util
from pathlib import Path
import copy
import os
import sys
import pickle
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from tqdm import tqdm
from functools import reduce

class Preprocess:
    def __init__(self, granularity=250):
        self.data = CreateDataset('', granularity)



    def process_dataset(self, device_index=0, user_index=0):
        previous_table = self.data.data_table.copy() if self.data.data_table is not None else None
        self.data.data_table = load_to_dataframe(datasets[device_index][user_index])
        self.data.data_table['timestamp'] = pd.to_datetime(self.data.data_table['timestamp'])
        prefix = ['acc_phone_', 'gyr_phone_', 'acc_watch_', 'gyr_watch_'][user_index]
        for label in labels.values():
            self.data.data_table['label_' + label] = 0
        for i in tqdm(self.data.data_table.index):
            self.data.data_table.loc[i, 'label_' + labels[self.data.data_table.loc[i,'activity']]] = 1
        print('Aggregating data')
        self.data.add_numerical_dataset('', ['x', 'y', 'z'], 'avg', prefix=prefix[user_index], time_col='timestamp')
        if previous_table is not None:
            self.data.data_table = reduce(lambda x, y: pd.merge(x, y, left_index=True, right_index=True, how='outer'),
                                 [previous_table, self.data.data_table])

    def save(self, file):
        self.data.data_table.to_csv('')

# combine users

preprocess = Preprocess(granularity=250) # t=500
preprocess.process_dataset(0, 0)
preprocess.process_dataset(1, 0)
# for i in range(len(datasets)):
#     preprocess.process_dataset(i, 0)
preprocess.data.data_table.describe()
# data = CreateDataset('', 250, data_table=load_to_dataframe(datasets[0][0]))
# data.add_numerical_dataset('', 'timestamp', ['x','y','z'], 'avg', 'acc_phone_')
# print(data.data_table)