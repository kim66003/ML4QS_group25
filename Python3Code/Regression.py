##############################################################
#                                                            #
#    Mark Hoogendoorn and Burkhardt Funk (2017)              #
#    Machine Learning for the Quantified Self                #
#    Springer                                                #
#    Chapter 8                                               #
#                                                            #
##############################################################

from util.VisualizeDataset import VisualizeDataset
from Chapter7.PrepareDatasetForLearning import PrepareDatasetForLearning
from Chapter7.Evaluation import RegressionEvaluation
from Chapter8.LearningAlgorithmsTemporal import TemporalClassificationAlgorithms
from Chapter8.LearningAlgorithmsTemporal import TemporalRegressionAlgorithms
from statsmodels.tsa.stattools import adfuller
from pandas.plotting import autocorrelation_plot

import sys
import copy
import pandas as pd
from util import util
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
import pickle
# Set up file names and locations.
DATA_PATH = Path('./intermediate_datafiles/')
DATASET_FNAME = sys.argv[1] if len(sys.argv) > 1 else 'chapter2_result.csv'
RESULT_FNAME = sys.argv[2] if len(sys.argv) > 2 else 'chapter3_result_outliers.csv'

dataset = pickle.load(open('datasets/dataframes/concat_clustered.pkl', 'rb'))
# dataset.index = pd.to_datetime(dataset.index)

DataViz = VisualizeDataset(__file__, show=False)


# Let us consider our second task, namely the prediction of the heart rate. We consider this as a temporal task.

prepare = PrepareDatasetForLearning()

dataset = dataset.fillna(0)
print(dataset.index)
print(dataset.loc[dataset.index.values[0]])
train_X, test_X, train_y, test_y = prepare.split_single_dataset_regression_by_time(
    dataset, "Gyroscope z (rad/s)",
    dataset.index.values[0],
    dataset.index.values[int(len(dataset.index) * 0.7)],
    dataset.index.values[-1])

print('Training set length is: ', len(train_X.index))
print('Test set length is: ', len(test_X.index))

# Select subsets of the features that we will consider:

print('Training set length is: ', len(train_X.index))
print('Test set length is: ', len(test_X.index))

# Select subsets of the features that we will consider:

basic_features = [
    'Acceleration x (m/s^2)', 'Acceleration y (m/s^2)', 'Acceleration z (m/s^2)', "Gyroscope x (rad/s)",
    "Gyroscope y (rad/s)",  "Linear Acceleration x (m/s^2)","Linear Acceleration y (m/s^2)",
    "Linear Acceleration z (m/s^2)",
    "Magnetic field x (µT)","Magnetic field y (µT)","Magnetic field z (µT)"]
pca_features = []
time_features = [name for name in dataset.columns if ('temp_' in name and not 'hr_watch' in name)]
freq_features = [name for name in dataset.columns if (('_freq' in name) or ('_pse' in name))]
print('#basic features: ', len(basic_features))
print('#PCA features: ', len(pca_features))
print('#time features: ', len(time_features))
print('#frequency features: ', len(freq_features))
cluster_features = ['cluster']
print('#cluster features: ', len(cluster_features))
features_after_chapter_3 = list(set().union(basic_features, pca_features))
features_after_chapter_4 = list(set().union(basic_features, pca_features, time_features, freq_features))
features_after_chapter_5 = list(set().union(basic_features, pca_features, time_features, freq_features, cluster_features))
selected_features = ['Acceleration x (m/s^2)', 'Acceleration y (m/s^2)', 'Acceleration z (m/s^2)', "Gyroscope x (rad/s)",
    "Gyroscope y (rad/s)"]
possible_feature_sets = [basic_features, features_after_chapter_3, features_after_chapter_4, features_after_chapter_5, selected_features]
feature_names = ['initial set', 'Chapter 3', 'Chapter 4', 'Chapter 5', 'Selected features']

# Let us first study whether the time series is stationary and what the autocorrelations are.

dftest = adfuller(dataset["Gyroscope z (rad/s)"], autolag='AIC')

plt.Figure(); autocorrelation_plot(dataset["Gyroscope z (rad/s)"])
DataViz.save(plt)
plt.show()

# Now let us focus on the learning part.

learner = TemporalRegressionAlgorithms()
eval = RegressionEvaluation()

