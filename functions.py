
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
import tqdm
from ta.volatility import BollingerBands
from ta.momentum import StochasticOscillator
from ta.trend import MACD
import numpy as np


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

def tradear(data: pd.DataFrame, sl: float, tp: float, vol: int):
    operaciones_cerradas = []
    operaciones_activas = []
    # Hacemos hasta 10 operaciones
    max_num_operaciones = 10
    cash = 100_000
    valor_port = [cash]

    for _, price_stats in data.iterrows():
        precio = price_stats["close"]
        fecha = price_stats["time"]
        buy_signals = [price_stats["bb_low_signal"], price_stats["stochastic_buy_signal"],
                       price_stats["macd_buy_signal"]]
        sell_signals = [price_stats["bb_high_signal"], price_stats["stochastic_sell_signal"],
                        price_stats["macd_sell_hist"]]

        if sum(buy_signals) >= 2 and len(operaciones_activas) < max_num_operaciones and cash > (
                (10_000 // precio) * 1.00125):
            # Sacar numero de titulos
            num_titulos = vol
            # Sacar costo de compra
            costo = num_titulos * precio
            # Agregar comisiones
            costo_com = costo * 1.00125
            # Descontar al cash
            cash -= costo_com
            # Poner stop loss y take profit
            stop_loss = precio * (1 - sl)
            take_profit = precio * (1 + tp)
            # agregar a operaciones activas
            operaciones_activas.append({
                "fecha": fecha,
                "precio_compra": precio,
                "num_titulos": num_titulos,
                "costo": costo,
                "cost_com": costo_com,
                "stop_loss": stop_loss,
                "take_profit": take_profit
            })
            # print(f"Comprando {num_titulos} a {precio} - Cash {cash}")

        # Checar sl y tp
        for operacion_activa in operaciones_activas:

            if precio < operacion_activa["stop_loss"] or precio > operacion_activa["take_profit"]:
                tipo = "stop loss" if precio < operacion_activa["stop_loss"] else "take profit"
                operacion_activa["fecha_cierre"] = fecha
                operacion_activa["precio_venta"] = precio
                operacion_activa["valor_port"] = cash + operacion_activa["num_titulos"] * precio
                num_titulos = operacion_activa["num_titulos"]
                venta = num_titulos * precio
                venta_com = venta * (1 - 0.00125)  # Comision descontada
                cash += venta_com
                operaciones_cerradas.append(operacion_activa)
                operaciones_activas.remove(operacion_activa)
                #print(f"Vendiendo por {tipo} {num_titulos} a {precio} - Cash {cash}")

        if sum(sell_signals) >= 2:
            for operacion_activa in operaciones_activas:
                operacion_activa["fecha_cierre"] = fecha
                operacion_activa["precio_venta"] = precio
                operacion_activa["valor_port"] = cash + operacion_activa["num_titulos"] * precio
                num_titulos = operacion_activa["num_titulos"]
                venta = num_titulos * precio
                venta_com = venta * (1 - 0.00125)  # Comision descontada
                cash += venta_com
                operaciones_cerradas.append(operacion_activa)
                # print(f"Vendiendo {num_titulos} a {precio} - Cash {cash}")
            operaciones_activas = []

        # Historico del valor del portafolio
        if operaciones_activas:
            num_titulos = sum(list(map(lambda operacion: operacion["num_titulos"], operaciones_activas)))
            valor_port.append(cash + num_titulos * precio)
        else:
            valor_port.append(cash)

    return valor_port[-1]


def busqueda_exhaustiva(data):
    sl_ = np.linspace(0.001, 0.05, 20)
    tp_ = np.linspace(0.001, 0.05, 20)
    vol_ = np.linspace(5000, 15000, 50)
    resultados = {
        "stop_loss": [],
        "take_profit": [],
        "volumen": [],
        "profit": []
    }
    for i in tqdm.tqdm(range(len(sl_))):
        sl = sl_[i]
        for tp in tp_:
            for vol in vol_:
                resultados["stop_loss"].append(sl)
                resultados["take_profit"].append(tp)
                resultados["volumen"].append(vol)
                resultados["profit"].append(tradear(data, sl, tp, vol))

    res_df = pd.DataFrame(resultados)
    profits = res_df.loc[:, "profit"].values
    max_profit_idx = np.argmax(profits)
    return res_df.iloc[max_profit_idx, :]


def busqueda_pso(data):
    rango_min = np.array([0.001, 0.001, 5000])  # sl, tp, vol
    rango_max = np.array([0.05, 0.05, 15000])  # sl, tp, vol
    bounds = (rango_min, rango_max)

    options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
    optimizer = ps.single.GlobalBestPSO(n_particles=10, dimensions=3, options=options, bounds=bounds)
    best_cost, best_pos = optimizer.optimize(lambda args: np.array([tradear(data, arg[0], arg[1], arg[2]) for arg in args]), iters=100)
    return best_cost, best_pos
