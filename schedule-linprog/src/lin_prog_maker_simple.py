import pulp as plp

from .data_processor import DataProcessor


class LinProgMaker:
    """Solves simplified task when time between matrix changes is max duration of one of the orders.
    """

    def __init__(self, processor: DataProcessor):

        self.init_const(processor)

        self.prob = plp.LpProblem("ProdSchedule", plp.LpMinimize)

        self.init_decision_variables()

    def solve(self) -> None:
        self.obective()

        self.ct_any_order_starts_once()
        self.ct_one_order_per_slot_at_one_step()
        self.ct_time_step_less_than_max_duration()

        self.prob.solve(
            plp.PULP_CBC_CMD(
                msg=True,
                #gapRel=0.05,
                # timeLimit=200,
            )
        )

        self.status = plp.LpStatus[self.prob.status]
        self.objective_value = plp.value(self.prob.objective)

    def init_const(self, processor: DataProcessor) -> None:
        self.orders = processor.get_orders()
        self.slots = processor.get_slots()
        self.time_intervals = range(1, processor.get_min_number_interval() + 1)
        self.durations = processor.get_durations()
        self.Tchange = processor.get_changing_time()
        self.Theat = processor.get_heating_time()

    def init_decision_variables(self) -> None:
        self.x = plp.LpVariable.dicts(
            "X", [k for k in self.time_intervals], cat=plp.LpInteger, lowBound=0
        )
        self.y = plp.LpVariable.dicts(
            "y",
            [
                (i, j, k)
                for i in self.orders
                for j in self.slots
                for k in self.time_intervals
            ],
            cat=plp.LpBinary,
        )

    def obective(self) -> None:
        self.prob += plp.lpSum(
            self.Tchange + self.Theat + self.x[k] for k in self.time_intervals
        )

    def ct_any_order_starts_once(self) -> None:
        for i in self.orders:
            self.prob += (
                plp.lpSum(
                    self.y[i, j, k] for j in self.slots for k in self.time_intervals
                )
                == 1,
                f"single start {i}",
            )
    
    def ct_one_order_per_slot_at_one_step(self):
        for j in self.slots:
            for k in self.time_intervals:
                self.prob += plp.lpSum(self.y[i, j, k] for i in self.orders) <= 1

    def ct_time_step_less_than_max_duration(self) -> None:
        for j in self.slots:
            for k in self.time_intervals:
                self.prob += (
                    plp.lpSum(self.y[i, j, k] * self.durations[i] for i in self.orders)
                    <= self.x[k]
                )

    def write(self, filename: str = "model.lp") -> None:
        self.prob.writeLP(filename)
