import click
import datetime

from src.press import THEAT
from src.orders_io import get_orders, save_orders

from src.press_working_strategy import DoShortOrderAndStopStrategy
from src.press_working_strategy import CheckNextOrderBeforeStopStrategy
from src.press_working_strategy import DoLongestOrderStrategy


from src.optimize import brute_force_optimize

DATAFILE = "../data/orders.xlsx"
OUTDIR = "../result/"

STRATEGY_DO_SHORT_ORDER = "do-short-order"
STRATEGY_DO_LONG_ORDER = "do-long-order"
STRATEGY_CHK_NEXT_ORDER = "chk-next-order"


@click.command()
@click.option("--num-orders", type=int, help="Number of orders to consider.")
@click.option(
    "--strategy",
    type=click.Choice(
        [STRATEGY_CHK_NEXT_ORDER, STRATEGY_DO_LONG_ORDER, STRATEGY_DO_SHORT_ORDER],
        case_sensitive=False,
    ),
    required=True,
    help="Strategy to deal with current orders under process.",
)
@click.option(
    "--batchsize", default=20000, type=int, help="Batch size for paralell computation.",
)
def main(num_orders, strategy, batchsize):
    time_start = datetime.datetime.now()
    print(f"Time start = {time_start.strftime('%Y-%m-%d %H:%M:%S')}")
    orders = get_orders(num_orders)

    if strategy == STRATEGY_DO_SHORT_ORDER:
        work_strategy = DoShortOrderAndStopStrategy()
    if strategy == STRATEGY_CHK_NEXT_ORDER:
        work_strategy = CheckNextOrderBeforeStopStrategy(THEAT)
    if strategy == STRATEGY_DO_LONG_ORDER:
        work_strategy = DoLongestOrderStrategy()

    print("--> ", orders)
    best_time, best_cycle_number, best_sequence = brute_force_optimize(
        orders, work_strategy, batchsize
    )

    outfile = f"{OUTDIR}brute-{strategy}-{num_orders}-orders.txt"
    save_orders(outfile, strategy, best_time, best_cycle_number, best_sequence)

    print(f"best time = {best_time}")
    print(f"cycles = {best_cycle_number}")
    print(f"length of min orders set = {len(best_sequence)}")
    print(best_sequence[0])
    time_end = datetime.datetime.now()
    print(f"Time end = {time_end.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total time = {time_end - time_start}")
    return


if __name__ == "__main__":
    main()
