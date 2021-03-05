import pymysql
from db.config import DB_CONFIG
class DBMS:
    def __init__(self):
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host=DB_CONFIG['ip'], user=DB_CONFIG['user'], password=DB_CONFIG['password'], db=DB_CONFIG['database'], charset='utf8')
        self.cur = self.conn.cursor()

    def query(self, query):
        try:
            self.connect()
            self.cur.execute(query)
            self.conn.commit()
        finally:
            self.conn.close()

    def select(self, table):
        try:
            self.connect()
            sql = f'select * from {table}'
            self.cur.execute(sql)

            rows = self.cur.fetchall()

        finally:
            self.conn.close()

        return rows