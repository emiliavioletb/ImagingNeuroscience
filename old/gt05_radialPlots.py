import matplotlib.pyplot as plt
import pandas as pd

from common.functions import *

vars = ['mmse_total', 'age']
sig_corrs = pd.read_csv('./output/graph_theory/only_sig_corrs.csv')
for var in vars:
    if var in sig_corrs['var'].to_list():
        corrs = pd.read_csv(f'./output/graph_theory/{var}_corr_group.csv')
        remap_labels = {'avgBtwCentrality': 'Average Betweeness \nCentrality',
                        'avgClustering': 'Average Clustering',
                        'avgDegDensity': 'Average Degree \nDensity',
                        'avgDegree':'Average Node \nDegree',
                        'avgEigCentrality': 'Average Eigen Centrality',
                        'globEfficiency': 'Global Efficiency',
                        'totalStrength': 'Total Strength'}
        labels = sig_corrs['metric'].to_list()

        filtered_corrs = corrs[corrs['Metric'].isin(labels)]
        values1 = filtered_corrs.loc[filtered_corrs['Group'] == 'AD', 'Corr'].astype(float).tolist()
        values2 = filtered_corrs.loc[filtered_corrs['Group'] == 'HC', 'Corr'].astype(float).tolist()
        num_vars = len(values1)

        angles1 = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        values1 += values1[:1]
        angles1 += angles1[:1]

        angles2 = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        values2 += values2[:1]
        angles2 += angles2[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.plot(angles1, values1, color='#1aaf6c', linewidth=1, label="Alzheimer's Disease")
        ax.fill(angles1, values1, color='#1aaf6c', alpha=0.25)
        ax.plot(angles2, values2, color='#ff6347', linewidth=1, label='Healthy controls')
        ax.fill(angles2, values2, color='#ff6347', alpha=0.25)

        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_ylim(-1, 1)
        ax.tick_params(colors='#222222')
        # ax.axhline(0, color='black', linewidth=2.5, linestyle='-', zorder=10)
        remapped_labels = [remap_labels[label] for label in labels]
        ax.set_thetagrids(np.degrees(angles1[:-1]), remapped_labels, fontsize=10)
        ax.set_rlabel_position(180 / num_vars)
        for label, angle in zip(ax.get_xticklabels(), angles1):
            label.set_fontweight('bold')
            if angle in (0, np.pi):
                label.set_horizontalalignment('center')
            elif 0 < angle < np.pi:
                label.set_horizontalalignment('left')
            else:
                label.set_horizontalalignment('right')
        ax.legend(loc='upper left', bbox_to_anchor=(0.85, 1.2), fontsize=10, frameon=False)
        ax.tick_params(axis='y', labelsize=8)
        ax.grid(color='#AAAAAA')
        ax.spines['polar'].set_color('#222222')
        ax.set_facecolor('#FAFAFA')
        plt.tight_layout()
        # ax.set_title(f'Correlation with {var}')
        plt.show()
        # plt.savefig(f'./output/graph_theory/figures/{var}_radialplot.png', format='png', dpi=500)

