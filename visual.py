
import logging
import sys
import os

from SimCombat import *
from ParameterSweep import ParameterSweep

if len(sys.argv) > 3:
    print('Usage: visual.py [enc_file=encounter.txt] [(' +
        '|'.join(reversed(logging_levels)) + ')=METADETAIL].')
    sys.exit(1)

if len(sys.argv) > 1:
    enc_file = (
        sys.argv[1].split('=')[1] if sys.argv[1].startswith('enc_file') 
        else sys.argv[1])
else:
    enc_file = 'encounter.txt'

if len(sys.argv) > 2:
    logging.getLogger().setLevel(sys.argv[3])
else:
    logging.getLogger().setLevel('METADETAIL')

really_not_a_sweep = ParameterSweep.from_filename(enc_file)
encounter = really_not_a_sweep._encounter
results = encounter.simulate()
print(results)
