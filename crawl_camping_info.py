import re
import json
import requests
import configparser
import pandas as pd
from loguru import logger
from bs4 import BeautifulSoup
from db.dbconnector import DBConnector

class CrawlCampsiteInfo():
    def __init__(self):
        config             = configparser.ConfigParser()
        config.read('config.ini', encoding='utf8')
        self.url           = 'https://map.naver.com/v5/api/search?caller=pcweb&query=<%KeyWord%>&type=all&page=1&displayCount=50&isPlaceRecommendationReplace=true&lang=ko'
        self.db            = DBConnector()
        self.keepCrawl     = True
        self.do_list       = config['CampSite_By_Do']['do_list'].split(', ')
        
        
    def Init_RC4Y(self):
        """ 네이버 지도에서 도별(경기도, 충청북도, 충청남도, 강원도 등..) 캠핑장 데이터 수집 """
        try:
            for do in self.do_list:
                try:
                    url = self.url.replace('<%KeyWord%>',do)
                    keepCrawl  = self.keepCrawl                  
                    while(keepCrawl):
                        try:
                            # 헤더 설정
                            custom_headers = {
                                'User-Agent'   : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36',
                            }
                            request = requests.get(url, headers=custom_headers, timeout=10)
                            # 200 OK 코드가 아닌 경우 에러 발동
                            request.raise_for_status()
                            # 한글깨짐 현상으로 인해 'UTF-8'로 인코딩
                            request.encoding='UTF-8'

                            html = request.text
                            data = json.loads(html)
                            campsites = data['result']['place']['list']
                            scrap_data = self.Get_Campsite_Info(campsites)

                        except Exception as e:
                            print(e)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

    def Get_Campsite_Info(self, campsites):
        try:
            scrap_data = {'Category' : '', 'CampingId' : '', 'CampSiteName' : '', 'RoadAddress' : '', 'Lotaddress' : '', 'Latitude' : '',
                          'Longitude' : '', 'PhoneNumber' : '', 'VirtualNumber' : '', 'siteUrl' : '', 'Facility' : '', 'ImageUrls' : '', 'UseFlag' : ''}
            keyType = re.compile('^AccommodationSummary')
            for campsite in campsites:
                try:
                    try:
                        scrap_data['Category'] = ', '.join(category for category in campsite['category'])
                    except:
                        scrap_data['Category'] = ''
                    scrap_data['CampSiteID'] = campsite['id']
                    scrap_data['CampSiteName'] = campsite['name']
                    scrap_data['RoadAddress'] = campsite['roadAddress']
                    scrap_data['Lotaddress'] = campsite['address']
                    scrap_data['Latitude'] = campsite['x']
                    scrap_data['Longitude'] = campsite['y']
                    scrap_data['PhoneNumber'] = campsite['telDisplay']
                    scrap_data['VirtualNumber'] = campsite['virtualTel']
                    try:
                        scrap_data['siteUrl'] = campsite['homePage']
                    except:
                        scrap_data['siteUrl'] = ''
                    try:
                        scrap_data['Facility'] = ', '.join(info for info in campsite['menuInfo'].split(' | '))
                    except:
                        scrap_data['Facility'] = ''
                    scrap_data['ImageUrls'] = ', '.join(imageUrl for imageUrl in campsite['thumUrls'])
                    scrap_data['UseFlag'] = 'Y'

                    print(scrap_data)
                    
                    selectQuery = f'''
                                    select *
                                    from tb_CampSite_Info
                                    where CampSiteID = {scrap_data['CampSiteID']}
                                    '''
                    result = self.db.select(selectQuery)
                    if result == []:
                        insertQuery = f'''
                                    INSERT INTO tb_CampSite_Info (Category, CampSiteID, CampSiteName, RoadAddress, Lotaddress, Latitude, Longitude, PhoneNumber, VirtualNumber, siteUrl, Facility, ImageUrls, UseFlag)
                                    VALUES (%s, %d, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                '''
                        value = f'''{scrap_data['Category']} / {scrap_data['CampSiteID']} / {scrap_data['CampSiteName']} / {scrap_data['RoadAddress']} / {scrap_data['Lotaddress']} / {scrap_data['Latitude']} / {scrap_data['Longitude']} / {scrap_data['PhoneNumber']} / {scrap_data['VirtualNumber']} / {scrap_data['siteUrl']} / {scrap_data['Facility']} / {scrap_data['ImageUrls']} / {scrap_data['UseFlag']}'''
                        values =  tuple(value.split(' / '))
                        self.db.insert_object(values)

                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

        return scrap_data

if __name__ == '__main__':
    c = CrawlCampsiteInfo()
    c.Init_RC4Y()

