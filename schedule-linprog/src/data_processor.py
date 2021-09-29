from typing import Dict, List
from .const import Const


class DataProcessor:
    def __init__(self, num_time_interval: int, orders: Dict[int, int], const: Const):
        self.num_time_interval = num_time_interval
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

    def get_orders_number(self) -> int:
        return len(self.orders)

    def get_heating_time(self) -> int:
        return self.const.THEAT

    def get_min_number_interval(self) -> int:
        return (self.get_orders_number() + 2)//3

    def get_time_steps(self) -> List[int]:
        if self.num_time_interval is None:
            time_steps_number = max(2, len(self.orders) - 1)
        else:
            time_steps_number = self.num_time_interval + 1
        return [i for i in range(1, time_steps_number + 1)]

    def get_max_duration(self) -> int:
        return  max(self.get_durations().values())

    def get_min_working_time(self) -> int:
        """Most general estimation - one order may be so long that others finish earlier."""
        init_time = self.const.TCHANGE + self.const.THEAT
        #max_duration = max([i for i in self.get_durations().values()])
        max_duration = max(self.get_durations().values())
        return init_time + max_duration
