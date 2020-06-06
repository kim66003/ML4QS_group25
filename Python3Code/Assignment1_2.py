from Chapter2.CreateDataset import CreateDataset
from util.VisualizeDataset import VisualizeDataset
from util import util
from pathlib import Path
import copy
import os
import sys

DATASET_PATH = './datasets/crowdsignals/csv-participant-one/'
RESULT_PATH = './intermediate_datafiles/'
RESULT_FNAME = sys.argv[2] if len(sys.argv) > 2 else 'chapter2_result.csv'

dataset = CreateDataset(DATASET_PATH, 250)

dataset.add_numerical_dataset('accelerometer_phone.csv', 'timestamps', ['x','y','z'], 'avg', 'acc_phone_', None)
dataset.add_numerical_dataset('accelerometer_smartwatch.csv', 'timestamps', ['x','y','z'], 'avg', 'acc_watch_', None)

dataset.add_numerical_dataset('gyroscope_phone.csv', 'timestamps', ['x','y','z'], 'avg', 'gyr_phone_', None)
dataset.add_numerical_dataset('gyroscope_smartwatch.csv', 'timestamps', ['x','y','z'], 'avg', 'gyr_watch_', None)

dataset.add_event_dataset('labels.csv', 'label_start', 'label_end', 'label', 'binary')

dataset = dataset.data_table
dataset_walking = dataset[dataset['labelWalking'] == 1]
dataset_sitting = dataset[dataset['labelSitting'] == 1]
dataset_running = dataset[dataset['labelRunning'] == 1]
print(dataset['labelWalking'])
# Plot the data
DataViz = VisualizeDataset(__file__)

# Boxplot
DataViz.plot_dataset_boxplot(dataset_walking, ['acc_phone_x','acc_phone_y','acc_phone_z',])
DataViz.plot_dataset_boxplot(dataset_sitting, ['acc_phone_x','acc_phone_y','acc_phone_z',])
DataViz.plot_dataset_boxplot(dataset_running, ['acc_phone_x','acc_phone_y','acc_phone_z',])

# # Plot all data
# DataViz.plot_dataset(dataset, ['acc_', 'gyr_',  'label'],
#                               ['like', 'like', 'like', ],
#                               ['line', 'line', 'line', ])

# And print a summary of the dataset.
print(dataset.columns)
# print(dataset['acc_phone_x'].max(), dataset['acc_phone_y'].max(), dataset['acc_phone_z'].max())
print(dataset['acc_phone_x'].min(), dataset['acc_phone_y'].min(), dataset['acc_phone_z'].min())
print(dataset['acc_phone_x'].mean(), dataset['acc_phone_y'].mean(), dataset['acc_phone_z'].mean())
print(dataset['acc_phone_x'].std(), dataset['acc_phone_y'].std(), dataset['acc_phone_z'].std())
util.print_statistics(dataset_walking, describe=True)
util.print_statistics(dataset_sitting, describe=True)
util.print_statistics(dataset_running, describe=True)

