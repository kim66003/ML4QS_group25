from Chapter5.DistanceMetrics import InstanceDistanceMetrics
from Chapter5.DistanceMetrics import PersonDistanceMetricsNoOrdering
from Chapter5.DistanceMetrics import PersonDistanceMetricsOrdering
from Chapter5.Clustering import NonHierarchicalClustering
from Chapter5.Clustering import HierarchicalClustering
import util.util as util
from util.VisualizeDataset import VisualizeDataset

import sys
import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# As usual, we set our program constants, read the input file and initialize a visualization object.

all_data = True if len(sys.argv) > 1 else False

DATA_PATH = Path('./intermediate_datafiles/')
DATASET_FNAME = sys.argv[1] if len(sys.argv) > 1 else 'chapter4_result.csv'
RESULT_FNAME = sys.argv[2] if len(sys.argv) > 2 else 'chapter5_result.csv'

try:
    dataset = pd.read_csv(DATA_PATH / DATASET_FNAME, index_col=0)
    if not all_data:
        dataset = dataset[:14780]
    dataset.index = pd.to_datetime(dataset.index)
except IOError as e:
    print('File not found, try to run previous crowdsignals scripts first!')
    raise e

DataViz = VisualizeDataset(__file__)

# We'll start by applying non-hierarchical clustering.
clusteringNH = NonHierarchicalClustering()


# Let us look at k-means first.
k_values = range(2, 10)
silhouette_values = []
attributes_to_cluster = ['gyr_phone_x','gyr_phone_y','gyr_phone_z']
## Do some initial runs to determine the right number for k

print('===== kmeans clustering =====')
for k in k_values:
    print(f'k = {k}')
    dataset_cluster = clusteringNH.k_means_over_instances(copy.deepcopy(dataset), attributes_to_cluster, k, 'default', 20, 10)
    silhouette_score = dataset_cluster['silhouette'].mean()
    print(f'silhouette = {silhouette_score}')
    silhouette_values.append(silhouette_score)

DataViz.plot_xy(x=[k_values], y=[silhouette_values], xlabel='k', ylabel='silhouette score',
                ylim=[0,1], line_styles=['b-'])

# And run the knn with the highest silhouette score

# k = 6 # todo: replaced with np.argmax call over silhouette scores
k = k_values[np.argmax(silhouette_values)]
print(f'Highest K-Means silhouette score: k = {k}')

dataset_knn = clusteringNH.k_means_over_instances(copy.deepcopy(dataset), attributes_to_cluster, k, 'default', 50, 50)
DataViz.plot_clusters_3d(dataset_knn, attributes_to_cluster, 'cluster', ['label'])
DataViz.plot_silhouette(dataset_knn, 'cluster', 'silhouette')
util.print_latex_statistics_clusters(dataset_knn, 'cluster', attributes_to_cluster, 'label')
del dataset_knn['silhouette']

k_values = range(2, 10)
silhouette_values = []


print('===== k medoids clustering =====')
for k in k_values:
    print(f'k = {k}')
    dataset_cluster = clusteringNH.k_medoids_over_instances(copy.deepcopy(dataset), attributes_to_cluster, k, 'default', 20, n_inits=10)
    silhouette_score = dataset_cluster['silhouette'].mean()
    print(f'silhouette = {silhouette_score}')
    silhouette_values.append(silhouette_score)

DataViz.plot_xy(x=[k_values], y=[silhouette_values], xlabel='k', ylabel='silhouette score',
                ylim=[0,1], line_styles=['b-'])

# And run k medoids with the highest silhouette score

# k = 6 # todo: replaced with np.argmax call over silhouette scores
k = k_values[np.argmax(silhouette_values)]
print(f'Highest K-Medoids silhouette score: k = {k}')

dataset_kmed = clusteringNH.k_medoids_over_instances(copy.deepcopy(dataset), attributes_to_cluster, k, 'default', 20, n_inits=50)
DataViz.plot_clusters_3d(dataset_kmed, attributes_to_cluster, 'cluster', ['label'])
DataViz.plot_silhouette(dataset_kmed, 'cluster', 'silhouette')
util.print_latex_statistics_clusters(dataset_kmed, 'cluster', attributes_to_cluster, 'label')

# And the hierarchical clustering is the last one we try

clusteringH = HierarchicalClustering()

k_values = range(2, 10)
silhouette_values = []

print('===== agglomerative clustering =====')
for k in k_values:
    print(f'k = {k}')
    dataset_cluster, l = clusteringH.agglomerative_over_instances(copy.deepcopy(dataset), attributes_to_cluster, k, 'euclidean', use_prev_linkage=True, link_function='ward')
    silhouette_score = dataset_cluster['silhouette'].mean()
    print(f'silhouette = {silhouette_score}')
    silhouette_values.append(silhouette_score)
    if k == k_values[0]:
        DataViz.plot_dendrogram(dataset_cluster, l)

DataViz.plot_xy(x=[k_values], y=[silhouette_values], xlabel='k', ylabel='silhouette score',
                ylim=[0,1], line_styles=['b-'])

# And we select the outcome dataset of the knn clustering....

dataset_knn.to_csv(DATA_PATH / RESULT_FNAME)