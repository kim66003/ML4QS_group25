import pickle
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


dataset = pickle.load(open('datasets\dataframes\df_concat_with_labels.pkl', 'rb'))
dataset.index = pd.to_datetime(dataset.index)
DataViz = VisualizeDataset(__file__)

attributes_to_impute = [
"Acceleration x (m/s^2)","Acceleration y (m/s^2)","Acceleration z (m/s^2)",
"Magnetic field x (µT)","Magnetic field y (µT)","Magnetic field z (µT)",
"Gyroscope x (rad/s)","Gyroscope y (rad/s)","Gyroscope z (rad/s)",
"Linear Acceleration x (m/s^2)","Linear Acceleration y (m/s^2)","Linear Acceleration z (m/s^2)",

]

milliseconds_per_instance = (dataset.index[1] - dataset.index[0]).microseconds/1000
MisVal = ImputationMissingValues()
KalFilter = KalmanFilters()
print(dataset['Gyroscope x (rad/s)'].isnull().sum())
for attribute in attributes_to_impute:
    dataset = MisVal.impute_interpolate(copy.deepcopy(dataset), attribute)

# dataset = KalFilter.apply_kalman_filter(dataset, 'Gyroscope x (rad/s)')
# dataset = KalFilter.apply_kalman_filter(dataset, 'Gyroscope y (rad/s)')
# dataset = KalFilter.apply_kalman_filter(dataset, 'Gyroscope z (rad/s)')

pickle.dump(dataset, open('datasets\dataframes\concat_imputed.pkl', 'wb'))