import click
import datetime

from typing import Dict

from src.orders_reader import OrdersReader
from src.data_processor import DataProcessor
from src.lin_prog_maker import LinProgMaker
from src.data_writer import DataWriter
from src.const import Const


def run(orders: Dict[int, int], outfile: str) -> None:
    if not orders:
        print("No orders to process.")
        return
    processor = DataProcessor(orders, Const())
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
def main(num_orders):
    infile = "../data/orders.xlsx"
    outfile = "../result/lin_prog_out.xlsx"

    time_start = datetime.datetime.now()
    print(f"Time start = {time_start.strftime('%Y-%m-%d %H:%M:%S')}")

    orders = get_orders(num_orders, infile)
    print(orders)
    run(orders, outfile)

    time_end = datetime.datetime.now()
    print(f"Time end = {time_end.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total time = {time_end - time_start}")
    return


if __name__ == "__main__":
    main()
