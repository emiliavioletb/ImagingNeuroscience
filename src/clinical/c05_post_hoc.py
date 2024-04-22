import pandas as pd

from common.functions import *
from common.stats_test import *

significance_data = pd.read_csv((study_folder + 'NEUROPSYCH/group_significance.csv'))
data = pd.read_csv((study_folder + 'NEUROPSYCH/filtered_data.csv'))
data = data.fillna(0)

num_comparisons = len(list(set(data['diagnosis'])))*2

post_hoc = []
for index, row in significance_data.iterrows():
    if row['significant'] == 'Yes':
        comparisons = []
        if row['feature'] in clinical_vars:
            excl = True
        else:
            excl=False
        for i in list(set(data['diagnosis'])):
            for j in list(set(data['diagnosis'])):
                if (i != j) & (f'{i} vs {j}' not in comparisons) & (f'{j} vs {i}' not in comparisons):
                    if row['normality'] == 0:
                        f, p, res, lev = mann_whitney(list(data.loc[data['diagnosis'] == i, row['feature']]),
                                            list(data.loc[data['diagnosis'] == j, row['feature']]),
                                                      num_comparisons)
                    else:
                        s, p, res, lev = t_test(list(data.loc[data['diagnosis'] == i, row['feature']]),
                                            list(data.loc[data['diagnosis'] == j, row['feature']]),
                                                      num_comparisons)
                    if res == 'Yes':
                        d = pd.DataFrame({'feature': [row['feature']], 'comparison': [(f'{i} vs {j}')],
                                          'p': [p], 'f': f, 'level': [lev],
                                          'test': ['mann_whitney]']})
                        post_hoc.append(d)

post_hoc = pd.concat(post_hoc, axis=0)
post_hoc.to_csv((study_folder + 'NEUROPSYCH/post_hoc_results.csv'))