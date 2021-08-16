from typing import List
from abc import ABC, abstractmethod
from dataclasses import dataclass


class WorkingStrategy(ABC):
    """Strategy decides how the orders should be processed."""

    @abstractmethod
    def get_worktime_till_stop(self) -> int:
        pass

class DoLongestOrderStrategy(WorkingStrategy):
    """Do the longest order from all slots. After that put new orders.
    There is very fast and simple solution for this strategy.
    See (jupyter/05_brute_force_simple).
    """
    def get_worktime_till_stop(
        self, orders_left: int, order_durations: List[int]
    ) -> int:
        return max(order_durations)

class DoShortOrderAndStopStrategy(WorkingStrategy):
    """After the shortest order is done change matrix for the next order."""

    def get_worktime_till_stop(
        self, orders_left: int, order_durations: List[int]
    ) -> int:
        if orders_left == 0:
            return max(order_durations)
        else:
            return min(order_durations)


@dataclass
class CheckNextOrderBeforeStopStrategy(WorkingStrategy):
    """Check if after the shortest order is done and new order is heating another order finishes.
    If yes, do not start immediately but wait for the other order finishes.  
    """

    time_treshold: int

    def get_worktime_till_stop(
        self, orders_left: int, order_durations: List[int]
    ) -> int:
        if orders_left == 0:
            return max(order_durations)
        else:
            tmin = min(order_durations)
            return max(
                [t for t in order_durations if tmin <= t <= tmin + self.time_treshold]
            )
