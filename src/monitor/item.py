import threading


class StockItem(threading.Thread):
    def __init__(self):
        super().__init__()
    def run(self):
        print('run StockItem')
        pass
