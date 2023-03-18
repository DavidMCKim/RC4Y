import asyncio
import pymysql
import configparser

class DBConnector :
    def __init__(self) :
        # config.ini 파일 가져오기
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf8')
        self.host     = config['DB_INFO']['host']
        self.user     = config['DB_INFO']['user']
        self.password = config['DB_INFO']['password']
        self.db       = config['DB_INFO']['db']
        self.charset  = config['DB_INFO']['charset']
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset=self.charset)

    def select(self, query) :
        result = None
        try :
            cursor = self.conn.cursor()

            cursor.execute(query)
            res = cursor.fetchall()

            result = []
            for r in res :
                result.append(list(r))

        except Exception as ex :
            print(ex)

        finally:
            cursor.close()
            self.conn.close()

        return result

    def insert(self, query, values) :
        result = -1
        try :
            cursor = self.conn.cursor()
            

            cursor.execute(query, ())
            self.db.commit()

            result = cursor.rowcount

        except Exception as ex :
            print(ex)

        finally:
            cursor.close()
            self.conn.close()

        return result

    def insert_object(self, values) :
        result = -1
        try :
            cursor = self.conn.cursor()
            
            query = f'''
                INSERT INTO tb_CampSite_Info (Category, CampSiteID, CampSiteName, RoadAddress, Lotaddress, Latitude, Longitude, PhoneNumber, VirtualNumber, siteUrl, Facility, ImageUrls, UseFlag)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            
            cursor.execute(query, values)
            self.db.commit()

            result = cursor.rowcount

        except Exception as ex :
            print(ex)   

        finally:
            cursor.close()
            self.conn.close()

        return result

    def update(self, query) :
        result = -1
        try:
            cursor = self.conn.cursor()

            cursor.execute(query)
            self.db.commit()

            result = cursor.rowcount
        
        except Exception as ex :
            print(ex)

        finally:
            cursor.close()
            self.conn.close()

        return result
