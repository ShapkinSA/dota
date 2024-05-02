from logs.CustomLogger import CustomLogger
class StrategyStatistic:

    balance = 0
    balance_need = 0
    scheduler = None

    sumLive = 0
    margin = 0

    max_bet_win = 0
    max_bet_lose = 0

    win = 0
    lose = 0
    all = 0

    #Фиксируем наибольшую серию побед и поражений
    lose_streak_counter = 0
    win_streak_counter = 0

    lose_streak_counter_max = 0
    win_streak_counter_max = 0

    @staticmethod
    def onPredict(bet):
        #Увеличиваем сумму денег в лайве
        StrategyStatistic.sumLive += bet

        #Уменьшаем баланс
        StrategyStatistic.balance -= bet

    @staticmethod
    def onResult(isWin, coeff, bet):
        #Убираем сумму денег из лайва
        StrategyStatistic.sumLive -= bet

        if(isWin):
            #Фиксируем победу
            StrategyStatistic.win += 1

            #Начинаем или продолжаем серию побед
            StrategyStatistic.win_streak_counter += 1

            #Сбрасываем счётчик поражений
            StrategyStatistic.lose_streak_counter = 0

            #Прирост баланса
            StrategyStatistic.balance += bet * coeff

            #Прибыль с каждой ставки
            StrategyStatistic.margin += bet * (coeff-1)

            # Фиксация самой большой выиграной ставки
            if (bet > StrategyStatistic.max_bet_win):
                StrategyStatistic.max_bet_win = bet


        else:
            #Фиксируем покажение
            StrategyStatistic.lose += 1

            #Начинаем или продолжаем серию побед
            StrategyStatistic.lose_streak_counter += 1

            #Сбрасываем счётчик побед
            StrategyStatistic.win_streak_counter = 0

            #Фиксируем прибыль на данной ставке
            StrategyStatistic.margin -= bet


            # Фиксация самой большой выиграной ставки
            if (bet > StrategyStatistic.max_bet_lose):
                StrategyStatistic.max_bet_lose = bet


        #Фиксируем окончание игры
        StrategyStatistic.all += 1

        #Пересчитываем счётчики для серии побед и поражений
        if(StrategyStatistic.win_streak_counter > StrategyStatistic.win_streak_counter_max):
            StrategyStatistic.win_streak_counter_max = StrategyStatistic.win_streak_counter

        if (StrategyStatistic.lose_streak_counter > StrategyStatistic.lose_streak_counter_max):
            StrategyStatistic.lose_streak_counter_max = StrategyStatistic.lose_streak_counter
