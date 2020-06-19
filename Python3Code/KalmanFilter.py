import sys
import copy
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from util.VisualizeDataset import VisualizeDataset
from Chapter3.DataTransformation import LowPassFilter
from Chapter3.DataTransformation import PrincipalComponentAnalysis
from Chapter3.ImputationMissingValues import ImputationMissingValues
from Chapter3.KalmanFilters import KalmanFilters
from Load import *

attributes_to_impute = [
"Acceleration x (m/s^2)","Acceleration y (m/s^2)","Acceleration z (m/s^2)",
"Gyroscope x (rad/s)","Gyroscope y (rad/s)","Gyroscope z (rad/s)",

]

save_names = {
    "Acceleration x (m/s^2)": 'acc_x',
    "Acceleration y (m/s^2)": 'acc_y',
    "Acceleration z (m/s^2)": 'acc_z',
    "Gyroscope x (rad/s)": 'gyr_x',
    "Gyroscope y (rad/s)": 'gyr_y',
    "Gyroscope z (rad/s)": 'gyr_z',
}

DataViz = VisualizeDataset(__file__, show=False)
KalFilter = KalmanFilters()

dataset = pd.read_csv(preprocessed_phone_data)
dataset.index = pd.to_datetime(dataset[time_col])

for col in attributes_to_impute:
    print('Applying kalman filter for ', col)
    dataset = KalFilter.apply_kalman_filter(dataset, col)
    DataViz.save_path = save_names[col] + '_phone_imputed_values'
    DataViz.plot_imputed_values(dataset, ['original', 'kalman'], col, dataset[col])
    DataViz.save_path = save_names[col] + '_phone_all_data'
    DataViz.plot_dataset(dataset, [col, col + '_kalman'], ['exact','exact'], ['line', 'line'])

print(dataset.columns)
dataset.to_csv(outlier_phone_data)

dataset = pd.read_csv(preprocessed_watch_data)
dataset.index = pd.to_datetime(dataset[time_col])

for col in attributes_to_impute:
    print('Applying kalman filter for ', col)
    dataset = KalFilter.apply_kalman_filter(dataset, col)
    DataViz.save_path = save_names[col] + '_watch_imputed_values'
    DataViz.plot_imputed_values(dataset, ['original', 'kalman'], col, dataset[col])
    DataViz.save_path = save_names[col] + '_watch_all_data'
    DataViz.plot_dataset(dataset, [col, col + '_kalman'], ['exact','exact'], ['line', 'line'])

print(dataset.columns)
dataset.to_csv(outlier_watch_data)
