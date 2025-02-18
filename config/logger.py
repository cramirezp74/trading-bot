import logging
import os
from logging.handlers import TimedRotatingFileHandler

# Crear carpeta logs si no existe
os.makedirs("data/logs", exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if logger.hasHandlers():
    logger.handlers.clear()

# Configurar un handler que rote el log diariamente (a medianoche)
file_handler = TimedRotatingFileHandler(
    "data/logs/bot.log",
    when="midnight",      # rota a medianoche
    interval=1,           # cada 1 día
    backupCount=7,        # mantener 7 archivos de respaldo
    encoding="utf-8"
)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
