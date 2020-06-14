##############################################################
#                                                            #
#    Mark Hoogendoorn and Burkhardt Funk (2017)              #
#    Machine Learning for the Quantified Self                #
#    Springer                                                #
#    Chapter 7                                               #
#                                                            #
##############################################################

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
import shelve

my_shelf = shelve.open('temp/shelve.out')
for key in my_shelf:
    try:
        globals()[key]=my_shelf[key]
    except:
        print('Unable to load ', key)
my_shelf.close()

for i in range(0, len(possible_feature_sets)):
    print(datetime.now())
    print('possible feature sets', i)
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
        print('Feedforward')
        class_train_y, class_test_y, class_train_prob_y, class_test_prob_y = learner.feedforward_neural_network(
            selected_train_X, train_y, selected_test_X, gridsearch=True
        )
        performance_tr_nn += eval.accuracy(train_y, class_train_y)
        performance_te_nn += eval.accuracy(test_y, class_test_y)
        print('Random Forest')
        class_train_y, class_test_y, class_train_prob_y, class_test_prob_y = learner.random_forest(
            selected_train_X, train_y, selected_test_X, gridsearch=True
        )
        performance_tr_rf += eval.accuracy(train_y, class_train_y)
        performance_te_rf += eval.accuracy(test_y, class_test_y)

        # class_train_y, class_test_y, class_train_prob_y, class_test_prob_y = learner.support_vector_machine_with_kernel(
        #     selected_train_X, train_y, selected_test_X, gridsearch=True
        # )
        # performance_tr_svm += eval.accuracy(train_y, class_train_y)
        # performance_te_svm += eval.accuracy(test_y, class_test_y)
        print(datetime.now())


    overall_performance_tr_nn = performance_tr_nn/N_KCV_REPEATS
    overall_performance_te_nn = performance_te_nn/N_KCV_REPEATS
    overall_performance_tr_rf = performance_tr_rf/N_KCV_REPEATS
    overall_performance_te_rf = performance_te_rf/N_KCV_REPEATS
    # overall_performance_tr_svm = performance_tr_svm/N_KCV_REPEATS
    # overall_performance_te_svm = performance_te_svm/N_KCV_REPEATS

    # And we run our deterministic classifiers:
    print('deterministic classifiers')
    class_train_y, class_test_y, class_train_prob_y, class_test_prob_y = learner.k_nearest_neighbor(
        selected_train_X, train_y, selected_test_X, gridsearch=True
    )
    performance_tr_knn = eval.accuracy(train_y, class_train_y)
    performance_te_knn = eval.accuracy(test_y, class_test_y)
    print('decision tree')
    class_train_y, class_test_y, class_train_prob_y, class_test_prob_y = learner.decision_tree(
        selected_train_X, train_y, selected_test_X, gridsearch=True
    )
    performance_tr_dt = eval.accuracy(train_y, class_train_y)
    performance_te_dt = eval.accuracy(test_y, class_test_y)
    print('naive bayes')
    class_train_y, class_test_y, class_train_prob_y, class_test_prob_y = learner.naive_bayes(
        selected_train_X, train_y, selected_test_X
    )
    performance_tr_nb = eval.accuracy(train_y, class_train_y)
    performance_te_nb = eval.accuracy(test_y, class_test_y)

    scores_with_sd = util.print_table_row_performances(
        feature_names[i], len(selected_train_X.index), len(selected_test_X.index), [
            (overall_performance_tr_nn, overall_performance_te_nn),
            (overall_performance_tr_rf, overall_performance_te_rf),
            (performance_tr_knn, performance_te_knn), (performance_tr_dt, performance_te_dt),
            (performance_tr_nb, performance_te_nb)
        ]
    )
    scores_over_all_algs.append(scores_with_sd)
    print(datetime.now())

with shelve.open('temp/ch7_part2.out', 'n') as f:
    for key in dir():
        print(key)
        try:
            f[key] = globals()[key]
        except TypeError:
            #
            # __builtins__, my_shelf, and imported modules can not be shelved.
            #
            print('ERROR shelving: {0}'.format(key))

DataViz.plot_performances_classification(['NN', 'RF', 'KNN', 'DT', 'NB'], feature_names, scores_over_all_algs)

# datetime object containing current date and time
now7 = datetime.now()
# dd/mm/YY H:M:S
dt_string = now7.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string)

diff = now7 - now6
print('difference time', diff)

# And we study two promising ones in more detail. First, let us consider the decision tree, which works best with the
# selected features.

class_train_y, class_test_y, class_train_prob_y, class_test_prob_y = learner.decision_tree(
    train_X[selected_features], train_y, test_X[selected_features],gridsearch=True,print_model_details=True,
    export_tree_path=EXPORT_TREE_PATH, save_path='ch7_decision_tree.pkl')

class_train_y, class_test_y, class_train_prob_y, class_test_prob_y = learner.random_forest(
    train_X[selected_features], train_y, test_X[selected_features],
    gridsearch=True, print_model_details=True)

test_cm = eval.confusion_matrix(test_y, class_test_y, class_train_prob_y.columns)

DataViz.plot_confusion_matrix(test_cm, class_train_prob_y.columns, normalize=False)

with open('results/scores_all_algs.txt', 'w') as f:
    for item in scores_over_all_algs:
        f.write("%s\n" % item)

with open('results/crowdsignal_cm.txt', 'w') as f:
    f.write(str(test_cm))
# datetime object containing current date and time
now8 = datetime.now()
# dd/mm/YY H:M:S
dt_string = now8.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string)

diff = now8 - now7
print('difference time', diff)
