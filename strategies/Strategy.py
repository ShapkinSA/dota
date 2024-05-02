"""
    Отыгрыш дифицита без учёта отыгрываемой части дифицита в лайве
"""
from abc import abstractmethod

from console.ConsoleViewer import ConsoleViewer
from logs.CustomLogger import CustomLogger
from strategies.StrategyStatistic import StrategyStatistic


class Strategy:

    def __init__(self,strategy_cfg):
        StrategyStatistic.balance = float(strategy_cfg['balance_start'])
        StrategyStatistic.balance_need = float(strategy_cfg['balance_need'])
        self.logger = CustomLogger().getLogger(type(self).__name__)
        self.matches = dict()


    def predictMap(self, matchToPredict):
        match, additionalInfo = self.predictByStrategy(matchToPredict)

        #Если прогноз есть
        if(additionalInfo==None):
            return None

        # Вывод информации на консоль
        # ConsoleViewer.showPrediction(self, matchToPredict.showInfoWithCoeffs() + "\n" + additionalInfo)
        ConsoleViewer.showPrediction(self, "\n" + additionalInfo)

        # Фиксируем статистику стратегии
        if("Прогноз П1" in additionalInfo):
            StrategyStatistic.onPredict(match.bet_1)
        else:
            StrategyStatistic.onPredict(match.bet_2)

        return match

    def resultMap(self, match, old_match):
        current_score_1 = int(match.current_map_score.split(":")[0])
        prev_score_1 = int(old_match.current_map_score.split(":")[0])

        matchWithCoeffs = self.matches[match.__str__()]

        win_side = -1
        if(current_score_1>prev_score_1):
            # П1
            win_side = 0
        else:
            # П2
            win_side = 1

        # П1
        if(matchWithCoeffs.bet_1!=0):

            flag = -1
            if(win_side==0):
                flag = True
            else:
                flag = False

            # Подсчёт результата игры
            additionalInfo = self.resultByStrategy(self, flag, matchWithCoeffs.coef_1, matchWithCoeffs.bet_1)

            # Вывод информации на консоль
            ConsoleViewer.showResult(matchWithCoeffs, flag, additionalInfo)

            # Фиксируем статистику стратегии
            needBalanceDone = StrategyStatistic.onResult(flag, matchWithCoeffs.coef_1, matchWithCoeffs.bet_1)

            # Вывод информации о статистике стратегии
            ConsoleViewer.showStatistic()

        # П2
        if (matchWithCoeffs.bet_2 != 0):

            flag = -1
            if (win_side == 1):
                flag = True
            else:
                flag = False

            # Подсчёт результата игры
            additionalInfo = self.resultByStrategy(self, flag,  matchWithCoeffs.coef_2, matchWithCoeffs.bet_2)

            # Вывод информации на консоль
            ConsoleViewer.showResult(matchWithCoeffs, flag, additionalInfo)

            # Фиксируем статистику стратегии
            needBalanceDone = StrategyStatistic.onResult(flag, matchWithCoeffs.coef_2, matchWithCoeffs.bet_2)

            # Вывод информации о статистике стратегии
            ConsoleViewer.showStatistic()


    @abstractmethod
    def predictByStrategy(self, match):
        raise NotImplementedError("Must override predictByStrategy")



    @abstractmethod
    def resultByStrategy(self, matchToPredict, isWin, coeff, bet):
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

