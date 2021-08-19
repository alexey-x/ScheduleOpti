import pandas as pd
from pulp.pulp import value

from . lin_prog_maker import LinProgMaker


class DataWriter:
    def __init__(self, task: LinProgMaker, out_file: str):
        self.writer = pd.ExcelWriter(out_file, engine="xlsxwriter")
        self.task = task

    def save_work(self) -> None:
        cols = ["TimeStep", "Slot", "Order", "WorkTime"]
        result = pd.DataFrame(columns=cols)
        row_number = 0
        for k in self.task.time_intervals:
            for j in self.task.slots:
                for i in self.task.orders:
                    if self.task.a[i, j, k].value() == 0:
                        continue
                    result.loc[row_number, cols] = k, j, i, self.task.t[i, j, k].value()
                    row_number += 1

    def save(self) -> None:

        self.save_work().to_excel(self.writer, sheet_name="Work", index=False)

        self.writer.save()
        self.writer.close()

    def write_lp_model(self, file_name="model.lp") -> None:
        self.task.write(file_name)
