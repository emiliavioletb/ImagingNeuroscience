import matplotlib.pyplot as plt
import pandas as pd

from common.functions import *
from common.stats_test import *
from common.visualisation import *

plt.rcParams["font.family"] = "Arial"
allDat = pd.read_csv('./data/regression_data.csv')

gtMetrics = ['avgBtwCentrality', 'totalStrength']
allDat = allDat.dropna(subset=gtMetrics + ['age', 'mmse_total'])

remap_labels = {'avgBtwCentrality': 'Average Betweenness Centrality',
                'totalStrength': 'Total Strength'}

fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
for m, metric in enumerate(gtMetrics):
    pal = sns.color_palette()
    color_palette = {'HC': pal[0], 'MCI': pal[1], 'AD': pal[2]}
    sns.scatterplot(x='mmse_total', y=metric, hue='diagnosis', data=allDat, palette=color_palette,
                    hue_order=['HC', 'MCI', 'AD'], ax=axs[m], s=85)
    sns.regplot(data=allDat, x='mmse_total', y=metric, scatter=False, ax=axs[m])
    sns.set_theme(style='whitegrid')
    axs[m].set_ylabel(remap_labels[metric], fontsize=20)
    axs[m].set_xlabel('MMSE score', fontsize=20)
    axs[m].set_xlim([11, 32])
    axs[m].set_xticks([15, 20, 25, 30])
    axs[m].tick_params(axis='both', labelsize=13)
plt.legend(title='Group', fontsize=17, title_fontproperties={'weight':'bold', 'size': 20}, loc='center left',
           bbox_to_anchor=(1, 0.85), markerscale=3, fancybox=True)
plt.tight_layout()
# plt.show()
plt.savefig((f'./output/graph_theory/figures/correlations.png'), format='png', dpi=500)
