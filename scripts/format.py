#!/usr/bin/env python3

'''
Format Output Text File
Author: @edurso
'''

import os
import re
import sys
import utils

if len(sys.argv) > 1:
	year = int(sys.argv[1])
	if year not in utils.YEARS:
		print('Given year ({}) is invalid.\nYear must be 2020, 2016, 2012, or 0'.format(year))
		exit(1)
else:
	year = utils.get_year()

fname = '../out/results-{}.txt'.format(year)

regex = re.compile(r'[A-Z]{4}.*')

with open(fname, 'r') as f, open(fname+'.orig', 'w') as out:
	inp = f.read()
	match = int(re.search(regex, inp).start()) + 2
	out.write(inp[:match]+'\n')
	
	while match != None:
		inp = inp[match:]
		try:
			match = int(re.search(regex, inp).start()) + 2
			out.write(inp[:match]+'\n')
		except:
			out.write(inp)
			break

os.rename(fname, 'tmp')
os.rename(fname+'.orig', fname)
os.remove('tmp')
