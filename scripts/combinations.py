#!/usr/bin/env python3

'''
Data Processing
Reads data-{YEAR}.csv file and determines combinations of WTA and 
CDM districts and who would have won the election in that year.
Author: @edurso
'''

import sys
import math
import matplotlib.pyplot as plt

import utils

def complete_sim():
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

		scenario_winner = utils.get_winner(rep_electoral_votes, dem_electoral_votes)

		if scenario_winner == utils.REPUBLICAN:
			rep_wins += 1
		elif scenario_winner == utils.DEMOCRAT:
			dem_wins += 1
		else:
			print('Oh no, no one won')

		# print(bin_str, scenario_winner)

if len(sys.argv) > 1:
	year = int(sys.argv[1])
	if year not in utils.YEARS:
		print('Given year ({}) is invalid.\nYear must be 2020, 2016, 2012, or 0'.format(year))
		exit(1)
else:
	year = utils.get_year()


print('Using data for year {}'.format(year))

df = utils.get_data(year)

rep_wins = 0
dem_wins = 0

complete_sim()

percent_rep = (float(rep_wins) / (float(rep_wins) + float(dem_wins))) * 100
percent_dem = 100 - percent_rep

print('rep: {}, dem: {}'.format(percent_rep, percent_dem))

labels = ['Republican', 'Democrat']
colors = ['red', 'blue']
nums = [percent_rep, percent_dem]

plt.pie(nums, labels=labels, colors=colors, autopct='%1.1f%%')
plt.legend(loc='upper left')
plt.savefig('../figs/data-{}.png'.format(year))
plt.show()
