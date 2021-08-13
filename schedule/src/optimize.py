from typing import List, Tuple
from copy import deepcopy
from multiprocessing import Pool

from itertools import permutations, islice

from src.press import Press
from src.order import Order
from src.press_working_strategy import WorkingStrategy



def get_run_time(orders: List[Order], strategy: WorkingStrategy) -> Tuple[int, List[Order]]:
    press = Press(strategy)
    press.run(deepcopy(orders))
    return press.total_work_time, orders


def brute_force_optimize(sequence: List[Order], strategy: WorkingStrategy, batchsize: int) -> Tuple[int, List[List[Order]]]:
    all_perm = permutations(sequence)
    best_time = sum((order.order_duration  for order in sequence))
    best_sequence = []
    while True:
        pool = Pool()
        _result = [pool.apply(get_run_time, args=(list(perm), strategy)) for perm in list(islice(all_perm, batchsize))]
        for runtime, runseq in _result:
            if best_time == runtime:
                best_sequence.append(runseq)
            elif best_time > runtime:
                best_time = runtime
                best_sequence = [runseq]

        if len(_result) == 0:
            break
    return best_time, best_sequence