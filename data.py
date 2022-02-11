#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DATA_FILE = 'election-data-congressional-district.csv'

# Determine year to look at
year = input('Enter Presidential Election Year: ')
while not (int(year) == 2020 or int(year) == 2016 or int(year) == 2012):
	year = input('Enter A Recent Presidential Election Year (2020, 2016, or 2012): ')

data_frame = pd.read_csv(DATA_FILE)

# Find data for candidates that year
dem_candidate, rep_candidate = [col for col in data_frame.columns if str(year) in col]
df = data_frame[['State', 'District', dem_candidate, rep_candidate]]

# Determine winner per district & edit scope of dataframe
winner_col = np.where(df[rep_candidate] > df[dem_candidate], 'R', 'D')
df['Winner'] = winner_col
df = df[['State', 'District', 'Winner']]

out_dict = {}
out_dict['State'] = [state[0] for state in df.groupby(['State'])['State'].unique()]
winner_take_all = []
cong_dist_method_rep, cong_dist_method_dem = [], []

for state in out_dict['State']:
	print(state)
	dem_count, rep_count = 0, 0
	sub = df.loc[df['State'] == state]
	for district in sub['District']:
		row = sub.loc[sub['District'] == district]
		#print('\t', row)
		print('\t' + district, row['Winner'])
	

	winner_take_all.append(0)
	cong_dist_method_rep.append(0)
	cong_dist_method_dem.append(0)

out_dict['WTA'] = winner_take_all
out_dict['CDM-R'] = cong_dist_method_rep
out_dict['CDM-D'] = cong_dist_method_dem
df_ = pd.DataFrame(out_dict)

# for debugging only
#print(df_)
#df.to_csv('out.csv')
