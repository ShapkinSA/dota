"""
    Основная модель данных
"""
from datetime import datetime

from bs4 import BeautifulSoup

from browser.Browser import Browser

class Match:

    def __init__(self, info, team_1, team_2, uri, logger, strategy):
        self.date_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.strategy = strategy
        self.info = info
        self.team_1 = team_1
        self.team_2 = team_2
        self.uri = uri
        self.logger = logger
        self.tick = 5
        self.uri = uri
        self.coef_1 = 0
        self.coef_2 = 0
        self.bet_1 = 0
        self.bet_2 = 0
        self.map_score = "10:10"
        self.map = 0


    def startBrowser(self):
        self.browser = Browser(self.uri)
        self.soup = BeautifulSoup(self.browser.browser.page_source, 'html.parser')

    def closeBrowser(self):
        self.browser.closeBrowser()

    def __str__(self):
        return f'{self.info}\n{self.team_1} - {self.team_2}'

    def showInfoWithCoeffs(self):
        return f'{self.info}\nКарта №{self.map}\nСчёт карты {self.map_score}\n{self.team_1} - {self.team_2}\nП1 {self.coef_1} : П2 {self.coef_2}\n{self.uri}'

    def parseDataFromSite(self):
        return True

    # @staticmethod
    # def getParametersLength():
    #     #4 - название игры (игроки и команды)
    #     return 4
    #
    # def getAllParametersVector(self, players, teams):
    #     if(players.get(self.player_1) == None or players.get(self.player_2) == None):
    #         return None
    #     return np.array([players[self.player_1], teams[self.team_1], players[self.player_2], teams[self.team_2]])
    #
    # def equalPlayerTeamWithSide(self, match):
    #     return (match.player_1 == self.player_1) and (match.player_2 == self.player_2) and (match.team_1 == self.team_1) and (match.team_2 == self.team_2)
    #
    # def equalPlayerTeamWithoutSide(self, match):
    #     return ((match.player_1 == self.player_1) and (match.player_2 == self.player_2) and (match.team_1 == self.team_1) and (match.team_2 == self.team_2)) \
    #            or \
    #            ((match.player_1 == self.player_2) and (match.player_1 == self.player_2) and (match.team_1 == self.team_2) and (match.team_1 == self.team_2))
    #
    # def equalsMatches(self,match):
    #     return self.date == match.date and self.date_datetime == match.date_datetime \
    #            and self.player_1 == match.player_1\
    #            and self.team_1 == match.team_1\
    #            and self.score_1 == match.score_1\
    #            and self.player_2 == match.player_2\
    #            and self.team_2 == match.team_2\
    #            and self.score_2 == match.score_2
    #
    # def getUniversalMatchName(self):
    #     if(self.player_1<self.player_2):
    #         return f'{self.player_1} ({self.team_1}) - ({self.team_2}) {self.player_2}'
    #     return f'{self.player_2} ({self.team_2}) - ({self.team_1}) {self.player_1}'
    #
    # def getMatchName(self):
    #     return f'{self.player_1} ({self.team_1}) - ({self.team_2}) {self.player_2}'