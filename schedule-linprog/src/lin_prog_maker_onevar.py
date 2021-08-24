import pulp as plp

from .data_processor import DataProcessor


class LinProgMaker:
    def __init__(self, processor: DataProcessor):
        self.init_const(processor)

        self.prob = plp.LpProblem("ProdSchedule", plp.LpMinimize)

        self.init_decision_variables()

    def solve(self) -> None:
        self.obective()

        self.ct_any_order_starts_once()
        # self.ct_first_change_and_heat() it seems wrong
        self.ct_time_between_steps()
        self.ct_orders_duration()
        self.ct_start_order()
        self.ct_order_duration_in_time_interval()
        self.ct_process_order_in_one_slot()
        self.ct_one_order_per_slot()
        self.ct_same_slot_for_consecutive_steps()

        self.prob.solve(plp.PULP_CBC_CMD(msg=True, fracGap=0.005))

        self.status = plp.LpStatus[self.prob.status]
        self.objective_value = plp.value(self.prob.objective)

    def init_const(self, processor: DataProcessor) -> None:
        self.orders = processor.get_orders()
        self.slots = processor.get_slots()
        self.time_steps = processor.get_time_steps()
        self.last_time_step = self.time_steps[-1]

        self.time_intervals = self.time_steps[:-1]
        self.time_intervals_exclude_last = self.time_intervals[:-1]

        self.durations = processor.get_durations()
        self.Tchange = processor.get_changing_time()
        self.Theat = processor.get_heating_time()

        self.minDuration = min([i for i in self.durations.values()])
        self.min_working_time = processor.get_min_working_time()

    def init_decision_variables(self) -> None:
        self.Ts = plp.LpVariable.dicts(
            "Ts", [k for k in self.time_steps], cat=plp.LpInteger, lowBound=0
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
            cat=plp.LpInteger,
            lowBound=0,
        )

        self.x = plp.LpVariable.dicts(
            "x",
            [(j, k) for j in self.slots for k in self.time_intervals],
            cat=plp.LpInteger,
            lowBound=0,
        )

    def obective(self) -> None:
        self.prob += self.Ts[self.last_time_step]

    def ct_any_order_starts_once(self) -> None:
        for i in self.orders:
            self.prob += (
                plp.lpSum(
                    self.s[i, j, k] for j in self.slots for k in self.time_intervals
                )
                == 1
            )

    def ct_first_change_and_heat(self):
        for i in self.orders:
            for j in self.slots:
                for k1 in self.time_intervals:
                    for k2 in self.time_intervals:
                        if k2 > k1:
                            self.prob += self.s[i, j, k1] >= self.s[i, j, k2]

    def ct_time_between_steps(self) -> None:
        self.prob += self.Ts[1] == 0
        self.prob += self.Ts[self.last_time_step] >= self.min_working_time
        for j in self.slots:
            for k in self.time_intervals:
                self.prob += (
                    self.Ts[k + 1] - self.Ts[k]
                    == plp.lpSum(
                        self.Tchange * self.a[i, j, k]
                        + self.Theat * self.s[i, j, k]
                        + self.t[i, j, k]
                        for i in self.orders
                    )
                    + self.x[j, k]
                )

    def ct_orders_duration(self) -> None:
        for i in self.orders:
            self.prob += (
                plp.lpSum(
                    self.t[i, j, k] for j in self.slots for k in self.time_intervals
                )
                == self.durations[i]
            )

    def ct_start_order(self) -> None:
        for i in self.orders:
            for j in self.slots:
                for k in self.time_intervals:
                    self.prob += self.a[i, j, k] >= self.s[i, j, k]

    def ct_order_duration_in_time_interval(self) -> None:
        for i in self.orders:
            for j in self.slots:
                for k in self.time_intervals:
                    self.prob += self.t[i, j, k] <= self.durations[i] * self.a[i, j, k]

    def ct_process_order_in_one_slot(self) -> None:
        for i in self.orders:
            for k in self.time_intervals:
                self.prob += plp.lpSum(self.a[i, j, k] for j in self.slots) <= 1

    def ct_one_order_per_slot(self):
        for j in self.slots:
            for k in self.time_intervals:
                self.prob += plp.lpSum(self.a[i, j, k] for i in self.orders) <= 1

    def ct_same_slot_for_consecutive_steps(self) -> None:
        for i in self.orders:
            for k in self.time_intervals_exclude_last:
                for j1 in self.slots:
                    for j2 in self.slots:
                        if j1 == j2:
                            continue
                        self.prob += self.a[i, j1, k] + self.a[i, j2, k + 1] <= 1

    def write(self, filename: str = "model.lp") -> None:
        self.prob.writeLP(filename)
