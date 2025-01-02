import matplotlib.pyplot as plt
import pandas as pd

from common.functions import *
from common.clinical_functions import *
from common.stats_test import *

# Load data
filename = study_folder + 'NEUROPSYCH/Optical*'
filename = glob.glob(filename)[0]
redcap_data = pd.read_csv(filename)
cleaned_columns = pd.read_csv(study_folder + 'NEUROPSYCH/columns_to_keep.csv', header=None)

# Filter out excluded participants
included_data = redcap_data[redcap_data['included']==1]
included_data = included_data.drop(columns=['included'])

# Isolate visual hallucinations
VH_dat = included_data[['subject_code', 'visual_1', 'visual_2', 'visual_3', 'visual_4',
                        'visual_5', 'visual_6']]
VH_dat['tot'] = VH_dat[['visual_1', 'visual_2', 'visual_3', 'visual_4',
                                          'visual_5', 'visual_6']].sum(axis=1)
VH_dat['visual_hallucinations'] = np.where(VH_dat['tot'] > 0, 1, 0)
VH_dat = VH_dat[['subject_code', 'visual_hallucinations']]

# Included only relevant columns
columns = format_dataframe(cleaned_columns)
filtered_data = included_data[columns]

# Convert diagnosis to string labels
filtered_data = convert_diagnosis(filtered_data)

# Replace Nans with 0
filtered_data['farnsworth_test'] = filtered_data['farnsworth_test'].fillna(0)

# Compute Farnsworth scores and re-save data
standard = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
for j in filtered_data['subject_code'].unique():
    farnsworth_all = filtered_data.loc[filtered_data['subject_code'] == j, 'farnsworth_test'].to_list()
    if farnsworth_all == [0] or farnsworth_all == '[nan]':
        farnsworth_error = np.NaN
    else:
        farnsworth_all = [int(x) for a in farnsworth_all for x in a.split(',')]
        if sum(farnsworth_all) != 120:
            farnsworth_error = np.NaN
        else:
            farnsworth_error = 0
            for num in standard:
                error = abs(standard.index(num) - farnsworth_all.index(num))
                farnsworth_error += error
    filtered_data.loc[filtered_data['subject_code'] == j, 'farnsworth_error'] = farnsworth_error
columns.append('farnsworth_error')

# Add atrophy ratings to data
atrophy_rating = pd.read_csv((study_folder + 'NEUROPSYCH/atrophy_ratings.csv'), usecols=['ID', 'total'])
atrophy_rating = atrophy_rating.rename(columns={'ID': 'subject_code'})
filtered_data['subject_suffix'] = filtered_data['subject_code'].str.split('_').str[1]
filtered_data = pd.merge(filtered_data, atrophy_rating, left_on='subject_suffix', right_on='subject_code', \
                         suffixes=('', '_drop'), how='left')
filtered_data.drop(['subject_suffix', 'subject_code_drop'], axis=1, inplace=True)
filtered_data = filtered_data.rename(columns={'total': 'atrophy_rating'})
columns.append('atrophy_rating')

# Fix trails data
filtered_data['trail_a_time'] = filtered_data['trail_a_time'].astype(float)
filtered_data['trail_b_time'] = filtered_data['trail_b_time'].astype(float)
for index, row in filtered_data.iterrows():
    if filtered_data['trail_a_time'][index] == 0:
        filtered_data['trail_a_errors'][index] = np.nan
        filtered_data['trail_a_time'][index] = np.nan
        filtered_data['trail_b_errors'][index] = np.nan
        filtered_data['trail_b_time'][index] = np.nan

# Add presence of visual hallucinations
filtered_data = pd.merge(filtered_data, VH_dat, on='subject_code', how='inner')
columns.append('visual_hallucinations')

# Save filtered data (NB. This is the final copy)
filtered_data.to_csv('./data/filtered_data.csv', index=False)

# Remove un-needed columns
columns.remove('participant_number')
columns.remove('subject_code')
columns.remove('farnsworth_correct')
columns.remove('farnsworth_test')

# Variable summary and plotting
features_summary = []
for j in columns:
    if j != 'diagnosis':
        plt.figure()
        sns.histplot(data=filtered_data, x=j, hue='diagnosis')
        plt.xlabel('Group')
        plt.title(j)
        plt.savefig(f'./figures/f01_data_cleaning/hist_{j}.png', format='png', dpi=500)
        plt.close()
        plt.figure()
        sns.boxplot(data=filtered_data, x='diagnosis', y=j)
        plt.xlabel('Group')
        plt.title(j)
        plt.savefig(f'./figures/f01_data_cleaning/boxplot_{j}.png', format='png', dpi=500)
        plt.close()
        feature_df = pd.DataFrame({'feature': [j],
                                   'AD_mean': round(np.nanmean(filtered_data.loc[filtered_data['diagnosis'] =='AD'][j]),3),
                                   'AD_std': round(np.nanstd(filtered_data.loc[filtered_data['diagnosis'] =='AD'][j]),3),
                                   'MCI_mean': round(np.nanmean(filtered_data.loc[filtered_data['diagnosis'] == 'MCI'][j]),3),
                                   'MCI_std': round(np.nanstd(filtered_data.loc[filtered_data['diagnosis'] == 'MCI'][j]),3),
                                   #'DLB_mean': round(np.mean(filtered_data.loc[filtered_data['diagnosis'] == 'DLB'][j]),3),
                                   #'DLB_std': round(np.std(filtered_data.loc[filtered_data['diagnosis'] == 'DLB'][j]),3),
                                   'HC_mean': round(np.nanmean(filtered_data.loc[filtered_data['diagnosis'] == 'HC'][j]),3),
                                   'HC_std': round(np.nanstd(filtered_data.loc[filtered_data['diagnosis'] == 'HC'][j]),3)})
        features_summary.append(feature_df)

features_summary = pd.concat(features_summary, axis=0, ignore_index=True)
features_summary.to_csv('./data/feature_summary.csv')

len_AD = len(filtered_data.loc[filtered_data['diagnosis']=='AD'])
len_HC = len(filtered_data.loc[filtered_data['diagnosis']=='HC'])
len_MCI = len(filtered_data.loc[filtered_data['diagnosis']=='MCI'])
print(f'Number of AD: {len_AD}, \nNumber of HC: {len_HC}, \nNumber of MCI: {len_MCI}')
