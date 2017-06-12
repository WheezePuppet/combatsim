
from random import randint
import copy
import sys

from Combatant import Combatant
from SimCombat import *
from EncounterResults import EncounterResults


class Encounter():

    total_num_simulations = 0

    def __init__(self, party, monsters, environment={}):
        self.party = party
        self.monsters = monsters
        self.environment = environment

    def simulate(self):

        Combatant.reset_ids()
        Encounter.total_num_simulations += 1
        log_meta_detail('Starting sim #{}...'.
                                format(Encounter.total_num_simulations))

        for combatant in self.party + self.monsters:
            combatant._num_incarnated = 0

        party = [character.incarnate() for character in self.party 
            for _ in range(character.stats['quantity']) ]
        monsters = [monster.incarnate() for monster in self.monsters 
            for _ in range(monster.stats['quantity']) ]

        log_meta_detail('This fight features ' + 
            ','.join([str(pm) for pm in party]) + ' vs. ' +
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
                    log_meta_detail('*** Party wins! :)')
                    return EncounterResults(len(party),len(monsters))
            elif character in monsters:
                other_monsters = monsters.copy()
                other_monsters.remove(character)
                character.take_action(other_monsters, party)
                party = [c for c in party if not c.is_dead()]
                if len(party) == 0:
                    log_meta_detail('*** Monsters win! :(')
                    return EncounterResults(len(party),len(monsters))
            else:
                print('{} not in either!'.format(str(character)))
                sys.exit(1)

            if not character.is_dead():
                turn_order.append(character)
            turn_order = [c for c in turn_order if not c.is_dead()]

        return None   # This should never happen!

    def __str__(self):
        return str_form(self.party) + " vs. " + str_form(self.monsters)


def run_sample_encounter(party_size=2, num_monsters=3):

    party = [Combatant.from_filename('commoner', party_size)]
    monsters = [Combatant.from_filename('kobold', num_monsters)]

    results = Encounter(party, monsters).simulate()
    print(results)

