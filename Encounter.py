
from random import randint
import logging
import copy

from Combatant import Combatant
from SimCombat import roll
from EncounterResults import EncounterResults


class Encounter():

    def __init__(self, party, monsters, environment={}):
        self.party = party
        self.monsters = monsters
        self.environment = environment

    def simulate(self, logging_level='DEBUG'):

        logging.getLogger().setLevel(logging_level)
        logging.info("Starting sim...")

        party = copy.deepcopy(self.party)
        monsters = copy.deepcopy(self.monsters)

        logging.critical("simulating {}, {}".format(len(party),len(monsters)))
        while len(party) > 0 and len(monsters) > 0:

            for character in party:
                other_party = party.copy()
                other_party.remove(character)
                character.take_action(other_party, monsters)
            monsters = [m for m in monsters if not m.is_dead()]
            if len(monsters) == 0:
                logging.error("*** Party wins! :)")
                return EncounterResults(len(party),len(monsters))

            for monster in monsters:
                other_monsters = monsters.copy()
                other_monsters.remove(monster)
                monster.take_action(other_monsters, party)
            party = [c for c in party if not c.is_dead()]
            if len(party) == 0:
                logging.error("*** Monsters win! :(")
                return EncounterResults(len(party),len(monsters))

        return None   # This should never happen!


def run_sample_encounter(party_size=2, num_monsters=3):

    party = [Combatant.from_filename('commoner') for _ in range(party_size)]
    monsters = [Combatant.from_filename('kobold') for _ in range(num_monsters)]
    results = Encounter(party, monsters).simulate('DEBUG')
    print(results)

