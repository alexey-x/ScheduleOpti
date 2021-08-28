# Purpose

It is simulation of the work of printing doors press.

The idea is to generate all possible sequencies of input orders and select the one
with the shortest working time.

There are tree different strategies for selecting next order to process from
the input sequence of orders.

See detailes either in presentation folder (russian) or TaskDescription_EN jupyter notebook (english). 

## How to run

Try
```
python SchedulePrintDoor.py --help
```

The input file is in the data folder "orders.xlsx".


Use DoShortOrderAndStopStrategy for the first 7 orders. 
```
python SchedulePrintDoor.py --strategy=do-short-order --num-orders=7
```

The output will be the file "brute-do-short-order-7-orders.txt" in the result folder.


Use CheckNextOrderBeforeStopStrategy for the first 7 orders.
```
python SchedulePrintDoor.py --strategy=chk-next-order --num-orders=7
```

The output will be the file "brute-chk-next-order-7-orders.txt" in the result folder.