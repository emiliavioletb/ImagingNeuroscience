
import pandas as pd
import json
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pickle
import scipy.io
from itertools import chain
import glob
from collections import Counter
sns.set()
import mat73

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Computer Modern Sans Serif']
plt.rcParams['mathtext.fontset'] = 'cm'  # Use Computer Modern for math



def config_json():
    with open('config.json') as f:
        data = json.load(f)
        json_path = data['path']
        clinical_vars = data['clinical_variables']
    return json_path, clinical_vars

def load_json(f):
    f = open(f)
    data = json.load(f)
    return data

def load_csv(path):
    loaded_csv = pd.read_csv(path)
    return loaded_csv

def convert_period(period):
    pass

def save_pickle(file, path):
    pickle.dump(file, open(path, "wb"))

def load_pickle(path):
    with open(path,'rb') as f:
        pC = pickle.load(f)
    return pC

def save_json(file, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(file, f, ensure_ascii=False, indent=4)
    print('Saving as json...')

def unpack_list(list):
    flat_list = [item for sublist in list for item in sublist]
    return flat_list

study_folder, clinical_vars = config_json()

def format_dataframe(dataframe):
    formatted_dataframe = []
    dataframe = dataframe[0].to_list()
    for j in dataframe:
        f = "{}".format(j)
        formatted_dataframe.append(f)
    return formatted_dataframe