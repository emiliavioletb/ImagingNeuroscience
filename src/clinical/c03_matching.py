import numpy as np
import pandas as pd

from common.functions import *
from common.stats_test import *
from common.clinical_functions import *

ages = pd.read_csv((study_folder + 'NEUROPSYCH/ages.csv'))
# TODO: not all ages included
demographic_data = pd.read_csv((study_folder + 'NEUROPSYCH/filtered_data.csv'))
demographic_data = demographic_data[['participant_number', 'diagnosis', 'sex']]
demographic_data = pd.merge(demographic_data, ages, on='participant_number')

# Test for differences in age
norm_age = []
for j in list(set(demographic_data['diagnosis'])):
    f, p = stats.shapiro(demographic_data.loc[demographic_data['diagnosis']==j, 'Age'])
    if p < 0.05:
        norm_age.append(1)
    else:
        norm_age.append(0)

age_transformed = [list(demographic_data.loc[demographic_data['diagnosis']==j, 'Age']) for j in list(set(demographic_data['diagnosis']))]

if 0 in norm_age:
    f, p = kruskal_wallis(age_transformed, 'Age')
else:
    f, p = one_way_anova(age_transformed, 'Age')

# Post-hoc tests
comparisons = []
for i in list(set(demographic_data['diagnosis'])):
    for j in list(set(demographic_data['diagnosis'])):
        if (i != j) & (f'{i} vs {j}' not in comparisons) & (f'{j} vs {i}' not in comparisons):
            f, p = mann_whitney(demographic_data.loc[demographic_data['diagnosis']==i, 'Age'],
                                demographic_data.loc[demographic_data['diagnosis']==j, 'Age'])
            if p < 0.05:
                res = 'Yes'
            else:
                res = 'No'
            comparisons.append(f'{i} vs {j}')
            comparisons.append(f'{j} vs {i}')
            print(f'{res} significant difference between {i} and {j}')

# Plotting age
plt.figure()
sns.boxplot(data=demographic_data, x='diagnosis', y='Age', palette='ocean_r')
plt.tight_layout()
plt.savefig('./figures/f01_data_cleaning/age.png', format='png', dpi=500)

# Testing for differences in sex
demographic_data = convert_gender(demographic_data)
contigency = pd.crosstab(demographic_data['sex'], demographic_data['diagnosis'])
c, p, dof, expected = stats.chi2_contingency(contigency)
contigency_pct = pd.crosstab(demographic_data['sex'], demographic_data['diagnosis'], normalize='columns')

# Plotting sex
contigency_pct = contigency_pct.T
plt.figure()
cmap = sns.color_palette('ocean_r')
contigency_pct.plot(kind='bar', stacked=True, color=cmap)
plt.ylabel('Proportion')
plt.xlabel('Sex')
plt.legend(title='Sex', loc='lower right')
plt.tight_layout()
plt.savefig('./figures/f01_data_cleaning/sex.png', format='png', dpi=500)
