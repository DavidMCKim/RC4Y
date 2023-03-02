import re
import requests
import pandas as pd
from loguru import logger
from bs4 import BeautifulSoup

class CrawlCampingInfo():
    def __init__(self):
        self.url = 'https://pcmap.place.naver.com/accommodation/list?query=<%keyword%>&mapUrl=https://map.naver.com/v5/search/<%keyword%>'
        self.baseUrl = 'https://www.map.naver.com/v5/search/<%keyword%>'
        
        
    def Crawl_Camping_Info(self):
        """ crawl start date, crawl end date 사이에 있는 뉴스 링크 수집 """
        try:
            url = self.url.replace('<%keyword%>', '경기도 캠핑장')

            # 헤더 설정
            custom_headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
                'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cookie': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                'Referer': 'https://map.naver.com/',
                'Host': 'pcmap.place.naver.com'
            }
            request = requests.get(url, headers=custom_headers)
            # 200 OK 코드가 아닌 경우 에러 발동
            request.raise_for_status()
            # 한글깨짐 현상으로 인해 'UTF-8'로 인코딩
            request.encoding='UTF-8'

            html = request.text
            soup = BeautifulSoup(html, "html.parser")
            type = str(soup.find_all("script")[2])
            test = re.compile('^window.__APOLLO_STATE__ = ')
            print(test.findall(type))
            


        except Exception as e:
            print(e)

if __name__ == '__main__':
    c = CrawlCampingInfo()
    c.Crawl_Camping_Info()

