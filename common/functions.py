
import pandas as pd
import json
import seaborn as sns
import h5py
import numpy as np
import pickle
sns.set()

def load_json_path():
    with open('config.json') as f:
        data = json.load(f)
        json_path = data['path']
    return json_path

def load_csv(path):
    loaded_csv = pd.read_csv(path)
    return loaded_csv

def load_mat(path, variables=None):
    loaded_mat = h5py.File(path, 'r')
    if variables:
        loaded_mat = loaded_mat.get(variables)
        loaded_mat = np.array(loaded_mat)
    return loaded_mat

def convert_period(period):
    pass

def save_pickle(file, path):
    pickle.dump(file, open(path, "wb"))

def save_json(file, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(file, f, ensure_ascii=False, indent=4)

study_folder = load_json_path()