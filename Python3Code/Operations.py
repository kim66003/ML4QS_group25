
import copy
import numpy as np
import pandas as pd
import pickle


dataset = pickle.load(open('datasets\dataframes\df_concat_with_labels.pkl', 'rb'))
dataset.index = pd.to_datetime(dataset.index)
print(dataset.columns)
print(dataset['labelNo_activity'].unique())