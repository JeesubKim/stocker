import threading
import time
from db.dbms import DBMS




class Fluctuation(threading.Thread):
    def __init__(self):
        super().__init__()
        self.db = DBMS()
    def run(self):
        table = 'stock_item'
        stock_items = self.db.select(table)
        cnt=0
        
        for stock_item in list(stock_items):
            code = stock_item['code']
            print(stock_item['name'], f'{cnt}/{len(stock_items)}')
            cnt+=1
            query = f'select * from stock_history where (code={code}) order by datetime'
            rows = self.db.query(query)

            self.db.connect()
            for index, row in enumerate(rows[1:]):
                # started with 0, but it is 1 in real rows
                
                fluc = ((float(row['closingPrice']) /float(rows[index]['closingPrice'])) - 1) * 100
                fluc = round(fluc, 2)
                
                self.db.updateById('stock_history',f'fluctuation={fluc}', row['id'])
                # time.sleep(0.1)
        
            self.db.conn.commit()
            self.db.conn.close()

        
            