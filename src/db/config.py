
from util.file import *
import sys, os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/'))
sys.path.append(path)

print(path)
DB_CONFIG = read(f'{path}\\config.json')['db']