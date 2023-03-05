import re
import json
import requests
import pandas as pd
from loguru import logger
from bs4 import BeautifulSoup
from db.dbconnector import DBConnector

class CrawlCampsiteInfo():
    def __init__(self):
        self.url     = 'https://pcmap.place.naver.com/accommodation/list?query=<%keyword%>&mapUrl=https://map.naver.com/v5/search/<%keyword%>'
        self.baseUrl = 'https://www.map.naver.com/v5/search/<%keyword%>'
        self.db      = DBConnector()
        
        
    def Init_RC4Y(self):
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
            # split이 위험할 수도 있으니 정규표현식으로 변경할 수 있도록 수정 필요!!
            html_campsite_info = str(soup.find_all("script")[2]).split(';')[4]
            html_campsite_info = f"{html_campsite_info.replace('window.__APOLLO_STATE__ = ','')}"
            json_campsite_info = json.loads(html_campsite_info)
            self.Get_Campsite_Info(json_campsite_info)
               
        except Exception as e:
            print(e)

    def Get_Campsite_Info(self, json_campsite_info):
        try:
            scrap_data = {'Category' : '', 'CategoryCode' : '', 'CampingId' : '', 'CampSiteName' : '', 'RoadAddress' : '', 'Lotaddress' : '', 'Latitude' : '',
                          'Longitude' : '', 'PhoneNumber' : '', 'VirtualNumber' : '', 'PromotionTitle' : '', 'Facility' : '', 'ImageUrls' : '', 'UseFlag' : ''}
            keyType = re.compile('^AccommodationSummary')
            for key in json_campsite_info.keys():
                if keyType.match(key):
                    print(json_campsite_info[key])
                    campsiteInfo = json_campsite_info[key]
                    try:
                        scrap_data['Category'] = campsiteInfo['businessCategory']
                        scrap_data['CategoryCode'] = campsiteInfo['categoryCode']
                        scrap_data['CampingId'] = campsiteInfo['id']
                        scrap_data['CampSiteName'] = campsiteInfo['name']
                        scrap_data['RoadAddress'] = campsiteInfo['roadAddress']
                        scrap_data['Lotaddress'] = campsiteInfo['commonAddress'] + campsiteInfo['address']
                        scrap_data['Latitude'] = campsiteInfo['x']
                        scrap_data['Longitude'] = campsiteInfo['y']
                        scrap_data['PhoneNumber'] = campsiteInfo['phone']
                        scrap_data['VirtualNumber'] = campsiteInfo['virtualPhone']
                        scrap_data['PromotionTitle'] = campsiteInfo['promotionTitle']
                        scrap_data['Facility'] = campsiteInfo['facility']
                        scrap_data['ImageUrls'] = campsiteInfo['imageUrls']
                        scrap_data['UseFlag'] = 'Y'

                        self.db.select('''
                                    
                                       ''')

                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    c = CrawlCampsiteInfo()
    c.Init_RC4Y()

