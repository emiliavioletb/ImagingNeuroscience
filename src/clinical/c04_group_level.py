
from common.functions import *

# load datat
data = pd.read_csv('./data/filtered_data.csv')
normality = load_json('./data/normality_test_results.json')

# test for significance at group-level
group_total = []
for key in normality:
    sig_data = data[['diagnosis', key]]
    if key in clinical_vars:
        sig_data = sig_data[sig_data['diagnosis']!='HC']
    sig_data = sig_data.dropna()
    sig_data = [list(sig_data.loc[sig_data['diagnosis']==j, key]) for j in list(set(sig_data['diagnosis']))]
    if normality[key] == 1:
        if key in clinical_vars:
            f, p = stats.ttest_ind(*sig_data)
        else:
            f, p = stats.f_oneway(*sig_data)
    else:
        if key in clinical_vars:
            f, p = stats.mannwhitneyu(*sig_data)
        else:
            f, p = stats.kruskal(*sig_data)
    if p < 0.05:
        res = 'Yes'
    else:
        res = 'No'
    results = pd.DataFrame({'feature': [key], 'normality': [normality[key]],
                            'f': [f], 'p': [round(p, 3)], 'significant': [p<0.05]})
    group_total.append(results)
group_total = pd.concat(group_total, axis=0)
group_total.to_csv('./output/neuropsych/group_significance.csv')

# correct for multiple comparisons
p_vals = group_total['p'].to_list()
corrected_p_values = multipletests(p_vals, alpha=0.05, method='fdr_bh')
group_total['corrected_p'] = [round(x, 3) for x in corrected_p_values[1]]
group_total['corrected_sig'] = corrected_p_values[0]
group_total.to_csv('./output/neuropsych/group_significance_FDR_corrected.csv')
