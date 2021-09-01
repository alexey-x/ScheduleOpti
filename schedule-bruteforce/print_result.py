from typing import List
import click

from copy import deepcopy

from src.order import Order
from src.press import Press, THEAT
from src.orders_reader import OrdersReader

from src.press_working_strategy import WorkingStrategy
from src.press_working_strategy import DoShortOrderAndStopStrategy
from src.press_working_strategy import CheckNextOrderBeforeStopStrategy
from src.press_working_strategy import DoLongestOrderStrategy

STRATEGY_DO_SHORT_ORDER = "do-short-order"
STRATEGY_DO_LONG_ORDER = "do-long-order"
STRATEGY_CHK_NEXT_ORDER = "chk-next-order"


def str_to_list_int(orders: str, sep: str = ",") -> List[int]:
    return list(map(int, orders.split(sep)))


def get_orders(orders_indexes: List[int]) -> List[Order]:
    filename = "../data/orders.xlsx"
    orders = OrdersReader(filename)
    names = orders.get_matricies_names()
    durations = orders.get_orders_duration()
    return [Order(ix, durations[ix], names[ix]) for ix in orders_indexes]


def run(orders: List[Order], strategy: WorkingStrategy) -> None:
    press = Press(strategy, verbose=True)
    press.run(deepcopy(orders))
    return


@click.command()
@click.option("--orders", type=str, help="File with brute-force output")
@click.option(
    "--strategy",
    type=click.Choice(
        [STRATEGY_CHK_NEXT_ORDER, STRATEGY_DO_LONG_ORDER, STRATEGY_DO_SHORT_ORDER],
        case_sensitive=False,
    ),
    required=True,
    help="Strategy to deal with current orders under process.",
)
def main(orders, strategy):
    orders_indexes = str_to_list_int(orders)
    orders_list = get_orders(orders_indexes)
    print(orders_list)

    if strategy == STRATEGY_DO_SHORT_ORDER:
        work_strategy = DoShortOrderAndStopStrategy()
    if strategy == STRATEGY_CHK_NEXT_ORDER:
        work_strategy = CheckNextOrderBeforeStopStrategy(THEAT)
    if strategy == STRATEGY_DO_LONG_ORDER:
        work_strategy = DoLongestOrderStrategy()

    run(orders_list, work_strategy)


if __name__ == "__main__":
    main()
