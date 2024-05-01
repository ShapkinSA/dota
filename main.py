# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import subprocess
import sys

from cfg.WorkingWithCfg import WorkingWithCfg
from logs.CustomLogger import CustomLogger
from reflection.Reflection import Reflection
from scheduler.Scheduler import Scheduler


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # sys.tracebacklimit = 0

    # subprocess.call("TASKKILL /f  /IM  CHROMEDRIVER.EXE")

    logger = CustomLogger().getLogger("main")

    scheduler_cfg, monitoring_cfg, strategy_cfg, = WorkingWithCfg.parsing_xml("cfg.xml")

    #Создаём статегию
    strategy = Reflection.get_class("strategies."+strategy_cfg["name"]+".py", strategy_cfg)

    monitor = Reflection.get_class("monitoring.MarathonBet.py", monitoring_cfg, strategy)

    scheduler = Scheduler(scheduler_cfg, monitor)
    scheduler.startMonitoring()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
