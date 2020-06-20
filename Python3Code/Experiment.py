
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
import shelve

N_FORWARD_SELECTION = 2

basic_features = ['acc_x', 'acc_y', 'acc_z', "gyr_x",
    "gyr_y", "gyr_z", ]


def print_date():
    begin = datetime.now()
    dt_string = begin.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)


def log(list):
    with open('results/classification.txt', 'w+') as f:
        f.writelines(list)


def experiment(file):
    dataset = pd.read_csv(file, index_col=time_col)
    DataViz = VisualizeDataset(file.split('.')[0] + __file__, show=False)
    dataset.index = pd.to_datetime(dataset.index)
    prepare = PrepareDatasetForLearning()
    train_X, test_X, train_y, test_y = prepare.split_single_dataset_classification(dataset, ['label'], 'like', 0.7,
                                                                                   filter=False, temporal=False,
                                                                                   drop_na=False, fill_na=True)

    time_features = [name for name in dataset.columns if '_temp' in name]
    freq_features = [name for name in dataset.columns if (('_freq' in name) or ('_pse' in name))]
    cluster_features = ['cluster']
    features_2 = list(set().union(basic_features, time_features))
    features_3 = list(set().union(basic_features, time_features, freq_features))
    features_4 = list(set().union(basic_features, time_features, freq_features, cluster_features))

    print('feature selection')
    fs = FeatureSelectionClassification()
    features, selected_features, ordered_scores = fs.forward_selection(N_FORWARD_SELECTION,
                                                                      train_X[features_4], train_y)
    log([str(ordered_scores), str(selected_features)])
    DataViz.plot_xy(x=[range(1, N_FORWARD_SELECTION + 1)], y=[selected_features],
                    xlabel='number of features', ylabel='accuracy')

    print('feature selection finished for %s'%file)
    learner = ClassificationAlgorithms()
    eval = ClassificationEvaluation()

    performance_training = []
    performance_test = []

    possible_feature_sets = [basic_features, features_2, features_3,
                             features_4, selected_features]
    feature_names = ['Basic features', 'Features with time', 'Features with frequency', 'Features with cluster',
                     'Selected features']

    with shelve.open('temp/shelve.out', 'n') as f:
        for key in dir():
            try:
                f[key] = globals()[key]
            except:
                print('ERROR shelving: {0}'.format(key))

    N_KCV_REPEATS = 1

    scores_over_all_algs = []

    for i in range(0, len(possible_feature_sets)):
        print(datetime.now())
        print('possible feature sets', i)
        log(['Features %d'%i])
        selected_train_X = train_X[possible_feature_sets[i]]
        selected_test_X = test_X[possible_feature_sets[i]]

        # First we run our non deterministic classifiers a number of times to average their score.

        performance_tr_nn = 0
        performance_tr_rf = 0
        performance_tr_svm = 0
        performance_te_nn = 0
        performance_te_rf = 0
        performance_te_svm = 0

        for repeat in range(0, N_KCV_REPEATS):
            print(datetime.now())
            print('\nRepeat', repeat)
            print('Random Forest')
            class_train_y, class_test_y, class_train_prob_y, class_test_prob_y = learner.random_forest(
                selected_train_X, train_y, selected_test_X, gridsearch=True
            )
            test_cm = eval.confusion_matrix(test_y, class_test_y, class_train_prob_y.columns)

            DataViz.plot_confusion_matrix(test_cm, class_train_prob_y.columns, normalize=False)

            performance_tr_rf += eval.accuracy(train_y, class_train_y)
            performance_te_rf += eval.accuracy(test_y, class_test_y)

            print(datetime.now())

        overall_performance_tr_rf = performance_tr_rf / N_KCV_REPEATS
        overall_performance_te_rf = performance_te_rf / N_KCV_REPEATS
        log(['RF' + ' train acc: %f'%performance_te_rf + ' test acc: %f'%performance_te_rf])

        # And we run our deterministic classifiers:

        print('decision tree')
        class_train_y, class_test_y, class_train_prob_y, class_test_prob_y = learner.decision_tree(
            selected_train_X, train_y, selected_test_X, gridsearch=True
        )
        performance_tr_dt = eval.accuracy(train_y, class_train_y)
        performance_te_dt = eval.accuracy(test_y, class_test_y)
        test_cm = eval.confusion_matrix(test_y, class_test_y, class_train_prob_y.columns)

        DataViz.plot_confusion_matrix(test_cm, class_train_prob_y.columns, normalize=False)

        log(['DT' + ' train acc: %f'%performance_tr_dt + ' test acc: %f'%performance_te_dt])
        scores_with_sd = util.print_table_row_performances(
            feature_names[i], len(selected_train_X.index), len(selected_test_X.index), [
                (overall_performance_tr_rf, overall_performance_te_rf),
                (performance_tr_dt, performance_te_dt),
            ]
        )
        scores_over_all_algs.append(scores_with_sd)

    DataViz.plot_performances_classification(['RF', 'DT'], feature_names, scores_over_all_algs)
    print(datetime.now())

if __name__ == '__main__':
    print('experiment with phone')
    experiment(features_phone_data)
    print('experiment with watch')
    experiment(features_watch_data)