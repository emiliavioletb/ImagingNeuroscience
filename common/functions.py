
import pandas as pd
import json
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pickle
import scipy.io
import os
import re
from itertools import chain
import glob
from collections import Counter
from functools import reduce
import mat73
import copy
import matplotlib as mpl
from matplotlib.patches import Polygon
from matplotlib.colors import ListedColormap
from scipy import stats
import statsmodels.api as sm
from sklearn.preprocessing import LabelEncoder
import statsmodels.stats.api as sms
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.graphics.regressionplots import plot_leverage_resid2
from statsmodels.stats.multitest import multipletests
from matplotlib import rc
sns.set()

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Computer Modern Sans Serif']
plt.rcParams['mathtext.fontset'] = 'cm'  # Use Computer Modern for math

def config_json():
    with open('config.json') as f:
        data = json.load(f)
        json_path = data['path']
        clinical_vars = data['clinical_variables']
        features = data['features']
    return json_path, clinical_vars, features

study_folder, clinical_vars, features = config_json()

def load_json(f):
    f = open(f)
    data = json.load(f)
    return data

def save_json(file, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(file, f, ensure_ascii=False, indent=4)
    print('Saving as json...')

def format_dataframe(dataframe):
    formatted_dataframe = []
    dataframe = dataframe[0].to_list()
    for j in dataframe:
        f = "{}".format(j)
        formatted_dataframe.append(f)
    return formatted_dataframe

def convert_diagnosis(dataframe):
    column = dataframe['diagnosis'].replace({1: 'HC', 2: 'AD', 3: 'DLB', 4: 'MCI'})
    dataframe['diagnosis'] = column
    return dataframe

def convert_gender(dataframe):
    column = dataframe['sex'].replace({1: 'F', 0: 'M'})
    dataframe['sex'] = column
    return dataframe








