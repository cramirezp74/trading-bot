import pandas as pd
from core.data_fetcher import obtener_datos
from config.settings import RSI_SOBREVENTA, RSI_SOBRECOMPRA
from config.logger import logger

def calcular_rsi(data, periodo=14):
    delta = data["Close"].diff()
    ganancia = delta.where(delta > 0, 0).rolling(periodo).mean()
    perdida = -delta.where(delta < 0, 0).rolling(periodo).mean()
    rs = ganancia / perdida
    return 100 - (100 / (1 + rs))

def evaluar_mercado():
    datos = obtener_datos()
    if datos is None:
        logger.warning("⚠️ No se pudo obtener datos, se omite esta iteración.")
        return "mantener"

    datos["RSI"] = calcular_rsi(datos)
    rsi_actual = datos["RSI"].iloc[-1]
    precio_actual = datos["Close"].iloc[-1]

    logger.info(f"📊 RSI: {rsi_actual:.2f} | Precio: ${precio_actual:.2f}")

    if rsi_actual < RSI_SOBREVENTA:
        logger.info("📉 RSI en sobreventa: Se recomienda COMPRAR")
        return "comprar"
    elif rsi_actual > RSI_SOBRECOMPRA:
        logger.info("📈 RSI en sobrecompra: Se recomienda VENDER")
        return "vender"
    
    logger.info("🔵 RSI en rango neutral: No hacer nada")
    return "mantener"
