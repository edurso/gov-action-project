#!/usr/bin/env python3

'''
Simulation
Reads data-{YEAR}.csv and simulates converting select states to CDM.
States are selected if they:
1. Were won by the winner of the election
2. Have 1 or more congressional district that favors the party that lost
Author: @edurso
'''

import sys
import math
import pandas as pd
import matplotlib.pyplot as plt

import utils

if len(sys.argv) > 1:
	year = int(sys.argv[1])
	if year not in utils.YEARS:
		print('Given year ({}) is invalid.\nYear must be 2020, 2016, 2012, or 0'.format(year))
		exit(1)
else:
	year = utils.get_year()

dem_won = not year == 2016
# print(dem_won)

fname = '../out/results-{}.txt'.format(year)

print('Using data for year {}'.format(year))

df = utils.get_data(year)

rep_wins = 0
dem_wins = 0
no_win = 0

delta_win_scenarios = []

# find democratic states w/republican districts
del_states = []
for state in df['State']:
	cdmd = df.loc[df['State'] == state, 'CDM-D'].values[0] 
	cdmr = df.loc[df['State'] == state, 'CDM-R'].values[0] 
	winner = df.loc[df['State'] == state, 'WTA'].values[0]
	# print('W {} D {} R {}'.format(winner, cdmd, cdmr))
	if dem_won and winner == utils.DEMOCRAT and cdmr > 0:
		del_states.append(state)
	elif not dem_won and winner == utils.REPUBLICAN and cdmd > 0:
		del_states.append(state)
# print(len(del_states))

# calculate votes for states not in list
electoral_votes_dem = 0
electoral_votes_rep = 0
for state in df['State']:
	if state not in del_states:
		cdmd = df.loc[df['State'] == state, 'CDM-D'].values[0] 
		cdmr = df.loc[df['State'] == state, 'CDM-R'].values[0] 
		winner = df.loc[df['State'] == state, 'WTA'].values[0]
		if winner == utils.DEMOCRAT:
			electoral_votes_dem += (cdmd + cdmr)
		elif winner == utils.REPUBLICAN:
			electoral_votes_rep += (cdmd + cdmr)
		else:
			raise Exception('No winner of state')
# print('electorate so far: D {} R {}'.format(electoral_votes_dem, electoral_votes_rep))

# build experimental directory of states
states_dir = {}
wta, cdmd, cdmr = [], [], []
for state in del_states:
	cdmd.append(df.loc[df['State'] == state, 'CDM-D'].values[0])
	cdmr.append(df.loc[df['State'] == state, 'CDM-R'].values[0])
	wta.append(df.loc[df['State'] == state, 'WTA'].values[0])

states_dir['State'] = del_states
states_dir['WTA'] = wta
states_dir['CDM-D'] = cdmd
states_dir['CDM-R'] = cdmr
df = pd.DataFrame(states_dir)
# print(df)

# loop through all permeutations of the rest of the states, add to the electoral votes, and check results
for x in range(int(math.pow(2,len(df['State'])))):
	bin_str = str(bin(x)[2:].zfill(len(df['State']))) # binary sequence of string

	dem_electoral_votes = 0
	rep_electoral_votes = 0

	for n, state in zip(bin_str, df['State']):

		cdmd = df.loc[df['State'] == state, 'CDM-D'].values[0] 
		cdmr = df.loc[df['State'] == state, 'CDM-R'].values[0] 
		winner = df.loc[df['State'] == state, 'WTA'].values[0]

		if int(n) == utils.CDM:
			dem_electoral_votes += cdmd 
			rep_electoral_votes += cdmr
		elif int(n) == utils.WTA:
			if winner == utils.REPUBLICAN:
				rep_electoral_votes += (cdmr + cdmd)
			elif winner == utils.DEMOCRAT:
				dem_electoral_votes += (cdmr + cdmd)
			else:
				print('Neither party carried state?')
		else:
			print('Unknown elector allocation method. Needs to be CDM or WTA')

	scenario_winner = utils.get_winner(rep_electoral_votes + electoral_votes_rep, dem_electoral_votes + electoral_votes_dem)

	if scenario_winner == utils.REPUBLICAN:
		rep_wins += 1
		if dem_won:
			cdm_states = [state for n, state in zip(bin_str, df['State']) if int(n) == utils.CDM]
			delta_win_scenarios.append(cdm_states)
			print('Republican Party Won with the following states CDM: {}'.format(cdm_states))
	elif scenario_winner == utils.DEMOCRAT:
		dem_wins += 1
		if not dem_won:
			cdm_states = [state for n, state in zip(bin_str, df['State']) if int(n) == utils.CDM]
			delta_win_scenarios.append(cdm_states)
			print('Democratic Party Won with the following states CDM: {}'.format(cdm_states))
	else:
		no_win += 1

	# print(bin_str, scenario_winner)

# report results
percent_rep = (float(rep_wins) / (float(rep_wins) + float(dem_wins) + float(no_win))) * 100
percent_dem = (float(dem_wins) / (float(rep_wins) + float(dem_wins) + float(no_win))) * 100
percent_no = (float(no_win) / (float(rep_wins) + float(dem_wins) + float(no_win))) * 100

print('rep: {}, dem: {}, no: {}'.format(percent_rep, percent_dem, percent_no))

with open(fname, 'w') as f:
	for combination in delta_win_scenarios:
		f.write(', '.join(combination)+'\n')

labels = ['Republican', 'Democrat', 'No Winner']
colors = ['red', 'blue', 'white']
nums = [percent_rep, percent_dem, percent_no]

plt.pie(nums, labels=labels, colors=colors, autopct='%1.1f%%')
plt.legend(loc='upper left')
plt.savefig('../figs/data-{}.png'.format(year))
plt.show()
