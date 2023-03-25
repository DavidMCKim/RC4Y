import re
import json
import requests
import configparser
import pandas as pd
from loguru import logger
from bs4 import BeautifulSoup
from db.dbconnector import DBConnector

class CrawlCampsiteComments ():
    def __init__(self):
        config             = configparser.ConfigParser()
        config.read('config.ini', encoding='utf8')
        self.url           = 'https://map.naver.com/v5/api/search?caller=pcweb&query=<%KeyWord%>&type=all&page=1&displayCount=50&isPlaceRecommendationReplace=true&lang=ko'
        self.db            = DBConnector()
        self.keepCrawl     = True
        self.do_list       = config['CampSite_By_Do']['do_list'].split(', ')

    def Crawl_CampSite(self):
        