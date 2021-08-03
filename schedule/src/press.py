
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
        self.slot[i] = order

    def get_durations(self) -> List:
        return [order.get_order_duration() for order in self.slot]

    #def get_first_finish_slot(self, min_duration: int) -> List[int]:
    #    return [i for i, order in enumerate(self.slot) if order.get_order_duration() == min_duration]

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

    def count_change_order_time(self) -> None:
        self.total_work_time += TCHANGE


    def __repr__(self):
        s = f"Total time: {self.total_work_time}\n"
        for i in range(NSLOTS):
            s += f"{i}: {self.slot[i]}\n"
        return s


    
       

    def process_single_step(self):
        # find slot first finish

        # decrease all orders by delta

        # change matrix

        # start work
        #  --heat slot
        #  --others others work according policy till end of heating
        #  --heating over
        #  --continue normal work or change matrix 


        print("process")
        for i in range(NSLOTS):
            self.process_single_slot(i)

    


    def run(self):
        while self.orders:
            self.process_single_step()