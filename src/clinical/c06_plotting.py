import pandas as pd

from common.visualisation import *
from common.functions import *

# Load data
data = pd.read_csv((study_folder + 'NEUROPSYCH/filtered_data.csv')).fillna(0)
significance_data = pd.read_csv((study_folder + 'NEUROPSYCH/group_significance.csv'))
post_hoc = pd.read_csv((study_folder + 'NEUROPSYCH/post_hoc_results.csv'))['feature'].unique()

# Create violin plots for each variable
for index, row in significance_data.iterrows():
    plt.figure()
    y = row['feature']
    sns.boxplot(data=data, x='diagnosis', y=y)
    plt.xlabel('Group')
    # if y in post_hoc:
    #     significance_bars(y)
    # plt.show()
    # plt.savefig((f'./figures/f02_plots/{y}_plot.png'), format='png', dpi=500)
    plt.close()