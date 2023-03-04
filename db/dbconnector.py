import asyncio
import aiomysql
from mysql.connector import pooling

import logging

logger = logging.getLogger('db')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(u'[%(asctime)s] [%(levelname)s] :: %(message)s')
file_handler = logging.FileHandler(filename = './ccnd_web_api.log', encoding = 'utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
    
class DBConnector :
    def __init__(self) :
        ##### docker
        # self.db = mysql.connector.connect(
        #         host="203.245.41.195",
        #         user="ccnd",
        #         password="ccnd123",
        #      l   database="ccnd" 
        # )
        # self.db = pooling.MySQLConnectionPool(
        #         pool_size = 5,
        #         pool_name = 'ccndpool',
        #         host="203.245.41.195",
        #         user="ccnd",
        #         password="ccnd123",
        #         database="ccnd" 
        # )

        ##### rfc SERVER
        # self.db = mysql.connector.connect(
        #         host="121.124.126.43",
        #         user="root",
        #         password="Rlaguscjf13@$",
        #         database="DATA_MART_CN",
        # )
        # self.db = pooling.MySQLConnectionPool(
        #         pool_size = 15,
        #         pool_name = 'ccndpool',
        #         host="121.124.126.43",
        #         user="root",
        #         password="Rlaguscjf13@$",
        #         database="DATA_MART_CN" 
        # )
        
        #### SERVER private
        # self.db = pooling.MySQLConnectionPool(
        #         pool_size = 15,
        #         pool_name = 'ccndpool',
        #         host="172.30.1.222",
        #         user="cu",
        #         password="Rlaguscjf13@$",
        #         database="CCND_DATA" 
        # )

        # #### SERVER
        self.db = pooling.MySQLConnectionPool(
                pool_size = 15,
                pool_name = 'rc4ypool',
                host="localhost",
                user="root",
                password="Mckim1996!@#$",
                database="rc4y" 
        )

    def select(self, query) :
        result = None
        try :
            conn = self.db.get_connection()
            logger.debug(f'Connected to Database using Pool >> {conn}')
            cursor = conn.cursor()

            cursor.execute(query)
            res = cursor.fetchall()

            result = []
            for r in res :
                result.append(list(r))

        except Exception as ex :
            logger.error(f'/select >> {ex}')

        finally:
            if conn.is_connected() or conn.pool_name is not None :
                cursor.close()
                conn.close()

        return result

    def insert(self, query) :
        result = -1
        try :
            conn = self.db.get_connection()
            logger.debug(f'Connected to Database using Pool >> {conn}')
            cursor = conn.cursor()

            cursor.execute(query)
            self.db.commit()

            result = cursor.rowcount

        except Exception as ex :
            logger.error(f'/select >> {ex}')

        finally:
            if conn.is_connected() or conn.pool_name is not None :
                cursor.close()
                conn.close()

        return result

    def insert_object(self, tablename, column, value) :
        result = -1
        try :
            conn = self.db.get_connection()
            logger.debug(f'Connected to Database using Pool >> {conn}')
            cursor = conn.cursor()

            value_tmp = str(tuple(('%s' for i in range (0, len(column))))).replace('\'', '')
            
            query = f'''
            INSERT INTO {tablename}{str(tuple(column))}
            VALUES {value_tmp}
            '''
            
            cursor.execute(query, value)
            self.db.commit()

            result = cursor.rowcount

        except Exception as ex :
            logger.error(f'/select >> {ex}')

        finally:
            if conn.is_connected() or conn.pool_name is not None :
                cursor.close()
                conn.close()

        return result

    def update(self, query) :
        result = -1
        try:
            conn = self.db.get_connection()
            logger.debug(f'Connected to Database using Pool >> {conn}')
            cursor = conn.cursor()

            cursor.execute(query)
            self.db.commit()

            result = cursor.rowcount
        
        except Exception as ex :
            logger.error(f'/select >> {ex}')

        finally:
            if conn.is_connected() or conn.pool_name is not None :
                cursor.close()
                conn.close()

        return result
