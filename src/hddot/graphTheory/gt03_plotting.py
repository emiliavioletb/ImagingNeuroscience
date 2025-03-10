import matplotlib.pyplot as plt

from common.stats_test import *
from common.visualisation import *
sns.set_theme(style='whitegrid')
plt.rcParams["font.family"] = "Arial"  # Set global font to Arial

allData = pd.read_csv('./output/graph_theory/macroProperties.csv')
significance_labels = load_json('./output/graph_theory/macroSignificance.json')
significance_labels.pop('avgDegree', None)

# Boxplot metrics with significance bars
remap_labels = {'totalStrength': 'Total Strength',
                'avgDegDensity': 'Degree Density',
                'globEfficiency': 'Global Efficiency',
                'avgBtwCentrality': 'Betweenness Centrality',
                'avgClustering': 'Clustering',
                'avgEigCentrality': 'Eigenvector Centrality'}

y_shift = 1
x_shift = -2
fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(11, 6.5))
axs = axs.flatten()
metrics = list(remap_labels.keys())
for idx, metric in enumerate(metrics):
    ax = axs[idx]
    figDat = allData.loc[allData['Metric']==metric]
    sns.boxplot(data=figDat, x='Group', y='Value', order=['HC', 'MCI', 'AD'], width=0.5,
                flierprops={'marker': 'o', 'markersize': 5, 'markerfacecolor': 'none'}, ax=ax)
    x1, x2, x3 = 0, 1, 2
    y, h, col = max(figDat['Value']) + (max(figDat['Value'])*0.03), 0.2, 'k'
    if metric == 'avgBtwCentrality':
        ax.set_ylim([0, 0.055])
        ax.text(x_shift, ax.get_ylim()[1] * y_shift, "(d)", fontsize=20, fontweight='bold', va='top', ha='left')

    if metric == 'avgEigCentrality':
        ax.set_ylim([0, 0.2])
        ax.set_yticks(np.arange(0, 0.25, 0.05))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.2f}'))
        ax.text(x_shift, ax.get_ylim()[1] * y_shift, "(f)", fontsize=20, fontweight='bold', va='top', ha='left')

    if metric == 'globEfficiency':
        ax.set_ylim([0, 0.27])
        ax.set_yticks(np.arange(0, 0.3, 0.05))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.2f}'))
        y, h, col = max(figDat['Value']) + (max(figDat['Value']) * 0.03), 0.2, 'k'
        ax.plot([x1, x1, x2, x2], [y, y + (y*0.055), y + (y*0.055), y], lw=1.5, c=col)
        ax.text((x1 + x2) * .5, y + (y*0.00001), "**", ha='center', va='bottom', color=col, fontsize=25)
        y, h, col = max(figDat['Value']) + (max(figDat['Value'])*0.3), 0.2, 'k'
        ax.plot([x1, x1, x3, x3], [y, y + (y*0.04), y + (y*0.04), y], lw=1.5, c=col)
        ax.text((x1 + x3) * .5, y + (y*0.00001), "**", ha='center', va='bottom', color=col, fontsize=25)
        ax.text(x_shift, ax.get_ylim()[1] * y_shift, "(c)", fontsize=20, fontweight='bold', va='top', ha='left')

    if metric == 'totalStrength':
        ax.set_ylim([0, 700])
        ax.set_yticks(np.arange(0, 700, 100))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0f}'))
        y, h, col = max(figDat['Value']) + (max(figDat['Value']) * 0.05), 0.2, 'k'
        ax.plot([x1, x1, x2, x2], [y, y + (y*0.05), y + (y*0.05), y], lw=1.5, c=col)
        ax.text((x1 + x2) * .5, y + (y*0.00001), "*", ha='center', va='bottom', color=col, fontsize=25)
        y, h, col = max(figDat['Value']) + (max(figDat['Value'])*0.3), 0.2, 'k'
        ax.plot([x1, x1, x3, x3], [y, y + (y*0.05), y + (y*0.05), y], lw=1.5, c=col)
        ax.text((x1 + x3) * .5, y + (y*0.00001), "*", ha='center', va='bottom', color=col, fontsize=25)
        ax.text(x_shift, ax.get_ylim()[1]*y_shift, "(a)", fontsize=20, fontweight='bold', va='top', ha='left')

    if metric == 'avgDegDensity':
        ax.set_ylim([0, 0.77])
        ax.set_yticks(np.arange(0, 0.8, 0.1))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.1f}'))
        y, h, col = max(figDat['Value']) + (max(figDat['Value']) * 0.12), 0.2, 'k'
        ax.plot([x1, x1, x2, x2], [y, y + (y*0.05), y + (y*0.05), y], lw=1.5, c=col)
        ax.text((x1 + x2) * .5, y + (y*0.00001), "**", ha='center', va='bottom', color=col, fontsize=25)
        y, h, col = max(figDat['Value']) + (max(figDat['Value'])*0.4), 0.2, 'k'
        ax.plot([x1, x1, x3, x3], [y, y + (y*0.04), y + (y*0.04), y], lw=1.5, c=col)
        ax.text((x1 + x3) * .5, y + (y*0.00001), "**", ha='center', va='bottom', color=col, fontsize=25)
        ax.text(x_shift, ax.get_ylim()[1] * y_shift, "(b)", fontsize=20, fontweight='bold', va='top', ha='left')

    if metric == 'avgClustering':
        ax.set_ylim([0, 0.27])
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.2f}'))
        ax.text(x_shift, ax.get_ylim()[1] * y_shift, "(e)", fontsize=20, fontweight='bold', va='top', ha='left')

    ax.set_ylabel(remap_labels[metric], fontsize=16)
    ax.set_xticks([0, 1, 2], labels=['HC', 'MCI', 'AD'], fontsize=13)
    ax.set_xlabel('Group', fontsize=17)
plt.tight_layout()
plt.subplots_adjust(hspace=0.36, wspace=0.6)
# plt.show()
plt.savefig((f'./output/graph_theory/figures/global_metrics_plot.png'), format='png', dpi=500)
