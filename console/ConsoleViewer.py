"""
    Вывод информации об игре в лайве + текущей статистики алгоритма
"""
from strategies.StrategyStatistic import StrategyStatistic


class ConsoleViewer:

    @staticmethod
    def showPrediction(mathcToPredict, additionalInfo):
        print("\n")
        mathcToPredict.logger.info(additionalInfo)

        # baseString = "Найдена новая игра\n" + mathcToPredict.__str__() + "\n" + f'П1 : {mathcToPredict.dCoef1}   Н : {mathcToPredict.dCoefX}   П2 : {mathcToPredict.dCoef2} \n' + probabilities + '\n' + mathcToPredict.game_prediction + ' ' + str(mathcToPredict.prediction_coef)
        # if(additionalInfo!=None):
        #     mathcToPredict.logger.debug(f"{baseString}\nСумма ставки {betByStrategy}\n{additionalInfo}\n{game_status}")
        # else:
        #     mathcToPredict.logger.debug(f"{baseString}\nСумма ставки {betByStrategy}\n{game_status}")


    @staticmethod
    def showResult(matchToPredict, isWin, additionalInfo):

        print("\n")
        info = f'Карта завершёна\n{matchToPredict.showInfoWithCoeffs()}\n{additionalInfo}'

        if (isWin):
            matchToPredict.logger.info(f"{info}")
        else:
            matchToPredict.logger.warning(f"{info}")


    @staticmethod
    def showStatistic():
        print(f"\nОбщее число игр {StrategyStatistic.all}"
              f"\nУгаданных исходов {StrategyStatistic.win}"
              f"\nПроигранных исходов {StrategyStatistic.lose}"
              f"\nКПД стратегии {StrategyStatistic.win/(StrategyStatistic.win+StrategyStatistic.lose)*100.0}"
              f"\nТекущий баланс {StrategyStatistic.balance}"
              f"\nСуммарно в лайве {StrategyStatistic.sumLive}"
              f"\nСуммарно прибыль со всех ставок {StrategyStatistic.margin}"
              f"\nНаибольшая проигранная ставка {StrategyStatistic.max_bet_lose}"
              f"\nНаибольшая выигранная ставка {StrategyStatistic.max_bet_win}"              
              f"\nМаксимальная длительность серии побед {StrategyStatistic.win_streak_counter_max}"
              f"\nМаксимальная длительность серии поражений {StrategyStatistic.lose_streak_counter_max}"
              )