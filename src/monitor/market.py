import threading

from db.dbms import DBMS
from util.http import get
from util.pandas import read_html, concat, arrangeNewDataFrame

MARKET_LIST = [
    'https://finance.naver.com/sise/sise_index_day.nhn?code=KOSPI&page=',
    'https://finance.naver.com/sise/sise_index_day.nhn?code=KOSDAQ&page=',
    'https://finance.naver.com/sise/sise_index_day.nhn?code=KPI200&page=',
]

MARKET = [
    'KOSPI',
    'KOSDAQ',
    'KOSPI200'
]

TARGET_DATE = '2020.01.01' 
TARGET_DATE_DEFAULT = '2020.01.01' 

COLUMNS = ['날짜', '체결가','등락률','거래량(천주)','거래대금(백만)']
COLUMNS_IN_DB = ['datetime', 'price', 'fluctuation', 'volumn', 'tradeCost']
TABLE = 'stock_market'
class StockMarket(threading.Thread):
    def __init__(self):
        super().__init__()
        self.db = DBMS()
    def run(self):
        print('run StockMarket')

        
        for idx, market in enumerate(MARKET_LIST):
            target_condition = True
            page_num = 1
            sum_data = None

            latest_item = self.db.select_latest_market(TABLE, MARKET[idx])
            print('latest_item',latest_item)
            
            if len(latest_item) != 0:
                TARGET_DATE = latest_item[0]['datetime'].strftime('%Y.%m.%d')
            else:
                TARGET_DATE = TARGET_DATE_DEFAULT
            

            while target_condition:
                path = f'{market}{page_num}'
                
                
                res = get(path)
                table = read_html(res.text, None, None)
                data = table[0].dropna().reset_index(drop=True)
                
                data = data[data['날짜'] > TARGET_DATE]
                print(data)
                
                print(data,len(data))
                # break if there's nothing to update
                if len(data) == 0:
                    break
                sum_data = concat(sum_data, data)
                
                target_condition = data.iloc[len(data) - 1]['날짜'] > TARGET_DATE
                
                page_num += 1
                
                print(table[1][table[1].columns[len(table[1].columns)-1]][0])
                if table[1][table[1].columns[len(table[1].columns)-1]][0] != '맨뒤' and page_num > 1:
                    # There's no more data
                    print(table[1][table[1].columns[len(table[1].columns)-1]][0] != '맨뒤')
                    break
            
            if str(type(sum_data))!="<class 'NoneType'>":
                
                print(f'{market} - Updating...')
                final_data = sum_data.reset_index(drop=True)
                
                for final_idx in final_data.index:
                    data = dict.fromkeys(COLUMNS_IN_DB)
                    for col_idx, col in enumerate(COLUMNS_IN_DB):
                        data[col] = str(final_data.iloc[final_idx][COLUMNS[col_idx]])

                    data['market'] = MARKET[idx]
                    self.db.insert(TABLE, data)


            # break
            



        
