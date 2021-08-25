import sys

sys.path.append("./src")
sys.path.append("..")

from src.press import THEAT, TCHANGE, Press
from src.press_working_strategy import DoShortOrderAndStopStrategy
from src.order import Order

def run_press(orders):
    press = Press(DoShortOrderAndStopStrategy())
    press.run(orders)
    return press.total_work_time

def test_no_orders():
    assert run_press([]) == 0, "no orders => work time = 0"

def test_one_order():
    order_duration = 10
    orders = [Order(1, order_duration, "1")]
    assert run_press(orders) == TCHANGE + THEAT + order_duration

def test_tree_orders_longer_than_THEAT():
    """max_duration > THEAT"""
    max_duration = 50
    orders = [Order(1, max_duration, "1"), Order(2, 3, "2"), Order(3, 2, "3")]
    assert run_press(orders) == TCHANGE + THEAT + max_duration

def test_tree_orders_shorter_than_THEAT():
    """max_duration < THEAT"""
    max_duration = 10
    orders = [Order(1, max_duration, "1"), Order(2, 3, "2"), Order(3, 2, "3")]
    assert run_press(orders) == TCHANGE + THEAT + max_duration

def test_four_orders():
    max_duration = 50
    orders = [Order(1, max_duration, "2"), Order(2, 3, "2"), Order(3, 2, "3"),  Order(3, 1, "4")]
    assert run_press(orders) == TCHANGE + THEAT + TCHANGE + max_duration

def test_seven_orders():
    orders = [Order(i, 1, str(i)) for i in range(7)]
    assert run_press(orders) == 3*(TCHANGE + THEAT + 1)