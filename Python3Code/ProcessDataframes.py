import pickle
import pandas as pd
import datetime


dataframe_paths = {
    'no_activity': 'datasets\dataframes\df_no_activity_gran_250.pkl',
    'cycling': 'datasets\dataframes\df_cycling_gran_250.pkl',
    'running': 'datasets\dataframes\df_running_gran_250.pkl',
    'sitting': 'datasets\dataframes\df_sitting_gran_250.pkl',
    'walking': 'datasets\dataframes\df_walking_gran_250.pkl',
}

first_dataframe = True
num_of_5_mins = 0

for key, value in dataframe_paths.items():
    if first_dataframe:
        dataframe = pickle.load(open(value, 'rb'))
        dataframe.index = pd.to_datetime(dataframe.index)
        dataframe['label'] = key
    else:
        activity_dataframe = pickle.load(open(value, 'rb'))
        activity_dataframe.index = pd.to_datetime(activity_dataframe.index) + datetime.timedelta(
            minutes=num_of_5_mins * 5)
        activity_dataframe['label'] = key
        print(activity_dataframe)
        dataframe = dataframe.append(activity_dataframe)
    first_dataframe = False
    num_of_5_mins += 1

pickle.dump(dataframe, open('datasets\dataframes\df_concat_with_labels.pkl', 'wb'),)