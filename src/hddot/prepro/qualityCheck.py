import matplotlib.pyplot as plt

from common.functions import *
rc('text', usetex=True)

# load data
datDir = '/Users/emilia/Documents/STUDIES/ONAC/hpc/'
filtered_data = pd.read_csv('./data/filtered_data.csv')
folders = [name for name in os.listdir(datDir) if os.path.isdir(os.path.join(datDir, name))]

# clean data
dataQualPerChannels = []
totalChannels = []
channelDists = ['[0  20]', '[20 27.5]', '[27.5 32.5]', '[32.5 37.5]', '[37.5 42.5]', '[42.5 Inf]']
for j in folders:
    if j[0] != 'D':
        if j in filtered_data['subject_code'].to_list():
            txtfilepath = '/Users/emilia/Documents/STUDIES/ONAC/hpc/' + j + '/hddot/' + j + \
                          '_restingqualityCheck_nirsfile_dataQualityCheck.txt'
            exist = os.path.exists(txtfilepath)
            if exist:
                with open(txtfilepath, 'r') as file:
                    content = file.read()
                    dataQualPerChannel = []
                    for i in channelDists:
                        pattern = fr"Percentage of good channels in range {re.escape(i)} = (\d+\.?\d*)%"
                        match = re.search(pattern, content)
                        percentChannel = float(match.group(1))
                        tested = int(filtered_data.loc[filtered_data['subject_code'] == j, 'testing_loc'])
                        dataQualPerChannel.append((i, percentChannel, tested))
                    dataQualPerChannel = pd.DataFrame(dataQualPerChannel, columns=['dist', 'percent_channel', 'testing_loc'])
                    dataQualPerChannels.append(dataQualPerChannel)
                    # Get number of good channels
                    pattern = r"Total number of good fNIRS channels = (\d+)/\d+"
                    match = re.search(pattern, content)
                    good_channels = int(match.group(1))
                    totalChannel = pd.DataFrame({'num_channels': [good_channels]})
                    totalChannels.append(totalChannel)
totalChannels = pd.concat(totalChannels, ignore_index=True)
dataQualPerChannels = pd.concat(dataQualPerChannels, ignore_index=True)

# test significant between locations
at_home = dataQualPerChannels.loc[dataQualPerChannels['testing_loc'] == 1]
at_hsb = dataQualPerChannels.loc[dataQualPerChannels['testing_loc'] == 0]
norm = []
for j in dataQualPerChannels['dist'].unique():
    for i in [0, 1]:
        x = dataQualPerChannels.loc[(dataQualPerChannels['dist'] == j)
                                    & (dataQualPerChannels['testing_loc'] == i), 'percent_channel']
        f, p = stats.shapiro(x)
        if p < 0.05:
            norm.append(j)

testing_loc_results = []
for j in dataQualPerChannels['dist'].unique():
    if j in list(set(norm)):
        f, p = stats.ttest_ind(
            dataQualPerChannels.loc[(dataQualPerChannels['dist'] == j) &
                                (dataQualPerChannels['testing_loc'] == 0), 'percent_channel'],
            dataQualPerChannels.loc[(dataQualPerChannels['dist'] == j) &
                                    (dataQualPerChannels['testing_loc'] == 1), 'percent_channel'])
    else:
        f, p = stats.mannwhitneyu(
            dataQualPerChannels.loc[(dataQualPerChannels['dist'] == j) &
                                (dataQualPerChannels['testing_loc'] == 0), 'percent_channel'],
            dataQualPerChannels.loc[(dataQualPerChannels['dist'] == j) &
                                    (dataQualPerChannels['testing_loc'] == 1), 'percent_channel'])
    if p < 0.001:
        sig = '***'
    elif p < 0.01:
        sig = '**'
    elif p < 0.05:
        sig = '*'
    else:
        sig = 'ns'
    d = pd.DataFrame({'dist': j, 'p': [p], 'f': f, 'level': sig})
    testing_loc_results.append(d)
testing_loc_results = pd.concat(testing_loc_results, ignore_index=True)

# plot data
fig1, ax1 = plt.subplots(figsize=(7.5, 5))
palette = sns.color_palette("mako", n_colors=2)
sns.set_theme(style='whitegrid')
sns.boxplot(data=dataQualPerChannels, x='dist', y='percent_channel', hue='testing_loc',
            boxprops={'alpha': 0.7}, flierprops={'marker': 'o','markersize': 5, 'markerfacecolor': 'none'})
plt.ylabel('Percentage of good channels (\%)', fontsize=22)
plt.xlabel('Range of channel distances (mm)', fontsize=22)
plt.xticks(fontsize=9)
legend_labels = [r"Clinic (\textit{n}=23)", r"Home (\textit{n}=42)"]
handles, _ = ax1.get_legend_handles_labels()
ax1.legend(handles=handles, labels=legend_labels, title='Testing Location',
           loc='upper left', bbox_to_anchor=(1, 1), title_fontsize=16, fontsize=16,
           markerscale=2, handlelength=2)
[ax1.axvline(x+.5,color='k', linewidth=0.3) for x in ax1.get_xticks()]
plt.tight_layout()
# plt.show()
plt.savefig('./figures/prepro/dataQual_testing.png', format='png', dpi=500)

