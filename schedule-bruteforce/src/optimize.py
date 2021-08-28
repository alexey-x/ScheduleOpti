from typing import List, Tuple
from copy import deepcopy
from multiprocessing import Pool

from itertools import islice

from src.press import Press, NSLOTS
from src.order import Order
from src.press_working_strategy import WorkingStrategy
from src.sub_tasks import get_permutations

def get_run_time(
    orders: List[Order], strategy: WorkingStrategy
) -> Tuple[int, List[Order]]:
    press = Press(strategy)
    press.run(deepcopy(orders))
    return press.total_work_time, orders


def brute_force_optimize(
    sequence: List[Order], strategy: WorkingStrategy, batchsize: int
) -> Tuple[int, List[List[Order]]]:
    all_perm = get_permutations(sequence, NSLOTS)
    best_time = sum((order.get_order_duration() for order in sequence))
    best_sequence = []
    while True:
        pool = Pool()
        _result = [
            pool.apply(get_run_time, args=(list(perm), strategy))
            for perm in list(islice(all_perm, batchsize))
        ]
        print(f"Batch calc is done. Pool length = {len(_result)}")
        for runtime, runseq in _result:
            if best_time == runtime:
                best_sequence.append(runseq)
            elif best_time > runtime:
                best_time = runtime
                best_sequence = [runseq]
        print("Local best sequence is found.")
        if len(_result) == 0:
            break
    return best_time, best_sequence
