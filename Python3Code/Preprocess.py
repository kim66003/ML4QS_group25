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

    def create_labels(self, device_index=0, user_index=0):
        label_columns = ['sensor_type', 'device_type', 'label', 'label_start', 'label_start_datetime', 'label_end', 'label_end_datetime']
        self.data.data_table = load_to_dataframe(datasets[device_index][user_index])
        label_data = []
        current_label = None
        print('Creating labels')
        for i in tqdm(self.data.data_table.index):
            if self.data.data_table.loc[i]['activity'] != current_label:
                current_label = self.data.data_table.loc[i]['activity']
                label_data.append([
                    'interval_label', '-', current_label, '-', str(self.data.data_table.loc[i]['timestamp']), '-', '-',
                ])
                if i > 0:
                    label_data[-2][-1] = str(self.data.data_table.loc[i - 1]['timestamp'])
            if i == len(self.data.data_table.index) - 1 and len(label_data) > 0:
                label_data[-1][-1] = str(self.data.data_table.loc[i - 1]['timestamp'])
        return pd.DataFrame(label_data, columns=label_columns, )


    def process_dataset(self, device_index=0, user_index=0):
        previous_table = self.data.data_table.copy() if self.data.data_table is not None else None
        self.data.data_table = load_to_dataframe(datasets[device_index][user_index])
        self.data.data_table['timestamp'] = pd.to_datetime(self.data.data_table['timestamp'])
        prefix = ['acc_phone_', 'gyr_phone_', 'acc_watch_', 'gyr_watch_'][user_index]
        # for label in labels.values():
        #     self.data.data_table['label_' + label] = 0
        # print(self.data.data_table['timestamp'])
        # print('Making labels')
        # for i in tqdm(self.data.data_table.index):
        #     self.data.data_table.loc[i, 'label_' + labels[self.data.data_table.loc[i,'activity']]] = 1
        # print(self.data.data_table)
        # print(self.data.data_table.isna().sum())
        print('Aggregating data')
        self.data.add_numerical_dataset('', ['x', 'y', 'z'], 'avg', prefix=prefix[user_index], time_col='timestamp')
        self.data.merge_datasets()
        self.data.data_table.index = self.data.data_table['timestamp']
        labels_dataframe = self.create_labels(device_index, user_index)
        print(self.data.data_table.index)
        self.data.add_event_dataset(
            '', 'label_start_datetime', 'label_end_datetime', 'label','binary', from_file=False, dataset=labels_dataframe
        )
        if previous_table is not None:
            self.data.data_table = reduce(lambda x, y: pd.merge(x, y, left_index=True, right_index=True, how='outer'),
                                 [previous_table, self.data.data_table])

    def one_hot_labels(self, file=None):
        if file is not None:
            self.data.data_table = pd.read_csv(file)
        for label in labels.values():
            self.data.data_table['label_' + label] = 0
        print(self.data.data_table['timestamp'])
        print('Making labels')
        for i in tqdm(self.data.data_table.index):
            self.data.data_table.loc[i, 'label_' + labels[self.data.data_table.loc[i,'activity']]] = 1
        print(self.data.data_table)
        print(self.data.data_table.isna().sum())

    def save(self, file):
        self.data.data_table = self.data.data_table.dropna()
        self.data.data_table.to_csv(file)

# combine users

preprocess = Preprocess(granularity=250) # t=500
preprocess.one_hot_labels('intermediate_datafiles\preprocessed_phone_data_person_21.csv')
preprocess.save(preprocessed_phone_data)
preprocess.one_hot_labels('intermediate_datafiles\preprocessed_watch_data_person_21.csv')
preprocess.save(preprocessed_watch_data)
