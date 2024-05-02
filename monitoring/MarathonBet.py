"""
    Считывание информации о текущих матчах с Винлайна
"""
import json
import os
import time
from urllib.request import urlopen

import urllib.request as urllib2
from xml import etree

import requests
from bs4 import BeautifulSoup

from parsel import Selector

from selenium import webdriver
from selenium.webdriver.common.by import By

from browser.Browser import Browser
from logs.CustomLogger import CustomLogger
from pyxtension.streams import stream
from selenium.webdriver.chrome.options import Options
from datetime import datetime

from model.MarathonBetMatch import Match
from reflection.Reflection import Reflection


class MarathonBet:

    # strategy = None

    def createObjByArgs(args):
        return MarathonBet(args[0], args[1])

    def __init__(self, monitoring_cfg, strategy):
        self.monitoring_cfg = monitoring_cfg
        self.browser = None
        self.strategy = strategy
        # MarathonBet.strategy = strategy
        self.all_live_id = 1372932
        self.old_number = -12
        self.findGame = False
        self.current_game = None
        self.isResult = False
        self.validGame = False
        self.currentGames = dict()
        self.errorGames = dict()
        self.predictions = dict()
        self.isActualBrowser = True
        self.logger = CustomLogger().getLogger(type(self).__name__)

        self.all_current_games = dict()
        self.max_ticks = int(monitoring_cfg["max_ticks"])

        self.all_error_games = dict()

        # Открываем браузер
        # self.browser = Browser("https://www.marathonbet.ru/su/live/1372932")
        self.searchingTheGame()
        # self.soup = BeautifulSoup(self.browser.page_source, 'html.parser')

    def getGameNameStatusAndCoefs(self, match_text, header_text):

        match_text = header_text + match_text
        match_text_split = match_text.split(" ")

        # Статус игры
        if (match_text[0] == "+"):
            gameStatus = match_text_split[0]
        else:
            gameStatus = match_text_split[0] + " " + match_text_split[1]

        match_text = match_text.replace(gameStatus, "")
        gameName = match_text.split("Матч")[0][1:len(match_text.split("Матч")[0]) - 1].replace("  ", " - ")

        gameStatus = gameStatus + " " + match_text.split("Матч")[1][0] + ":" + match_text.split("Матч")[1][1]

        # Если данная игра уже есть, то не находим коэффициенты
        if (self.all_current_games.get(gameName) != None):
            return gameName, gameStatus, None

        # Проверка на ошибку парсинга
        if (gameName[0] == "(" or len(match_text.split("Матч")[1]) < 7):
            return None, None, None

        # 5 - 1T, 8 - 2T
        shift = 5 if (match_text.split("Матч")[1][6] == '.' or match_text.split("Матч")[1][7] == '.') else 8

        coefs = [match_text.split("Матч")[1][shift: shift + 4],
                 match_text.split("Матч")[1][shift + 4: shift + 8],
                 match_text.split("Матч")[1][shift + 8: shift + 12]
                 ]

        coefs_float = []
        for c in coefs:
            try:
                coefs_float.append(float(c))
            except:
                # print(f"Ошибка парсинга коэффициентов {coefs} {c} {gameName}")
                return None, None, None

        return gameName, gameStatus, coefs_float

    def setScheduler(self, scheduler):
        self.scheduler = scheduler

    # def OnCreate(self):
    #     self.StartBrowser()
    #     # self.browser.get("https://betboom.ru/esport?pageRoute=timeline&type=live&sportId=2")
    #     # self.browser.get("https://betboom.ru/esport")
    #     self.browser.get("https://www.marathonbet.ru/su/live/1372932")
    #     last_height = self.browser.execute_script("return document.body.scrollHeight")
    #     while True:
    #         self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #         time.sleep(0.5)
    #         new_height = self.browser.execute_script("return document.body.scrollHeight")
    #         if new_height == last_height:
    #             break
    #         last_height = new_height
    #
    # def StartBrowser(self):
    #     # self.logger.debug("Открытие браузера")
    #     self.chromedriver = 'chromedriver.exe'
    #     os.environ['webdriver.chrome.driver'] = self.chromedriver
    #     options = Options()
    #     options.add_argument('--headless')
    #     options.add_argument('--disable-gpu')
    #     options.add_experimental_option('detach', True)
    #
    #     #Проверка на существование браузера
    #     if(self.browser!=None):
    #         # self.logger.info("Замена текущего браузера")
    #         new_browser = webdriver.Chrome(self.chromedriver, chrome_options=options)
    #         #Подмена браузера
    #         self.browser.close()
    #         self.browser = new_browser
    #         self.isActualBrowser = True
    #     else:
    #         # self.logger.info("Создание нового браузера")
    #         self.browser = webdriver.Chrome(self.chromedriver, chrome_options=options)

    # def checkBrowserState(self):
    #     # Если не нашли ни одной игры
    #     if (self.arrChampNameElems.size() == 0 and self.isActualBrowser):
    #         self.isActualBrowser = False
    #         return
    #
    #     # На следующем тике осуществляем подмену браузера
    #     if (self.arrChampNameElems.size() == 0 and self.isActualBrowser==False):
    #         self.OnCreate()

    def searchingTheGame(self):
        while(True):

            strHTML = requests.get("https://www.marathonbet.ru/su/live/1372932")
            time.sleep(5)

            startInd = strHTML.text.index("reactData")
            endInd = 0
            for i in range(startInd, 100000000):
                if (strHTML.text[i] == '\n'):
                    endInd = i - 1
                    break

            site_live_json = json.loads(strHTML.text[startInd + 12:endInd])
            # dotaMatches = stream(stream(site_live_json["liveMenuEvents"]["childs"]).filter(lambda x: x["label"] == "Киберспорт").toList()[0]["childs"]).filter(lambda x: "Dota 2" in x["label"]).toList()
            dotaMatches = stream(stream(site_live_json["liveMenuEvents"]["childs"]).filter(lambda x: x["label"] == "Киберспорт").toList()[0]["childs"]).filter(lambda x: "Counter" in x["label"]).toList()




            for matchJson in dotaMatches:
                match = Reflection.get_class("model." + type(self).__name__ + "Match.py", matchJson["label"],
                                             matchJson["childs"][0]["label"].split(" - ")[0],
                                             matchJson["childs"][0]["label"].split(" - ")[1],
                                             "https://www.marathonbet.ru" + matchJson["childs"][0]["url"], self.logger, self.strategy)

                # if self.all_current_games.get(match.__str__()) is None:
                #     self.all_current_games[match.__str__()] = match

                strHTML = requests.get(match.uri)
                soup = BeautifulSoup(strHTML.text, 'html.parser')
                time.sleep(5)

                # TODO add handler to add game (monitoring coefficients)
                isAlive = match.parseDataFromSite(soup)

                sc_1 = int(match.current_map_score.split(":")[0])
                sc_2 = int(match.current_map_score.split(":")[1])

                if (isAlive and self.all_current_games.get(match.__str__()) and (sc_1 + sc_2) == 7):
                    self.strategy.resultMap(match, self.all_current_games[match.__str__()])
                    self.all_current_games.pop(match.__str__())
                    continue

                # if (isAlive and self.all_current_games.get(match.__str__()) and match.map != self.all_current_games[match.__str__()].map):
                #     self.strategy.resultMap(match, self.all_current_games[match.__str__()])
                #     self.all_current_games.pop(match.__str__())
                #     continue

                # if self.all_current_games.get(match.__str__()):
                #     self.all_current_games[match.__str__()] = match

                match = self.strategy.predictMap(match)
                if (match!=None and self.all_current_games.get(match.__str__())==None):
                    self.all_current_games[match.__str__()] = match
