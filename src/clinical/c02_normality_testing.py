from common.functions import *

# load data
cleaned_data = pd.read_csv('./data/filtered_data.csv')
groups = list(set(cleaned_data['diagnosis']))

# testing features for normality
normality_dict = {}
for j in features:
    dat = cleaned_data[[j, 'diagnosis']]
    norm = []
    for m in groups:
        x = dat.loc[dat['diagnosis']== m, j]
        f, p = stats.shapiro(x)
        if p < 0.05:
            res = 0
        else:
            res = 1
        norm.append(res)
    if 0 in norm:
        normality_dict[j] = 0
    else:
        normality_dict[j] = 1

save_json(normality_dict, ('./data/normality_test_results.json'))