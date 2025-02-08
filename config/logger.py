import logging
import os

# Crear carpeta logs si no existe
os.makedirs("data/logs", exist_ok=True)

# Configuración del logger
logging.basicConfig(
    filename="data/logs/bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Logger para importar en otros módulos
logger = logging.getLogger(__name__)
