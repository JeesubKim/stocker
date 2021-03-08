import pymysql
from db.config import DB_CONFIG
class DBMS:
    def __init__(self):
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host=DB_CONFIG['ip'], user=DB_CONFIG['user'], password=DB_CONFIG['password'], db=DB_CONFIG['database'], charset='utf8', cursorclass=pymysql.cursors.DictCursor)
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

    def select_latest(self, table, code):
        try:
            self.connect()
            sql = f'select * from \
                (\
                    select * \
                        from {table} \
                            where (code, datetime) in (\
                                select code, max(datetime) as datetime\
                                    from {table} where code={code}\
                                ) order by datetime desc\
                ) t\
                group by t.code'
            self.cur.execute(sql)

            rows = self.cur.fetchall()
        finally:
            self.conn.close()

        return rows

    def select_latest_market(self, table, market):
        try:
            self.connect()
            sql = f'select * from \
                (\
                    select * \
                        from {table} \
                            where (market, datetime) in (\
                                select market, max(datetime) as datetime\
                                    from {table} where market="{market}"\
                                ) order by datetime desc\
                ) t\
                group by t.market'

            self.cur.execute(sql)

            rows = self.cur.fetchall()
        finally:
            self.conn.close()

        return rows

    def insert(self, table, data):
        try:
            self.connect()
            # 1. combile keys
            columns = ','.join(data.keys())
            placeholders = ','.join(['%s '] * len(data))

            sql = f'insert into {table}({columns}) values({placeholders});'
            # print(sql)
            self.cur.execute(sql, list(data.values()))
            self.conn.commit()
            

        finally:
            self.conn.close()

        
    def upsert(self, table, data):
        try:
            self.connect()
            # 1. combile keys
            columns = ','.join(data.keys())
            placeholders = ','.join(['%s '] * len(data))

            upsert_list = []
            for d in list(data.keys()):
                upsert_list.append(f'{d}={str(data[d])}')

            upsert = ','.join(upsert_list)

            sql = f'insert into {table}({columns}) values({placeholders}) on duplicate key update ({upsert});'
            print(sql)
            self.cur.execute(sql, list(data.values()))
            self.conn.commit()
            

        finally:
            self.conn.close()


        

