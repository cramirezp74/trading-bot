# main.py

import time
import datetime
from core.trading import ejecutar_trading
from core.market_recorder import registrar_ultimo_candle
from config.logger import logger
from config.settings import INTERVALO

def convertir_intervalo(intervalo_str):
    # Convierte "5m", "1h", etc. a segundos.
    unidad = intervalo_str[-1].lower()
    valor = int(intervalo_str[:-1])
    if unidad == "m":
        return valor * 60
    elif unidad == "h":
        return valor * 3600
    else:
        return 300  # Valor por defecto: 5 minutos

def calcular_proxima_ejecucion():
    ahora = datetime.datetime.now()
    minutos_actuales = ahora.minute
    minutos_proximo = (minutos_actuales // 5 + 1) * 5
    if minutos_proximo >= 60:
        proxima_ejecucion = ahora.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)
    else:
        proxima_ejecucion = ahora.replace(minute=minutos_proximo, second=0, microsecond=0)
    return proxima_ejecucion

if __name__ == "__main__":
    logger.info("🚀 Iniciando bot de trading...")
    intervalo_segundos = convertir_intervalo(INTERVALO)
    while True:
        try:
            ahora = datetime.datetime.now()
            logger.info(f"📅 Análisis de mercado a {ahora.strftime('%Y-%m-%d %H:%M:%S')}")

            # Registrar el último candle para mantener un histórico de datos
            registrar_ultimo_candle("BTCUSDT")

            ejecutar_trading()
            proxima_ejecucion = calcular_proxima_ejecucion()
            logger.info(f"⏳ Próxima ejecución programada para: {proxima_ejecucion.strftime('%Y-%m-%d %H:%M:%S')}")
            tiempo_espera = (proxima_ejecucion - datetime.datetime.now()).total_seconds()
            time.sleep(max(0, tiempo_espera))
        except Exception as e:
            logger.error(f"⚠️ Error crítico en el bot: {e}")
            time.sleep(intervalo_segundos)
