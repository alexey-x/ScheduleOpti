import sys

sys.path.append("./src")
sys.path.append("..")

from src.sub_tasks import flatten
from src.sub_tasks import get_permutations

# Flaltten is taken from stackoverflow.
# Run simple test on it.
def test_flatten():
    """Make nested structure flat"""
    sequence = [(1, 2), [3, 4, [5, [6, [7]]]]]
    assert  list(flatten(sequence)) == [1, 2, 3, 4, 5, 6, 7]

def test_get_perm_empty():
    a = 3 # any number > 0
    assert list(get_permutations([], a)) == [[]]

