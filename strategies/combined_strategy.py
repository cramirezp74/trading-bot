# strategies/combined_strategy.py

import pandas as pd
from core.data_fetcher import obtener_datos
from config.settings import RSI_SOBREVENTA, RSI_SOBRECOMPRA
from config.logger import logger

def calcular_rsi(data, periodo=14):
    delta = data["Close"].diff()
    ganancia = delta.where(delta > 0, 0).rolling(periodo).mean()
    perdida = -delta.where(delta < 0, 0).rolling(periodo).mean()
    rs = ganancia / perdida
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calcular_ema(data, periodo=50):
    return data["Close"].ewm(span=periodo, adjust=False).mean()

def calcular_bollinger(data, periodo=20, num_std=2):
    sma = data["Close"].rolling(window=periodo).mean()
    rstd = data["Close"].rolling(window=periodo).std()
    bollinger_upper = sma + num_std * rstd
    bollinger_lower = sma - num_std * rstd
    return sma, bollinger_upper, bollinger_lower

def evaluar_mercado():
    datos = obtener_datos()
    if datos is None or datos.empty:
        logger.warning("No se pudieron obtener datos para evaluar el mercado")
        return "mantener"

    # Calcular indicadores:
    datos["RSI"] = calcular_rsi(datos, 14)
    datos["EMA"] = calcular_ema(datos, 50)
    sma, bb_upper, bb_lower = calcular_bollinger(datos, 20, 2)
    datos["BB_upper"] = bb_upper
    datos["BB_lower"] = bb_lower

    # Tomamos la última fila para los valores actuales:
    ultima = datos.iloc[-1]
    rsi_actual = ultima["RSI"]
    precio_actual = ultima["Close"]
    ema_actual = ultima["EMA"]
    bb_lower_actual = ultima["BB_lower"]
    bb_upper_actual = ultima["BB_upper"]

    logger.info(f"RSI: {rsi_actual:.2f} | Precio: {precio_actual:.2f} | EMA50: {ema_actual:.2f} | BB Lower: {bb_lower_actual:.2f} | BB Upper: {bb_upper_actual:.2f}")

    # Definimos un margen (por ejemplo, 0.5% del precio) para considerar "cercanía" a la banda
    margin = 0.005 * precio_actual

    # Condición de COMPRA:
    # - Tendencia alcista: Precio > EMA50
    # - RSI indica sobreventa: RSI < RSI_SOBREVENTA (por ejemplo, 30)
    # - Precio está cerca de la banda inferior: precio <= (BB_lower + margin)
    if (precio_actual > ema_actual) and (rsi_actual < RSI_SOBREVENTA) and (precio_actual <= bb_lower_actual + margin):
        logger.info("Condiciones de COMPRA cumplidas.")
        return "comprar"

    # Condición de VENTA:
    # - Tendencia bajista: Precio < EMA50
    # - RSI indica sobrecompra: RSI > RSI_SOBRECOMPRA (por ejemplo, 70)
    # - Precio está cerca de la banda superior: precio >= (BB_upper - margin)
    if (precio_actual < ema_actual) and (rsi_actual > RSI_SOBRECOMPRA) and (precio_actual >= bb_upper_actual - margin):
        logger.info("Condiciones de VENTA cumplidas.")
        return "vender"

    # Si no se cumplen las condiciones, se mantiene la posición
    return "mantener"
