
# Emilia Butters, Cambridge University, October 2023

from scipy import stats
import numpy as np
import statsmodels.api as sm
from sklearn.preprocessing import LabelEncoder
import statsmodels.stats.api as sms
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson
from statsmodels.graphics.regressionplots import plot_leverage_resid2
from statsmodels.stats.multitest import multipletests

def significance(x, num_comparisons=1, feature=None):
    if x <= 0.05/num_comparisons:
        res = 'Yes'
        lev = '*'
        if feature is not None:
            print(f'Significant differences in {feature} with p value of {x}')
        if x <= 0.01/num_comparisons:
            lev = '**'
            if x <= 0.001/num_comparisons:
                lev='***'
    elif x > 0.05/num_comparisons:
        res = 'No'
        if feature is not None:
            print(f'No significant difference in {feature} with p value of {x}')
        lev='ns'
    return res, lev

def normality_test(x, y='var', print_output=0):
    pval = 0.05
    if len(x) < 3:
        distribution = 0
    else:
        f, p = stats.shapiro(x)
        if p < pval:
            print ('Data for {} is not normally distributed'.format(str(y))) if print_output else None
            distribution = 0
        elif p > pval:
            print ('Data for {} is normally distributed'.format(str(y))) if print_output else None
            distribution = 1
    return distribution

def one_way_anova(x, y=None):
    pval = 0.05
    f, p = stats.f_oneway(*x)
    if y is not None:
        res = significance(p, feature=y)
    else:
        res = significance(p)
    return f, round(p, 3), res

def kruskal_wallis(x, y=None):
    pval = 0.05
    f, p = stats.kruskal(*x)
    if y is not None:
        res = significance(p, feature=y)
    else:
        res = significance(p)
    return round(f, 3), round(p, 3), res

def t_test(x, y=None):
    pval = 0.05
    s, p = stats.ttest_ind(*x)
    if y is not None:
        res = significance(p, feature=y)
    else:
        res = significance(p)
    return round(s, 3), round(p, 3)

def mann_whitney(x, y=None):
    pval = 0.05
    f, p = stats.mannwhitneyu(*x)
    if y is not None:
        res = significance(p, feature=y)
    else:
        res = significance(p)
    return round(f, 3), round(p, 3)

def get_mean(x, decimal_places=3):
    m = round(np.mean(x),decimal_places)
    return m

def get_std(x, decimal_places=3):
    s = round(np.std(x),decimal_places)
    return s

def get_corr(x, y):
    r = np.corrcoef(x, y)
    return r



