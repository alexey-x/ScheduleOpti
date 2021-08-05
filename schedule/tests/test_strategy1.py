import sys

sys.path.append("./src")
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

# Better reject such orders before processing
#def test_order_zero_duration():
#    order_duration = 0
#    orders = [Order(1, order_duration)]
#    assert run_press(orders) == TCHANGE # better raise exception

def test_tree_orders_longer_than_THEAT():
    """max_duration > THEAT"""
    max_duration = 50
    orders = [Order(1, max_duration), Order(2, 3), Order(3, 2)]
    assert run_press(orders) == TCHANGE + THEAT + max_duration

def test_tree_orders_shorter_than_THEAT():
    """max_duration < THEAT"""
    max_duration = 10
    orders = [Order(1, max_duration), Order(2, 3), Order(3, 2)]
    assert run_press(orders) == TCHANGE + THEAT + max_duration

def test_four_orders():
    max_duration = 50
    orders = [Order(1, max_duration), Order(2, 3), Order(3, 2),  Order(3, 1)]
    assert run_press(orders) == TCHANGE + THEAT + TCHANGE + max_duration

def test_seven_orders():
    orders = [Order(i, 1) for i in range(7)]
    assert run_press(orders) == 3*(TCHANGE + THEAT + 1)