
from typing import Dict, List
from pandas import read_excel, DataFrame

# excel column names
# i want them as constants

ORDERSIZE = "OrderSize"
MATRIXNAME = "MatrixName"


class OrdersReader:
    def __init__(self, filename: str):
        self.orders:DataFrame = read_excel(filename)

    def get_orders_number(self) -> int:
        return self.orders.shape[0]
    
    def get_orders_indexes(self) -> List[int]:
        return list(self.orders.index.values)

    def get_orders_duration(self) -> Dict[int, int]:
        return self.orders["OrderSize"].to_dict()

    def get_matricies_names(self) -> Dict[int, str]:
        return self.orders[MATRIXNAME].to_dict()