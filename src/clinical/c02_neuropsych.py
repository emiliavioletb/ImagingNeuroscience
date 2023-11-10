
# Emilia Butters, Cambridge University, October 2023

from common.functions import *

redcap_data_uncleaned = pd.read_csv((study_folder + '/redcap_data.csv'))
columns_to_keep = pd.read_csv((study_folder + '/redcap_columns.csv'))
redcap_data = redcap_data_uncleaned[columns_to_keep]

# Visual inspection: plot histograms of our variables

# Cleaning & removing outliers

# Creating cleaned dataframe
cleaned_redcap_data =

# Saving new dataframe
