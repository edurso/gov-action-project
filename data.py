#!/usr/bin/env python3

'''
Data Preprocessing
Writes to data-{YEAR}.csv
Author: @edurso
'''

import pandas as pd
import numpy as np

import utils

year = utils.get_year()

data_frame = pd.read_csv(utils.DATA_FILE)

# Find data for candidates that year
dem_candidate, rep_candidate = [col for col in data_frame.columns if str(year) in col]
df = data_frame[['State', 'District', dem_candidate, rep_candidate]]

# Determine winner per district & edit scope of dataframe
winner_col = np.where(df[rep_candidate] > df[dem_candidate], utils.REPUBLICAN, utils.DEMOCRAT)
df['Winner'] = winner_col
df = df[['State', 'District', 'Winner']]

out_dict = {}
out_dict['State'] = [state[0] for state in df.groupby(['State'])['State'].unique()]
winner_take_all = []
cong_dist_method_rep, cong_dist_method_dem = [], []

for state in out_dict['State']:
	dem_count, rep_count = 0, 0
	sub = df.loc[df['State'] == state]

	# Count winners per districts
	for district in sub['District']:
		row = sub.loc[sub['District'] == district]
		if(row['Winner'].values[0] == utils.REPUBLICAN):
			rep_count += 1
		elif(row['Winner'].values[0] == utils.DEMOCRAT):
			dem_count += 1
		else:
			print('Independent? Or Something is Worng...')
	
	winner = ''
	# Add winners to each division
	if(dem_count > rep_count): # add senator numbers
		dem_count += 2
		winner = utils.DEMOCRAT
	elif(rep_count > dem_count):
		rep_count += 2
		winner = utils.REPUBLICAN
	else:
		print('They Tied... Oops.')
		print(state)
		# TODO default to republican? idk
		winner = utils.REPUBLICAN
		# if districts split, then add one for each party per state
		rep_count += 1
		dem_count += 1

	winner_take_all.append(winner) # TODO need to calculate winner based on popular vote, not district things
	cong_dist_method_rep.append(rep_count)
	cong_dist_method_dem.append(dem_count)

out_dict['WTA'] = winner_take_all
out_dict['CDM-R'] = cong_dist_method_rep
out_dict['CDM-D'] = cong_dist_method_dem
df_ = pd.DataFrame(out_dict)

# for debugging only
print(df_)
df_.to_csv('./data/data-{}.csv'.format(year), index=False)
