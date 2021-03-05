import threading


class StockMarket(threading.Thread):
    def __init__(self):
        super().__init__()
    def run(self):
        print('run StockMarket')
        pass
