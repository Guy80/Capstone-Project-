# -*- coding: utf-8 -*-
"""
@author: Dominic Fergus
"""

# Load required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
# Set paths
main_dir = './'
data_dir = main_dir + 'Data\\'
output_dir = main_dir + 'Output\Reports\\'
os.chdir(main_dir)
# Remove annoying error
pd.options.mode.chained_assignment = None # default='warn'
pd.set_option('display.max_rows', 26)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)
# Load files
# Load AllTraffic
data = pd.read_csv(data_dir + "AllTraffic_1.csv", sep="\t", lineterminator='\r', dtype='str',
encoding='utf8')
# Remove rows with invalid data
# Remove rows with invalid country data
country = data[~data['country'].isin(['None','none','n/a','nan',''])]
# Remove empty rows and bad source IP
country = country[~country['source_ip'].isin(['None','none','n/a','nan','','000.000.000.000','127.0.0.1'])]
# Group data by country
country = country.groupby(['country']).size().to_frame('number_of_attacks').reset_index().sort_values(by=['number_of_attacks','country'], ascending=[False, True])
#Use the rank function to rank countries by the number of attacks
country['Rank'] = country['number_of_attacks'].rank(method='dense', ascending=False).astype(int)
# Reset index
country.index = range(len(country))
# Calculate the percentage of country attacks
country['Percentage'] = (country.number_of_attacks/country.number_of_attacks.sum()).map(lambda n:
'{:,.6%}'.format(n))
print(country[0:25])
country.to_csv(output_dir + 'Project 01 - Top 25 Countries.csv', encoding='utf-8', header=True,
index=False, sep=',')
####################################################################
# Graph Top 25 Countries
####################################################################
fig, ax = plt.subplots()
country[0:25].plot('country','number_of_attacks', legend = None, \
kind='bar', color = '#1f77b4', figsize=(18, 9), ax=ax)
ax.set_title('Project 01\nTop 25 Countries\n', fontweight="bold", fontsize=30)
ax.set_xlabel('\nCountry', fontweight="bold", size=16)
ax.set_ylabel('Number of Attacks', fontweight="bold", size=16)
ax.set_xticklabels(ax.get_xticklabels(), fontsize=14, rotation=45, ha="right")
#ax.set_xticklabels(ax.get_xticklabels(), fontsize=14, fontweight="bold", rotation=45, ha="right")
# Don't allow the axis to be on top of your data
ax.set_axisbelow(True)
# Puts number on top of bar chart
for p in ax.patches: ax.annotate(np.round(p.get_height(),decimals=2), \
(p.get_x()+p.get_width()/2., p.get_height()), ha='center', va='center', xytext=(0, 10), \
textcoords='offset points')
# Turn on the minor TICKS, which are required for the minor GRID
ax.minorticks_on()
# Customize the major grid
ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
# Customize the minor grid
ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
# Turn off the display of all ticks.
ax.tick_params(which='both', # Options for both major and minor ticks
top=True, # turn off top ticks
left=True, # turn off left ticks
right=True, # turn off right ticks
bottom=True) # turn off bottom ticks
# Save graph
fig.savefig(output_dir + 'Project 01 - Top 25 Countries.png', bbox_inches = 'tight')