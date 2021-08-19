from pandas import ExcelWriter
from pandas import DataFrame
from pulp.pulp import value

from . lin_prog_maker import LinProgMaker


class DataWriter:
    def __init__(self, task: LinProgMaker, out_file: str):
        self.writer = ExcelWriter(out_file, engine="xlsxwriter")
        self.task = task

    def save_work(self) -> DataFrame:
        cols = ["TimeStep", "Slot", "Order", "WorkTime"]
        result = DataFrame(columns=cols)
        row_number = 0
        for k in self.task.time_intervals:
            for j in self.task.slots:
                for i in self.task.orders:
                    if self.task.a[i, j, k].value() == 0:
                        continue
                    result.loc[row_number, cols] = k, j, i, self.task.t[i, j, k].value()
                    row_number += 1
        return result

    def save(self) -> None:
        try:
            self.save_work().to_excel(self.writer, sheet_name="Work", index=False)
            self.writer.save()
        except PermissionError:
            print("Close excel file!")
        self.writer.close()

    def write_lp_model(self, filename="model.lp") -> None:
        self.task.write(filename)
