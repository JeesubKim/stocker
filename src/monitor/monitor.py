from history import StockHistory
from item import StockItem
from market import StockMarket
# This file will be running using ubuntu crontab

def run_monitoring_items():
    sh = StockHistory()
    si = StockItem()
    sm = StockMarket()

    sh.start()
    si.start()
    sm.start()

if __name__ == '__main__':
    run_monitoring_items()
    