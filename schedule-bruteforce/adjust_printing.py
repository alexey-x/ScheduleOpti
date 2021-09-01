from copy import deepcopy

from src.press_working_strategy import DoShortOrderAndStopStrategy
from src.press_working_strategy import CheckNextOrderBeforeStopStrategy
from src.press_working_strategy import DoLongestOrderStrategy


from src.order import Order
from src.press import Press, THEAT

def main():
    orders = [
        Order(0, 734, "Орион - 600"),
        Order(1, 722, "Орион - 700"),
        Order(8, 42, "Сатурн ПГ: 42"),
        Order(2, 1622, "Орион - 800"),
        Order(3, 218, "Весна - 600"),
        Order(5, 820, "Весна  - 800"),
        Order(4, 350, "Весна  - 700"),
        Order(6, 292, "Сафари"),
        Order(9, 584, "Сатурн ПО"),
        Order(7, 352, "Сафари 2"),
        Order(10, 374, "Соло"),
        Order(11, 30, "Арабеска ПО 800"),
        Order(12, 38, "Октава"),
    ]

    #press_work_strategy = DoShortOrderAndStopStrategy()
    #press_work_strategy = DoLongestOrderStrategy()
    press_work_strategy = CheckNextOrderBeforeStopStrategy(THEAT)
    press = Press(press_work_strategy, verbose=True)
    press.run(deepcopy(orders))
    #out_excel_file = "../result/test_press_out.xlsx"
    #press.result.to_excel(out_excel_file, sheet_name="WorkProcess", index=False)


if __name__ == "__main__":
    main()