import json
import os
import threading
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import threading
from threading import Thread

class Browser:

    # class thread(threading.Thread):
    #
    #     def __init__(self, browser):
    #         threading.Thread.__init__(self)
    #         self.browser = browser
    #
    #         # helper function to execute the threads
    #
    #     def run(self):
    #         last_height = self.browser.execute_script("return document.body.scrollHeight")
    #         while True:
    #             self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #             time.sleep(0.5)
    #             new_height = self.browser.execute_script("return document.body.scrollHeight")
    #             if new_height == last_height:
    #                 break
    #             last_height = new_height


    def __init__(self, url):
        self.onCreate(url)
        self.loop = True
        self.soup = BeautifulSoup(self.browser.page_source, 'html.parser')


    def onCreate(self, url):
        self.startBrowser()
        self.browser.get(url)

        # thread = Thread(target=self.runThread)
        # thread.start()

        last_height = self.browser.execute_script("return document.body.scrollHeight")
        while True:
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def runThread(self):
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        while self.loop:
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


    def startBrowser(self):
        # self.logger.debug("Открытие браузера")
        self.chromedriver = 'chromedriver.exe'
        os.environ['webdriver.chrome.driver'] = self.chromedriver
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_experimental_option('detach', True)
        self.browser = webdriver.Chrome(self.chromedriver, chrome_options=options)


    def closeBrowser(self):
        self.loop = False
        self.browser.close()

        # #Проверка на существование браузера
        # if(self.browser!=None):
        #     # self.logger.info("Замена текущего браузера")
        #     new_browser = webdriver.Chrome(self.chromedriver, chrome_options=options)
        #     #Подмена браузера
        #     self.browser.close()
        #     self.browser = new_browser
        #     self.isActualBrowser = True
        # else:
        #     # self.logger.info("Создание нового браузера")
        #     self.browser = webdriver.Chrome(self.chromedriver, chrome_options=options)