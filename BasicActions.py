
import random

from SimCombat import *


class MeleeAttack():

    def __init__(self, mod=0, reach=5, damage='d4', dam_type='bludgeoning'):
        self.mod = mod
        self.reach = reach
        self.damage = damage
        self.dam_type = dam_type

    def execute(self, actor, allies, enemies):
        if not enemies:
            log_noaction('Nobody left to kill! Go get ice cream!')
            pass
        else:
            enemy = random.choice(enemies)
            if roll('d20{:+d}'.format(self.mod)) >= enemy.ac:
                dam_amt = roll(self.damage)
                log_action('{} hits {}! for {} damage'.format(actor,
                    enemy, dam_amt))
                enemy.take_damage(dam_amt, self.dam_type)
            else:
                log_action('{} misses {}'.format(actor, enemy))

    def __repr__(self):
        return 'MeleeAttack(mod={},reach={},damage="{}",dam_type="{}")'.format(
            self.mod,self.reach,self.damage,self.dam_type)
