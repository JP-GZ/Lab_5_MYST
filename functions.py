
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: THE LICENSE TYPE AS STATED IN THE REPOSITORY                                               -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import MetaTrader5 as mt5
import pytz
from datetime import datetime
import pandas as pd
from ta.volatility import BollingerBands
from ta.momentum import StochasticOscillator
from ta.trend import MACD


def import_data():
    # mt5.initialize()
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()
    # set time zone to UTC
    timezone = pytz.timezone("Etc/UTC")
    utc_from = datetime(2020,1, 1, tzinfo=timezone)
    utc_to = datetime(2021, 1, 1, tzinfo=timezone)
    rates = mt5.copy_rates_range("EURUSD", mt5.TIMEFRAME_D1, utc_from, utc_to)
    # create DataFrame out of the obtained data
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    rates_frame.to_csv('EURUSD2021.csv')
    return rates_frame

def technicals(data):
    data = data.copy()
    bollinger = BollingerBands(close=data.close, window=21)
    stoc = StochasticOscillator(high=data['high'], low=data['low'], close=data['close'])
    macd = MACD(close=data['close'])
    # ------------------------------------------------------------------------------------
    data['bb_bbm'] = bollinger.bollinger_mavg()
    data['bb_bbh'] = bollinger.bollinger_hband()
    data['bb_bbl'] = bollinger.bollinger_lband()
    data['bb_high_signal'] = bollinger.bollinger_hband_indicator()
    data['bb_low_signal'] = bollinger.bollinger_lband_indicator()
    # ------------------------------------------------------------------------------------
    data['stochastic'] = stoc.stoch()
    data['stochastic_buy_signal'] = stoc.stoch() < 20
    data['stochastic_sell_signal'] = stoc.stoch() > 80
    # ------------------------------------------------------------------------------------
    data['macd'] = macd.macd()
    data['macd_signal'] = macd.macd_signal()
    data['macd_hist'] = macd.macd_diff()
    data['macd_buy_signal'] = macd.macd() > macd.macd_signal()
    data['macd_sell_hist'] = macd.macd() < macd.macd_diff()

    data = data.drop(['Unnamed: 0'], axis=1)
    return data

def transaccion(vol, pips, df):
    rett = []

    while len(df) > 2:
        precio_transaccion = df['close'].iloc[0]
        posicion = precio_transaccion * vol

        cierres = df.query('(close >= @precio_transaccion + @pips/100) or (close <= @precio_transaccion - @pips/100)')
        precio_cierre = cierres.iloc[0, 5]
        closed_transaction = precio_cierre * vol
        day0 = df.iloc[0, 0]
        day1 = cierres.iloc[0, 0]
        days = (day1 - day0)
        days = int(days.total_seconds() + days.days * pd.Timedelta(days=1).total_seconds())
        ret = 246 * (closed_transaction / posicion - 1) / days
        rett.append(ret)
        df = df.loc[cierres.iloc[0, 0]:]

    return rett
