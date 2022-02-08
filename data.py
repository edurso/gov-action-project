#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DATA_FILE = 'election-data-congressional-district.csv'

data_frame = pd.read_csv(DATA_FILE)
print(data_frame)
