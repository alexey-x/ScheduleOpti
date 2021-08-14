
from itertools import combinations
from collections import Iterable

def flatten(lst):
    """Make flat nested lists or tuples."""
    for item in lst:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:        
            yield item



#   See Task description for details.
#   For bruete force we need all permutations of orders. Then we start from first triple and proceed.
#   For the 13 orders there are 13! permutations. The number impossible to handle even with 8 processors.
#   But notice that reuslt for (1, 2, 3) will not differ from the one for (2, 3, 1). 
#   So, I don't need all permutations but only subset with unqiue triples.
#   This functions solves the problem.


# TODO 
# 1. rename the function and variables
def get_permutations(sequence: Iterable, n: int): # returns generator of lists
    seq_length = len(sequence)
    filled_slots, rest  = divmod(seq_length, n)
    # combinations when all slots are full 
    # time of the task is max duration of single orders
    comb_all_slots = []
    for k in combinations(sequence, n):
        comb_all_slots.append(k)

    # combinations of rests 
    comb_rest = []
    for k in combinations(sequence, rest):
        comb_rest.append(k)

    for seq in combinations(comb_all_slots, filled_slots):
        f1 = list(flatten(seq))
        if len(f1) != len(set(f1)):
            continue

        for r in comb_rest:
            f2 = f1 + list(r)
            if len(f2) == len(set(f2)):
                yield f2
