"""
    Отыгрыш дифицита без учёта отыгрываемой части дифицита в лайве
"""

from logs.CustomLogger import CustomLogger
from strategies.Strategy import Strategy


class ComebackOne(Strategy):

    def createObjByArgs(args):
        return ComebackOne(args[0])

    def __init__(self, strategy_cfg):
        super(ComebackOne, self).__init__(strategy_cfg)
        self.logger.info(f"Стратегия DeficitOne")
        self.logger.info(f"Стартовый баланс {strategy_cfg['balance_start']}")
        self.logger.info(f"Требуемый баланс {strategy_cfg['balance_need']}")
        self.logger.info(f"Сумма ставки {strategy_cfg['baseBet']}")
        self.logger.info(f"Минимальные коэффициент для совершение ставки {strategy_cfg['minCoeff']}")
        # self.logger.info(f"Минимальный дефицит для запуска {strategy_cfg['minDeficit']}")
        # self.logger.info(f"Коэффициент отыгрывания дефицита с одной игры {strategy_cfg['deficitCoef']}")
        # self.logger.info(f"Минимальный коэффициент события для отыгрывания дефицита {strategy_cfg['gameCoefMin']}")

        self.deficit = 0
        self.matches = dict()
        self.baseBets = dict()

        self.balance_start = float(strategy_cfg['balance_start'])
        self.balance_need = float(strategy_cfg['balance_need'])
        self.baseBet = float(strategy_cfg['baseBet'])
        self.minCoeff = float(strategy_cfg['minCoeff'])
        # self.deficitCoef = float(strategy_cfg['deficitCoef'])
        # self.gameCoefMin = float(strategy_cfg['gameCoefMin'])

    def predictByStrategy(self, matchToPredict):

        # Только при равном счёте в текущей карте
        if (matchToPredict.map_score != "0:0"):
            return matchToPredict, None

        if (matchToPredict.coef_1 > self.minCoeff):
            # Фиксируем игру на П1
            if (self.matches.get(matchToPredict.__str__()) == None):
                self.matches[matchToPredict.__str__()] = matchToPredict
            if (self.matches[matchToPredict.__str__()].bet_1 == 0):
                self.matches[matchToPredict.__str__()].bet_1 = self.baseBet
                return matchToPredict, f"{matchToPredict.showInfoWithCoeffs()}\nПроноз: П1. Сумма ставки {self.baseBet}"

        if (matchToPredict.coef_2 > self.minCoeff):
            # Фиксируем игру на П2
            if (self.matches.get(matchToPredict.__str__()) == None):
                self.matches[matchToPredict.__str__()] = matchToPredict
            if (self.matches[matchToPredict.__str__()].bet_2 == 0):
                self.matches[matchToPredict.__str__()].bet_2 = self.baseBet
                return matchToPredict, f"{matchToPredict.showInfoWithCoeffs()}\nПроноз: П2. Сумма ставки {self.baseBet}"

        return matchToPredict, None

    def resultByStrategy(self, matchToPredict, isWin):
        if (isWin):
            return f"Сумма ставки {matchToPredict.bet}\nПрибыль с данной ставки {self.baseBets[matchToPredict.__str__()].bet * (matchToPredict.prediction_coef - 1)}"
        else:
            return f"Сумма ставки {matchToPredict.bet}\nОбщий дефицит {self.deficit}"

    # Обработка внезапного исчезновения игры
    # def isDisappearedGame(self,matchToPredict):
    #     self.logger.error(f"Увеличиваем дефицит на ставку исчезнувшей игры")
    #     self.deficit += matchToPredict.bet
