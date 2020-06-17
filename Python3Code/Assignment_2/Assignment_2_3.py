
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
import pickle
from Chapter5.Clustering import NonHierarchicalClustering, HierarchicalClustering

dataset = pickle.load(open('datasets/dataframes/concat_imputed.pkl', 'rb'))
DATA_PATH = Path('datasets/dataframes')
DATASET_FNAME = 'chapter5_result.csv'
RESULT_FNAME = 'chapter7_classification_result.csv'
EXPORT_TREE_PATH = Path('./figures/crowdsignals_ch7_classification/')

clusteringNH = NonHierarchicalClustering()
clusteringH = HierarchicalClustering()

attributes = [
"Acceleration x (m/s^2)","Acceleration y (m/s^2)","Acceleration z (m/s^2)",
"Magnetic field x (µT)","Magnetic field y (µT)","Magnetic field z (µT)",
"Gyroscope x (rad/s)","Gyroscope y (rad/s)","Gyroscope z (rad/s)",
"Linear Acceleration x (m/s^2)","Linear Acceleration y (m/s^2)","Linear Acceleration z (m/s^2)",

]

k_values = range(2, 3)
silhouette_values = []

for k in k_values:
    print(f'k = {k}')
    dataset_cluster, l = clusteringH.agglomerative_over_instances(copy.deepcopy(dataset),
                                                                  attributes, k,
                                                                  'euclidean', use_prev_linkage=True,
                                                                  link_function='ward')
    silhouette_score = dataset_cluster['silhouette'].mean()
    print(f'silhouette = {silhouette_score}')
    silhouette_values.append(silhouette_score)

prepare = PrepareDatasetForLearning()
print(dataset_cluster.shape)
print(dataset_cluster.columns)
# dataset_cluster = dataset.rename(columns = {'label': 'class'})
train_X, test_X, train_y, test_y = prepare.split_single_dataset_classification(
    dataset_cluster, ['label'], 'like', 0.7,  filter=True, temporal=False)
