# core/market_recorder.py

from core.data_fetcher import obtener_datos
from core.db import registrar_market_data
from config.logger import logger

def registrar_ultimo_candle(symbol="BTCUSDT"):
    """
    Obtiene los datos de mercado de Binance (última vela) y los registra en la base de datos.
    
    Se asume que la función 'obtener_datos()' ya establece el índice del DataFrame
    como la fecha de cierre (Close time) y que la columna "Open time" permanece.
    """
    datos = obtener_datos()
    if datos is None or datos.empty:
        logger.warning("No se pudieron obtener datos de mercado para registrar.")
        return
    # Obtener el último registro (última vela)
    ultimo = datos.iloc[-1]
    # Como 'obtener_datos()' estableció el índice como "Close time", usamos ese valor.
    close_time = datos.index[-1]
    # Si la columna "Open time" está disponible, la usamos para open_time.
    open_time = ultimo["Open time"] if "Open time" in datos.columns else None
    open_val = ultimo["Open"]
    high = ultimo["High"]
    low = ultimo["Low"]
    close = ultimo["Close"]
    volume = ultimo["Volume"]
    
    # Registrar los datos en la base de datos
    registrar_market_data(symbol, open_time, close_time, open_val, high, low, close, volume)
    logger.info("Datos del último candle registrados correctamente.")
