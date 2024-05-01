"""
    Класс, осуществяющий мониторинг сайта конторы с определённой периодичностью, а так же перезапуск браузера
"""
import time
from apscheduler.schedulers.background import BackgroundScheduler
from logs.CustomLogger import CustomLogger
class Scheduler:

    def __init__(self,scheduler_cfg, monitor):
        self.scheduler_cfg = scheduler_cfg
        self.monitor = monitor
        self.monitor_refresh_time = float(scheduler_cfg["monitor_refresh_time"])
        self.browser_refresh_time = float(scheduler_cfg["browser_refresh_time"])
        self.logger = CustomLogger().getLogger(type(self).__name__)
        self.logger.info(f"Время периодического опроса сайта {self.monitor_refresh_time} сек")
        self.logger.info(f"Время замены браузера {self.browser_refresh_time} сек")


    def startMonitoring(self):
        # Мониторинг игр
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.monitor.searchingTheGame, 'interval', id="monitor", seconds=self.monitor_refresh_time)
        # self.scheduler.add_job(self.monitor.checkBrowserState, 'interval', id="browser_scheduler", seconds=self.browser_refresh_time)

        # Запоминаем scheduler для вызова мониторинга
        self.monitor.setScheduler(self.scheduler)
        self.scheduler.start()
        try:
            while True:
                time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown()