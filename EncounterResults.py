
from collections import namedtuple

EncounterResults = namedtuple(
    'EncounterResults','party_remaining monsters_remaining')

def printEncounterResults(self):
    return 'party: {}, monsters: {}'.format(*self)

EncounterResults.__str__ = printEncounterResults
