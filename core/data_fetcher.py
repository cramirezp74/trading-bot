from binance.client import Client
import pandas as pd
from config.settings import API_KEY, API_SECRET, INTERVALO
from config.logger import logger

client = Client(API_KEY, API_SECRET)

def obtener_datos():
    try:
        logger.info("📡 Solicitando datos a Binance...")
        klines = client.get_klines(symbol="BTCUSDT", interval=INTERVALO, limit=50)

        columnas = [
            "Open time", "Open", "High", "Low", "Close", "Volume",
            "Close time", "Quote asset volume", "Number of trades",
            "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"
        ]

        df = pd.DataFrame(klines, columns=columnas)
        # Convertir los tiempos de milisegundos a datetime
        df["Open time"] = pd.to_datetime(df["Open time"], unit="ms")
        df["Close time"] = pd.to_datetime(df["Close time"], unit="ms")
        # Convertir valores numéricos
        df["Open"] = df["Open"].astype(float)
        df["High"] = df["High"].astype(float)
        df["Low"] = df["Low"].astype(float)
        df["Close"] = df["Close"].astype(float)
        df["Volume"] = df["Volume"].astype(float)

        # Establecer el índice con "Close time" (o "Open time", según prefieras)
        df.set_index("Close time", inplace=True)
        
        logger.info("✅ Datos obtenidos con éxito")
        return df

    except Exception as e:
        logger.error(f"⚠️ Error al obtener datos de Binance: {e}")
        return None
