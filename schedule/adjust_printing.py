import sys

sys.path.append(".")

from typing import List

from src.order import Order
from src.press_working_strategy import WorkingStrategy
from src.press import Press, NSLOTS


NSLOTS = 3
TCHANGE = 20
THEAT = 40


if __name__ == "__main__":
    from copy import deepcopy

    from src.press_working_strategy import DoShortOrderAndStopStrategy
    from src.press_working_strategy import CheckNextOrderBeforeStopStrategy
    from src.press_working_strategy import DoLongestOrderStrategy

    orders = [
        Order(0, 734, "Орион - 600"),
        Order(1, 722, "Орион - 700"),
        Order(8, 42, "Сатурн ПГ: 42"),
        Order(2, 1622, "Орион - 800"),
        Order(3, 218, "Весна - 600"),
        Order(5, 820, "Весна  - 800"),
        Order(4, 350, "Весна  - 700"),
        Order(6, 292, "Сафари"),
        Order(9, 584, "Сатурн ПО"),
        Order(7, 352, "Сафари 2"),
        Order(10, 374, "Соло"),
        Order(11, 30, "Арабеска ПО 800"),
        Order(12, 38, "Октава"),
    ]

    # press_work_strategy = DoShortOrderAndStopStrategy()
    #press_work_strategy = DoLongestOrderStrategy()
    press_work_strategy = CheckNextOrderBeforeStopStrategy(THEAT)
    press = Press(press_work_strategy)
    press.run(deepcopy(orders), verbose=True)
