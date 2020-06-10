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


dataset = pickle.load(open('datasets\dataframes\concat_df_gran_250.pkl', 'rb'))
dataset.index = pd.to_datetime(dataset.index)
DataViz = VisualizeDataset(__file__)


milliseconds_per_instance = (dataset.index[1] - dataset.index[0]).microseconds/1000
MisVal = ImputationMissingValues()
KalFilter = KalmanFilters()
print(dataset['Gyroscope x (rad/s)'].isna().count())
imputed_interpolation_dataset = MisVal.impute_interpolate(copy.deepcopy(dataset), 'Gyroscope x (rad/s)')
print(imputed_interpolation_dataset['Gyroscope x (rad/s)'].isna().count())
imputed_interpolation_dataset = MisVal.impute_interpolate(copy.deepcopy(imputed_interpolation_dataset), 'Gyroscope y (rad/s)')
imputed_interpolation_dataset = MisVal.impute_interpolate(copy.deepcopy(imputed_interpolation_dataset), 'Gyroscope z (rad/s)')
# dataset = KalFilter.apply_kalman_filter(dataset, 'Gyroscope x (rad/s)')
# dataset = KalFilter.apply_kalman_filter(dataset, 'Gyroscope y (rad/s)')
# dataset = KalFilter.apply_kalman_filter(dataset, 'Gyroscope z (rad/s)')

pickle.dump(imputed_interpolation_dataset, open('datasets\dataframes\concat_df_imputed_gyro.pkl', 'wb'))