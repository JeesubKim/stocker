from monitor.history import StockHistory
from monitor.item import StockItem
from monitor.market import StockMarket
# This file will be running using ubuntu crontab

from monitor.fluctuation import Fluctuation
from monitor.trend import StockTrend
def run_monitoring_items():
    sh = StockHistory()
    sm = StockMarket()
    # si = StockItem()

    # fluc = Fluctuation()
    # trend = StockTrend()

    sh.start()
    sm.start()
    # si.start()
    # fluc.start()
    # trend.start()

if __name__ == '__main__':
    run_monitoring_items()
    