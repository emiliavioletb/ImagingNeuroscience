from common.functions import *
from common.stats_test import *
import pandas as pd

# Features we want to test
features_norm_test = ['acer_total', 'mmse_total', 'moca_total', 'hads_total',
                      'updrs_total', 'smell_total', 'pareidolia_total',
                      'farnsworth_error', 'gdss_score', 'sleep_total',
                      'badls_total', 'dcfs_total', 'npi_total', 'cbi_total',
                      'cdr_total', 'caf_total_one_day', 'caf_total']

cleaned_data = pd.read_csv('./data/filtered_data.csv')
groups = list(set(cleaned_data['diagnosis']))

# Testing features for normality
normality_dict = {}
for j in features_norm_test:
    dat = cleaned_data[[j, 'diagnosis']]
    norm = []
    for m in groups:
        x = dat.loc[dat['diagnosis']== m, j]
        f, p = stats.shapiro(x)
        if p < 0.05:
            res = 0
        else:
            res = 1
        norm.append(res)
    if 0 in norm:
        normality_dict[j] = 0
    else:
        normality_dict[j] = 1

save_json(normality_dict, ('./data/normality_test_results.json'))