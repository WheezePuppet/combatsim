
from random import randint
import pandas as pd

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


    def execute(self, suite_size=10):

        log_meta('Starting sweep...')
        results = pd.DataFrame(columns=[
                            'combatant','param','value','party_win_freq'])

        for combatant, params in self._sweep_params.items():
            for param, vals in params.items():
                for val in vals:
                    if type(combatant) is tuple:
                        [c.set_stat(param, val) for c in combatant]
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


def run_sample_sweep(suite_size=10):

    party = [Combatant.from_filename('commoner') for _ in range(3)]
    monsters = [Combatant.from_filename('kobold') for _ in range(4)]
    encounter = Encounter(party, monsters)

    commoner1 = party[0]
    commoner2 = party[1]

    sweep_params = {
        (commoner1,commoner2):{'hp': ['d6+'+str(mod) for mod in range(0,80)]}}

    return ParameterSweep(encounter, sweep_params).execute(suite_size)


