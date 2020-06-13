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

# As usual, we set our program constants, read the input file and initialize a visualization object.
dataset = pickle.load(open('concat_clustered.pkl', 'rb'))
dataset.index = pd.to_datetime(dataset.index)


# Let us create our visualization class again.
DataViz = VisualizeDataset(__file__)

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
for ws in window_sizes:
    dataset_copy = NumAbs.abstract_numerical(dataset_copy, ['Acceleration x (m/s^2)'], ws, 'mean')
    dataset_copy = NumAbs.abstract_numerical(dataset_copy, ['Acceleration x (m/s^2)'], ws, 'std')
    print('window size', ws)

ws = int(float(0.5*60000)/milliseconds_per_instance)
selected_predictor_cols = [c for c in dataset.columns if not 'label' in c]
dataset = NumAbs.abstract_numerical(dataset, selected_predictor_cols, ws, 'mean')
dataset = NumAbs.abstract_numerical(dataset, selected_predictor_cols, ws, 'std')


print('temporal', dataset.shape)

print('attributes frequency domain')

# Now we move to the frequency domain, with the same window size.

FreqAbs = FourierTransformation()
fs = float(1000)/milliseconds_per_instance
periodic_predictor_cols = ['Acceleration x (m/s^2)', 'Acceleration y (m/s^2)', 'Acceleration z (m/s^2)', "Gyroscope x (rad/s)",
    "Gyroscope y (rad/s)", "Gyroscope z (rad/s)", "Linear Acceleration x (m/s^2)","Linear Acceleration y (m/s^2)",
    "Linear Acceleration z (m/s^2)", "Magnetic field x (µT)","Magnetic field y (µT)","Magnetic field z (µT)"]
data_table = FreqAbs.abstract_frequency(copy.deepcopy(dataset), ['Acceleration x (m/s^2)'], int(float(10000)/milliseconds_per_instance), fs)

print('frequency', dataset.shape)
# Spectral analysis.
print(data_table.shape)

dataset = FreqAbs.abstract_frequency(dataset, periodic_predictor_cols, int(float(10000)/milliseconds_per_instance), fs)

print('frequency all col', dataset.shape)
for col in dataset.columns:
    print(col, dataset[dataset[col].isna() == True].count())
exit()
# Now we only take a certain percentage of overlap in the windows, otherwise our training examples will be too much alike.

# The percentage of overlap we allow
window_overlap = 0.9
skip_points = int((1-window_overlap) * ws)
dataset = dataset.iloc[::skip_points,:]


pickle.dump(dataset, open('concat_frequency.pkl', 'wb'))
