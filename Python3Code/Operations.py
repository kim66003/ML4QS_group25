
import copy
import numpy as np
import pandas as pd
import pickle

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

if __name__ == '__main__':
    dataset = pickle.load(open('concat_no_skipping.pkl', 'rb'))
    # dataset.index = pd.to_datetime(dataset.index)
    # print(dataset.columns)
    # print(dataset.shape)
    dataset = rename(dataset)
    print(dataset.columns)