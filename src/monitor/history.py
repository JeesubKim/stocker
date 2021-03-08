import threading
from db.dbms import DBMS
from util.http import get
from util.pandas import read_html, concat, arrangeNewDataFrame
import time

TARGET_DATE = '2020.01.01' 
TARGET_DATE_DEFAULT = '2020.01.01' 
TABLE = 'stock_history'


COLUMNS = ['날짜', '종가', '시가', '고가', '저가', '거래량']
COLUMNS_IN_DB = ['datetime', 'closingPrice', 'marketPrice', 'highPrice', 'lowPrice', 'volume']
EXTRA_COLUMNS_IN_DB = ['name', 'code']

class StockHistory(threading.Thread):
    def __init__(self):
        super().__init__()
        self.db = DBMS()
    def run(self):
        print('run StockHistory')

        table = 'stock_item'
        stock_items = self.db.select(table)

        for stock_item in list(stock_items):
            page_num = 1
            # page_num=35
            target_condition = True
            sum_data = None
            
            # retrieve stock_code
            code = stock_item['code']
            
            # convert stock_code to 6 digit
            code = f'00000{code}'[-6:]
            
            # retrieve latest stock information from db
            
            latest_item = self.db.select_latest('stock_history', code)
            print('latest_item',latest_item)
            
            if len(latest_item) != 0:
                TARGET_DATE = latest_item[0]['datetime'].strftime('%Y.%m.%d')
            else:
                TARGET_DATE = TARGET_DATE_DEFAULT
            
            # configure target date
            while target_condition:
                # path = f'https://finance.naver.com/item/sise_day.nhn?code=373200&page=240'
                path = f'https://finance.naver.com/item/sise_day.nhn?code={code}&page={page_num}'
                # send http get and get response
                
                res = get(path)
                table = read_html(res.text, None, None)
                
                
                data = table[0].dropna().reset_index(drop=True)
                
                data = data[data['날짜'] > TARGET_DATE]
                print(data,len(data))
                # break if there's nothing to update
                if len(data) == 0:
                    break
                sum_data = concat(sum_data, data)
                
                target_condition = data.iloc[len(data) - 1]['날짜'] > TARGET_DATE
                
                page_num += 1
                
                print(table[1][table[1].columns[len(table[1].columns)-1]][0])
                # time.sleep(2)
                if table[1][table[1].columns[len(table[1].columns)-1]][0] != '맨뒤' and page_num > 1:
                    # There's no more data
                    print(table[1][table[1].columns[len(table[1].columns)-1]][0] != '맨뒤')
                    break
            
            if str(type(sum_data))!="<class 'NoneType'>":
                stock_item_name = stock_item['name']
                print(f'{stock_item_name} - Updating...')
                final_data = sum_data.reset_index(drop=True)
                
                for idx in final_data.index:
                    data = dict.fromkeys(COLUMNS_IN_DB)
                    for col_idx, col in enumerate(COLUMNS_IN_DB):
                        data[col] = str(final_data.iloc[idx][COLUMNS[col_idx]])
                    data['name'] = stock_item_name
                    data['code'] = code
                    self.db.insert(TABLE, data)

        
