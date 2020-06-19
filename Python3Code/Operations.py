
import copy
import numpy as np
import pandas as pd
import pickle
from Load import *

rename_dict = {
        'Acceleration x (m/s^2)': 'acc_x',
                    'Acceleration y (m/s^2)': 'acc_y',
                  'Acceleration z (m/s^2)': 'acc_z',
                  "Gyroscope x (rad/s)": 'gyr_x',
        "Gyroscope y (rad/s)": 'gyr_y',
        "Gyroscope z (rad/s)": 'gyr_z',

    }

def rename(dataset):
    rename_dict = {
        'Acceleration x (m/s^2)': 'acc_x',
                    'Acceleration y (m/s^2)': 'acc_y',
                  'Acceleration z (m/s^2)': 'acc_z',
                  "Gyroscope x (rad/s)": 'gyr_x',
        "Gyroscope y (rad/s)": 'gyr_y',
        "Gyroscope z (rad/s)": 'gyr_z',

        "Magnetic field x (µT)": 'mag_x',
                  "Magnetic field y (µT)": 'mag_y',
                  "Magnetic field z (µT)": 'mag_z'
    }
    for col in dataset.columns:
        if 'Linear' in col:
            dataset = dataset.rename(columns={
                col: col.replace('Linear ', 'l')
            })
    for col in dataset.columns:
        for name in rename_dict.keys():
            if name in col or col == name:
                dataset = dataset.rename(columns={
                    col: col.replace(name, rename_dict[name])
                })
    return dataset

def rename_like(path, rename_dict, suffix):
    dataset = pd.read_csv(path)
    columns_to_save = [col for col in dataset.columns if suffix in col or col not in rename_dict.keys()]
    dataset = dataset[columns_to_save]
    dataset = dataset.rename(columns = {
        x + suffix: rename_dict[x] for x in rename_dict.keys()
    })
    dataset.to_csv(path)
    print(dataset.columns)

if __name__ == '__main__':
    # df1 = pd.read_csv(outlier_watch_data)
    # df2 = pd.read_csv(outlier_phone_data)
    # print(pd.concat([df1, df2]).drop_duplicates(keep=False))
    rename_like(outlier_phone_data, rename_dict, '_kalman')
    rename_like(outlier_watch_data, rename_dict, '_kalman')
