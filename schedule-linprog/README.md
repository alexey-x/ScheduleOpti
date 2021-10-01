# Purpose

Linear programming approach to the task.

Try

```
python ScheduleLinProg.py --help

Usage: ScheduleLinProg.py [OPTIONS]

Options:
  --num-orders INTEGER            Number of orders to consider.
  --num-time-interval INTEGER     Number of work time intervals.
  --strategy [simple-task|full-task]
                                  Defines what kind of lin. programming task
                                  to solve.  [required]
  --help                          Show this message and exit.

```

There are two strategies "simple-task" and "full-task".

The "simple-task" is the linear programming task where the orders once put into the press 
will be there untill the longest one is finished. It is kind of benchmark. The result coincides
with the brute-force approch for the "do-long-order" strategy.

The "full-task" is the linear programming task where the order can be processed over
several time intervals. Currently the performance is worse than for brute-forces approach
for "do-short-order" and "chk-next-order" strategies.

--num-orders - If None consider all orders from the file.

--num-time-interval - Applicable only "full-task". Igonored for "simple-task".