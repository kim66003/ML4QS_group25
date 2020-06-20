
import os
import copy
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from Chapter7.PrepareDatasetForLearning import PrepareDatasetForLearning
from Chapter7.LearningAlgorithms import ClassificationAlgorithms
from Chapter7.LearningAlgorithms import RegressionAlgorithms
from Chapter7.Evaluation import ClassificationEvaluation
from Chapter7.Evaluation import RegressionEvaluation
from Chapter7.FeatureSelection import FeatureSelectionClassification
from Chapter7.FeatureSelection import FeatureSelectionRegression
from util import util
from util.VisualizeDataset import VisualizeDataset
from datetime import datetime
from Load import *


N_FORWARD_SELECTION = 20

# datetime object containing current date and time
begin = datetime.now()
# dd/mm/YY H:M:S
dt_string = begin.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string)

dataset = pd.read_csv(features_phone_data, index_col=time_col)
DataViz = VisualizeDataset(__file__, show=False)

dataset.index = pd.to_datetime(dataset.index)

prepare = PrepareDatasetForLearning()
train_X, test_X, train_y, test_y = prepare.split_single_dataset_classification(dataset, ['label'], 'like', 0.7,
                                                                               filter=False, temporal=False,
                                                                               drop_na=False, fill_na=True)

basic_features = ['acc_x', 'acc_y', 'acc_z', "gyr_x",
    "gyr_y", "gyr_z", ]
time_features = [name for name in dataset.columns if '_temp' in name]
freq_features = [name for name in dataset.columns if (('_freq' in name) or ('_pse' in name))]
cluster_features = ['cluster']
features_after_chapter_3 = list(set().union(basic_features, time_features))
features_after_chapter_4 = list(set().union(basic_features, time_features, freq_features))
features_after_chapter_5 = list(set().union(basic_features, time_features, freq_features, cluster_features))

fs = FeatureSelectionClassification()
features, ordered_features, ordered_scores = fs.forward_selection(N_FORWARD_SELECTION,
                                                                  train_X[features_after_chapter_5], train_y)
print(ordered_scores)
print(ordered_features)
DataViz.plot_xy(x=[range(1, N_FORWARD_SELECTION+1)], y=[ordered_scores],
                xlabel='number of features', ylabel='accuracy')

