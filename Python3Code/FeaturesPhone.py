##############################################################
#                                                            #
#    Mark Hoogendoorn and Burkhardt Funk (2017)              #
#    Machine Learning for the Quantified Self                #
#    Springer                                                #
#    Chapter 4                                               #
#                                                            #
##############################################################

import sys
import copy
import pandas as pd
from pathlib import Path

from util.VisualizeDataset import VisualizeDataset
from Chapter4.TemporalAbstraction import NumericalAbstraction
from Chapter4.TemporalAbstraction import CategoricalAbstraction
from Chapter4.FrequencyAbstraction import FourierTransformation
from Chapter4.TextAbstraction import TextAbstraction

# Read the result from the previous chapter, and make sure the index is of the type datetime.
import pickle
from Load import *

# As usual, we set our program constants, read the input file and initialize a visualization object.
dataset = pd.read_csv(cluster_phone_data)
dataset.index = pd.to_datetime(dataset[time_col])


# Let us create our visualization class again.
DataViz = VisualizeDataset(__file__, show=False)

# Compute the number of milliseconds covered by an instance based on the first two rows
milliseconds_per_instance = (dataset.index[1] - dataset.index[0]).microseconds/1000


# Chapter 4: Identifying aggregate attributes.
print('attributes time domain')

# First we focus on the time domain.

# Set the window sizes to the number of instances representing 5 seconds, 30 seconds and 5 minutes
window_sizes = [int(float(5000)/milliseconds_per_instance), int(float(0.5*60000)/milliseconds_per_instance), int(float(5*60000)/milliseconds_per_instance)]

print('total window sizes', window_sizes)

NumAbs = NumericalAbstraction()

dataset_copy = copy.deepcopy(dataset)


periodic_predictor_cols = ['Acceleration x (m/s^2)', 'Acceleration y (m/s^2)', 'Acceleration z (m/s^2)', "Gyroscope x (rad/s)",
    "Gyroscope y (rad/s)", "Gyroscope z (rad/s)", ]

for ws in window_sizes:
    dataset_copy = NumAbs.abstract_numerical(dataset_copy, ['Acceleration x (m/s^2)'], ws, 'mean')
    dataset_copy = NumAbs.abstract_numerical(dataset_copy, ['Acceleration x (m/s^2)'], ws, 'std')
    print('window size', ws)

ws = int(float(0.5*60000)/milliseconds_per_instance)
dataset = NumAbs.abstract_numerical(dataset, periodic_predictor_cols, ws, 'mean')
dataset = NumAbs.abstract_numerical(dataset, periodic_predictor_cols, ws, 'std')


print('temporal', dataset.shape)

print('attributes frequency domain')

# Now we move to the frequency domain, with the same window size.

FreqAbs = FourierTransformation()
fs = float(1000)/milliseconds_per_instance

print('frequency', dataset.shape)
# Spectral analysis.

dataset = FreqAbs.abstract_frequency(dataset, periodic_predictor_cols, int(float(10000)/milliseconds_per_instance), fs)

print('frequency all col', dataset.shape)
for col in dataset.columns:
    print(col, dataset[dataset[col].isna() == True].count())
# Now we only take a certain percentage of overlap in the windows, otherwise our training examples will be too much alike.

pickle.dump(dataset, open('concat_no_skipping.pkl', 'wb'))
# The percentage of overlap we allow
window_overlap = 0.9
skip_points = int((1-window_overlap) * ws)
dataset = dataset.iloc[::skip_points,:]
dataset.to_csv(features_phone_data)
print(dataset.shape)
