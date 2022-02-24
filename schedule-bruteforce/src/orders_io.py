from typing import List

from src.order import Order
from src.orders_reader import OrdersReader


def get_orders(filename: str, num_orders: int) -> List[Order]:
    orders = OrdersReader(filename, num_orders)
    order_names = orders.get_matricies_names()
    return [
        Order(ix, dur, order_names[ix])
        for ix, dur in orders.get_orders_duration().items()
    ]


def save_orders(
    outfile: str,
    strategy: str,
    best_time: int,
    best_cycle_number: int,
    best_sequence: List[List[Order]],
) -> None:
    with open(outfile, "w") as out:
        print(f"Strategy = {strategy}", file=out)
        print(f"BestTime = {best_time}", file=out)
        print(f"Cycles = {best_cycle_number}", file=out)
        for i, seq in enumerate(best_sequence):
            order_indexes = ", ".join(str(order.get_order_index()) for order in seq)
            print(f"{i}: {order_indexes}", file=out)
