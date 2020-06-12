
import copy
import numpy as np
import pandas as pd
import pickle


dataset = pickle.load(open('concat_frequency.pkl', 'rb'))
dataset.index = pd.to_datetime(dataset.index)
print(dataset.columns)
print(dataset.shape)