from typing import List

from .order import Order
from .press_working_strategy import WorkingStrategy


NSLOTS = 3
TCHANGE = 20
THEAT = 40


class Press:
    def __init__(self, working_strategy: WorkingStrategy):
        self.working_strategy = working_strategy
        self.total_work_time = 0
        self.slot = [Order(-1, 0, "")] * NSLOTS

    def put_order_to_slot(self, i: int, order: Order) -> None:
        if order.get_order_duration() > 0:
            self.slot[i] = order
        else:
            print(
                f"Order {order.get_order_index()} has duration <= 0 -- order skipped."
            )

    def get_durations(self) -> List:
        return [
            order.get_order_duration()
            for order in self.slot
            if order.get_order_duration() > 0
        ]

    def get_empty_slot(self):
        return [
            i for i, order in enumerate(self.slot) if order.get_order_duration() == 0
        ]

    def all_slots_empty(self) -> bool:
        if len(self.get_durations()) == 0:
            return True
        else:
            return False

    def process_orders(self, process_time: int) -> None:
        self.total_work_time += process_time
        for order in self.slot:
            order.process_order(process_time)

    def add_change_order_time(self) -> None:
        self.total_work_time += TCHANGE

    def run(self, orders: List[Order], verbose=False) -> None:
        if verbose:
            print("... Start.")
        cycle_number = 0
        while orders:
            cycle_number += 1
            self.add_change_order_time()
            for i in self.get_empty_slot():
                if len(orders) == 0:
                    break
                order = orders.pop(0)
                self.put_order_to_slot(i, order)

            if verbose:
                print(f"cycle = {cycle_number}")
                self.print_state("After put orders to slots.")

            self.process_orders(THEAT)
            if verbose:
                self.print_state("After heating.")

            worktime_till_stop = self.working_strategy.get_worktime_till_stop(
                len(orders), self.get_durations()
            )
            self.process_orders(worktime_till_stop)
            if verbose:
                self.print_state(f"After processing. Processing time = {worktime_till_stop}.")

        if verbose:
            print("." * 50)
            print(f"Number of cycles = {cycle_number}")
            print(f"Total time = {self.total_work_time}")
            print("... End.")

    def print_state(self, msg: str) -> None:
        print(f"Time = {self.total_work_time}. {msg}")
        s = ""
        for order in self.slot:
            s += f"{order.__str__()} | "
        print(s + "\n")


if __name__ == "__main__":
    from copy import deepcopy

    from press_working_strategy import DoShortOrderAndStopStrategy
    from press_working_strategy import CheckNextOrderBeforeStopStrategy

    orders = [
        Order(0, 734, ""),
        Order(1, 722, ""),
        Order(2, 218, ""),
        Order(3, 1622, ""),
    ]

    press_work_strategy = DoShortOrderAndStopStrategy()

    press = Press(press_work_strategy)
    press.run(deepcopy(orders), verbose=True)

    print("-" * 50)

    press_work_strategy = CheckNextOrderBeforeStopStrategy(THEAT)
    press = Press(press_work_strategy)
    press.run(deepcopy(orders), verbose=True)
