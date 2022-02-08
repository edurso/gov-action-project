#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DATA_FILE = 'election-data-congressional-district.csv'

year = input('Enter Presidential Election Year: ')
while not (int(year) == 2020 or int(year) == 2016 or int(year) == 2012):
	year = input('Enter A Recent Presidential Election Year (2020, 2016, or 2012): ')

data_frame = pd.read_csv(DATA_FILE)
print(data_frame)
