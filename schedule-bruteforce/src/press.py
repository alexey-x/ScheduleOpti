from typing import List, Optional
from pandas import DataFrame

from .order import Order
from .press_working_strategy import WorkingStrategy


NSLOTS = 3
TCHANGE = 20
THEAT = 40

STEP_CHANGE = "change"
STEP_HEAT = "heat"
STEP_WORK = "work"

class Press:
    def __init__(self, working_strategy: WorkingStrategy, verbose: bool = False):
        self.working_strategy = working_strategy
        self.verbose = verbose

        self.total_work_time = 0
        self.slot = [Order(-1, 0, "")] * NSLOTS
        self.cycle_number = 0
        if self.verbose:
            self.result_ix = 0
            self.result = DataFrame(columns=[
                "Cycle",
                "Slot",                
                "Order",
                "Duration",
                "Time",
                "WorkStep",
                "OrderState",
                "WorkTime",
                "OrderRest",
                ]
            )

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
        return len(self.get_durations()) == 0

    def process_orders(self, process_time: int) -> None:
        self.total_work_time += process_time
        for order in self.slot:
            order.process_order(process_time)

    def add_change_order_time(self) -> None:
        self.total_work_time += TCHANGE

    def run(self, orders: List[Order]) -> None:
        if self.verbose:
            print("... Start.")
        self.cycle_number = 0
        while orders:
            self.cycle_number += 1
            self.add_change_order_time()
            for i in self.get_empty_slot():
                if not orders:
                    break
                order = orders.pop(0)
                self.put_order_to_slot(i, order)

            if self.verbose:
                self.print_state("After put orders to slots.")
                self.save_state(STEP_CHANGE)

            self.process_orders(THEAT)
            if self.verbose:
                self.print_state("After heating.")
                self.save_state(STEP_HEAT)

            worktime_till_stop = self.working_strategy.get_worktime_till_stop(
                len(orders), self.get_durations()
            )
            self.process_orders(worktime_till_stop)
            if self.verbose:
                self.print_state(
                    f"After processing. Processing time = {worktime_till_stop}."
                )
                self.save_state(STEP_WORK, worktime_till_stop)

        if self.verbose:
            print("." * 50)
            print(f"Number of cycles = {self.cycle_number}")
            print(f"Total time = {self.total_work_time}")
            print("... End.")

    def print_state(self, msg: str) -> None:
        print(f"Cycle = {self.cycle_number}")
        print(f"Time = {self.total_work_time}. {msg}")
        s = "".join(f"{order.__str__()} | " for order in self.slot)
        print(s + "\n")

    def save_state(self, step: str, worktime_time_stop: Optional[int] = None) -> None:
        for slot_number, order in enumerate(self.slot):
            self.result.loc[self.result_ix, :] = (
                self.cycle_number,
                slot_number,
                order.get_order_index(),
                order.get_order_length(),
                self.total_work_time,
                step,
                order.get_order_state(),
                worktime_time_stop,
                order.get_order_duration()
            )
            self.result_ix += 1
