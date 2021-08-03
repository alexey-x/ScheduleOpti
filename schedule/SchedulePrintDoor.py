
from typing import Dict, List
from src.orders_reader import OrdersReader
from src.press import THEAT, Press
from src.order import Order

# 1. Wait till the heating is over. Change matrix for and start heating for another order.
# 2. Avoid such cases. Have a look to the future if another order will be finished during the heating do not change matrix, wait for another order.


def get_orders()->List:
    filename = "../data/orders.xlsx"
    orders = OrdersReader(filename)

    print(f"Number of orders {orders.get_orders_number()}")
    print(f"Orders indexies {orders.get_orders_indexes()}")
    print(f"Orders duration {orders.get_orders_duration()}")

    return orders

def get_orders_sequence(orders: Dict) -> List[Order]:
    return [Order(ix, dur) for ix, dur in orders.items()]

def main():
    #orders = get_orders()
    #orders = get_orders_sequence(orders.get_orders_duration())
    #x.sort(key=lambda x: dur[x], reverse=True)

    orders = [Order(1, 10)]

    press = Press()
    press.run(orders)
    

        # here the strategy applies
        # chose simplest 1. - take next order, put to slot, start press, heat, if during the heating another
        # order is finished DO NOT STOP PRESS!!!
    
    print("-"*50)
    print(press)

if __name__ == "__main__":
    main()
