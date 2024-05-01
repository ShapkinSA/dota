"""
    Основная модель данных
"""
import re
from pyxtension.streams import stream

from model.Match import Match


class MarathonBetMatch(Match):

    def createObjByArgs(args):
        return MarathonBetMatch(args[0],args[1],args[2],args[3],args[4],args[5])

    def __init__(self, info, team_1, team_2, uri, logger, strategy):
        super().__init__(info, team_1, team_2, uri, logger, strategy)

    def parseDataFromSite(self):
        #current map
        try:
            self.map = stream(self.soup.find_all(class_='name-field')).filter(
                lambda x: "Результат," in str(x) != None and "-я карта" in str(x) != None).map(
                lambda x: int(re.search(r'[0-9]+', str(x)).group(0))).toList()[0]
        except:
            return False


        # current map score
        self.map_score = self.soup.find(class_='cl-left red').find(class_='italic').text

        results = self.soup.find_all(class_='result-right')
        if(results!=None or results!=[]):
            lst_1 = stream(results).filter(lambda x: "Map_Result" in str(x) and "RN_H" in str(x)).map(lambda x: float(x.text)).toList()
            if(lst_1==None or lst_1==[]):
                return False

            lst_2 = stream(results).filter(lambda x: "Map_Result" in str(x) and "RN_A" in str(x)).map(lambda x: float(x.text)).toList()
            if(lst_2==None or lst_2==[]):
                return False

            self.coef_1 = lst_1[0]
            self.coef_2 = lst_2[0]
            self.logger.debug(self.showInfoWithCoeffs())
            print("\n")
            return True
        return False



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