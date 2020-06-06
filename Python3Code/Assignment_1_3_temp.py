from Assignment_1_3 import *

experiment = OutlierExperiment(data_path, data_file)


experiment.chauvenet(1)
experiment.mixture_model(2)
print(experiment.dataset.columns)
print(experiment.dataset['light_phone_lux_mixture'])
print(experiment.dataset['light_phone_lux_mixture'].sum() / experiment.dataset['light_phone_lux_mixture'].size)