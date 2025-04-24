

from common.functions import *

motifs = pd.read_csv('~/Documents/PUBLICATIONS/Human Brain Mapping/data/motifs.csv')
motifs = motifs.drop(motifs[motifs.Motif == ' triangle_extra'].index)

triangle = motifs.loc[motifs['Motif'] == 'triangle']
open_triad = motifs.loc[motifs['Motif'] == 'open_triad']

ratios = []

for j in range(len(triangle)):
    a = triangle.iloc[j]
    b = open_triad.iloc[j]
    ratio = a['Values']/b['Values']
    ratios.append(ratio)

all_ratios = pd.DataFrame({'Ratios': ratios, 'Group': triangle['Group']})

for k in all_ratios['Group'].unique():
    f, p = stats.shapiro(all_ratios.loc[all_ratios['Group'] == k, 'Ratios'])
    if p < 0.05:
        print('not norm')

f, p = stats.kruskal(all_ratios.loc[all_ratios['Group'] == 'AD', 'Ratios'],
                     all_ratios.loc[all_ratios['Group'] == 'MCI', 'Ratios'],
                     all_ratios.loc[all_ratios['Group'] == 'HC', 'Ratios'])
