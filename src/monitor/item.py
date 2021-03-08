import threading


from util.pandas import read_html
from db.dbms import DBMS


KOREA_EXCHANGE_URL = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download' #한국거래소 KRX URL

COLUMNS = ['회사명','종목코드','업종','주요제품','지역']
COLUMNS_IN_DB = ['name', 'code', 'category', 'product', 'location']
TABLE = 'stock_item'

class StockItem(threading.Thread):
    def __init__(self):
        super().__init__()
        self.db = DBMS()
    def run(self):
        print('run StockItem')
        # 1. retrieve market list from KRX and read tables from html 
        market_list = read_html(KOREA_EXCHANGE_URL,0,0)
        # 2. filter columns with pre-defined list
        print(type(market_list))
        filtered_list = market_list[COLUMNS]
        
        # 3. insert into database , table : stock_item
        
        for idx in filtered_list.index:
            
            data = dict.fromkeys(COLUMNS_IN_DB)
            
            for col_idx, col in enumerate(COLUMNS_IN_DB):
                data[col] = str(filtered_list.iloc[idx][COLUMNS[col_idx]])

            code = data['code']
            data['code'] = f'00000{code}'[-6:]
            self.db.insert(TABLE, data)
            # self.db.upsert(TABLE, data)
