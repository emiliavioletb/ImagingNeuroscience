
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

def load_json_path():
    with open('config.json') as f:
        data = json.load(f)
        json_path = data['path']
    return json_path

def load_csv(path):
    loaded_csv = pd.read_csv(path)
    return loaded_csv

study_folder = load_json_path()