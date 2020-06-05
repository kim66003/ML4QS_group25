from crowdsignals_ch3_outliers import *
from util.VisualizeDataset import VisualizeDataset
from Chapter3.OutlierDetection import DistributionBasedOutlierDetection
from Chapter3.OutlierDetection import DistanceBasedOutlierDetection
import sys
import copy
import pandas as pd
import numpy as np
from pathlib import Path

data_path = Path('./intermediate_datafiles/')
data_file = 'chapter2_result.csv'

class OutlierExperiment:
    def __init__(self, data_path, data_file):
        self.dataset = pd.read_csv(Path(data_path / data_file), index_col=0)
        self.dataset =  self.dataset[:14780]
        self.dataset.index = pd.to_datetime(self.dataset.index)
        self.DataViz = VisualizeDataset(__file__, show=False)
        self.outlier_columns = ['acc_phone_x', 'light_phone_lux']
        self.OutlierDistr = DistributionBasedOutlierDetection()
        self.OutlierDist = DistanceBasedOutlierDetection()
        self.original_columns = self.dataset.columns
        self.num_outliers = {'acc_phone_x': 0, 'light_phone_lux': 0}

    def remove_columns(self):
        for to_remove in self.dataset.columns:
            if to_remove not in self.original_columns:
                del self.dataset[to_remove]

    def chauvenet(self, C):
        original_columns = self.dataset.columns
        for col in self.outlier_columns:
            print(f"Applying outlier criteria for column {col}")
            self.dataset = self.OutlierDistr.chauvenet(self.dataset, col, C)
            self.DataViz.plot_binary_outliers(self.dataset, col, col + '_outlier')
            self.num_outliers[col] = self.dataset[self.dataset[col + '_outlier'] == 1][col].size / self.dataset[
                col].size

    def mixture_model(self, n):
        for col in self.outlier_columns:
            print(f"Applying outlier criteria for column {col}")
            self.dataset = self.OutlierDistr.mixture_model(self.dataset, col, n)
            self.DataViz.plot_dataset(self.dataset, [col, col + '_mixture'], ['exact','exact'], ['line', 'points'])
            self.num_outliers[col] = self.dataset[col + '_mixture'].sum() / self.dataset[col].size

    def simple_distance_based(self, d_min, f_min):
        for col in self.outlier_columns:
            print(f"Applying outlier criteria for column {col}")
            self.dataset = self.OutlierDist.simple_distance_based(self.dataset, [col], 'euclidean', d_min, f_min)
            self.DataViz.plot_binary_outliers(self.dataset, col, 'simple_dist_outlier')
            self.num_outliers[col] = self.dataset[self.dataset['simple_dist_outlier'] == 1][col].size / self.dataset[
                col].size
            self.remove_columns()

    def local_outlier_factor(self, k):
        for col in self.outlier_columns:
            print(f"Applying outlier criteria for column {col}")
            self.dataset = self.OutlierDist.local_outlier_factor(self.dataset, [col], 'euclidean', k)
            self.DataViz.plot_dataset(self.dataset, [col, 'lof'], ['exact','exact'], ['line', 'points'])
            self.num_outliers[col] = self.dataset[self.dataset['lof'] == 1][col].size / self.dataset[
                col].size
            self.remove_columns()


if __name__ == '__main__':

    # experiment = OutlierExperiment(data_path, data_file)
    # experiment.chauvenet(2)
    # experiment.mixture_model(1)
    # print(experiment.num_outliers)
    # exit()
    # c_values = [1, 1.5, 2, 5, 7.5, 10, 20]
    # for c in c_values:
    #     experiment.chauvenet(c)
    #     print('chauvenet c=%d'%c, experiment.num_outliers)
    #     experiment.remove_columns()

    experiment = OutlierExperiment(data_path, data_file)
    d_mins = [0.1, 0.3, 0.5]
    f_mins = [0.99, 0.8, 0.6]
    output = []

    for d in d_mins:
        for f in f_mins:
            print('Experimenting with d=%f, f=%f' % (d, f))
            experiment.simple_distance_based(d, f)
            output.append(str([d, f, experiment.num_outliers]))
            experiment.remove_columns()

    print('Local Outlier Factor')

    ks = [4, 5, 6, 7]
    for k in ks:
        print('Experimenting with k=%f' % k)
        experiment.local_outlier_factor(k)
        output.append(str([k, experiment.num_outliers]))
        experiment.remove_columns()

    with open('results/1_3_output.txt','w+') as f:
        f.write(str(output))
