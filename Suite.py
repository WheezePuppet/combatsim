
from random import randint
import logging

from Encounter import Encounter
from Combatant import Combatant
from SimCombat import *


class Suite():
    '''Simulate an encounter some number of times and compute aggregate
    results.'''

    def __init__(self, encounter, size=10):
        self._encounter = encounter
        self._size = size

    def execute(self):

        log_meta("Starting suite...")

        results = [self._encounter.simulate() for _ in range(self._size)]
        return results


def run_sample_suite(size=10,
    party_size=2,
    num_monsters=3):

    party = [Combatant.from_filename('commoner') for _ in range(party_size)]
    monsters = [Combatant.from_filename('kobold') for _ in range(num_monsters)]
    encounter = Encounter(party, monsters)

    results = Suite(encounter,size).execute()
    party_wins = [result.monsters_remaining == 0 for result in results]
    print("The party won {:.1f}% of the time.".format(
        sum(party_wins)/len(party_wins)*100))

