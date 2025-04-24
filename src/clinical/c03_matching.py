
from common.functions import *

# load data
filtered_data = pd.read_csv('./data/filtered_data.csv')
filtered_data = filtered_data[['participant_number', 'diagnosis', 'sex', 'age']]

# remove DLBs
filtered_data = filtered_data.loc[filtered_data['diagnosis']!='DLB']

# test for differences in age
norm_age = []
for j in list(set(filtered_data['diagnosis'])):
    f, p = stats.shapiro(filtered_data.loc[filtered_data['diagnosis']==j, 'age'])
    if p < 0.05:
        norm_age.append(1)
    else:
        norm_age.append(0)
age_transformed = [list(filtered_data.loc[filtered_data['diagnosis']==j, 'age']) for j in list(set(filtered_data['diagnosis']))]

if 0 in norm_age:
    f, p = stats.kruskal(*age_transformed)
    test = 'kruskal'
else:
    f, p = stats.f_oneway(*age_transformed)
    test = 'one way'
print(f'p = {round(p, 3)}, f = {round(f, 3)} using {test}')

# post-hoc tests
comparisons = []
for i in list(set(filtered_data['diagnosis'])):
    for j in list(set(filtered_data['diagnosis'])):
        if (i != j) & (f'{i} vs {j}' not in comparisons) & (f'{j} vs {i}' not in comparisons):
            f, p = stats.mannwhitneyu(filtered_data.loc[filtered_data['diagnosis']==i, 'age'].to_list(),
                                filtered_data.loc[filtered_data['diagnosis']==j, 'age'].to_list())
            comparisons.append(f'{i} vs {j}')
            comparisons.append(f'{j} vs {i}')
            print(f'{(round(p, 3))<0.05} difference between {i} and {j}')

# plotting age
fig1, ax1 = plt.subplots(figsize=(4.8, 3.5))
sns.boxplot(data=filtered_data, x='diagnosis', y='age', palette='mako', order=['HC', 'MCI', 'AD'])
ax1.set_xlabel('Diagnosis')
# x1, x2, x3, x4  = 0,1,2,3
# y, h, col = (max(demographic_data[f]) + 1), 1, 'k'
# h = (h*2) + h_add
# plt.plot([dif1, dif1, dif2, dif2], [y+1, y+h, y+h, y+1], lw=1.5, c=col)
# plt.text((dif1+dif2)*.5, y+h, res, ha='center', va='bottom', color=col)
# h_add += 0.9
fig1.tight_layout()
plt.savefig('./figures/f01_data_cleaning/age.png', format='png', dpi=500)

# testing for differences in sex
demographic_data = convert_gender(filtered_data)
contigency = pd.crosstab(demographic_data['sex'], demographic_data['diagnosis'])
c, p_sex, dof, expected = stats.chi2_contingency(contigency)
contigency_pct = pd.crosstab(demographic_data['sex'], demographic_data['diagnosis'], normalize='columns')
print(f'p = {round(p, 3)}, c = {round(c, 3)}')

# plotting sex
fig, ax = plt.subplots(figsize=(4.8, 3.5))
contigency_pct = contigency_pct.reset_index()
contigency_pct_melted = contigency_pct.melt(id_vars="sex", value_vars=contigency_pct.columns[1:],
                                            var_name="diagnosis", value_name="Proportion")
contigency_pct_pivot = contigency_pct_melted.pivot_table(index='diagnosis', columns='sex', values='Proportion')
desired_order = ['HC', 'MCI', 'AD']
contigency_pct_pivot = contigency_pct_pivot.reindex(desired_order)
contigency_pct_pivot.plot(kind='bar', stacked=True, ax=ax, cmap=ListedColormap(['cadetblue', 'lightsteelblue']))
ax.set_ylabel('Proportion')
ax.set_xlabel('Sex')
ax.legend(loc='lower right')
fig.tight_layout()
plt.savefig('./figures/f01_data_cleaning/sex.png', format='png', dpi=500)

