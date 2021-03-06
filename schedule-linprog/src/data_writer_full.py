from pandas import ExcelWriter
from pandas import DataFrame
from pulp.pulp import value

from .lin_prog_maker_full import LinProgMaker


class DataWriter:
    def __init__(self, task: LinProgMaker, out_file: str):
        self.writer = ExcelWriter(out_file, engine="xlsxwriter")
        self.task = task

    def save_work(self) -> DataFrame:
        cols = [
            "TimeStep",
            "Slot",
            "Order",
            "Duration",
            "TimeStepStartTime",
            "TimeStepLength",
            "OrderProcessingTime",
            "IdleTime",
            "s",
            "a",
        ]
        result = DataFrame(columns=cols)
        row_number = 0
        ts = 0
        for k in self.task.time_intervals:
            for j in self.task.slots:
                for i in self.task.orders:
                    if self.task.a[i, j, k].value() == 0:
                        pass#continue
                    result.loc[row_number, cols] = (
                        k,
                        j,
                        i,
                        self.task.durations[i],
                        ts,
                        self.task.L[k].value(),
                        self.task.t[i, j, k].value(),
                        #self.task.L[k].value() - self.task.t[i, j, k].value() - self.task.Theat - self.task.Tchange,
                        self.task.x[j, k].value(),
                        self.task.s[i, j, k].value(),
                        self.task.a[i, j, k].value(),
                    )
                    row_number += 1
            ts += self.task.L[k].value()
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
        print(f"Objective value = {self.task.objective_value}\n\n")
        print("Parameters used:")
        print(f"Number of time steps = {self.task.time_steps}")
        #print(f"Minimal work time = {self.task.min_working_time}")
        print(f"Orders duration = {self.task.durations}")
        # print("Linear program configuration:")
        # for section in self.task.config.sections():
        #     print(f"[{section}]")
        #     for par, val in self.task.config[section].items():
        #         print(f"\t{par} = {val}")
