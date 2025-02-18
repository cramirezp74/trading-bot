# strategies/combined_strategy.py

import pandas as pd
import numpy as np
import json
from core.data_fetcher import obtener_datos
from config.settings import RSI_SOBREVENTA, RSI_SOBRECOMPRA, STOP_LOSS_PERCENTAGE, TAKE_PROFIT_PERCENTAGE
from config.logger import logger
from core.db import registrar_signal, registrar_indicator_log  # Funciones para registrar señales y logs

def calcular_rsi(data, periodo=7):
    delta = data["Close"].diff()
    ganancia = delta.where(delta > 0, 0).rolling(window=periodo).mean()
    perdida = -delta.where(delta < 0, 0).rolling(window=periodo).mean()
    perdida.replace(0, np.nan, inplace=True)
    rs = ganancia / perdida
    return 100 - (100 / (1 + rs))

def calcular_ema(data, periodo=5):
    """Calcula la EMA con el periodo especificado."""
    return data["Close"].ewm(span=periodo, adjust=False).mean()

def calcular_macd(data, corto=3, largo=6, senal=3):
    ema_corto = data["Close"].ewm(span=corto, adjust=False).mean()
    ema_largo = data["Close"].ewm(span=largo, adjust=False).mean()
    macd = ema_corto - ema_largo
    macd_senal = macd.ewm(span=senal, adjust=False).mean()
    return macd, macd_senal

def calcular_atr(data, periodo=5):
    high_low = data["High"] - data["Low"]
    high_close = np.abs(data["High"] - data["Close"].shift())
    low_close = np.abs(data["Low"] - data["Close"].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(window=periodo, min_periods=1).mean()

def calcular_adx(data, periodo=7):
    plus_dm = data["High"].diff()
    minus_dm = data["Low"].diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0
    atr = calcular_atr(data, periodo)
    plus_di = 100 * (plus_dm.rolling(window=periodo, min_periods=1).sum() / atr)
    minus_di = 100 * (abs(minus_dm.rolling(window=periodo, min_periods=1).sum()) / atr)
    dx = 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di + 1e-10)
    return dx.rolling(window=periodo, min_periods=1).mean()

def calcular_bollinger(data, periodo=10, num_std=2.5):
    sma = data["Close"].rolling(window=periodo).mean()
    rstd = data["Close"].rolling(window=periodo).std()
    bollinger_upper = sma + num_std * rstd
    bollinger_lower = sma - num_std * rstd
    return sma, bollinger_upper, bollinger_lower

