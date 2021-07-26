
TCHANGE = 20
THEAT = 40

class Press:
    def __init__(self, orders:list):
        self.orders = orders
        self.total_work_time = 0
        self.slots = []
    
    def process_single_slot(self):
        pass

    def process_single_step(self):
        # find slot first finish

        # decrease all orders by delta

        # change matrix

        # start work
        #  --heat slot
        #  --others others work according policy till end of heating
        #  --heating over
        #  --continue normal work or change matrix 


        print("process")
        for slot in self.slots:
            self.process_single_slot()

    def put_order_to_slot(self, slot):
        pass


    def run(self):
        while self.orders:
            self.process_single_step()