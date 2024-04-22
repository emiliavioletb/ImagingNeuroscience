
from common.functions import *
from common.stats_test import *

data = pd.read_csv((study_folder + 'NEUROPSYCH/filtered_data.csv'))
normality = load_json((study_folder + 'NEUROPSYCH/normality_test_results.json'))

# Test for significance across the groups for not normally-distributed data
group_total = []
for key in normality:
    sig_data = data[['diagnosis', key]]
    if key in clinical_vars:
        sig_data = sig_data[sig_data['diagnosis']!='HC']
    sig_data = sig_data.fillna(0)
    sig_data = [list(sig_data.loc[sig_data['diagnosis']==j, key]) for j in list(set(sig_data['diagnosis']))]
    if normality[key] == 1:
        f, p, res = one_way_anova(sig_data, key)
    else:
        f, p, res = kruskal_wallis(sig_data, key)
    results = pd.DataFrame({'feature': [key], 'normality': [normality[key]],
                            'f': [f], 'p': [p], 'significant': [res]})
    group_total.append(results)

group_total = pd.concat(group_total, axis=0)
group_total.to_csv((study_folder + 'NEUROPSYCH/group_significance.csv'))

