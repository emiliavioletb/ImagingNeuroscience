import pandas as pd

from common.visualisation import *
from common.functions import *

data = pd.read_csv((study_folder + 'NEUROPSYCH/filtered_data.csv')).fillna(0)
data = data.drop(40)
significance_data = pd.read_csv((study_folder + 'NEUROPSYCH/group_significance.csv'))

comparisons = []
for index, row in significance_data.iterrows():
    for index2, row2 in significance_data.iterrows():
        if (row['feature'] != row2['feature']) & ((f'{row["feature"]}_vs_{row2["feature"]}') not in comparisons):
            plt.figure()
            sns.lmplot(data=data, x=row["feature"], y=row2["feature"], hue='diagnosis', palette='mako')
            # plt.show()
            comparisons.append(f'{row["feature"]}_vs_{row2["feature"]}')
            comparisons.append(f'{row2["feature"]}_vs_{row["feature"]}')
            plt.savefig(f'./figures/f03_correlations/{row["feature"]}_vs_{row2["feature"]}.png', format='png', dpi=500)
            plt.close()

