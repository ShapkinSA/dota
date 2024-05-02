"""
    Вывод информации об игре в лайве + текущей статистики алгоритма
"""
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
    def showStatistic(strategyStatistic):
        print(f"\nОбщее число игр {strategyStatistic.all}"
              f"\nУгаданных исходов {strategyStatistic.win}"
              f"\nПроигранных исходов {strategyStatistic.lose}"
              f"\nКПД стратегии {strategyStatistic.win/(strategyStatistic.win+strategyStatistic.lose)*100.0}"
              f"\nТекущий баланс {strategyStatistic.balance}"
              f"\nСуммарно в лайве {strategyStatistic.sumLive}"
              f"\nСуммарно прибыль со всех ставок {strategyStatistic.margin}"
              f"\nНаибольшая проигранная ставка {strategyStatistic.max_bet_lose}"
              f"\nНаибольшая выигранная ставка {strategyStatistic.max_bet_win}"              
              f"\nМаксимальная длительность серии побед {strategyStatistic.win_streak_counter_max}"
              f"\nМаксимальная длительность серии поражений {strategyStatistic.lose_streak_counter_max}"
              )