import sys
import copy
import pandas as pd
from pathlib import Path

from util.VisualizeDataset import VisualizeDataset
from Chapter4.TemporalAbstraction import NumericalAbstraction
from Chapter4.TemporalAbstraction import CategoricalAbstraction
from Chapter4.FrequencyAbstraction import FourierTransformation
from Chapter4.TextAbstraction import TextAbstraction
import re
import matplotlib.pyplot as plt

DATA_PATH = Path('./intermediate_datafiles/')
DATASET_FNAME = 'chapter3_result_final.csv'
RESULT_FNAME = 'chapter4_result.csv'
categorical_abstraction_result_file = 'chapter4_categorical_result.csv'
task = 'frequency_plot'

dataset = pd.read_csv(DATA_PATH / DATASET_FNAME, index_col=0)
dataset.index = pd.Series({x: pd.to_datetime(x) for x in dataset.index})
DataViz = VisualizeDataset(__file__, show=False)
milliseconds_per_instance = (dataset.index[1] - dataset.index[0]).microseconds/1000

if task == 'frequency_plot':
    fs = float(1000) / milliseconds_per_instance
    FreqAbs = FourierTransformation()
    data_table = FreqAbs.abstract_frequency(copy.deepcopy(dataset), ['acc_phone_x'], int(float(10000)/milliseconds_per_instance), fs)
    frequencies = []
    values = []
    for col in data_table.columns:
        val = re.findall(r'freq_\d+\.\d+_Hz', col)
        if len(val) > 0:
            frequency = float((val[0])[5:len(val) - 4])
            frequencies.append(frequency)
            values.append(data_table.loc[data_table.index, col])

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.xlim([0, 5])
    ax1.plot(frequencies, values, 'b+')
    ax1.set_xlabel('Frequency (Hz)')
    ax1.set_ylabel('$a$')
    plt.show()
    plt.savefig('figures/crowdsignals_ch4/figure_2.png')

    exit()

print('milliseconds per instance', milliseconds_per_instance)

window_sizes = [int(float(5000)/milliseconds_per_instance), int(float(0.5*60000)/milliseconds_per_instance), int(float(5*60000)/milliseconds_per_instance)]

print('window sizes', window_sizes)

NumAbs = NumericalAbstraction()
CatAbs = CategoricalAbstraction()
dataset_copy = copy.deepcopy(dataset)

for ws in window_sizes:
    dataset_copy = NumAbs.abstract_numerical(dataset_copy, ['acc_phone_x'], ws, 'min')
    dataset_copy = NumAbs.abstract_numerical(dataset_copy, ['acc_phone_x'], ws, 'max')
    print('window size', ws)

DataViz.plot_dataset(dataset_copy, ['acc_phone_x', 'acc_phone_x_temp_min', 'label'],
                     ['exact', 'like', 'like'], ['line', 'line', 'points'])
DataViz.plot_dataset(dataset_copy, ['acc_phone_x', 'acc_phone_x_temp_max', 'label'],
                     ['exact', 'like', 'like'], ['line', 'line', 'points'])
DataViz.plot_dataset(dataset_copy, ['acc_phone_x', 'acc_phone_x_temp_max','acc_phone_x_temp_min', 'label'],
                     ['exact', 'like', 'like', 'like'], ['line', 'line', 'line', 'points'])

dataset_copy.to_csv(DATA_PATH / RESULT_FNAME)

dataset_copy = copy.deepcopy(dataset)
print('Cat Abs')
dataset = CatAbs.abstract_categorical(dataset_copy, ['label'], ['like'], 0.03, int(float(5*60000)/milliseconds_per_instance), 2)

dataset_copy.to_csv(DATA_PATH / categorical_abstraction_result_file)
