from monitor.history import StockHistory
from monitor.item import StockItem
from monitor.market import StockMarket
# This file will be running using ubuntu crontab

def run_monitoring_items():
    # sh = StockHistory()
    # si = StockItem()
    sm = StockMarket()

    # sh.start()
    # si.start()
    sm.start()

if __name__ == '__main__':
    run_monitoring_items()
    