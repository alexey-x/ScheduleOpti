import pulp as plp
import configparser

from .data_processor import DataProcessor


CONFIGFILE = "config/config_lin_prog_maker.cfg"


class LinProgMaker:
    def __init__(self, processor: DataProcessor):
        self.config = configparser.ConfigParser()
        self.config.read(CONFIGFILE)

        self.init_const(processor)

        self.prob = plp.LpProblem("ProdSchedule", plp.LpMinimize)

        self.init_decision_variables()

    def solve(self) -> None:
        self.obective()

        for constrain, apply in self.config["constraints"].items():
            if apply:
                self.__getattribute__(constrain)()

        self.prob.solve(
            plp.PULP_CBC_CMD(
                msg=self.config["solver"]["msg"],
                gapRel=self.config["solver"]["gapRel"],
                timeLimit=self.config["solver"]["timeLimit"],
            )
        )

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

        self.t1 = plp.LpVariable.dicts(
            "t1",
            [
                (i, j, k)
                for i in self.orders
                for j in self.slots
                for k in self.time_intervals
            ],
            cat=plp.LpInteger,
            lowBound=0,
        )

        self.t2 = plp.LpVariable.dicts(
            "t2",
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
            [
                (i, j, k)
                for i in self.orders
                for j in self.slots
                for k in self.time_intervals
            ],
            cat=plp.LpInteger,
            lowBound=0,
        )

    def obective(self) -> None:
        self.prob += self.Ts[self.last_time_step]

    def ct_first_step(self) -> None:
        self.prob += self.Ts[1] == 0

    def ct_last_step(self) -> None:
        self.prob += self.Ts[self.last_time_step] >= self.min_working_time

    def ct_any_order_starts_once(self) -> None:
        for i in self.orders:
            self.prob += (
                plp.lpSum(
                    self.s[i, j, k] for j in self.slots for k in self.time_intervals
                )
                == 1,
                f"single start {i}",
            )

    def ct_connect_start_step_with_next_step(self) -> None:
        for i in self.orders:
            for j in self.slots:
                for k in self.time_intervals_exclude_last:
                    self.prob += (
                        self.s[i, j, k + 1] - self.s[i, j, k]
                        <= self.a[i, j, k + 1] - self.a[i, j, k]
                    )

    def ct_no_stops_if_started(self) -> None:
        """ \forall i, j, k_1, k_2: k_2 > k_1
        k_2\times a_{ijk_1} \ge k_1\times(a_{ijk_2} - s_{ijk_2})
        """
        for i in self.orders:
            for j in self.slots:
                for k1 in self.time_intervals:
                    for k2 in self.time_intervals:
                        if k2 > k1:
                            self.prob += k2 * self.a[i, j, k1] >= k1 * (
                                self.a[i, j, k2] - self.s[i, j, k2]
                            )

    def ct_time_between_steps(self) -> None:
        for i in self.orders:
            for j in self.slots:
                for k in self.time_intervals:
                    self.prob += (
                        (
                            self.Ts[k + 1] - self.Ts[k]
                            == self.Tchange * self.a[i, j, k]
                            + self.Theat * self.s[i, j, k]
                            + self.t2[i, j, k]
                            - self.t1[i, j, k]
                            + self.x[i, j, k]
                        ),
                        f"time-between {i}, {j}, {k}",
                    )
                    self.prob += self.t1[i, j, k] <= self.t2[i, j, k]

    def ct_start_time_inside_step(self) -> None:
        for i in self.orders:
            for j in self.slots:
                for k in self.time_intervals:
                    self.prob += (
                        self.t1[i, j, k]
                        >= self.Ts[k]
                        + self.Tchange * self.a[i, j, k]
                        + self.Theat * self.s[i, j, k],
                        f"t1-start {i}, {j}, {k}",
                    )

    def ct_orders_duration(self) -> None:
        for i in self.orders:
            self.prob += (
                plp.lpSum(
                    self.t2[i, j, k] - self.t1[i, j, k]
                    for j in self.slots
                    for k in self.time_intervals
                )
                == self.durations[i],
                f"duration {i}",
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
                    self.prob += (
                        self.t2[i, j, k] - self.t1[i, j, k]
                        <= self.durations[i] * self.a[i, j, k]
                    )

    def ct_process_order_in_one_slot(self) -> None:
        for i in self.orders:
            for k in self.time_intervals:
                self.prob += plp.lpSum(self.a[i, j, k] for j in self.slots) <= 1

    def ct_one_order_per_slot_at_one_step(self):
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
