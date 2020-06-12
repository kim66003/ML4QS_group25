import pickle
import pandas as pd
import datetime


dataframe_paths = {
    'No_activity': 'datasets\dataframes\df_no_activity_gran_250.pkl',
    'Cycling': 'datasets\dataframes\df_cycling_gran_250.pkl',
    'Running': 'datasets\dataframes\df_running_gran_250.pkl',
    'Sitting': 'datasets\dataframes\df_sitting_gran_250.pkl',
    'Walking': 'datasets\dataframes\df_walking_gran_250.pkl',
}

first_dataframe = True
num_of_5_mins = 0

label_columns = ['label_' + x for x in dataframe_paths.keys()]

for key, value in dataframe_paths.items():
    if first_dataframe:
        dataframe = pickle.load(open(value, 'rb'))
        dataframe.index = pd.to_datetime(dataframe.index)
        for activity in dataframe_paths.keys():
            dataframe['label' + activity] = 1 if key == activity else 0
    else:
        activity_dataframe = pickle.load(open(value, 'rb'))
        activity_dataframe.index = pd.to_datetime(activity_dataframe.index) + datetime.timedelta(
            minutes=num_of_5_mins * 5)
        for activity in dataframe_paths.keys():
            activity_dataframe['label' + activity] = 1 if key == activity else 0
        dataframe = dataframe.append(activity_dataframe)
    first_dataframe = False
    num_of_5_mins += 1

pickle.dump(dataframe, open('datasets\dataframes\df_concat_with_labels.pkl', 'wb'),)