
from util.VisualizeDataset import VisualizeDataset
from Chapter3.OutlierDetection import DistributionBasedOutlierDetection
from Chapter3.OutlierDetection import DistanceBasedOutlierDetection
import pandas as pd

def outliers(data_file, save_file, sub_path):
    
    DataViz = VisualizeDataset(__file__, show=False)

    # Set up file names and locations.

    # Next, import the data from the specified location and parse the date index.
    dataset = pd.read_csv(data_file)
    dataset.index = pd.to_datetime(dataset['timestamp'])

    # We'll create an instance of our visualization class to plot the results.

    # Compute the number of milliseconds covered by an instance using the first two rows.
    milliseconds_per_instance = (dataset.index[1] - dataset.index[0]).microseconds/1000

    # Step 1: Let us see whether we have some outliers we would prefer to remove.

    # Determine the columns we want to experiment on.
    outlier_columns = [
        "Acceleration x (m/s^2)","Acceleration y (m/s^2)","Acceleration z (m/s^2)",
        "Gyroscope x (rad/s)","Gyroscope y (rad/s)","Gyroscope z (rad/s)",
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
        DataViz.plot_binary_outliers(dataset, col, col + '_outlier', save_path=sub_path+'/chauvenet')
        
        dataset = OutlierDistr.mixture_model(dataset, col)
        DataViz.plot_dataset(dataset, [col, col + '_mixture'], ['exact','exact'], ['line', 'points'], save_path=sub_path+'/mixture')
        print('data shape: ', dataset.shape)
        # This requires:
        # n_data_points * n_data_points * point_size =
        # 31839 * 31839 * 32 bits = ~4GB available memory
        #
        try:
            dataset = OutlierDist.simple_distance_based(dataset, [col], 'euclidean', 0.10, 0.99)
            DataViz.plot_binary_outliers(dataset, col, 'simple_dist_outlier', save_path=sub_path+'/simple_dist')
            print(dataset['simple_dist_outlier'].mean())
        except MemoryError as e:
            print('Not enough memory available for simple distance-based outlier detection...')
            print('Skipping.')

#         try:
#             dataset = OutlierDist.local_outlier_factor(dataset, [col], 'euclidean', 5)
#             DataViz.plot_dataset(dataset, [col, 'lof'], ['exact','exact'], ['line', 'points'], save_path=sub_path+'/lof')
#         except MemoryError as e:
#             print('Not enough memory available for lof...')
#             print('Skipping.')

        # Remove all the stuff from the dataset again.
        cols_to_remove = [col + '_outlier', col + '_mixture', 'simple_dist_outlier']
        for to_remove in cols_to_remove:
            if to_remove in dataset:
                del dataset[to_remove]

    # We take Chauvenet's criterion and apply it to all but the label data...

    # for col in [c for c in dataset.columns if not 'label' in c]:
    #     print(f'Measurement is now: {col}')
    #     dataset = OutlierDistr.chauvenet(dataset, col)
    #     dataset.loc[dataset[f'{col}_mixture'] == True, col] = np.nan
    #     del dataset[col + '_outlier']

    dataset.to_csv(save_file)

if __name__ == '__main__':
    preprocessed_phone_data = 'intermediate_datafiles/data_phone.csv'
    preprocessed_watch_data = 'intermediate_datafiles/data_watch.csv'
    outlier_phone_data = 'intermediate_datafiles/outliers_phone.csv'
    outlier_watch_data = 'intermediate_datafiles/outliers_watch.csv'
    
    outliers(preprocessed_phone_data, outlier_phone_data, 'phone')
    outliers(preprocessed_watch_data, outlier_watch_data, 'watch')