

class Order:
    def __init__(self, order_index: int, order_duration: int, order_name: str):
        self._order_index = order_index
        self._order_duration = order_duration
        self._order_name = order_name
        self._order_length = order_duration
        self._heated = False
        self.__set_order_state()

    def get_order_index(self) -> int:
        return self._order_index

    def get_order_duration(self) -> int:
        return self._order_duration

    def get_order_length(self) -> int:
        return self._order_length

    def get_order_name(self) -> str:
        return self._order_name

    def get_order_state(self) -> str:
        return self._order_state

    def __set_order_state(self) -> None:
        if not self._heated:
            self._order_state = "new"
        elif self._heated and self._order_duration == self._order_length:
            self._order_state = "heat"
        elif self._heated and 0 < self._order_duration < self._order_length:
            self._order_state = "work"
        elif self._heated and self._order_duration == 0:
            self._order_state = "done"
        else:
            self._order_state = "UNEXPECTED"

    def process_order(self, order_process_time: int) -> None:
        if self._heated:
            self._order_duration = max(0, self._order_duration - order_process_time)
        else:
            self._heated = True
        self.__set_order_state()

    def __repr__(self):
        return f"Order({self._order_index}: {self._order_duration}, heated={self._heated})"

    def __str__(self):
        return f"{self._order_name} -> {self._order_duration if self._order_duration != 0 else 'done'}"