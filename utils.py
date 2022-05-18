#!/usr/bin/env python3

'''
Utility Functions
Author: @edurso
'''

import pandas as pd
import numpy as np

from os.path import exists

DATA_FILE = './data/election-data-congressional-district.csv'
POP_DATA_FILE = './data/popular-vote-data.csv'
REPUBLICAN = 'R'
DEMOCRAT = 'D'
YEARS = [2020, 2016, 2012, 0000] # 0000 for test data (small)
CDM = 1
WTA = 0

def get_year() -> int:
	'''
	prompts user to input a recent presidential election year
	returns the entered year
	'''
	year = int(input('Enter Presidential Election Year: '))
	while not year in YEARS:
		year = int(input('Enter A Recent Presidential Election Year (2020, 2016, or 2012): '))
	return year

def get_data(year: int) -> pd.DataFrame:
	'''
	reads data-{YEAR}.csv file
	returns dataframe of file contents
	'''
	fname = './data/data-{}.csv'.format(year)
	if year not in YEARS or not exists(fname):
		print('datafile does not exist')
		return pd.DataFrame()
	df = pd.read_csv(fname)
	return df

def get_winner(rep: int, dem: int) -> str:
	if(rep >= 270 and dem < 270):
		return REPUBLICAN
	elif(dem >= 270 and rep < 270):
		return DEMOCRAT
	else:
		# print('No one met 270')
		return 'N' #DEMOCRAT if dem > rep else REPUBLICAN
	
	