import sys

sys.path.append("..")

from src.press import THEAT, TCHANGE, Press
from src.order import Order

def run_press(orders):
    press = Press()
    press.run(orders)
    return press.total_work_time

def test_no_orders():
    assert run_press([]) == 0, "no orders => work time = 0"

def test_one_order():
    order_duration = 10
    orders = [Order(1, order_duration)]
    assert run_press(orders) == TCHANGE + THEAT + order_duration

def test_order_zero_duration():
    order_duration = 0
    orders = [Order(1, order_duration)]
    assert run_press(orders) == 0