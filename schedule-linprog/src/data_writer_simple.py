from pandas import ExcelWriter
from pandas import DataFrame
from pulp.pulp import value

#from .lin_prog_maker import LinProgMaker

class DataWriter:
    def __init__(self, task, out_file: str):
        self.writer = ExcelWriter(out_file, engine="xlsxwriter")
        self.task = task

    def save_work(self) -> DataFrame:
        cols = [
            "TimeStep",
            "Slot",
            "Order",
            "Duration",
            "StepStartTime",
            "y",
        ]
        result = DataFrame(columns=cols)
        row_number = 0
        step_start_time = 0
        for k in self.task.time_intervals:
            for j in self.task.slots:
                for i in self.task.orders:
                    if self.task.y[i, j, k].value() == 0:
                        pass#continue
                    result.loc[row_number, cols] = (
                        k,
                        j,
                        i,
                        self.task.durations[i],
                        self.task.x[k].value(),
                        self.task.y[i, j, k].value(),
                    )
                    row_number += 1
            step_start_time += k * (self.task.Tchange + self.task.Theat) + self.task.x[k].value()
        # add last time point - or better "StopTime"
        #k = self.task.last_time_step
        #result.loc[row_number, ["TimeStep", "StepStartTime"]] = k, self.task.Ts[k].value()
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
        print(f"Orders duration = {self.task.durations}")
