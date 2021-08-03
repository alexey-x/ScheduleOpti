
from  typing import List

from . order import Order

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
            print(f"Order {order.get_order_index()} has duration <= 0 -- order skipped.")

    def get_durations(self) -> List:
        return [order.get_order_duration() for order in self.slot if order.get_order_duration() > 0]

    def get_empty_slot(self):
        return [i for i, order in enumerate(self.slot) if order.get_order_duration() == 0]

    def get_first_finish_time(self) -> int:
        return min(self.get_durations())

    def process_orders(self, process_time:int) -> None:
        self.total_work_time += process_time
        for order in self.slot:
            order.process_order(process_time)

    def heat_orders(self):
        self.total_work_time += THEAT

    def add_change_order_time(self) -> None:
        self.total_work_time += TCHANGE

    def run(self, orders: List[Order]) -> None:
        while orders:
            self.add_change_order_time()
            for i in self.get_empty_slot():
                if len(orders) == 0: break
                order = orders.pop(0)
                self.put_order_to_slot(i, order)

            if len(self.get_durations()) == 0:
                print("No orders in the slots. Better raise Exception")
                break
    
            self.process_orders(THEAT)

            first_finish_time = self.get_first_finish_time()
            self.process_orders(first_finish_time)

    def __repr__(self):
        s = f"Total time: {self.total_work_time}\n"
        for i in range(NSLOTS):
            s += f"{i}: {self.slot[i]}\n"
        return s