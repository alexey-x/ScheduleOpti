import pulp as plp

from data_processor import DataProcessor


class LinProgMaker:
    def __init__(self, processor: DataProcessor):
        self.init_const(processor)

        self.prob = plp.LpProblem("ProdSchedule", plp.LpMinimize)

        self.init_decision_variables()

    def solve(self) -> None:
        self.obective()

        self.prob.solve(plp.PULP_CBC_CMD(msg=True))

        self.status = plp.LpStatus[self.prob.status]
        self.objective_value = plp.value(self.prob.objective)

    def init_const(self, processor: DataProcessor) -> None:
        self.orders = processor.get_orders()
        self.slots = processor.get_slots()
        self.time_steps = processor.get_time_steps()
        self.time_intervals = processor.get_time_intervals()
        self.last_time_step = processor.get_last_time_step()
        self.durations = processor.get_durations()
        self.Tchange = processor.get_changing_time()
        self.Theat = processor.get_heating_time()

    def init_decision_variables(self) -> None:
        self.Ts = plp.LpVariable.dicts(
            "Ts", [k for k in self.time_steps], cat=plp.LpContinuous,
        )

        self.s = plp.LpVariable.dicts(
            "s",
            [
                (i, j, k)
                for i in self.orders
                for j in self.slots
                for k in self.time_intervals
            ],
            cat=plp.LpBinary,
        )

        self.a = plp.LpVariable.dicts(
            "a",
            [
                (i, j, k)
                for i in self.orders
                for j in self.slots
                for k in self.time_intervals
            ],
            cat=plp.LpBinary,
        )

        self.t = plp.LpVariable.dicts(
            "t",
            [
                (i, j, k)
                for i in self.orders
                for j in self.slots
                for k in self.time_intervals
            ],
            cat=plp.LpContinuous,
        )

        self.x = plp.LpVariable.dicts(
            "x",
            [
                (i, j, k)
                for i in self.orders
                for j in self.slots
                for k in self.time_intervals
            ],
            cat=plp.LpContinuous,
        )        

    def obective(self) -> None:
        self.prob +=  self.Ts[self.last_time_step]

    def ct_start_at_time_zero(self) -> None:
        pass
