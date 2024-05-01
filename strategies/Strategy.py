"""
    Отыгрыш дифицита без учёта отыгрываемой части дифицита в лайве
"""
from abc import abstractmethod

from console.ConsoleViewer import ConsoleViewer
from logs.CustomLogger import CustomLogger
from strategies.StrategyStatistic import StrategyStatistic


class Strategy:

    def __init__(self,strategy_cfg):
        self.strategyStatistic = StrategyStatistic(float(strategy_cfg['balance_start']), float(strategy_cfg['balance_need']))
        self.logger = CustomLogger().getLogger(type(self).__name__)


    def predictMap(self, matchToPredict):
        matchToPredict, additionalInfo = self.predictByStrategy(matchToPredict)

        #Если прогноз есть
        if(additionalInfo==None):
            return False

        # Вывод информации на консоль
        # ConsoleViewer.showPrediction(self, matchToPredict.showInfoWithCoeffs() + "\n" + additionalInfo)
        ConsoleViewer.showPrediction(self, "\n" + additionalInfo)

        # Фиксируем статистику стратегии
        if("П1" in additionalInfo):
            self.strategyStatistic.onPredict(matchToPredict.bet_1)
        else:
            self.strategyStatistic.onPredict(matchToPredict.bet_2)
        return True

    def resultMap(self, match, old_match):
        current_score_1 = int(match.map_score.split(":")[0])
        prev_score_1 = int(old_match.map_score.split(":")[0])

        win_side = -1
        if(current_score_1>prev_score_1):
            # П1
            win_side = 0
        else:
            # П2
            win_side = 1

        # П1
        if(match.bet_1!=0):

            flag = -1
            if(win_side==0):
                flag = True
            else:
                flag = False

            # Подсчёт результата игры
            additionalInfo = self.resultByStrategy(self, flag)

            # Вывод информации на консоль
            ConsoleViewer.showResult(self, flag, additionalInfo)

            # Фиксируем статистику стратегии
            needBalanceDone = self.strategyStatistic.onResult(self, True)

            # Вывод информации о статистике стратегии
            ConsoleViewer.showStatistic(self.strategyStatistic)

        # П2
        if (match.bet_2 != 0):

            flag = -1
            if (win_side == 1):
                flag = True
            else:
                flag = False

            # Подсчёт результата игры
            additionalInfo = self.resultByStrategy(self, flag)

            # Вывод информации на консоль
            ConsoleViewer.showResult(self, flag, additionalInfo)

            # Фиксируем статистику стратегии
            needBalanceDone = self.strategyStatistic.onResult(self, True)

            # Вывод информации о статистике стратегии
            ConsoleViewer.showStatistic(self.strategyStatistic)


    @abstractmethod
    def predictByStrategy(self, matchToPredict):
        raise NotImplementedError("Must override predictByStrategy")



    @abstractmethod
    def resultByStrategy(self, matchToPredict, isWin):
        raise NotImplementedError("Must override predictByStrategy")

    # def resultByStrategy(self, matchToPredict, isWin):
    #
    #     if (isWin):
    #         # Отыгрывают дефицит специальные ставки
    #         if (self.deficitBets.get(matchToPredict.__str__())!=None):
    #             self.deficit -= self.deficitBets[matchToPredict.__str__()].bet * (matchToPredict.prediction_coef - 1)
    #             if(self.deficit<0):
    #                 self.deficit = 0
    #             return f"Сумма ставки {matchToPredict.bet}\nСумма отыгрыша {self.deficitBets[matchToPredict.__str__()].bet * (matchToPredict.prediction_coef - 1)}\nОбщий дефицит {self.deficit}"
    #         else:
    #             return f"Сумма ставки {matchToPredict.bet}\nПрибыль с данной ставки {self.baseBets[matchToPredict.__str__()].bet * (matchToPredict.prediction_coef - 1)}"
    #
    #     else:
    #         self.deficit += matchToPredict.bet
    #         return f"Сумма ставки {matchToPredict.bet}\nОбщий дефицит {self.deficit}"

