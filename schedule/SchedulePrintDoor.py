import click
import datetime

from typing import Dict, List
from numpy import array
from itertools import permutations

from src.orders_reader import OrdersReader
from src.press import THEAT, Press
from src.order import Order

# 1. Wait till the heating is over. Change matrix for and start heating for another order.
#   take next order, put to slot, start press, heat, if during the heating another
#   order is finished DO NOT STOP PRESS to change order 
#   also DO NOT STOP when heating is done - continue and change two orders next time!!!
#   TODO -- change order when heating is done
# 2. Avoid such cases. Have a look to the future if another order will be finished during the heating do not change matrix, 
#    wait for another order.
#    Here there are subtle cases what if another order finishes just one minute after the heating etc?
#    It is possible to introduce another somoothing time but it seems there always be more optimal solution. 


def get_orders() -> Dict[int, int]:
    filename = "../data/orders.xlsx"
    orders = OrdersReader(filename)

    # print(f"Number of orders {orders.get_orders_number()}")
    # print(f"Orders indexies {orders.get_orders_indexes()}")
    # print(f"Orders duration {orders.get_orders_duration()}")

    return orders.get_orders_duration()


def get_orders_list(indexes: List[int], durations: Dict[int, int]) -> List[Order]:
    return [Order(ix, durations[ix]) for ix in indexes if durations[ix] > 0]

def calc_disorder(x0: array, x: array) -> int:
    return ((x0 - x) != 0).sum()


def get_run_time(orders: List[Order]) -> int:
    press = Press()
    press.run(orders)
    return press.total_work_time


@click.command()
@click.option(
    "--num-orders", default=13, type=int, help="Number of orders to consider."
)
def main(num_orders):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    orders_durations = get_orders()

    orders_indexes = list(orders_durations.keys())
    orders_indexes.sort(key=lambda x: orders_durations[x], reverse=True)
    zero_entropy_orders_set = orders_indexes[:num_orders]
    orders = get_orders_list(zero_entropy_orders_set, orders_durations)
    zero_entropy_time = get_run_time(orders)

    print(f"entropy0 = {zero_entropy_orders_set}, time = {zero_entropy_time}")

    current_min_set = [zero_entropy_orders_set]
    current_min_time = zero_entropy_time
    for perm in permutations(zero_entropy_orders_set):
        perm_time = get_run_time(get_orders_list(perm, orders_durations))
        # entropy = calc_disorder(array(zero_entropy_orders_set), array(perm))
        if perm_time == current_min_time:
            current_min_set.append(perm)
        elif perm_time < current_min_time:
            # TODO: add output for std here
            current_min_time = perm_time
            current_min_set = [perm]
        # print(perm, entropy, perm_time)
    print(f"min time = {current_min_time}")
    print(f"lenght of min orders set = {len(current_min_set)}")
    print(current_min_set[0])
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    main()
