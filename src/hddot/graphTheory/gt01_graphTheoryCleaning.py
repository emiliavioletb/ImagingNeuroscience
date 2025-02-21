import pandas as pd

from common.functions import *
from common.stats_test import *
from functools import reduce

# Define data folders
datFolder = '/Users/emilia/Documents/Publications/Human Brain Mapping/data/'

# Define metrics of interest
gtMetrics = ['avgBtwCentrality', 'avgClustering', 'avgDegDensity', 'avgDegree', 'avgEigCentrality',
             'globEfficiency', 'totalStrength']

# Load data
MCI = mat73.loadmat(datFolder + 'MCI_gtMetrics.mat')['macroProperties']
HC = mat73.loadmat(datFolder + 'HC_gtMetrics.mat')['macroProperties']
AD = mat73.loadmat(datFolder + 'AD_gtMetrics.mat')['macroProperties']

# Extract metrics for each subject group and create dataframe to store data
allData = []
for j in gtMetrics:
    a = pd.DataFrame({'Group': ['MCI']*len(MCI[j]), 'Value': MCI[j],
                      'subject_code': np.array(MCI['fname']).flatten()})
    b = pd.DataFrame({'Group': ['AD'] * len(AD[j]), 'Value': AD[j],
                      'subject_code': np.array(AD['fname']).flatten()})
    c = pd.DataFrame({'Group': ['HC'] * len(HC[j]), 'Value': HC[j],
                      'subject_code': np.array(HC['fname']).flatten()})
    d = pd.concat([a, b, c], axis=0)
    d['Metric'] = str(j)
    allData.append(d)
allData = pd.concat(allData, ignore_index=True)

allData.to_csv('./output/graph_theory/macroProperties.csv', index=False)

# Pivot table so each row is a subject and each column is a metric
pivot_df = allData.pivot(index='subject_code', columns='Metric', values='Value').reset_index()

# Extract num_parcels per group and re-name index column 'subject_code'
num_parcels = pd.concat([pd.DataFrame(MCI)[['fname', 'num_parcels']],
                        pd.DataFrame(AD)[['fname', 'num_parcels']],
                        pd.DataFrame(HC)[['fname', 'num_parcels']]], axis=0)
num_parcels['subject_code'] = [x[0] if isinstance(x, list) else x for x in num_parcels['fname']]
num_parcels = num_parcels.drop(columns='fname')

# Merge graph theory metrics, neuropsych, and num_parcels
neuropsych = pd.read_csv('./data/filtered_data.csv')
allData_reg = reduce(lambda  left,right: pd.merge(left,right,on=['subject_code'],
                                            how='inner'), [pivot_df, neuropsych, num_parcels])
allData_reg.to_csv('./data/regression_data.csv', index=False)

# Test each metric for normality
normMetrics = {}
for j in gtMetrics:
    norm = []
    for m in list(allData['Group'].unique()):
        x = allData.loc[(allData['Group'] == m) & (allData['Metric'] == j), ['Value']]
        f, p = stats.shapiro(x)
        if p < 0.05:
            norm.append(1)
        else:
            norm.append(0)
    if 1 in norm:
        normMetrics[j] = 'not norm'
    else:
        normMetrics[j] = 'norm'
save_json(normMetrics, './output/graph_theory/macroProperties_norm.json')

