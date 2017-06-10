
from random import randint
import re
import logging
import collections


roll_re = re.compile('(^[0-9]*d[0-9]+$)|(^[0-9]*d[0-9]+[+-][0-9]+$)')

def roll(string, enforced_min=1):
    '''string is of the form "d8" or "d6+3" or "14d12-8"'''

    if not roll_re.match(string):
        raise ValueError('Invalid roll string: {}'.format(string))

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

logging_levels = collections.OrderedDict([
    ('META', 30),
    ('METADETAIL', 20),
    ('DEATH', 18),
    ('INCARNATE', 16),
    ('ACTION', 15),
    ('NOACTION', 14),
    ('DAMAGE', 12),
])

logging.basicConfig(format='%(levelname)s:%(message)s')

for level_name, level_value in logging_levels.items():
    logging.addLevelName(level_value, level_name)
#    setattr(logging, level_name.lower(),
#        lambda *args : (lambda val : logging.log(val,*args)(level_value))(level_value))

def log(level):
    logging.getLogger().setLevel(level)

def log_death(*args):
    logging.log(logging_levels['DEATH'], *args)

def log_action(*args):
    logging.log(logging_levels['ACTION'], *args)

def log_noaction(*args):
    logging.log(logging_levels['NOACTION'], *args)

def log_damage(*args):
    logging.log(logging_levels['DAMAGE'], *args)

def log_incarnate(*args):
    logging.log(logging_levels['INCARNATE'], *args)

def log_meta(*args):
    logging.log(logging_levels['META'], *args)

def log_meta_detail(*args):
    logging.log(logging_levels['METADETAIL'], *args)

def pr(alist):
    '''Print the str() representation of each element in the list. (Needed
    because I'm being stupid at the moment.)'''
    print([str(i) for i in alist])

def str_form(athing):
    '''Return the str() representation of the thing passed. If it's a tuple,
    return a string concatenating the elements. (Needed because I'm being 
    stupid at the moment.)'''
    if type(athing) is tuple:
        return '('+','.join([str(i) for i in athing])+')'
    elif type(athing) is list:
        return '['+','.join([str(i) for i in athing])+']'
    elif type(athing) is dict:
        return '{'+','.join([str(k)+":"+str(v) 
            for k,v in athing.items()])+'}'
    else:
        return(str(athing))

def prstr(athing):
    print(str_form(athing))
