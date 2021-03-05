import json

def read(path):
    with open(path) as json_file:
        return json.load(json_file)