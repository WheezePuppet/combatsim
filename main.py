
import logging
import sys
import os

from SimCombat import *
from ParameterSweep import run_sample_sweep

if len(sys.argv) > 4:
    print('Usage: main.py [suite_size=1] [(' +
        '|'.join(reversed(logging_levels)) + 
        ')=DEBUG] [plot=True].')
    sys.exit(1)

if len(sys.argv) > 1:
    suite_size=int(sys.argv[1])
else:
    suite_size=1

if len(sys.argv) > 2:
    logging.getLogger().setLevel(sys.argv[2])
else:
    logging.getLogger().setLevel('DEBUG')

if len(sys.argv) > 3:
    plot = True if sys.argv[3] == 'True' else False
else:
    plot = True

with open('results.csv','w') as f:
    run_sample_sweep(suite_size).to_csv(f, index=False)
if plot:
    os.system('Rscript plotParamSweep.R')
    os.system('evince plot.pdf &')
