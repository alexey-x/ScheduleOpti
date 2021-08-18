import click
import datetime

from typing import Dict

from src.orders_reader import OrdersReader
from src.data_processor import DataProcessor
from src.lin_prog_maker import LinProgMaker
from src.const import Const

def run(orders: Dict[int, int]) -> None:

    processor = DataProcessor(orders, Const())
    task = LinProgMaker(processor)
    task.solve()
    #writer = DataWriter(task, out_file)
    #writer.save()

    print(orders)


def get_orders(num_orders: int) -> Dict[int, int]:
    filename = "../data/orders.xlsx"
    orders = OrdersReader(filename, num_orders)
    return orders.get_orders_duration()


@click.command()
@click.option(
    "--num-orders", type=int, help="Number of orders to consider."
)
def main(num_orders):
    outfile = "../result/"
    time_start = datetime.datetime.now()
    print(f"Time start = {time_start.strftime('%Y-%m-%d %H:%M:%S')}")
    orders = get_orders(num_orders)

    run(orders)

    time_end = datetime.datetime.now()
    print(f"Time end = {time_end.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total time = {time_end - time_start}")
    return

if __name__ == "__main__":
    main()