
from Chapter2.CreateDataset import CreateDataset
from util.VisualizeDataset import VisualizeDataset
import pandas as pd
import matplotlib.pyplot as plt

activity_paths = [
       'datasets/Walking_2020-06-04_12-53-11/',
       'datasets/Cycling_2020-06-04_13-57-11/',
       'datasets/Sitting_2020-06-04_13-28-48/',
       'datasets/Running_2020-06-04_12-40-48/',
       'datasets/No_Activity_2020-06-04_13-13-43/'
]

activities = [
       'walking',
       'cycling',
       'sitting',
       'running',
       'none'
]

crosstrainer_path = 'datasets/crowdsignals'

sensors = {
       'Accelerometer.csv': [
              'Acceleration x (m/s^2)', 'Acceleration y (m/s^2)', 'Acceleration z (m/s^2)'
       ],
       'Gyroscope.csv': [
              "Gyroscope x (rad/s)", "Gyroscope y (rad/s)", "Gyroscope z (rad/s)"
       ],
       'Linear Acceleration.csv': [
              "Linear Acceleration x (m/s^2)","Linear Acceleration y (m/s^2)","Linear Acceleration z (m/s^2)"
       ],
       'Location.csv': [
              "Latitude (°)","Longitude (°)","Height (m)","Velocity (m/s)","Direction (°)","Horizontal Accuracy (m)","Vertical Accuracy (m)"
       ],
       'Magnetometer.csv' : [
              "Magnetic field x (µT)","Magnetic field y (µT)","Magnetic field z (µT)"
       ]
}

axis_abbreviations = {'Accelerometer.csv': 'acc_', 'Gyroscope.csv': 'gyr_', 'Linear Acceleration.csv': 'lin_',
                      'Location.csv':'loc_', 'Magnetometer.csv' : 'mag_'}

time_column_name = 'Time (s)'

granularities = [60000, 1000, 250]

task = '1_1'

if __name__ == '__main__':
       if task == '1_1':
              sensor = 'Gyroscope.csv'
              dataset = CreateDataset('datasets/Running_2020-06-04_12-40-48/', 250)
              dataset.add_numerical_dataset('Gyroscope.csv', time_column_name, sensors[sensor], 'avg',
                                            axis_abbreviations[sensor])
              dataset = dataset.data_table
              print(dataset.shape)
              fig = plt.figure(figsize=(5, 3.5))
              ax = fig.add_subplot(111)
              ax.boxplot([dataset['gyr_Gyroscope x (rad/s)'], dataset['gyr_Gyroscope y (rad/s)'],
                          dataset['gyr_Gyroscope z (rad/s)']], widths = 0.6)
              xlabels = ["gyr_x", "gyr_y", 'gyr_z']
              ax.set_xticklabels(xlabels)
              plt.ylim([-5, 5])
              plt.savefig('figures/1_1_selected/running_gyr_250.png')


       if task != 'create_plots':
              exit(2)

       for granularity in granularities:
              for i, activity_path in enumerate(activity_paths):
                     print('Activity: ', activity_path)
                     dataset = CreateDataset(activity_path, granularity)

                     for sensor_name, sensor_axis in sensors.items():
                            dataset.add_numerical_dataset(sensor_name, time_column_name, sensor_axis, 'avg', axis_abbreviations[
                                   sensor_name])
                     dataset = dataset.data_table

                     DataViz = VisualizeDataset(__file__)
                     for sensor_name, sensor_axis in sensors.items():
                            DataViz.plot_dataset_boxplot(dataset, [
                                   axis_abbreviations[sensor_name] + x for x in sensors[sensor_name]],
                                                         save_path=str(granularity) + '/' +activities[i])
                     DataViz.plot_dataset(dataset, [x for x in axis_abbreviations.values()],
                                          ['like' for x in axis_abbreviations.keys()],
                                          ['line' for x in axis_abbreviations.keys()],
                                          save_path=str(granularity) + '/' + activities[i])



