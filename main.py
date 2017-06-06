
import logging
import sys
import os

from SimCombat import *
from ParameterSweep import ParameterSweep

if len(sys.argv) > 4:
    print('Usage: main.py [sweep_file=sweep.txt] [suite_size=1] [(' +
        '|'.join(reversed(logging_levels)) +
        ')=DEBUG] [plot=False].')
    sys.exit(1)

if len(sys.argv) > 1:
    enc_file = (
        sys.argv[1].split('=')[1] if sys.argv[1].startswith('sweep_file') 
        else sys.argv[1])
else:
    enc_file = 'sweep.txt'

if len(sys.argv) > 2:
    suite_size = (
        sys.argv[2].split('=')[1] if sys.argv[2].startswith('suite_size') 
        else sys.argv[2])
    suite_size=int(suite_size)
else:
    suite_size=1

if len(sys.argv) > 3:
    logging.getLogger().setLevel(sys.argv[3])
else:
    logging.getLogger().setLevel('DEBUG')

if len(sys.argv) > 4:
    plot = False if sys.argv[4] in ['False', 'plot=False'] else True
else:
    plot = False

with open('results.csv','w') as f:
    results = ParameterSweep.from_filename(enc_file).execute(suite_size)
    results.to_csv(f, index=False)
if plot:
    os.system('Rscript plotParamSweep.R')
    os.system('evince plot.pdf &')
