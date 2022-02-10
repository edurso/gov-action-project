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
dem, rep = [col for col in data_frame.columns if str(year) in col]
df = data_frame[['State', 'District', dem, rep]]

# Determine winner per district & edit scope of dataframe
winner_col = np.where(df[rep] > df[dem], 'R', 'D')
df['Winner'] = winner_col
df = df[['State', 'District', 'Winner']]


# for debugging only
print(df)
#df.to_csv('out.csv')
