
import json
from collections import namedtuple
import copy

from SimCombat import *
from BasicActions import *


class Combatant():
    '''A participant in combat. This class is used for PCs and NPCs.'''

    @classmethod
    def from_filename(cls, name):
        with open('combatants/{}.py'.format(name),"r") as f:
            return Combatant(json.load(f))

    @classmethod
    def reset_ids(cls):
        cls.combatant_id = 0

    combatant_id = 0

    def __init__(self, stats):
        '''stats is a dictionary containing all static information about the
        type of creature, not specific information about an instance. For
        instance, all kobolds have '2d-6' hit points; therefore, the key/val
        pair "hp":"2d-6" will be in the "stats" dictionary. Any particular
        kobold may have (say) 5 HP, and therefore, that instance-specific
        value is computed by the code in this class, not handed to it via the
        "stats" dictionary. That instance-specific information can be
        re-computed via the method "incarnate()".'''

        # Save "stats" as an object attribute, just in case we want it to
        # serialize this object later. Then, copy each of its elements into
        # its own object attribute for easy access.
        self.stats = stats
        for key, value in stats.items():
            setattr(self, key, value)

        self.actions = [
            self.build_action(action) for action in self.action_strs]

        # self.incarnate()  Meh...actually, don't self-incarnate yet.


    def incarnate(self):
        '''Actually produce an individual battle participator from this
        template Combatant.'''

        # (Shallow copy of template okay. If stats ever need to be instance
        # separate, we'll need to do deep copy.)
        incarnated = copy.copy(self)  

        incarnated._id = Combatant.combatant_id
        Combatant.combatant_id += 1

        '''(Re-)roll all the instance-specific parameters for this object, so
        that a fresh incarnation of this type of adventurer/monster exists.'''
        log_incarnate("------> incarnating {}...".format(str(incarnated)))
        for stat, val in incarnated.stats.items():
            if type(val) is str and roll_re.match(val):
                new_value = roll(val)
                log_incarnate("  {}'s {}, rolled from {}, is a: {}".format(
                    str(incarnated), stat, val, new_value))
                setattr(incarnated, stat, roll(val))
        return incarnated

    def set_stat(self, key, value):
        self.stats[key] = value

    def __str__(self):
        return self.name + str(self._id)

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
            log_death('{} DIES!'.format(str(self)))
        else:
            log_damage('Ouch! ({} now has {} HP)'.format(str(self), self.hp))

    def is_dead(self):
        return self.hp <= 0


# Load a monster (kobold) from disk.
#with open("combatants/kobold.py","r") as f:
#    kobold = Combatant(json.load(f))

# Here's some code to create a "starter" disk file, just for gigs.
#absc = dict(AbilityScores._make([7,15,9,8,7,8])._asdict())
#absc.update({'hp':'2d6-2', 'name':'kobold'})
#kobold = Combatant(absc)
#with open("combatants/kobold.py","w") as f:
#    kobold.serialize(f)
