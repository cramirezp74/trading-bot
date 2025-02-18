import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de Binance y otros parámetros existentes
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
RSI_SOBREVENTA = float(os.getenv("RSI_SOBREVENTA", 30))
RSI_SOBRECOMPRA = float(os.getenv("RSI_SOBRECOMPRA", 70))
CANTIDAD = float(os.getenv("TRADE_AMOUNT", 50))
INTERVALO = os.getenv("TRADE_INTERVAL", "5m")
SIMULAR = os.getenv("SIMULATE_TRADES", "True").lower() == "true"
STOP_LOSS_PERCENTAGE = float(os.getenv("STOP_LOSS_PERCENTAGE", 0.002))
TAKE_PROFIT_PERCENTAGE = float(os.getenv("TAKE_PROFIT_PERCENTAGE", 0.004))

# Configuración de Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Configuración de la base de datos MariaDB
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "trading_bot")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")