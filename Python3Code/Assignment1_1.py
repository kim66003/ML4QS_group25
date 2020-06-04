
from Chapter2.CreateDataset import CreateDataset
from util.VisualizeDataset import VisualizeDataset
import pandas as pd

activity_paths = [
       'datasets/Walking_2020-06-03_15-13-20/',
       'datasets/Cycling_2020-06-03_15-44-48',
       'datasets/Playing_Piano_2020-06-03_16-20-32',
       'datasets/Running_2020-06-03_15-24-11',
]

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
       ]
}

axis_abbreviations = {'Accelerometer.csv': 'acc_', 'Gyroscope.csv': 'gyr_', 'Linear Acceleration.csv': 'lin_', 'Location.csv':'loc_'}

time_column_name = 'Time (s)'

granularities = [60000, 250]


if __name__ == '__main__':
       for granularity in granularities:
              dataset = CreateDataset(activity_paths[0], granularity)

              for sensor_name, sensor_axis in sensors.items():
                     dataset.add_numerical_dataset(sensor_name, 'Time (s)', sensor_axis, 'avg', axis_abbreviations[
                            sensor_name])
              dataset = dataset.data_table



              DataViz = VisualizeDataset(__file__)

              DataViz.plot_dataset_boxplot(dataset, ['acc_' + x for x in ['Acceleration x (m/s^2)', 'Acceleration y ('
                                                                                                'm/s^2)',
                     'Acceleration z (m/s^2)']])
              DataViz.plot_dataset(dataset, [x for x in axis_abbreviations.values()],
                                   ['like' for x in axis_abbreviations.keys()])

