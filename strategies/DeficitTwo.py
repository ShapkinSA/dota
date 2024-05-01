"""
    Отыгрыш дифицита с учётом отыгрываемой части дифицита в лайве
"""
from logs.CustomLogger import CustomLogger
class DeficitTwo:

    def createObjByArgs(args):
        return DeficitTwo(args[0])


    def __init__(self, strategy_cfg):
        self.logger = CustomLogger().getLogger(type(self).__name__)
        self.logger.info(f"Стратегия DeficitOne")
        self.logger.info(f"Стартовый баланс {strategy_cfg['balance_start']}")
        self.logger.info(f"Требуемый баланс {strategy_cfg['balance_need']}")
        self.logger.info(f"Сумма ставки {strategy_cfg['baseBet']}")
        self.logger.info(f"Минимальный дефицит для запуска {strategy_cfg['minDeficit']}")
        self.logger.info(f"Коэффициент отыгрывания дефицита с одной игры {strategy_cfg['deficitCoef']}")
        self.logger.info(f"Минимальный коэффициент события для отыгрывания дефицита {strategy_cfg['gameCoefMin']}")

        self.deficit = 0
        self.deficit_live = 0
        self.deficitBets = dict()
        self.baseBets = dict()
        self.local_deficits = dict()

        self.balance_start = float(strategy_cfg['balance_start'])
        self.balance_need = float(strategy_cfg['balance_need'])
        self.baseBet = float(strategy_cfg['baseBet'])
        self.minDeficit = float(strategy_cfg['minDeficit'])
        self.deficitCoef = float(strategy_cfg['deficitCoef'])
        self.gameCoefMin = float(strategy_cfg['gameCoefMin'])


    def predictByStrategy (self, matchToPredict):

        if(self.deficit>self.minDeficit and matchToPredict.prediction_coef > self.gameCoefMin):

            # Фиксируем игру, на которой будет произведён отыгрыш
            self.deficitBets[matchToPredict.__str__()] = matchToPredict

            #Расчёт ставки исходя их суммарного долга
            localDeficit = self.deficit * self.deficitCoef

            #Расчёт ставки на данное событие с учётом коэффициента и объёма отыгрыша
            self.deficitBets[matchToPredict.__str__()].bet = localDeficit/(matchToPredict.prediction_coef-1)

            #Если расчитанная ставка меньше стандартной
            if(self.deficitBets[matchToPredict.__str__()].bet < self.baseBet ):
                self.deficitBets[matchToPredict.__str__()].bet = self.baseBet

                # Пересчёт отыгрыша с учётом базовой ставки
                localDeficit = self.deficitBets[matchToPredict.__str__()].bet * (matchToPredict.prediction_coef - 1)


            #Фиксируемт попытку отыграть дефицит (убираем этот дифицит из текущего дефицита)
            self.deficit_live += localDeficit

            #Убираем этот дифицит из текущего дефицита
            self.deficit -= localDeficit

            #Ставка на отыгрыш локального дифицита
            self.local_deficits[matchToPredict.__str__()] = localDeficit

            return self.deficitBets[matchToPredict.__str__()].bet, f"Попытка отыгрыша {localDeficit}\nСуммарно в лайве отыгрывается {self.deficit_live} при общем дефиците {  self.deficit + self.deficit_live   }"

        else:

            #Фиксируем игру, на которой не будет произведён отыгрыш
            self.baseBets[matchToPredict.__str__()] = matchToPredict

            self.baseBets[matchToPredict.__str__()].bet = self.baseBet

            #Базовая ставка
            return self.baseBet,  None


    def resultByStrategy (self, matchToPredict, isWin):

        if (isWin):

            # Отыгрывают дефицит специальные ставки
            if (self.deficitBets.get(matchToPredict.__str__())!=None):

                #Убираем дифицит из лайва и не возвращаем в общий
                self.deficit_live -= self.local_deficits[matchToPredict.__str__()]

                if(self.deficit_live<0):
                    self.deficit_live = 0

                #Сообщение для вывода информации
                message = f"Сумма ставки {self.deficitBets[matchToPredict.__str__()].bet}\nСумма отыгрыша {self.local_deficits[matchToPredict.__str__()]}\nОбщий дефицит {self.deficit + self.deficit_live}"

                #Удаление информации из словаря
                self.deficitBets.pop(matchToPredict.__str__())
                self.local_deficits.pop(matchToPredict.__str__())

                return message
            else:

                message = f"Сумма ставки {self.baseBet}\nПрибыль с данной ставки {self.baseBet * (self.baseBets[matchToPredict.__str__()].prediction_coef - 1)}"

                #Удаление информации из словаря
                self.baseBets.pop(matchToPredict.__str__())

                return message
        else:

            #Это была дефицитная ставка?
            if(self.deficitBets.get(matchToPredict.__str__())!=None):

                #Добавляется сразу ставка на данную игру и дефицит, который должен был отыграться (возвращаем из лайва)
                self.deficit += self.deficitBets[matchToPredict.__str__()].bet + self.local_deficits[matchToPredict.__str__()]

                #Убираем этот дифицит, который не смогли отыграть
                self.deficit_live -= self.local_deficits[matchToPredict.__str__()]

                message = f"Сумма ставки {self.deficitBets[matchToPredict.__str__()].bet}\nНеудачная попытка отыгрыша {self.local_deficits[matchToPredict.__str__()]} Общий дефицит {self.deficit}"

                #Удаление информации из словаря
                self.deficitBets.pop(matchToPredict.__str__())
                self.local_deficits.pop(matchToPredict.__str__())

                return message
            else:
                self.deficit += self.baseBets[matchToPredict.__str__()].bet

                message = f"Сумма ставки {self.baseBet}\nОбщий дефицит {self.deficit}"

                #Удаление информации из словаря
                self.baseBets.pop(matchToPredict.__str__())

                return message


    #Обработка внезапного исчезновения игры
    def isDisappearedGame(self,matchToPredict):

        #Проверка на исчезновение дефицитной ставки
        if(self.deficitBets.get(matchToPredict.__str__())!=None):
            self.logger.error(f"Увеличиваем дефицит на ставку дефицитной исчезнувшей игры")
            self.deficit += matchToPredict.bet
            self.deficit_live -= matchToPredict.bet

            #Удаляем игру из текущих
            self.deficitBets.pop(matchToPredict.__str__())
            return True

        # Проверка на исчезновение базовой ставки
        if (self.baseBets.get(matchToPredict.__str__()) != None):
            self.logger.error(f"Увеличиваем дефицит на ставку базовой исчезнувшей игры")
            self.deficit += matchToPredict.bet

            #Удаляем игру из текущих
            self.baseBets.pop(matchToPredict.__str__())
            return True

        #Данная игра уже отсутствует
        return False



