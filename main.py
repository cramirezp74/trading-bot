import time
import datetime
from core.trading import ejecutar_trading
from config.logger import logger

if __name__ == "__main__":
    logger.info("🚀 Iniciando bot de trading...")

    while True:
        try:
            print("<--------------------------->")
            ahora = datetime.datetime.now()
            logger.info(f"📅 Análisis de mercado a las {ahora.strftime('%Y-%m-%d %H:%M:%S')}")

            ejecutar_trading()

            logger.info("⏳ Esperando 60 minutos para la siguiente iteración...")
            time.sleep(3600)  # Esperar 60 minutos
        except Exception as e:
            logger.error(f"⚠️ Error crítico en el bot: {e}")
            logger.info("⏳ Reiniciando en 60 minutos...")
            time.sleep(3600)
