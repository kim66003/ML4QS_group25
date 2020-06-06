import sys
import copy
import pandas as pd
from pathlib import Path

from util.VisualizeDataset import VisualizeDataset
from Chapter4.TemporalAbstraction import NumericalAbstraction
from Chapter4.TemporalAbstraction import CategoricalAbstraction
from Chapter4.FrequencyAbstraction import FourierTransformation
from Chapter4.TextAbstraction import TextAbstraction

DATA_PATH = Path('./intermediate_datafiles/')
DATASET_FNAME = sys.argv[1] if len(sys.argv) > 1 else 'chapter3_result_final.csv'
RESULT_FNAME = sys.argv[2] if len(sys.argv) > 2 else 'chapter4_result.csv'

