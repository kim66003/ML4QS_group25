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
data_file = 'chapter3_result_outliers.csv'


class OutlierExperiment:
    def __init__(self, data_path, data_file):
        dataset = pd.read_csv(Path(data_path / data_file), index_col=0)
        dataset.index = pd.to_datetime(dataset.index)