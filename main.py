
import logging
import sys

from SimCombat import *
from ParameterSweep import run_sample_suite

if len(sys.argv) > 3:
    print('Usage: main.py [(' + '|'.join(reversed(logging_levels)) +
        ')] [suite_size].')
    sys.exit(1)

if len(sys.argv) > 1:
    logging.getLogger().setLevel(sys.argv[1])
else:
    logging.getLogger().setLevel('DEBUG')

if len(sys.argv) > 2:
    suite_size=int(sys.argv[2])
else:
    suite_size=1

with open('results.csv','w') as f:
    run_sample_suite(suite_size).to_csv(f, index=False)
