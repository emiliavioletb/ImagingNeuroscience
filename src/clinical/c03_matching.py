import pandas as pd

from common.functions import *
from common.stats_test import *

# ages = pd.read_csv((study_folder + 'NEUROPSYCH/ages.csv'))

demographic_data = pd.read_csv((study_folder + 'NEUROPSYCH/filtered_data.csv'))
demographic_data = demographic_data[['participant_number', 'diagnosis', 'sex']]

# Test for differences in age
norm_age = []
for j in list(set(demographic_data['diagnosis'])):
    f, p = stats.shapiro(demographic_data.loc[demographic_data['diagnosis']==j, 'age'])
    if p < 0.05:
        norm_age.append(1)
    else:
        norm_age.append(0)

age_transformed = [list(demographic_data.loc[demographic_data['diagnosis']==j, 'age']) for j in list(set(demographic_data['diagnosis']))]

if 0 in norm_age:
    f, p = kruskal_wallis(*age_transformed, 'age')
else:
    f, p = one_way_anova(*age_transformed, 'age')

# Plotting age
plt.figure()
sns.boxplot(data=demographic_data, x='diagnosis', y='age')
plt.tight_layout()
plt.savefig('./figures/f01_data_cleaning/age.png', format='png', dpi=500)

# Testing for differences in sex


# Plotting sex
plt.figure()
# sns.boxplot
plt.tight_layout()
plt.savefig('./figures/f01_data_cleaning/sex.png', format='png', dpi=500)
