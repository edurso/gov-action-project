#!/usr/bin/env python3

'''
Data Preprocessing
Writes to data-{YEAR}.csv
Author: @edurso
'''

import sys
import pandas as pd
import numpy as np

import utils

if len(sys.argv) > 1:
	year = int(sys.argv[1])
	if year not in utils.YEARS:
		print('Given year ({}) is invalid.\nYear must be 2020, 2016, 2012, or 0'.format(year))
		exit(1)
else:
	year = utils.get_year()

if year == 0:
	print('This file cannot process year 0')
	exit(1)

data_frame = pd.read_csv(utils.DATA_FILE)

# find data for candidates that year
dem_candidate, rep_candidate = [col for col in data_frame.columns if str(year) in col]
df = data_frame[['State', 'District', dem_candidate, rep_candidate]]

# determine winner per district & edit scope of dataframe
winner_col = np.where(df[rep_candidate] > df[dem_candidate], utils.REPUBLICAN, utils.DEMOCRAT)
df['Winner'] = winner_col
df = df[['State', 'District', 'Winner']]

out_dict = {}
out_dict['State'] = [state[0] for state in df.groupby(['State'])['State'].unique()]
winner_take_all = []
cong_dist_method_rep, cong_dist_method_dem = [], []

# popular vote datafile - determine winner take all
pop_df = pd.read_csv(utils.POP_DATA_FILE)
pop_df = pop_df.loc[pop_df['year'] == year][['state_po', 'party_simplified', 'candidatevotes', 'totalvotes']]
for state in pop_df.groupby(['state_po'])['state_po'].unique():
	sub = pop_df.loc[pop_df['state_po'] == state[0]]
	dem_votes = sub.loc[sub['party_simplified'] == 'DEMOCRAT', 'candidatevotes'].values[0]
	rep_votes = sub.loc[sub['party_simplified'] == 'REPUBLICAN', 'candidatevotes'].values[0]
	winner = utils.DEMOCRAT if dem_votes > rep_votes else utils.REPUBLICAN
	winner_take_all.append(winner)

for state in out_dict['State']:
	dem_count, rep_count = 0, 0
	sub = df.loc[df['State'] == state]

	# count winners per districts
	for district in sub['District']:
		row = sub.loc[sub['District'] == district]
		if(row['Winner'].values[0] == utils.REPUBLICAN):
			rep_count += 1
		elif(row['Winner'].values[0] == utils.DEMOCRAT):
			dem_count += 1
		else:
			print('Independent? Or Something is Worng...')
	
	# add senator numbers
	if(dem_count > rep_count):
		dem_count += 2
	elif(rep_count > dem_count):
		rep_count += 2
	else:
		# if districts split, then add one for each party per state
		rep_count += 1
		dem_count += 1

	cong_dist_method_rep.append(rep_count)
	cong_dist_method_dem.append(dem_count)

out_dict['WTA'] = winner_take_all
out_dict['CDM-R'] = cong_dist_method_rep
out_dict['CDM-D'] = cong_dist_method_dem
df_ = pd.DataFrame(out_dict)

# for debugging only
print(df_)
df_.to_csv('../data/data-{}.csv'.format(year), index=False)
