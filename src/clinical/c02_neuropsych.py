
# Emilia Butters, Cambridge University, October 2023

from common.functions import *

redcap_data_uncleaned = pd.read_csv((study_folder + '/redcap_data.csv'))
columns_to_keep = pd.read_csv((study_folder + '/redcap_columns.csv'))
redcap_data = redcap_data_uncleaned[columns_to_keep]

# Plot histograms for each variable
for i in redcap_data[0]:
    plt.hist(i)
    #plt.savefig(f'./figures/c02_neuropsych/hist_{i}.svg', format='svg')
    plt.show()

# Creating cleaned dataframe
cleaned_redcap_data =

# Saving new dataframe
