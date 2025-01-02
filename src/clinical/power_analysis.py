import scipy.stats
import statsmodels.stats.power as smp
import matplotlib.pyplot as plt
from statistics import mean, stdev
from math import sqrt

cohens_d = (0.42 - (-0.87)) / (sqrt(0.17 ** 2 + 0.37 ** 2) / 2)
power_analysis = smp.TTestIndPower()
sample_size = power_analysis.solve_power(effect_size=cohens_d, power=0.8, alpha=0.05, alternative='larger')
sample_size