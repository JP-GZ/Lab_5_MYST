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

def extraccion_data():
    data_Test = pd.read_csv('files/EURUSD2021.csv')
    data_Train = pd.read_csv('files/EURUSD2022.csv')
    return data_Test,data_Train

def entrenamiento(df:pd.DataFrame) -> pd.DataFrame:
    data = df.query('stochastic_buy_signal == True or stochastic_sell_signal == True')
    return data

data_Test,data_Train = extraccion_data()

data_Test = fun.technicals(data_Test).dropna()
data_Test['time'] = pd.to_datetime(data_Test['time'], format='%Y-%m-%d')

data_Train = fun.technicals(data_Train).dropna()
data_Train['time'] = pd.to_datetime(data_Train['time'], format='%Y-%m-%d')
# -------------------------------------------------------------------------
df = data_Test.query('stochastic_buy_signal == True or stochastic_sell_signal == True')
traiding_test = fun.tradear(df,0.03, 0.03, 8000)
print(f'Profit = {traiding_test:.4f}')

# opt_vals = fun.busqueda_exhaustiva(data_Train)
# trading_test = fun.tradear(data_Test, opt_vals["stop_loss"], opt_vals["take_profit"], opt_vals["volumen"])
# Se obtuvo como resultado

"""
stop_loss          0.026789
take_profit        0.001000
volumen         5000.000000
profit         99716.664875
"""

# trading_ex_test = fun.tradear(data_Test, 0.026789, 0.001000, 5000)
# print(f"Profit busqueda exhaustiva: ${trading_ex_test:,.4f}")

# best_cost, best_args = fun.busqueda_pso(data_Train)
# Optimizando por pso se obtuvo
# (97086.54226331878, array([9.88641118e-03, 3.20993169e-02, 1.46582293e+04]))
# trading_pso_test = fun.tradear(data_Test, 9.88641118e-03, 3.20993169e-02, 1.46582293e+04)
# print(f"Profit busqueda pso: ${trading_pso_test:,.4f}")

