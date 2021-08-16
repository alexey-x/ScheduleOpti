import click
import datetime

from typing import List

from src.press import THEAT
from src.orders_reader import OrdersReader
from src.press_working_strategy import DoShortOrderAndStopStrategy
from src.press_working_strategy import CheckNextOrderBeforeStopStrategy
from src.press_working_strategy import DoLongestOrderStrategy


from src.order import Order
from src.optimize import brute_force_optimize

# 1. Wait till the heating is over. Change matrix for and start heating for another order.
#   take next order, put to slot, start press, heat, if during the heating another
#   order is finished DO NOT STOP PRESS to change order
#   also DO NOT STOP when heating is done - continue and change two orders next time!!!
#   TODO -- change order when heating is done
# 2. Avoid such cases. Have a look to the future if another order will be finished during the heating do not change matrix,
#    wait for another order.
#    Here there are subtle cases what if another order finishes just one minute after the heating etc?
#    It is possible to introduce another somoothing time but it seems there always be more optimal solution.


def get_orders(num_orders: int) -> List[Order]:
    filename = "../data/orders.xlsx"
    orders = OrdersReader(filename, num_orders)
    order_names = orders.get_matricies_names()
    return [Order(ix, dur, order_names[ix]) for ix, dur in orders.get_orders_duration().items()]

def save_orders(outfile: str, best_time: int, best_sequence: List[List[Order]])-> None:
    with open(outfile, "w") as out:
        print(f"BestTime = {best_time}", file=out)
        for i, seq in enumerate(best_sequence):
            print(i, "-"*50, file=out)
            for order in seq:
                print(order, file=out)
    return

@click.command()
@click.option(
    "--num-orders", type=int, help="Number of orders to consider."
)
@click.option(
    "--strategy",
    type=click.Choice(["do_short_order", "check_next_order", "do_long_order"], case_sensitive=False),
    required=True,
    help="Strategy how to deal with current orders under process.",
)
@click.option(
    "--batchsize", default=1000000, type=int, help="Batch size for paralell computation."
)
def main(num_orders, strategy, batchsize):
    outfile = "../result/"
    time_start = datetime.datetime.now()
    print(f"Time start = {time_start.strftime('%Y-%m-%d %H:%M:%S')}")
    orders = get_orders(num_orders)
    
    if strategy == "do_short_order":
        work_strategy = DoShortOrderAndStopStrategy()
    if strategy == "check_next_order":
        work_strategy = CheckNextOrderBeforeStopStrategy(THEAT)
    if strategy == "do_long_order":
        work_strategy = DoLongestOrderStrategy()
    
    print("--> ", orders)
    best_time, best_sequence = brute_force_optimize(orders, work_strategy, batchsize)

    outfile += strategy + ".txt"
    save_orders(outfile, best_time, best_sequence)
    
    print(f"best time = {best_time}")
    print(f"length of min orders set = {len(best_sequence)}")
    print(best_sequence[0])
    time_end = datetime.datetime.now()
    print(f"Time end = {time_end.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total time = {time_end - time_start}")
    return


if __name__ == "__main__":
    main()
