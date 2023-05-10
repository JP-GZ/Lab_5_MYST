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

data_Test=pd.read_csv('files/BTC2021_2.csv')
data_Train=pd.read_csv('files/BTC2022.csv')

data_Test = fun.technicals(data_Test).dropna()
#data_Test = fun.tec2(data_Test).dropna()
# data_Train = fun.technicals(data_Train).dropna()


vol=0.5 # volumen en bitcoin
pips=9000 # exposicion por operacion 100 usd
df = data_Test[(data_Test['stochastic_buy_signal']==True) | (data_Test['stochastic_sell_signal']==True)] # df con las señales de compra y venta

precio_transaccion = df['close'].iloc[0]
posicion = precio_transaccion * vol
day0 = (df.iloc[0, 0])
print(df['close'].iloc[0])
print(df.iloc[0, 0])

closed = df[(df['close'] >= (precio_transaccion + pips / 100)) | (df['close'] <= (precio_transaccion - pips / 100))]
print(closed)
closed_price = closed.iloc[0, 5]
print(closed_price)
closed_transaction = closed_price * vol
print(closed_transaction)
day1 = (closed.iloc[0, 0])
print(day1)
print((day1 - day0))
ret = 246 * (closed_transaction / posicion - 1)/ (day1 - day0)
# transacciones = fun.transaccion(vol, pips, df)

# print(transacciones)