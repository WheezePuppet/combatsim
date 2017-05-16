
from CombatSim import *
from collections import namedtuple

AbilityScores = namedtuple("AbilityScores","str dex int wis con cha")

class Combatant():

    def __init__(self, name, ability_scores, hp):
        print("dude")
        self.name = name
        self.ability_scores = ability_scores
        if type(hp) is int:
            self.hp = hp
        elif type(hp) is str:
            self.hp = roll(hp)
        else:
            print("Illegal hp type ", type(hp), ".", sep="")
            exit(1)

    def __repr__(self):
        return self.name + " (" + str(self.hp) + " HP)"


sample_combatants = [
    Combatant('kobold',AbilityScores._make([7,15,9,8,7,8]),5)
]
