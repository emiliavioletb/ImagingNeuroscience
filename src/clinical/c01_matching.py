import matplotlib.pyplot as plt
import pandas as pd

# Emilia Butters, Cambridge University, October 2023

from common.functions import *
from common.stats_test import *

demo_data = pd.read_csv((study_folder + 'ANALYSIS/demographic_data.csv'))
demo_variables = ['age', 'sex']

for i in demo_variables:
    x = demo_data[i]
    norm_test = normality_test(x, i)
    x_transformed = list(demo_data.groupby('group')[i].apply(list))
    if norm_test:
        one_way_anova(x_transformed, i)
    else:
        kruskal_wallis(x_transformed, i)

# Plotting age
age_gb = demo_data.groupby(['group'])['age'].mean()
age_gb_std = demo_data.groupby(['group'])['age'].std()
age_gb.plot(kind='bar', title='Mean age across groups', ylabel='Mean age (years)',
         xlabel='Group', yerr=[age_gb_std])
plt.tight_layout()
plt.savefig('./figures/demo_age.svg', format='svg')

# Plotting sex
sex_gb = demo_data.groupby(['group'])['sex'].sum()/demo_data.groupby(['group'])['sex'].count()*100
sex_gb.plot(kind='bar', title='Percent females across groups', ylabel='Percent females (%)',
         xlabel='Group')
plt.tight_layout()
plt.savefig('./figures/demo_sex.svg', format='svg')
