import threading


class StockHistory(threading.Thread):
    def __init__(self):
        super().__init__()
    def run(self):
        print('run StockHistory')
        pass