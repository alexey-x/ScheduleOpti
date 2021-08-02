
class Order:
    def __init__(self, order_index: int, order_duration: int):
        self.order_index = order_index
        self.order_duration = order_duration
        self.heated = False

    def get_order_index(self):
        return self.order_index

    def get_order_duration(self):
        return self.order_duration

    def process_order(self, order_process_time: int) -> None:
        if self.heated:
            self.order_duration = max(0, self.order_duration - order_process_time)
        else:
            self.heated = True

    def __repr__(self):
        return f"Order({self.order_index}: {self.order_duration}, heated={self.heated})"