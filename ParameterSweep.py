
from random import randint
import pandas as pd
import re

from Suite import Suite
from Combatant import Combatant
from Encounter import Encounter
from SimCombat import *

class ParameterSweep():
    '''Simulate an encounter while varying some number of parameters within a
    range of values, and compute aggregate results. Each set of parameter
    values will be executed as a suite (i.e., multiple times.)'''

    def __init__(self, encounter, sweep_params):
        '''"encounter" is the generic type of Encounter (i.e., two sets of
        Combatant objects for the party and the monsters) to be simulated.
        "sweep_params" is a dictionary whose keys are Combatants and whose
        values are dictionaries; these dictionaries' keys are attributes of
        the Combatant in question and values are lists of values to set each
        attribute to.'''
        self._encounter = encounter
        self._sweep_params = sweep_params

    @classmethod
    def from_filename(self, filename):
        '''Hydrate a ParameterSweep object from a file. The file should be in
        this format:

        --------------------------------------------------------------------
        Party:
        commoner,3,hp:d6+(9-50)

        Monsters:
        kobold,4
        hydra,2
        --------------------------------------------------------------------
        If present after the quantity, sweep parameters with ranges are
        defined for that combatant.
        '''
        with open(filename, "r") as f:
            lines = [line.rstrip() for line in f.readlines() 
                if len(line.strip()) > 0]
            party_lines = lines[1:lines.index('Monsters:')]
            monsters_lines = lines[lines.index('Monsters:')+1:]

            party, sweep_params = instantiate_group(party_lines)
            monsters, sweep_params2 = instantiate_group(monsters_lines)

            sweep_params.update(sweep_params2)

        return ParameterSweep(Encounter(party,monsters),sweep_params)

    def execute(self, suite_size=10):

        log_meta('Starting sweep...')
        results = pd.DataFrame(columns=[
                            'combatant','param','value','party_win_freq'])

        for combatant, params in self._sweep_params.items():
            for param, vals in params.items():
                for val in vals:
                    if type(combatant) is tuple:
                        for c in combatant:
                            c.set_stat(param, val)
                    else:
                        combatant.set_stat(param, val)
                    log_meta_detail(' ...running suite for {!s}.{!s}={!s}...'.
                        format(combatant, param, val))
                    suite = Suite(self._encounter, suite_size)
                    these_results = suite.execute()
                    party_wins = [r.party_remaining > r.monsters_remaining
                            for r in these_results]
                    party_win_freq = sum(party_wins)/len(party_wins)
                    results = results.append(pd.DataFrame.from_records([{
                        'combatant':prstr(combatant),
                        'param':param,
                        'value':val,
                        'party_win_freq':party_win_freq}]))
        return results[['combatant','param','value','party_win_freq']]


def instantiate_group(lines):
    group = []
    sweep_params = {}
    for combatant in lines:
        combatant_parts = combatant.split(',')
        these_combatants = [
            Combatant.from_filename(combatant_parts[0])
                for _ in range(int(combatant_parts[1]))]
        group.extend(these_combatants)
        if len(combatant_parts) > 2:
            for param in combatant_parts[2:]:
                param_parts = param.split(':')
                sweep_params.update(
                    {tuple(c for c in these_combatants):{
                    param_parts[0]:build_pv_list(param_parts[1])}})
    return group, sweep_params


def build_pv_list(string):
    '''From a string like 'd6+(0-5)', return a list incarnating all the
    values in parens. In this case, the list would be ['d6+0','d6+1','d6+2',
    'd6+3','d6+4','d6+5'].'''
    if '(' not in string:
        return [ string ]
    prefix = string[0:string.index('(')]
    first_num = int(string[string.index('(')+1:string.index('-')])
    last_num = int(string[string.index('-')+1:string.index(')')])
    return [ prefix + str(k) for k in range(first_num,last_num+1) ]


def run_sample_sweep(suite_size=10, party_size=2, num_monsters=3):

    party = {Combatant.from_filename('commoner'):party_size}
    monsters = {Combatant.from_filename('kobold'):num_monsters}
    encounter = Encounter(party, monsters)

    sweep_params = {
        tuple(party.keys()):{'hp': ['d6+'+str(mod) for mod in range(0,8)]}}

    return ParameterSweep(encounter, sweep_params).execute(suite_size)