# We repeat the experiment a number of times to get a bit more robust data as the initialization of e.g. the NN is random.

repeats = 10

# we set a washout time to give the NN's the time to stabilize. We do not compute the error during the washout time.

washout_time = 10

scores_over_all_algs = []

for i in range(0, len(possible_feature_sets)):

    print(f'Evaluating for features {possible_feature_sets[i]}')
    selected_train_X = train_X[possible_feature_sets[i]]
    selected_test_X = test_X[possible_feature_sets[i]]

    # First we run our non deterministic classifiers a number of times to average their score.

    performance_tr_res = 0
    performance_tr_res_std = 0
    performance_te_res = 0
    performance_te_res_std = 0
    performance_tr_rnn = 0
    performance_tr_rnn_std = 0
    performance_te_rnn = 0
    performance_te_rnn_std = 0

    for repeat in range(0, repeats):
        print(f'---- run {repeat} ---')
        regr_train_y, regr_test_y = learner.reservoir_computing(selected_train_X, train_y, selected_test_X, test_y, gridsearch=True, per_time_step=False)

        mean_tr, std_tr = eval.mean_squared_error_with_std(train_y.iloc[washout_time:,], regr_train_y.iloc[washout_time:,])
        mean_te, std_te = eval.mean_squared_error_with_std(test_y.iloc[washout_time:,], regr_test_y.iloc[washout_time:,])

        performance_tr_res += mean_tr
        performance_tr_res_std += std_tr
        performance_te_res += mean_te
        performance_te_res_std += std_te

        regr_train_y, regr_test_y = learner.recurrent_neural_network(selected_train_X, train_y, selected_test_X, test_y, gridsearch=True)

        mean_tr, std_tr = eval.mean_squared_error_with_std(train_y.iloc[washout_time:,], regr_train_y.iloc[washout_time:,])
        mean_te, std_te = eval.mean_squared_error_with_std(test_y.iloc[washout_time:,], regr_test_y.iloc[washout_time:,])

        performance_tr_rnn += mean_tr
        performance_tr_rnn_std += std_tr
        performance_te_rnn += mean_te
        performance_te_rnn_std += std_te


    # We only apply the time series in case of the basis features.
    if (feature_names[i] == 'initial set'):
        regr_train_y, regr_test_y = learner.time_series(selected_train_X, train_y, selected_test_X, test_y, gridsearch=True)

        mean_tr, std_tr = eval.mean_squared_error_with_std(train_y.iloc[washout_time:,], regr_train_y.iloc[washout_time:,])
        mean_te, std_te = eval.mean_squared_error_with_std(test_y.iloc[washout_time:,], regr_test_y.iloc[washout_time:,])

        overall_performance_tr_ts = mean_tr
        overall_performance_tr_ts_std = std_tr
        overall_performance_te_ts = mean_te
        overall_performance_te_ts_std = std_te
    else:
        overall_performance_tr_ts = 0
        overall_performance_tr_ts_std = 0
        overall_performance_te_ts = 0
        overall_performance_te_ts_std = 0

    overall_performance_tr_res = performance_tr_res/repeats
    overall_performance_tr_res_std = performance_tr_res_std/repeats
    overall_performance_te_res = performance_te_res/repeats
    overall_performance_te_res_std = performance_te_res_std/repeats
    overall_performance_tr_rnn = performance_tr_rnn/repeats
    overall_performance_tr_rnn_std = performance_tr_rnn_std/repeats
    overall_performance_te_rnn = performance_te_rnn/repeats
    overall_performance_te_rnn_std = performance_te_rnn_std/repeats

    scores_with_sd = [(overall_performance_tr_res, overall_performance_tr_res_std, overall_performance_te_res, overall_performance_te_res_std),
                      (overall_performance_tr_rnn, overall_performance_tr_rnn_std, overall_performance_te_rnn, overall_performance_te_rnn_std),
                      (overall_performance_tr_ts, overall_performance_tr_ts_std, overall_performance_te_ts, overall_performance_te_ts_std)]
    util.print_table_row_performances_regression(feature_names[i], len(selected_train_X.index), len(selected_test_X.index), scores_with_sd)
    scores_over_all_algs.append(scores_with_sd)

DataViz.plot_performances_regression(['Reservoir', 'RNN', 'Time series'], feature_names, scores_over_all_algs)

