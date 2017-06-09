
from random import randint
from collections import defaultdict
import copy
import sys

from Combatant import Combatant
from SimCombat import *
from EncounterResults import EncounterResults


class Encounter():

    total_num_simulations = 0

    def __init__(self, party, monsters, environment={}):
        '''Create an encounter which can be simulated. "party" and "monsters"
        can either be (a) lists of Combatants, or (b) dicts mapping Combatants
        to quantities.'''

        if type(party) is list:
            self.party = { p:1 for p in party }
        else:
            self.party = party
        if type(monsters) is list:
            self.monsters = { m:1 for m in monsters }
        else:
            self.monsters = monsters
        self.environment = environment

    def simulate(self):

        Combatant.reset_ids()
        Encounter.total_num_simulations += 1
        log_meta('Starting sim #{}...'.
                                format(Encounter.total_num_simulations))

        party = [character.incarnate() 
            for character, quantity in self.party.items() 
                for _ in range(quantity)]
        log_meta_detail("  The party is: " +
            ','.join([str(p) for p in party]))
        monsters = [monster.incarnate() 
            for monster, quantity in self.monsters.items() 
                for _ in range(quantity)]
        log_meta_detail("  The monsters are: " +
            ','.join([str(m) for m in monsters]))

        turn_order = party.copy()
        turn_order.extend(monsters)
        turn_order.sort(key= lambda c: c.initiative, reverse=True)

        while len(party) > 0 and len(monsters) > 0:

            character = turn_order.pop(0)

            if character in party:
                other_party = party.copy()
                other_party.remove(character)
                character.take_action(other_party, monsters)
                monsters = [m for m in monsters if not m.is_dead()]
                if len(monsters) == 0:
                    log_meta('*** Party wins! :)')
                    return EncounterResults(len(party),len(monsters))
            elif character in monsters:
                other_monsters = monsters.copy()
                other_monsters.remove(character)
                character.take_action(other_monsters, party)
                party = [c for c in party if not c.is_dead()]
                if len(party) == 0:
                    log_meta('*** Monsters win! :(')
                    return EncounterResults(len(party),len(monsters))
            else:
                print('{} not in either!'.format(str(character)))
                sys.exit(1)

            if not character.is_dead():
                turn_order.append(character)
            turn_order = [c for c in turn_order if not c.is_dead()]

        return None   # This should never happen!


def run_sample_encounter(party_size=2, num_monsters=3):

    party = {Combatant.from_filename('commoner'):party_size}
    monsters = {Combatant.from_filename('kobold'):num_monsters}
    results = Encounter(party, monsters).simulate()
    print(results)

