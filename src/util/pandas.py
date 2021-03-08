import pandas as pd 
import numpy as np




# pd.read_html returns table DataFrames from html tags
def read_html(path, header, index:None):
    table = pd.read_html(path, header=header)
    return index==None and table or table[index]


def concat( source, target) :
    return pd.concat([source, target])


def arrangeNewDataFrame( _input ) :
    return pd.DataFrames(_input)