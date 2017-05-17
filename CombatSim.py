
from random import randint
import re

def roll(string, enforced_min=1):
    '''string is of the form "d8" or "d6+3" or "14d12-8"'''

    if string[0] == 'd':
        number = 1
        string = string[1:]
    else:
        number = int(string.split('d')[0])
        string = string.split('d')[1]

    plus_minus_re = re.compile('[+-]')
    if plus_minus_re.search(string):
        die_type = int(plus_minus_re.split(string)[0])
        modifier = int(plus_minus_re.split(string)[1])
        if '-' in string:
            modifier = -modifier
    else:
        die_type = int(string)
        modifier = 0

    return max(enforced_min,
        sum([randint(1,die_type) for _ in range(number)]) + modifier)

# https://pythontips.com/2013/08/08/storing-and-loading-data-with-json/
def jsonDefault(object):
    return object.__dict__
