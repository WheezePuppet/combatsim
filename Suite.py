
from random import randint
import logging

from IPython.core.debugger import Tracer
from Encounter import Encounter
from Combatant import Combatant


class Suite():

    def __init__(self, encounter, size=10):
        self._encounter = encounter
        self._size = size

    def execute(self, logging_level='DEBUG'):

        logging.getLogger().setLevel(logging_level)
        logging.info("Starting suite...")

        results = [self._encounter.simulate(logging_level)
            for _ in range(self._size)]
        return results


def run_sample_suite(size=10,
    logging_level='INFO',
    party_size=2,
    num_monsters=3):

    party = [Combatant.from_filename('commoner') for _ in range(party_size)]
    monsters = [Combatant.from_filename('kobold') for _ in range(num_monsters)]
    encounter = Encounter(party, monsters)

    results = Suite(encounter,size).execute(logging_level)
    party_wins = [result.monsters_remaining == 0 for result in results]
    print("The party won {:.1f}% of the time.".format(
        sum(party_wins)/len(party_wins)*100))
