from pandas import ExcelWriter
from pandas import DataFrame
from pulp.pulp import value

from .lin_prog_maker import LinProgMaker


class DataWriter:
    def __init__(self, task: LinProgMaker, out_file: str):
        self.writer = ExcelWriter(out_file, engine="xlsxwriter")
        self.task = task

    def save_work(self) -> DataFrame:
        cols = [
            "TimeStep",
            "StartTime",
            "Slot",
            "Order",
            "Duration",
            "WorkTime",
            "IdleTime",
            "s",
            "a"
        ]
        result = DataFrame(columns=cols)
        row_number = 0
        for k in self.task.time_intervals:
            for j in self.task.slots:
                for i in self.task.orders:
                    if self.task.a[i, j, k].value() == 0:
                        continue
                    result.loc[row_number, cols] = (
                        k,
                        self.task.Ts[k].value(),
                        j,
                        i,
                        self.task.durations[i],
                        self.task.t[i, j, k].value(),
                        max([self.task.x[i1, j, k].value() for i1 in self.task.orders]),
                        self.task.s[i, j, k].value(),
                        self.task.a[i, j, k].value(),
                    )
                    row_number += 1
        # add last time point - actually the right way to call it is "StopTime"
        k = self.task.last_time_step
        result.loc[row_number, ["TimeStep", "StartTime"]] = k, self.task.Ts[k].value()
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

    def print_additional_info(self) -> None:
        print(f"Task status = {self.task.status}")
        print(f"Objective value = {self.task.objective_value}")
