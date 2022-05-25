#!/usr/bin/env python3

'''
Trend Analysis
Determines frequency of states that appear across simulated elections when result was altered.
Author: @edurso
'''

import sys
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

fname = '../out/results-{}.txt'.format(year)
datafile = '../data/data-{}.csv'.format(year)
df = pd.read_csv(datafile)

count = 0
states = {}

for state in df['State']:
	states[state] = 0

with open(fname, 'r') as f:
	lines = f.readlines()
	for line in lines:
		count += 1
		for state in line.split(' '):
			state = state[:2]
			states[state] += 1

for state in states:
	states[state] = float(states[state])/float(count) * 100.0

# print(states)
# print(count)

# creating the bar plot
for state in states.copy():
	if states[state] == 0.0:
		del states[state]
plt.bar(states.keys(), states.values(), color ='orange', width=0.4)

with open('../out/trend-{}.txt'.format(year), 'w') as f:
	for state in states:
		f.write('{}: {:.2f}%\n'.format(state, states[state]))
 
plt.xlabel('State')
plt.ylabel('% Of Scenarios')
plt.title('% Of Scenarios where State is CDM & Opposite Party Wins')
plt.savefig('../figs/trend-{}.png'.format(year))
plt.show()
