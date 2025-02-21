import matplotlib.pyplot as plt

from common.stats_test import *
from common.visualisation import *
import copy

# Load data
allData = pd.read_csv('./output/graph_theory/macroProperties.csv')
normMetrics = load_json('./output/graph_theory/macroProperties_norm.json')

# Save metric summary
Dat = {}
for j in allData['Metric'].unique():
    dat = {}
    for m in allData['Group'].unique():
        filtered_df = allData[(allData['Metric'] == j) & (allData['Group'] == m)]
        avg = filtered_df['Value'].mean()
        dat[m] = round(avg,4)
    Dat[j] = dat
save_json(Dat, './output/graph_theory/metric_summary.json')

# Test each metric for significance depending on normality
groupSignificance = {}
for j in normMetrics.keys():
    sig_data = [allData.loc[(allData['Group'] == m) & (allData['Metric'] == j), 'Value'].tolist()
        for m in set(allData['Group'])]
    if normMetrics[j] == 'norm':
        f, p = stats.f_oneway(*sig_data)
    else:
        f, p = stats.kruskal(*sig_data)
    groupSignificance[j] = float(p)
significance_labels = {group: {
    'significance': p < 0.05,
    'p_value': p,
    'norm': normMetrics[group] == 'norm',
    'f': f
} for group, p in groupSignificance.items()}
save_json(significance_labels, './output/graph_theory/macroSignificance.json')

# Correct for multiple comparisons
p_vals = [significance_labels[key]['p_value'] for key in significance_labels]
corrected_p_values = multipletests(p_vals, alpha=0.05, method='fdr_bh')
corrected_significance = {
    key: {
        **copy.deepcopy(value),  # Copy all original fields to preserve data structure
        'p_value': corr_p,       # Update corrected p-value
        'significance': sig      # Update corrected significance
    }
    for (key, value), corr_p, sig in zip(
        significance_labels.items(),
        corrected_p_values[1],  # Corrected p-values
        corrected_p_values[0]  # Corrected significance
    )
}
for key, value in corrected_significance.items():
    value['significance'] = str(value['significance'])  # Convert boolean to string
    value['norm'] = str(value['norm'])  # Convert 'norm' to string (if applicable)

save_json(corrected_significance, './output/graph_theory/macroSignificance_FDRcorrected.json')

# Post-hoc tests for each significant metric
post_hoc = []
for metric, metric_dict in significance_labels.items():
    significant = metric_dict['significance']
    norm = metric_dict['norm']
    if significant:
        comparisons = []
        p_values = []
        test_results = []

        for i in list(set(allData['Group'])):
            for j in list(set(allData['Group'])):
                if (i != j) & (f'{i} vs {j}' not in comparisons) & (f'{j} vs {i}' not in comparisons):
                    if norm:
                        f, p = stats.ttest_ind(
                            allData.loc[(allData['Group'] == i) & (allData['Metric'] == metric), 'Value'],
                            allData.loc[(allData['Group'] == j) & (allData['Metric'] == metric), 'Value'])
                    else:
                        f, p = stats.mannwhitneyu(
                            allData.loc[(allData['Group'] == i) & (allData['Metric'] == metric), 'Value'],
                            allData.loc[(allData['Group'] == j) & (allData['Metric'] == metric), 'Value'])

                    p_values.append(p)
                    test_results.append({'Metric': metric, 'comparison': f'{i} vs {j}',
                                         'p': p, 'f': f, 'test': norm})
                comparisons.append(f'{j} vs {i}')

        corrected = multipletests(p_values, method='fdr_bh')
        corrected_p_values = corrected[1]  # Adjusted p-values

        for idx, result in enumerate(test_results):
            result['p_corrected'] = corrected_p_values[idx]
            if corrected_p_values[idx] < 0.001:
                result['level'] = '***'
            elif corrected_p_values[idx] < 0.01:
                result['level'] = '**'
            elif corrected_p_values[idx] < 0.05:
                result['level'] = '*'
            else:
                result['level'] = ''
            if result['level']:  # Append only significant results
                post_hoc.append(pd.DataFrame(result, index=[0]))

post_hoc = pd.concat(post_hoc, axis=0)
post_hoc.to_csv('./output/graph_theory/macroSignificance_postHoc.csv')



