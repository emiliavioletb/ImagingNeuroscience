
from common.functions import *

#load datat
significance_data = pd.read_csv('./output/neuropsych/group_significance_FDR_corrected.csv', index_col=0)
data = pd.read_csv('./data/filtered_data.csv')
diagnoses = list(set(data['diagnosis']))

post_hoc = []
for index, row in significance_data.iterrows():
    if row['significant']:
        comparisons = []
        for i in diagnoses:
            for j in diagnoses:
                if (i != j) & (f'{i} vs {j}' not in comparisons) & (f'{j} vs {i}' not in comparisons):
                    if (row['feature'] in clinical_vars) and (i == 'HC' or j == 'HC'):
                        pass
                    else:
                        data_i = list(data.loc[data['diagnosis'] == i, row['feature']].dropna())
                        data_j = list(data.loc[data['diagnosis'] == j, row['feature']].dropna())

                        if row['normality'] == 0:
                            f, p = stats.mannwhitneyu(data_i, data_j)
                        else:
                            f, p = stats.ttest_ind(data_i, data_j)

                        d = pd.DataFrame({'feature': [row['feature']], 'comparison': [(f'{i} vs {j}')],
                                          'p': p, 'f': f})
                        post_hoc.append(d)
                        comparisons.append(f'{i} vs {j}')
post_hoc = pd.concat(post_hoc, axis=0)
post_hoc.to_csv('./output/neuropsych/post_hoc_results.csv')

# correct for multiple comparisons
p_vals = post_hoc['p'].to_list()
corrected_p_values = multipletests(p_vals, alpha=0.05, method='fdr_bh')
post_hoc['corrected_p'] = [round(x, 3) for x in corrected_p_values[1]]
post_hoc['corrected_sig'] = corrected_p_values[0]
post_hoc.to_csv('./output/neuropsych/post_hoc_FDR_corrected.csv')