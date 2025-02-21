import matplotlib.pyplot as plt

from common.stats_test import *
from common.visualisation import *
import copy

allData = pd.read_csv('./output/graph_theory/macroProperties.csv')
significance_labels = load_json('./output/graph_theory/macroSignificance.json')

# Boxplot metrics with significance bars
remap_labels = {'avgBtwCentrality': 'Average Betweeness \nCentrality',
                'avgClustering': 'Average Clustering',
                'avgDegDensity': 'Average Degree Density',
                'avgDegree':'Average Node degree',
                'avgEigCentrality': 'Average Eigenvector \nCentrality',
                'globEfficiency': 'Global Efficiency',
                'totalStrength': 'Total Strength'}
for metric in significance_labels.keys():
    sns.set_theme(style='whitegrid')
    if metric == 'avgBtwCentrality' or 'avgEigCentrality':
        fig1, ax1 = plt.subplots(figsize=(3.56, 3.5))
    else:
        fig1, ax1 = plt.subplots(figsize=(3.3, 3.5))
    figDat = allData.loc[allData['Metric']==metric]
    sns.boxplot(data=figDat, x='Group', y='Value', order=['HC', 'MCI', 'AD'], width=0.5,
                flierprops={'marker': 'o', 'markersize': 5, 'markerfacecolor': 'none'})
    plt.xlabel('Group')
    x1, x2, x3 = 0, 1, 2
    y, h, col = max(figDat['Value']) + (max(figDat['Value'])*0.03), 0.2, 'k'
    if metric == 'avgBtwCentrality':
        plt.ylim([0, y+(y*0.15)])
    if metric == 'avgEigCentrality':
        plt.ylim([0, 0.2])
        plt.yticks(np.arange(0, 0.25, 0.05))
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.2f}'))

    if metric == 'globEfficiency':
        plt.ylim([0, y + (y * 0.4)])
        plt.yticks(np.arange(0, 0.3, 0.05))
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.2f}'))
        y, h, col = max(figDat['Value']) + (max(figDat['Value']) * 0.03), 0.2, 'k'
        plt.plot([x1, x1, x2, x2], [y, y + (y*0.03), y + (y*0.03), y], lw=1.5, c=col)
        plt.text((x1 + x2) * .5, y + (y*0.00001), "**", ha='center', va='bottom', color=col, fontsize=25)

        y, h, col = max(figDat['Value']) + (max(figDat['Value'])*0.3), 0.2, 'k'
        plt.plot([x1, x1, x3, x3], [y, y + (y*0.03), y + (y*0.03), y], lw=1.5, c=col)
        plt.text((x1 + x3) * .5, y + (y*0.00001), "**", ha='center', va='bottom', color=col, fontsize=25)

    if metric == 'totalStrength':
        plt.ylim([0, y + (y * 0.5)])
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0f}'))
        y, h, col = max(figDat['Value']) + (max(figDat['Value']) * 0.05), 0.2, 'k'
        plt.plot([x1, x1, x2, x2], [y, y + (y*0.03), y + (y*0.03), y], lw=1.5, c=col)
        plt.text((x1 + x2) * .5, y + (y*0.00001), "*", ha='center', va='bottom', color=col, fontsize=25)

        y, h, col = max(figDat['Value']) + (max(figDat['Value'])*0.3), 0.2, 'k'
        plt.plot([x1, x1, x3, x3], [y, y + (y*0.03), y + (y*0.03), y], lw=1.5, c=col)
        plt.text((x1 + x3) * .5, y + (y*0.00001), "*", ha='center', va='bottom', color=col, fontsize=25)

    if metric == 'avgDegree':
        plt.ylim([0, y + (y * 0.6)])
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0f}'))
        y, h, col = max(figDat['Value']) + (max(figDat['Value']) * 0.12), 0.2, 'k'
        plt.plot([x1, x1, x2, x2], [y, y + (y*0.03), y + (y*0.03), y], lw=1.5, c=col)
        plt.text((x1 + x2) * .5, y + (y*0.00001), "*", ha='center', va='bottom', color=col, fontsize=25)

        y, h, col = max(figDat['Value']) + (max(figDat['Value'])*0.4), 0.2, 'k'
        plt.plot([x1, x1, x3, x3], [y, y + (y*0.03), y + (y*0.03), y], lw=1.5, c=col)
        plt.text((x1 + x3) * .5, y + (y*0.00001), "*", ha='center', va='bottom', color=col, fontsize=25)

    if metric == 'avgDegDensity':
        plt.ylim([0, y + (y * 0.6)])
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.1f}'))
        y, h, col = max(figDat['Value']) + (max(figDat['Value']) * 0.12), 0.2, 'k'
        plt.plot([x1, x1, x2, x2], [y, y + (y*0.03), y + (y*0.03), y], lw=1.5, c=col)
        plt.text((x1 + x2) * .5, y + (y*0.00001), "**", ha='center', va='bottom', color=col, fontsize=25)

        y, h, col = max(figDat['Value']) + (max(figDat['Value'])*0.4), 0.2, 'k'
        plt.plot([x1, x1, x3, x3], [y, y + (y*0.03), y + (y*0.03), y], lw=1.5, c=col)
        plt.text((x1 + x3) * .5, y + (y*0.00001), "**", ha='center', va='bottom', color=col, fontsize=25)

    if metric == 'avgClustering':
        plt.ylim([0, y + (y * 0.25)])
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.2f}'))

    plt.ylabel(remap_labels[metric], fontsize=17)
    plt.xticks([0, 1, 2], labels=['HC', 'MCI', 'AD'], fontsize=13)
    plt.xlabel('Group', fontsize=17)
    plt.tight_layout()
    # plt.show()
    plt.savefig((f'./output/graph_theory/figures/{metric}_plot.png'), format='png', dpi=500)
    plt.close()
