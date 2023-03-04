import asyncio
import aiomysql
from mysql.connector import pooling

class DBConnector :
    def __init__(self) :
        # #### SERVER
        self.db = pooling.MySQLConnectionPool(
                pool_size = 15,
                pool_name = 'rc4ypool',
                host="localhost",
                database="rc4y" 
        )

    def select(self, query) :
        result = None
        try :
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(query)
            res = cursor.fetchall()

            result = []
            for r in res :
                result.append(list(r))

        except Exception as ex :
            print(ex)

        finally:
            if conn.is_connected() or conn.pool_name is not None :
                cursor.close()
                conn.close()

        return result

    def insert(self, query) :
        result = -1
        try :
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(query)
            self.db.commit()

            result = cursor.rowcount

        except Exception as ex :
            print(ex)

        finally:
            if conn.is_connected() or conn.pool_name is not None :
                cursor.close()
                conn.close()

        return result

    def insert_object(self, tablename, column, value) :
        result = -1
        try :
            conn = self.db.get_connection()
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
            print(ex)   

        finally:
            if conn.is_connected() or conn.pool_name is not None :
                cursor.close()
                conn.close()

        return result

    def update(self, query) :
        result = -1
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute(query)
            self.db.commit()

            result = cursor.rowcount
        
        except Exception as ex :
            print(ex)

        finally:
            if conn.is_connected() or conn.pool_name is not None :
                cursor.close()
                conn.close()

        return result
