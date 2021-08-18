from typing import Dict, List
from const import Const


class DataProcessor:
    def __init__(self, orders: Dict[int, int], const: Const):
        self.orders = orders
        self.const = const

    def get_orders(self) -> List[int]:
        return list(self.orders.keys())

    def get_slots(self) -> List[int]:
        return [i for i in range(1, self.const.NSLOTS + 1)]

    def get_durations(self) -> Dict[int, int]:
        return self.orders

    def get_changing_time(self) -> int:
        return self.const.TCHANGE

    def get_heating_time(self) -> int:
        return self.const.THEAT

    def get_time_steps(self) -> List[int]:
        time_steps_number = len(self.orders) - self.const.NSLOTS
        return [i for i in range(1, time_steps_number + 1)]

    def get_time_intervals(self) -> List[int]:
        return self.get_time_steps()[:-1]

    def get_last_time_step(self) -> int:
        return self.get_time_steps()[-1]
