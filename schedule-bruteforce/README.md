How to run

Try
```
python SchedulePrintDoor.py --help
```

Use DoShortOrderAndStopStrategy for the first 7 orders. 
```
python SchedulePrintDoor.py --strategy=do_short_order --num-orders=7
```

Use CheckNextOrderBeforeStopStrategy for the first 7 orders.
```
python SchedulePrintDoor.py --strategy=check_next_order --num-orders=7
```