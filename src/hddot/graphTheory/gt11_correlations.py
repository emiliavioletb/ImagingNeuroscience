
from common.functions import *

plt.rcParams["font.family"] = "Arial"
allDat = pd.read_csv('./data/regression_data.csv')
gtMetrics = ['avgBtwCentrality', 'avgClustering', 'avgDegDensity', 'avgDegree', 'avgEigCentrality',
             'globEfficiency', 'totalStrength']
allDat = allDat.dropna(subset=gtMetrics + ['age', 'mmse_total'])

# testing normality of correlated variables
vars = ['age','mmse_total', 'atrophy_rating']
norm_dict = {}
for j in vars:
    dat = allDat[j]
    f, p = stats.shapiro(dat)
    if p < 0.05:
        print(f'{j} not normally distributed')
        norm_dict[j] = 0
    else:
        print(f'{j} normally distributed')
        norm_dict[j] = 1

# compute correlation between variables and graph theory metrics
remap_labels = {'avgBtwCentrality': 'Average Betweeness Centrality',
                'avgClustering': 'Average Clustering',
                'avgDegDensity': 'Average Degree Density',
                'avgDegree':'Average Node degree',
                'avgEigCentrality': 'Average Eigen Centrality',
                'globEfficiency': 'Global Efficiency',
                'totalStrength': 'Total Strength'}

list_sig_corrs = []
for var in vars:
    if var == 'mmse_total':
        gtMetric_pooled = []
        corrs_pooled = []
        pVals_pooled = []
        df_within = []
        group_within = []
        corrs_within = []
        pVal_within = []
        gtMetric_within = []
        fig, axs = plt.subplots(nrows=1, ncols=2)
        for metric in gtMetrics:
            print(f'Running variable {var}')
            if var == 'atrophy_rating':
                allDat = allDat.loc[allDat['diagnosis']!='HC']
            fig, ax = plt.subplots(figsize=(4.8, 3.5))
            pal = sns.color_palette()
            color_palette = {'HC': pal[0], 'MCI': pal[1], 'AD': pal[2]}
            graph = sns.lmplot(x=var, y=metric, hue='diagnosis', data=allDat, fit_reg=False, legend=False, palette=color_palette)
            sns.set_theme(style='whitegrid')
            sns.regplot(data=allDat, x=var, y=metric, scatter=False, ax=graph.axes[0, 0])
            plt.ylabel(remap_labels[metric], fontsize=17)
            plt.xlabel(var)
            if norm_dict[var]:
                corr, p_value = stats.pearsonr(allDat[var],
                                            allDat[metric])
                print(f"{metric} normally distributed so using Pearson's")
            else:
                corr, p_value = stats.spearmanr(allDat[var],
                                               allDat[metric])
                print(f"{metric} not normally distributed so using Spearman's")
            gtMetric_pooled.append(metric)
            corrs_pooled.append(corr)
            pVals_pooled.append(p_value)
            if p_value <= 0.05:
                # plt.figtext(0.2, 0.85, f'p = {round(p_value, 2)}', color='red', weight='bold')
                list_sig_corrs.append({'var': var, 'metric':metric})
            else:
                plt.figtext(0.2, 0.85, f'$p = {round(p_value, 2)}$')
            plt.legend(title="Group", fontsize=20, title_fontsize=20, loc='center left', bbox_to_anchor=(1, 0.5),
                       markerscale=3)
            plt.tight_layout()
            # plt.show()
            # y = f'{var} vs {metric}'
            plt.savefig((f'./output/graph_theory/figures/{y}.png'), format='png', dpi=500)
            for group in allDat['diagnosis'].unique():
                dat_group = allDat.loc[allDat['diagnosis'] == group]
                if norm_dict[var]:
                    corr, p_value = stats.pearsonr(dat_group[var],
                                                   dat_group[metric])
                else:
                    corr, p_value = stats.spearmanr(dat_group[var],
                                                    dat_group[metric])
                gtMetric_within.append(metric)
                group_within.append(group)
                pVal_within.append(p_value)
                corrs_within.append(corr)
        allCorrs_pooled = pd.DataFrame({
            'Metric': gtMetric_pooled,
            'Corr': corrs_pooled,
            'P_val': pVals_pooled
        })
        allCorrs_pooled.to_csv(f'./output/graph_theory/{var}_corr.csv')

        # Correct for multiple comparisons
        p_vals = allCorrs_pooled['P_val'].to_list()
        corrected_p_values = multipletests(p_vals, alpha=0.05, method='fdr_bh')
        corr_df_FDR = allCorrs_pooled.copy()
        corr_df_FDR['P_val'] = corrected_p_values[1]
        corr_df_FDR.to_csv(f'./output/graph_theory/{var}_corr_FDR.csv')

        allCorrs_within = pd.DataFrame({'Group': group_within, 'Metric': gtMetric_within,
                                      'P_val': pVal_within, 'Corr': corrs_within})
        allCorrs_within.to_csv(f'./output/graph_theory/{var}_corr_group.csv')

# save dataframe of significant correlations for future radial plotting
list_sig_corrs = pd.DataFrame(list_sig_corrs)
list_sig_corrs.to_csv('./output/graph_theory/only_sig_corrs.csv')


