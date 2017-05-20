
import json
import logging
from collections import namedtuple

from SimCombat import *
from BasicActions import *


abilities = 'str dex int wis con cha'
AbilityScores = namedtuple('AbilityScores',abilities)


class Combatant():

    @classmethod
    def from_filename(cls, name):
        with open('combatants/{}.py'.format(name),"r") as f:
            return Combatant(json.load(f))

    def __init__(self, stats):

        '''stats is a dictionary containing all static information about the
        type of creature, not specific information about an instance. For
        instance, all kobolds have '2d-6' hit points; therefore, the key/val
        pair "hp":"2d-6" will be in the "stats" dictionary. Any particular
        kobold may have (say) 5 HP, and therefore, that instance-specific
        value is computed by the code in this class, not handed to it via the
        "stats" dictionary.'''

        # Save "stats" as an object attribute, just in case we want it to
        # serialize this object later. Then, copy each of its elements into
        # its own object attribute for easy access.
        self.stats = stats
        for key, value in stats.items():
            setattr(self, key, value)

        self.ability_scores = AbilityScores._make(
            [stats[ability] for ability in abilities.split(' ')])
        self.hp = self.__compute_hp(stats['hp'])
        self.actions = [
            self.build_action(action) for action in self.action_strs]


    def __compute_hp(self, hp):
        if type(hp) is int:
            return hp
        elif type(hp) is str:
            return roll(hp)
        else:
            print('Illegal hp type ', type(hp), '.', sep='')
            exit(1)

    def __str__(self):
        return self.name + ' (' + str(self.hp) + ' HP)'

    def __repr__(self):
        return 'Combatant({})'.format(self.stats)

    def take_action(self, allies, enemies):
        random.choice(self.actions).execute(self,allies,enemies)

    def serialize(self, stream):
        '''Store a copy of this object's *static* information into the stream
        passed. This doesn't preserve instance-specific information about a
        *particular* kobold, just "the generic kobold stuff."'''
        json.dump(self.stats, stream, default=jsonDefault, indent=4)

    def build_action(self, action_str):
        return eval(action_str)

    def take_damage(self, dam_amt, dam_type):
        self.hp = max(0, self.hp - dam_amt)
        if self.hp <= 0:
            logging.warning('{} DIES!'.format(self.name))
        else:
            logging.debug('Ouch! (now has {} HP)'.format(self.hp))

    def is_dead(self):
        return self.hp <= 0


# Load a monster (kobold) from disk.
with open("combatants/kobold.py","r") as f:
    kobold = Combatant(json.load(f))

# Here's some code to create a "starter" disk file, just for gigs.
#absc = dict(AbilityScores._make([7,15,9,8,7,8])._asdict())
#absc.update({'hp':'2d6-2', 'name':'kobold'})
#kobold = Combatant(absc)
#with open("combatants/kobold.py","w") as f:
#    kobold.serialize(f)
