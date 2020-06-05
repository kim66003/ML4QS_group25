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
        self.dataset.index = pd.to_datetime(self.dataset.index)
        self.DataViz = VisualizeDataset(__file__)
        self.outlier_columns = ['acc_phone_x', 'light_phone_lux']
        self.OutlierDistr = DistributionBasedOutlierDetection()
        self.OutlierDist = DistanceBasedOutlierDetection()

    def chauvenet(self, C):
        for col in self.outlier_columns:
            print(f"Applying outlier criteria for column {col}")
            dataset = self.OutlierDistr.chauvenet(self.dataset, col, C)
            self.DataViz.plot_binary_outliers(dataset, col, col + '_outlier')

    def mixture_model(self, n):
        for col in self.outlier_columns:
            print(f"Applying outlier criteria for column {col}")
            dataset = self.OutlierDistr.mixture_model(self.dataset, col, n)
            self.DataViz.plot_binary_outliers(dataset, col, col + '_outlier')

    



experiment = OutlierExperiment(data_path, data_file)
experiment.chauvenet(4)