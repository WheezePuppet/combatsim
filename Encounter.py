
from random import randint
import logging

from Combatant import Combatant
from SimCombat import roll


class Encounter():

    def __init__(self, party, monsters, environment={}):
        self.party = party
        self.monsters = monsters
        self.environment = environment

    def simulate(self, logging_level='DEBUG'):

        logging.getLogger().setLevel(logging_level)
        logging.info("Starting sim...")

        party = self.party.copy()
        monsters = self.monsters.copy()

        while (not all([character.is_dead() for character in party]) and
            not all([monster.is_dead() for monster in monsters])):

            for character in party:
                other_party = party.copy()
                other_party.remove(character)
                character.take_action(other_party, monsters)
            if all([monster.is_dead() for monster in monsters]):
                logging.critical("*** Party wins! :)")
                return True

            for monster in monsters:
                other_monsters = monsters.copy()
                other_monsters.remove(monster)
                monster.take_action(other_monsters, party)
            if all([character.is_dead() for character in party]):
                logging.critical("*** Monsters win! :(")
                return False


def run_sample_encounter(party_size=2, num_monsters=3):

    party = [Combatant.from_filename('commoner') for _ in range(party_size)]
    monsters = [Combatant.from_filename('kobold') for _ in range(num_monsters)]
    Encounter(party, monsters).simulate('INFO')

