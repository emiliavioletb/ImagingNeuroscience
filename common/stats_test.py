
# Emilia Butters, Cambridge University, October 2023

from scipy import stats
from colorama import Fore


def normality_test(x, y):
    pval = 0.05
    f, p = stats.shapiro(x)
    if p < pval:
        print('Data for {} is not normally distributed'.format(str(y)))
        distribution = 0
    elif p > pval:
        print('Data for {} is normally distributed'.format(str(y)))
        distribution = 1
    return distribution

def one_way_anova(x, y):
    pval = 0.05
    f, p = stats.f_oneway(*x)
    if p < pval:
        print('Significant differences in {} between groups'.format(str(y)))
    elif p > pval:
        print('No significant difference in {} between groups'.format(str(y)))

def kruskal_wallis(x, y):
    pval = 0.05
    f, p = stats.kruskal(*x)
    if p < pval:
        print('Significant differences in {} between groups'.format(str(y)))
    elif p > pval:
        print('No significant difference in {} between groups'.format(str(y)))