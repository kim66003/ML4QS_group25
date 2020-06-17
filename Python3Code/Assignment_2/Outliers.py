
from util.VisualizeDataset import VisualizeDataset
from Chapter3.OutlierDetection import DistributionBasedOutlierDetection
from Chapter3.OutlierDetection import DistanceBasedOutlierDetection
import sys
import copy
import pandas as pd
import numpy as np
from pathlib import Path
import pickle

def main():

    # Set up file names and locations.

    # Next, import the data from the specified location and parse the date index.
    dataset = pickle.load(open('datasets\dataframes\df_concat_with_labels.pkl', 'rb'))



    # We'll create an instance of our visualization class to plot the results.
    DataViz = VisualizeDataset(__file__, show=False)

    # Compute the number of milliseconds covered by an instance using the first two rows.
    milliseconds_per_instance = (dataset.index[1] - dataset.index[0]).microseconds/1000

    # Step 1: Let us see whether we have some outliers we would prefer to remove.

    # Determine the columns we want to experiment on.
    outlier_columns = [
        "Acceleration x (m/s^2)","Acceleration y (m/s^2)","Acceleration z (m/s^2)",
        "Magnetic field x (µT)","Magnetic field y (µT)","Magnetic field z (µT)",
        "Gyroscope x (rad/s)","Gyroscope y (rad/s)","Gyroscope z (rad/s)",
        "Linear Acceleration x (m/s^2)","Linear Acceleration y (m/s^2)","Linear Acceleration z (m/s^2)",
    ]
    print(dataset.columns)
    # Create the outlier classes.
    OutlierDistr = DistributionBasedOutlierDetection()
    OutlierDist = DistanceBasedOutlierDetection()

    # And investigate the approaches for all relevant attributes.
    for col in outlier_columns:

        print(f"Applying outlier criteria for column {col}")

        # And try out all different approaches. Note that we have done some optimization
        # of the parameter values for each of the approaches by visual inspection.
        dataset = OutlierDistr.chauvenet(dataset, col)
        print(dataset.shape)
        # DataViz.plot_binary_outliers(dataset, col, col + '_outlier')
        dataset = OutlierDistr.mixture_model(dataset, col)
        print(dataset.shape)
        # DataViz.plot_dataset(dataset, [col, col + '_mixture'], ['exact','exact'], ['line', 'points'])
        # This requires:
        # n_data_points * n_data_points * point_size =
        # 31839 * 31839 * 32 bits = ~4GB available memory

        try:
            dataset = OutlierDist.simple_distance_based(dataset, [col], 'euclidean', 0.10, 0.99)
            # DataViz.plot_binary_outliers(dataset, col, 'simple_dist_outlier')
            print(dataset['simple_dist_outlier'].mean())
        except MemoryError as e:
            print('Not enough memory available for simple distance-based outlier detection...')
            print('Skipping.')

        try:
            dataset = OutlierDist.local_outlier_factor(dataset, [col], 'euclidean', 5)
            # DataViz.plot_dataset(dataset, [col, 'lof'], ['exact','exact'], ['line', 'points'])
        except MemoryError as e:
            print('Not enough memory available for lof...')
            print('Skipping.')

        # Remove all the stuff from the dataset again.
        cols_to_remove = [col + '_outlier', col + '_mixture', 'simple_dist_outlier', 'lof']
        for to_remove in cols_to_remove:
            if to_remove in dataset:
                del dataset[to_remove]

    # We take Chauvenet's criterion and apply it to all but the label data...

    for col in [c for c in dataset.columns if not 'label' in c]:
        print(f'Measurement is now: {col}')
        dataset = OutlierDistr.chauvenet(dataset, col)
        dataset.loc[dataset[f'{col}_outlier'] == True, col] = np.nan
        del dataset[col + '_outlier']

    pickle.dump(dataset, open('concat_outliers.pkl', 'wb'))

if __name__ == '__main__':
    main()