
from Chapter2.CreateDataset import CreateDataset
from util.VisualizeDataset import VisualizeDataset
import pandas as pd

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

granularities = [250]


if __name__ == '__main__':
       for granularity in granularities:
              for i, activity_path in enumerate(activity_paths):
                     print()
                     dataset = CreateDataset(activity_path, granularity)

                     for sensor_name, sensor_axis in sensors.items():
                            dataset.add_numerical_dataset(sensor_name, 'Time (s)', sensor_axis, 'avg', axis_abbreviations[
                                   sensor_name])
                     dataset = dataset.data_table



                     DataViz = VisualizeDataset(__file__)
                     for sensor_name, sensor_axis in sensors.items():
                            DataViz.plot_dataset_boxplot(dataset, [
                                   axis_abbreviations[sensor_name] + x for x in sensors[sensor_name]],
                                                         save_path=activities[i])
                     DataViz.plot_dataset(dataset, [x for x in axis_abbreviations.values()],
                                          ['like' for x in axis_abbreviations.keys()],
                                          ['line' for x in axis_abbreviations.keys()], save_path=activities[i])



