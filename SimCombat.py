
from random import randint
import re
import logging

from Combatant import Combatant


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


NUM_ALLIES = 3
NUM_ENEMIES = 2

def simulate(logging_level='DEBUG'):

    logging.getLogger().setLevel(logging_level)

    logging.info("Starting sim...")

    allies = [Combatant.from_filename('commoner') for _ in range(NUM_ALLIES)]
    enemies = [Combatant.from_filename('kobold') for _ in range(NUM_ENEMIES)]

    while (not all([ally.is_dead() for ally in allies]) and
        not all([enemy.is_dead() for enemy in enemies])):

        for ally in allies:
            other_allies = allies.copy()
            other_allies.remove(ally)
            ally.take_action(other_allies, enemies)
        if all([enemy.is_dead() for enemy in enemies]):
            logging.critical("*** Good guys win!")
            return

        for enemy in enemies:
            other_enemies = enemies.copy()
            other_enemies.remove(enemy)
            enemy.take_action(other_enemies, allies)
        if all([ally.is_dead() for ally in allies]):
            logging.critical("*** Bad guys win!")
            return

