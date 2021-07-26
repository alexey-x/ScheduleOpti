class Slot:
    def __int__(self):
        self.heating = None
        self.changing = None
        self.working = None

    def is_heating(self) -> bool:
        return self.heating

    def is_changing(self) -> bool:
        return self.changing

    def is_working(self) -> bool:
        return self.working

    def can_change_matrix(self) -> bool:
        return not self.heating

    def start_work(self):
        self.working = True
        self.changing = False
        self.heating = False

    def start_change(self):
        self.working = False
        self.changing = True
        self.heating = False

    def start_heat(self):
        self.working = False
        self.changing = False
        self.heating = True