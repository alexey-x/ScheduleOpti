from typing import List

from .order import Order

NSLOTS = 3
TCHANGE = 20
THEAT = 40


class Press:
    def __init__(self):
        self.total_work_time = 0
        self.slot = [Order(None, 0)] * NSLOTS

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

    def get_min_work_time(self) -> int:
        return min(self.get_durations())

    def get_max_work_time(self) -> int:
        return max(self.get_durations())

    def get_worktime_till_stop(self, orders_left: int) -> int:
        if orders_left == 0:
            return self.get_max_work_time()
        else:
            return self.get_min_work_time()

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
                print("Orders are in the slots. Change time counted.")
                print(f"cycle = {cycle_number}")
                print(self.__repr__())

            self.process_orders(THEAT)
            if verbose:
                print("Orders after heating.")
                print(self.__repr__())

            worktime_till_stop = self.get_worktime_till_stop(len(orders))
            self.process_orders(worktime_till_stop)
            if verbose:
                print("Orders after processing.")
                print(f"Processing time = {worktime_till_stop}")
                print(self.__repr__())

        if verbose:
            print("." * 50)
            print(f"Number of cycles = {cycle_number}")
            print(f"Total time = {self.total_work_time}")
            print("... End.")

    def __repr__(self):
        s = f"Total time: {self.total_work_time}\n"
        for i in range(NSLOTS):
            s += f"{i}: {self.slot[i]}, "
        return s + "\n"