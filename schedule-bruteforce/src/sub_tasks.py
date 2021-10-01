
from itertools import combinations
from collections import Iterable

def flatten(lst):
    """Make flat nested lists or tuples. Taken from github."""
    for item in lst:
        if isinstance(item, Iterable) and not isinstance(item, str):
            yield from flatten(item)
        else:        
            yield item

#  See TaskDescription_EN notebook for details (Sequences generation subsection.).
def get_permutations(sequence: Iterable, n: int): # returns generator of lists
    seq_length = len(sequence)
    filled_slots, rest  = divmod(seq_length, n)
    
    comb_all_slots = combinations(sequence, n)
    comb_rest = list(combinations(sequence, rest))

    for seq in combinations(comb_all_slots, filled_slots):
        f1 = list(flatten(seq))
        if len(f1) != len(set(f1)):
            continue

        for r in comb_rest:
            f2 = f1 + list(r)
            if len(f2) == len(set(f2)):
                yield f2