def evaluar_mercado():
    datos = obtener_datos()
    # Si no hay datos, registrar y retornar "mantener"
    if datos is None or datos.empty:
        msg = "Sin datos"
        logger.warning("No se pudieron obtener datos para evaluar el mercado")
        resultado = {"accion": "mantener", "motivos": msg}
        registrar_signal("BTCUSDT", resultado["accion"], None, None, msg)
        return resultado
    
    # Validar que los datos sean recientes (dentro de 5 minutos)
    ultimo_tiempo = datos.index[-1]  # Se asume que 'obtener_datos()' establece el índice como datetime
    if (pd.Timestamp.now() - ultimo_tiempo) > pd.Timedelta(minutes=5):
        msg = "Datos desactualizados"
        logger.warning("Los datos no están actualizados")
        resultado = {"accion": "mantener", "motivos": msg}
        registrar_signal("BTCUSDT", resultado["accion"], None, None, msg)
        return resultado
    
    # Calcular indicadores técnicos
    datos["RSI"] = calcular_rsi(datos, 7)
    datos["EMA5"] = calcular_ema(datos, 5)
    datos["EMA9"] = calcular_ema(datos, 9)
    datos["MACD"], datos["MACD_Senal"] = calcular_macd(datos, 3, 6, 3)
    datos["ATR"] = calcular_atr(datos, 5)
    datos["ADX"] = calcular_adx(datos, 7)
    sma, bb_upper, bb_lower = calcular_bollinger(datos, 10, 2.5)
    datos["BB_upper"] = bb_upper
    datos["BB_lower"] = bb_lower

    datos.dropna(inplace=True)
    ultima = datos.iloc[-1]
    precio_actual = ultima["Close"]
    ema5_actual = ultima["EMA5"]
    ema9_actual = ultima["EMA9"]
    rsi_actual = ultima["RSI"]
    macd_actual = ultima["MACD"]
    macd_senal_actual = ultima["MACD_Senal"]
    atr_actual = ultima["ATR"]
    adx_actual = ultima["ADX"]
    bb_lower_actual = ultima["BB_lower"]
    bb_upper_actual = ultima["BB_upper"]

    # Construir el log de indicadores
    log_msg = (
        f"RSI: {rsi_actual:.2f} | Precio: {precio_actual:.2f} | EMA5: {ema5_actual:.2f} | EMA9: {ema9_actual:.2f} | "
        f"MACD: {macd_actual:.2f} | ADX: {adx_actual:.2f} | ATR: {atr_actual:.2f} | "
        f"BB Lower: {bb_lower_actual:.2f} | BB Upper: {bb_upper_actual:.2f}"
    )
    logger.info(log_msg)
    # Registrar el log de indicadores en la base de datos
    registrar_indicator_log("BTCUSDT", rsi_actual, precio_actual, ema5_actual, ema9_actual,
                              macd_actual, adx_actual, atr_actual, bb_lower_actual, bb_upper_actual)
    
    # Definir márgenes para las condiciones: para compra 0.5% y para venta 0.7%
    margin_compra = 0.005 * precio_actual
    margin_venta = 0.007 * precio_actual

    # Evaluar condiciones para COMPRA y recolectar motivos si no se cumplen
    motivos_compra = []
    if not (precio_actual > ema5_actual):  # Usamos EMA5 para mayor sensibilidad en scalping
        motivos_compra.append("Precio no mayor que EMA5")
    if not (rsi_actual < 40):  # Relajamos el umbral para comprar a RSI < 40
        motivos_compra.append(f"RSI ({rsi_actual:.2f}) no menor que 40")
    if not (precio_actual <= bb_lower_actual + margin_compra):
        motivos_compra.append("Precio no cercano a la banda inferior")
    if not (macd_actual > macd_senal_actual):
        motivos_compra.append("MACD no mayor que su señal")
    if not (adx_actual > 20):
        motivos_compra.append("ADX no mayor que 20")

    # Evaluar condiciones para VENTA y recolectar motivos
    motivos_venta = []
    if not (precio_actual < ema5_actual):  # Usamos EMA5 para mayor sensibilidad
        motivos_venta.append("Precio no menor que EMA5")
    if not (rsi_actual > 55):  # Relajamos el umbral para vender a RSI > 55
        motivos_venta.append(f"RSI ({rsi_actual:.2f}) no mayor que 55")
    if not (precio_actual >= bb_upper_actual - margin_venta):
        motivos_venta.append("Precio no cercano a la banda superior")
    if not (macd_actual < macd_senal_actual):
        motivos_venta.append("MACD no menor que su señal")
    if not (adx_actual < 60):  # Requerimos que ADX sea inferior a 60 para indicar reversión\n        motivos_venta.append("ADX no menor que 60")
        motivos_venta.append("ADX no menor que 60")
    # Determinar la acción a tomar y calcular SL/TP dinámicamente usando ATR
    if len(motivos_compra) == 0:
        stop_loss = precio_actual - (0.5 * atr_actual)
        take_profit = precio_actual + (1.5 * atr_actual)
        logger.info(f"Señal de COMPRA: SL: {stop_loss:.2f}, TP: {take_profit:.2f}")
        resultado = {"accion": "comprar", "stop_loss": stop_loss, "take_profit": take_profit, "motivos": None}
        registrar_signal("BTCUSDT", resultado["accion"], stop_loss, take_profit, None)
        return resultado

    if len(motivos_venta) == 0:
        stop_loss = precio_actual + (0.5 * atr_actual)
        take_profit = precio_actual - (1.5 * atr_actual)
        logger.info(f"Señal de VENTA: SL: {stop_loss:.2f}, TP: {take_profit:.2f}")
        resultado = {"accion": "vender", "stop_loss": stop_loss, "take_profit": take_profit, "motivos": None}
        registrar_signal("BTCUSDT", resultado["accion"], stop_loss, take_profit, None)
        return resultado

    motivos = {"compra": motivos_compra, "venta": motivos_venta}
    if motivos is not None and not isinstance(motivos, str):
        motivos_str = json.dumps(motivos, ensure_ascii=False)
    else:
        motivos_str = motivos

    logger.info(f"No se cumple la estrategia. Motivos: {motivos_str}")
    resultado = {"accion": "mantener", "motivos": motivos_str}
    registrar_signal("BTCUSDT", resultado["accion"], None, None, motivos_str)
    return resultado
