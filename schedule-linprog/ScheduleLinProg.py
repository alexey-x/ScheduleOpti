import click
import datetime

from typing import Dict

from src.orders_reader import OrdersReader
from src.data_processor import DataProcessor
from src.const import Const

STRATEGY_SIMPLE = "simple-task"
STRATEGY_FULL = "full-task"


def run(
    num_time_interval: int, orders: Dict[int, int], strategy: str, outfile: str
) -> None:
    if not orders:
        print("No orders to process.")
        return
    processor = DataProcessor(num_time_interval, orders, Const())

    if strategy == STRATEGY_SIMPLE:
        from src.lin_prog_maker_simple import LinProgMaker
        from src.data_writer_simple import DataWriter
    elif strategy == STRATEGY_FULL:
        from src.lin_prog_maker_full import LinProgMaker
        from src.data_writer_full import DataWriter

    task = LinProgMaker(processor)
    task.solve()
    writer = DataWriter(task, outfile)
    writer.save()
    writer.write_lp_model()
    writer.print_additional_info()


def get_orders(num_orders: int, infile: str) -> Dict[int, int]:
    orders = OrdersReader(infile, num_orders)
    return orders.get_orders_duration()


@click.command()
@click.option("--num-orders", type=int, help="Number of orders to consider.")
@click.option("--num-time-interval", type=int, help="Number of work time intervals.")
@click.option(
    "--strategy",
    type=click.Choice([STRATEGY_SIMPLE, STRATEGY_FULL], case_sensitive=False,),
    required=True,
    help="Defines what kind of lin. programming task to solve.",
)
def main(num_orders, num_time_interval, strategy):
    infile = "../data/orders.xlsx"
    outfile = f"../result/lin-prog-{strategy}-{num_orders}-orders-{num_time_interval}-interval.xlsx"

    time_start = datetime.datetime.now()
    print(f"Time start = {time_start.strftime('%Y-%m-%d %H:%M:%S')}")

    orders = get_orders(num_orders, infile)
    run(num_time_interval, orders, strategy, outfile)

    time_end = datetime.datetime.now()
    print(f"Time end = {time_end.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total time = {time_end - time_start}")
    return


if __name__ == "__main__":
    main()
