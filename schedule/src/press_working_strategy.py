
from typing import List
from abc import ABC, abstractmethod
from dataclasses import dataclass

class WorkingStrategy(ABC):
    """Strategy decides how the orders should be processed."""

    @abstractmethod
    def get_worktime_till_stop(self, orders_left: int, order_durations: List[int]) -> int:
        pass

class DoShortOrderAndStopStrategy(WorkingStrategy):
    """After the shortest order is done change matrix for the next order."""

    def get_worktime_till_stop(self, orders_left: int, order_durations: List[int]) -> int:
        if orders_left == 0:
            return max(order_durations)
        else:
            return min(order_durations)

@dataclass
class CheckNextOrderBeforeStopStrategy(WorkingStrategy):
    """Check if after the shortest order is done and heating starts other order finishes.
    If yes, do not start immediately but wait for the other order finishes.  
    """

    time_treshold: int
    
    def get_worktime_till_stop(self, orders_left: int, order_durations: List[int]) -> int:
        if orders_left == 0:
            return max(order_durations)
        else:
            tmin = min(order_durations)
            return max(
                [
                    t
                    for t in order_durations
                    if t > tmin and t <= tmin + self.time_treshold
                ]
            )