regr_train_y, regr_test_y = learner.reservoir_computing(train_X[features_after_chapter_5], train_y, test_X[features_after_chapter_5], test_y, gridsearch=False)
DataViz.plot_numerical_prediction_versus_real(train_X.index, train_y, regr_train_y["Gyroscope z (rad/s)"], test_X.index, test_y, regr_test_y["Gyroscope z (rad/s)"], 'heart rate')
regr_train_y, regr_test_y = learner.recurrent_neural_network(train_X[basic_features], train_y, test_X[basic_features], test_y, gridsearch=True)
DataViz.plot_numerical_prediction_versus_real(train_X.index, train_y, regr_train_y['hr_watch_rate'], test_X.index, test_y, regr_test_y["Gyroscope z (rad/s)"], 'heart rate')
regr_train_y, regr_test_y = learner.time_series(train_X[basic_features], train_y, test_X[basic_features], test_y, gridsearch=True)
DataViz.plot_numerical_prediction_versus_real(train_X.index, train_y, regr_train_y['hr_watch_rate'], test_X.index, test_y, regr_test_y["Gyroscope z (rad/s)"], 'heart rate')
exit()
# And now some example code for using the dynamical systems model with parameter tuning (note: focus on predicting accelerometer data):

train_X, test_X, train_y, test_y = prepare.split_single_dataset_regression(copy.deepcopy(dataset), ['acc_phone_x', 'acc_phone_y'], 0.9, filter=False, temporal=True)

output_sets = learner.dynamical_systems_model_nsga_2(train_X, train_y, test_X, test_y, ['self.acc_phone_x', 'self.acc_phone_y', 'self.acc_phone_z'],
                                                     ['self.a * self.acc_phone_x + self.b * self.acc_phone_y', 'self.c * self.acc_phone_y + self.d * self.acc_phone_z', 'self.e * self.acc_phone_x + self.f * self.acc_phone_z'],
                                                     ['self.acc_phone_x', 'self.acc_phone_y'],
                                                     ['self.a', 'self.b', 'self.c', 'self.d', 'self.e', 'self.f'],
                                                     pop_size=10, max_generations=10, per_time_step=True)
DataViz.plot_pareto_front(output_sets)

DataViz.plot_numerical_prediction_versus_real_dynsys_mo(train_X.index, train_y, test_X.index, test_y, output_sets, 0, 'acc_phone_x')

regr_train_y, regr_test_y = learner.dynamical_systems_model_ga(train_X, train_y, test_X, test_y, ['self.acc_phone_x', 'self.acc_phone_y', 'self.acc_phone_z'],
                                                     ['self.a * self.acc_phone_x + self.b * self.acc_phone_y', 'self.c * self.acc_phone_y + self.d * self.acc_phone_z', 'self.e * self.acc_phone_x + self.f * self.acc_phone_z'],
                                                     ['self.acc_phone_x', 'self.acc_phone_y'],
                                                     ['self.a', 'self.b', 'self.c', 'self.d', 'self.e', 'self.f'],
                                                     pop_size=5, max_generations=10, per_time_step=True)

DataViz.plot_numerical_prediction_versus_real(train_X.index, train_y['acc_phone_x'], regr_train_y['acc_phone_x'], test_X.index, test_y['acc_phone_x'], regr_test_y['acc_phone_x'], 'acc_phone_x')

regr_train_y, regr_test_y = learner.dynamical_systems_model_sa(train_X, train_y, test_X, test_y, ['self.acc_phone_x', 'self.acc_phone_y', 'self.acc_phone_z'],
                                                     ['self.a * self.acc_phone_x + self.b * self.acc_phone_y', 'self.c * self.acc_phone_y + self.d * self.acc_phone_z', 'self.e * self.acc_phone_x + self.f * self.acc_phone_z'],
                                                     ['self.acc_phone_x', 'self.acc_phone_y'],
                                                     ['self.a', 'self.b', 'self.c', 'self.d', 'self.e', 'self.f'],
                                                     max_generations=10, per_time_step=True)

DataViz.plot_numerical_prediction_versus_real(train_X.index, train_y['acc_phone_x'], regr_train_y['acc_phone_x'], test_X.index, test_y['acc_phone_x'], regr_test_y['acc_phone_x'], 'acc_phone_x')
