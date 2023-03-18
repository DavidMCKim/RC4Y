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
            if self.conn.is_connected() or self.conn.pool_name is not None :
                cursor.close()
                self.conn.close()

        return result

    def insert(self, query) :
        result = -1
        try :
            cursor = self.conn.cursor()

            cursor.execute(query)
            self.db.commit()

            result = cursor.rowcount

        except Exception as ex :
            print(ex)

        finally:
            if self.conn.is_connected() or self.conn.pool_name is not None :
                cursor.close()
                self.conn.close()

        return result

    def insert_object(self, tablename, column, value) :
        result = -1
        try :
            cursor = self.conn.cursor()

            value_tmp = str(tuple(('%s' for i in range (0, len(column))))).replace('\'', '')
            
            query = f'''
            INSERT INTO {tablename}{str(tuple(column))}
            VALUES {value_tmp}
            '''
            
            cursor.execute(query, value)
            self.db.commit()

            result = cursor.rowcount

        except Exception as ex :
            print(ex)   

        finally:
            if self.conn.is_connected() or self.conn.pool_name is not None :
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
            if self.conn.is_connected() or self.conn.pool_name is not None :
                cursor.close()
                self.conn.close()

        return result
