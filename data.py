"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- PROYECTO: ANALISIS TÉCNICO                                                        -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: THE LICENSE TYPE AS STATED IN THE REPOSITORY                                               -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

from datetime import datetime

import pandas as pd
import pytz
import numpy as np
import functions as fun
import pyswarms as ps
from pyswarms.utils.functions import single_obj as fx

data_Test=pd.read_csv('files/EURUSD2021.csv')
data_Train=pd.read_csv('files/EURUSD2022.csv')

data_Test = fun.technicals(data_Test).dropna()
data_Test['time'] = pd.to_datetime(data_Test['time'], format='%Y-%m-%d')
capital_inicial = 100_000
vol=0.5
pips=1
df = data_Test.query('stochastic_buy_signal == True or stochastic_sell_signal == True')
print("---------------------------------")
print(df.columns)

