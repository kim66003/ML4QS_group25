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

dataset.add_numerical_dataset('heart_rate_smartwatch.csv', 'timestamps', ['rate'], 'avg', 'hr_watch_', None)

dataset.add_event_dataset('labels.csv', 'label_start', 'label_end', 'label', 'binary')

dataset.add_numerical_dataset('light_phone.csv', 'timestamps', ['lux'], 'avg', 'light_phone_', None)

dataset.add_numerical_dataset('magnetometer_phone.csv', 'timestamps', ['x','y','z'], 'avg', 'mag_phone_', None)
dataset.add_numerical_dataset('magnetometer_smartwatch.csv', 'timestamps', ['x','y','z'], 'avg', 'mag_watch_', None)

dataset.add_numerical_dataset('pressure_phone.csv', 'timestamps', ['pressure'], 'avg', 'press_phone_', None)

dataset = dataset.data_table
print(dataset['labelWalking'])
# Plot the data
DataViz = VisualizeDataset(__file__)

# Boxplot
DataViz.plot_dataset_boxplot(dataset, ['acc_phone_x','acc_phone_y','acc_phone_z','acc_watch_x','acc_watch_y','acc_watch_z'])

# Plot all data
DataViz.plot_dataset(dataset, ['acc_', 'gyr_', 'hr_watch_rate', 'light_phone_lux', 'mag_', 'press_phone_', 'label'],
                              ['like', 'like', 'like', 'like', 'like', 'like', 'like','like'],
                              ['line', 'line', 'line', 'line', 'line', 'line', 'points', 'points'])

# And print a summary of the dataset.
util.print_statistics(dataset)

