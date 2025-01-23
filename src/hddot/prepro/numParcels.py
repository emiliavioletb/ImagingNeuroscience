import pandas as pd

from common.functions import *
from common.stats_test import *

allDat = pd.read_csv('./data/regression_data.csv')

for j in np.unique(allDat['diagnosis']):
    f, p = stats.shapiro(allDat.loc[allDat['diagnosis']==j, 'num_parcels'])
    if p <= 0.05:
        print('Not normally distributed')

parcels_transformed = [list(allDat.loc[allDat['diagnosis']==j, 'num_parcels']) for j in list(set(allDat['diagnosis']))]
f, p = stats.kruskal(*parcels_transformed)

fig1, ax1 = plt.subplots(figsize=(5.5, 4.5))
sns.set_theme(style='whitegrid')
sns.violinplot(data=allDat, x='diagnosis', y='num_parcels', order=['HC', 'MCI', 'AD'])
plt.tight_layout()
plt.ylabel('Number of parcels', fontsize=20)
plt.ylim(0, 100)
plt.xlabel('Group', fontsize=20)
# plt.show()
plt.savefig('./figures/prepro/num_parcels.png', format='png', dpi=500)


