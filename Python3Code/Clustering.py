##############################################################
#                                                            #
#    Mark Hoogendoorn and Burkhardt Funk (2017)              #
#    Machine Learning for the Quantified Self                #
#    Springer                                                #
#    Chapter 5                                               #
#                                                            #
##############################################################

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
import pickle

# As usual, we set our program constants, read the input file and initialize a visualization object.
dataset = pickle.load(open('datasets\dataframes\concat_imputed.pkl', 'rb'))
dataset.index = pd.to_datetime(dataset.index)



# We'll start by applying non-hierarchical clustering.
clusteringNH = NonHierarchicalClustering()

# Let us look at k-means first.
k_values = range(2, 10)
silhouette_values = []

## Do some initial runs to determine the right number for k
attributes_to_cluster = [
"Acceleration x (m/s^2)","Acceleration y (m/s^2)","Acceleration z (m/s^2)",
]
print('===== kmeans clustering =====')
for k in k_values:
    print(f'k = {k}')
    dataset_cluster = clusteringNH.k_means_over_instances(copy.deepcopy(dataset), attributes_to_cluster, k, 'default', 20, 10)
    silhouette_score = dataset_cluster['silhouette'].mean()
    print(f'silhouette = {silhouette_score}')
    silhouette_values.append(silhouette_score)


# And run the knn with the highest silhouette score

# k = 6 # todo: replaced with np.argmax call over silhouette scores
k = k_values[np.argmax(silhouette_values)]
print(f'Highest K-Means silhouette score: k = {k}')

dataset_knn = clusteringNH.k_means_over_instances(copy.deepcopy(dataset), attributes_to_cluster, k, 'default', 50, 50)
util.print_latex_statistics_clusters(dataset_knn, 'cluster', attributes_to_cluster, 'label')
del dataset_knn['silhouette']

# And we select the outcome dataset of the knn clustering....
pickle.dump(dataset_knn, open('concat_clustered.pkl', 'wb'))